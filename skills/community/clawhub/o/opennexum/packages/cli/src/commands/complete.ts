import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import type { Command } from 'commander';
import {
  parseContract,
  parseEvalResult,
  getTask,
  readTasks,
  syncTasksWithContracts,
  updateTask,
  TaskStatus,
  loadConfig,
  resolveAgentExecution,
} from '@nexum/core';
import type { EvalVerdict, AgentCli, AgentRuntime, CriterionResult } from '@nexum/core';
import { renderRetryPrompt } from '@nexum/prompts';
// Notifications are handled by callback.ts, not here
import { archiveDoneTasks } from '../lib/archive.js';
import { resolveContractAgents } from '../lib/resolve-contract-agents.js';

export interface RetryPayload {
  action: 'retry';
  taskId: string;
  taskName: string;
  agentId: string;
  agentCli: AgentCli;
  runtime: AgentRuntime;
  runtimeAgentId: string;
  promptFile: string;
  promptContent: string;
  label: string;
  cwd: string;
  nextIteration: number;
}

export interface CompleteResult {
  action: 'done' | 'retry' | 'escalated' | 'failed';
  taskId: string;
  unlockedTasks?: string[];
  retryPayload?: RetryPayload;
  noop?: boolean;
}

const ESCALATED_TASK_STATUS = TaskStatus.Escalated;
const ESCALATED_REASON_PREFIX = 'Escalated:';
const FEEDBACK_SIMILARITY_THRESHOLD = 0.8;

function quoteShellArg(value: string): string {
  if (value === '') {
    return "''";
  }

  return `'${value.replace(/'/g, `'\\''`)}'`;
}

function tokenizeFeedback(text: string): string[] {
  return (text.toLowerCase().match(/[a-z0-9]+|[\u4e00-\u9fff]+/g) ?? []).filter(Boolean);
}

function calculateFeedbackSimilarity(left: string, right: string): number {
  const leftWords = new Set(tokenizeFeedback(left));
  const rightWords = new Set(tokenizeFeedback(right));

  if (leftWords.size === 0 || rightWords.size === 0) {
    return 0;
  }

  let commonCount = 0;
  for (const word of leftWords) {
    if (rightWords.has(word)) {
      commonCount += 1;
    }
  }

  return commonCount / Math.max(leftWords.size, rightWords.size);
}

function buildEvalResultPath(projectDir: string, taskId: string, iteration: number): string {
  return path.join(projectDir, 'nexum', 'runtime', 'eval', `${taskId}-iter-${iteration}.yaml`);
}

function isEscalatedTask(task: Awaited<ReturnType<typeof getTask>>): boolean {
  return Boolean(
    task &&
      (task.status === ESCALATED_TASK_STATUS ||
        task.last_error?.startsWith(ESCALATED_REASON_PREFIX))
  );
}

async function unlockDownstreamTasks(projectDir: string, completedTaskId: string): Promise<string[]> {
  const tasks = await readTasks(projectDir);
  const completedIds = new Set(
    tasks.filter((t) => t.status === TaskStatus.Done).map((t) => t.id)
  );
  completedIds.add(completedTaskId);

  const toUnlock = tasks.filter(
    (t) =>
      (t.status === TaskStatus.Blocked || t.status === TaskStatus.Pending) &&
      t.depends_on.includes(completedTaskId) &&
      t.depends_on.every((dep) => completedIds.has(dep))
  );

  for (const t of toUnlock) {
    if (t.status !== TaskStatus.Pending) {
      await updateTask(projectDir, t.id, { status: TaskStatus.Pending });
    }
  }

  return toUnlock.map((t) => t.id);
}

export async function runComplete(
  taskId: string,
  verdict: string,
  projectDir: string
): Promise<CompleteResult> {
  const normalizedVerdict = verdict as EvalVerdict;
  if (!['pass', 'fail', 'escalated'].includes(normalizedVerdict)) {
    throw new Error(`Invalid verdict: ${verdict}. Must be pass, fail, or escalated.`);
  }

  await syncTasksWithContracts(projectDir, { taskId });
  const task = await getTask(projectDir, taskId);
  if (!task) {
    throw new Error(`Task not found: ${taskId}`);
  }

  if (task.status === TaskStatus.Done && normalizedVerdict === 'pass') {
    return { action: 'done', taskId, unlockedTasks: [], noop: true };
  }

  if (
    task.status === TaskStatus.Escalated &&
    (normalizedVerdict === 'fail' || normalizedVerdict === 'escalated')
  ) {
    return { action: 'escalated', taskId, noop: true };
  }

  if (task.status !== TaskStatus.GeneratorDone && task.status !== TaskStatus.Evaluating) {
    throw new Error(
      `Task ${taskId} cannot complete from status ${task.status}. Expected generator_done or evaluating.`
    );
  }

  const contractAbsPath = path.isAbsolute(task.contract_path)
    ? task.contract_path
    : path.join(projectDir, task.contract_path);
  const contract = await parseContract(contractAbsPath);
  const config = await loadConfig(projectDir);
  const resolvedContract = resolveContractAgents(contract, config);

  const iteration = task.iteration ?? 0;

  const evalSummary = task.eval_result_path
    ? await parseEvalResult(task.eval_result_path)
    : { feedback: '', failedCriteria: [], passCount: 0, totalCount: 0, criteriaResults: [] };
  const previousEvalSummary =
    normalizedVerdict === 'fail' && iteration > 0
      ? await parseEvalResult(buildEvalResultPath(projectDir, taskId, iteration - 1))
      : null;
  const feedbackSimilarity = previousEvalSummary
    ? calculateFeedbackSimilarity(evalSummary.feedback, previousEvalSummary.feedback)
    : 0;
  const shouldEscalateBySimilarity =
    normalizedVerdict === 'fail' && feedbackSimilarity > FEEDBACK_SIMILARITY_THRESHOLD;
  const shouldEscalateByLimit =
    normalizedVerdict === 'fail' && iteration >= contract.max_iterations;

  // ── PASS ──
  if (normalizedVerdict === 'pass') {
    const now = new Date().toISOString();
    await updateTask(projectDir, taskId, {
      status: TaskStatus.Done,
      completed_at: now,
    });

    const unlockedIds = await unlockDownstreamTasks(projectDir, taskId);
    const tasks = await readTasks(projectDir);
    const doneCount = tasks.filter((t) => t.status === TaskStatus.Done).length;

    if (doneCount > 20) {
      await archiveDoneTasks(projectDir).catch((error) => {
        console.warn(
          'auto-archive failed:',
          error instanceof Error ? error.message : String(error)
        );
      });
    }

    return { action: 'done', taskId, unlockedTasks: unlockedIds };
  }

  // ── FAIL + can retry ──
  if (
    normalizedVerdict === 'fail' &&
    !shouldEscalateBySimilarity &&
    !shouldEscalateByLimit
  ) {
    const nextIteration = iteration + 1;
    const nextEvalResultPath = path.join(
      projectDir,
      'nexum',
      'runtime',
      'eval',
      `${taskId}-iter-${nextIteration}.yaml`
    );

    const quotedScopeFiles = contract.scope.files.map((file) => quoteShellArg(file)).join(' ');
    const gitCommitCmd = [
      `git add -- ${quotedScopeFiles}`,
      `git commit -m "feat(${taskId.toLowerCase()}): implement ${contract.name} (iter ${nextIteration})"`,
    ].join(' && ');

    const fieldReportPath = path.join(
      projectDir,
      'nexum',
      'runtime',
      'field-reports',
      `${taskId}.md`
    );

    const promptContent = renderRetryPrompt(
      {
        contract: resolvedContract,
        task: { id: task.id, name: task.name },
        gitCommitCmd,
        evalResultPath: nextEvalResultPath,
        fieldReportPath,
        lessons: [],
      },
      verdict,
      evalSummary.feedback,
      evalSummary.failedCriteria
    );

    const promptsDir = path.join(projectDir, 'nexum', 'runtime', 'prompts');
    await mkdir(promptsDir, { recursive: true });
    const promptFile = path.join(promptsDir, `${taskId}-retry-${Date.now()}.md`);
    await writeFile(promptFile, promptContent, 'utf8');

    await updateTask(projectDir, taskId, {
      status: TaskStatus.Pending,
      iteration: nextIteration,
      eval_result_path: nextEvalResultPath,
      base_commit: undefined,
      started_at: undefined,
      acp_session_key: undefined,
      acp_stream_log: undefined,
      generator_acp_session_key: undefined,
      generator_acp_stream_log: undefined,
      evaluator_acp_session_key: undefined,
      evaluator_acp_stream_log: undefined,
    });

    const execution = resolveAgentExecution(config, resolvedContract.generator);
    const label = `nexum-${taskId.toLowerCase()}-${resolvedContract.generator}-retry-${nextIteration}`;

    // Fail/retry notification is sent by callback --role evaluator, not here

    const retryPayload: RetryPayload = {
      action: 'retry',
      taskId,
      taskName: resolvedContract.name,
      agentId: resolvedContract.generator,
      agentCli: execution.cli,
      runtime: execution.runtime,
      runtimeAgentId: execution.runtimeAgentId,
      promptFile,
      promptContent,
      label,
      cwd: projectDir,
      nextIteration,
    };

    return { action: 'retry', taskId, retryPayload };
  }

  // ── ESCALATED or max iterations reached ──
  const similarityPercent = Math.round(feedbackSimilarity * 100);
  const escalationReason =
    normalizedVerdict === 'escalated'
      ? 'requires human intervention'
      : shouldEscalateBySimilarity
        ? `consecutive evaluator feedback similarity ${similarityPercent}% (> 80%), possible Contract criteria issue`
        : `max_iterations reached (${iteration}/${contract.max_iterations})`;
  await updateTask(projectDir, taskId, {
    status: ESCALATED_TASK_STATUS,
    last_error: `${ESCALATED_REASON_PREFIX} ${escalationReason}`,
  });

  // Escalation notification is sent by callback --role evaluator, not here

  return {
    action: 'escalated',
    taskId,
  };
}

export async function runRetry(
  taskId: string,
  projectDir: string,
  force: boolean
): Promise<{ ok: true; taskId: string; status: TaskStatus.Pending }> {
  if (!force) {
    throw new Error('retry requires --force');
  }

  const task = await getTask(projectDir, taskId);
  if (!task) {
    throw new Error(`Task not found: ${taskId}`);
  }

  if (!isEscalatedTask(task)) {
    throw new Error(`Task ${taskId} is not escalated.`);
  }

  await updateTask(projectDir, taskId, {
    status: TaskStatus.Pending,
    iteration: 0,
    last_error: null,
    eval_result_path: undefined,
    started_at: undefined,
    completed_at: undefined,
    acp_session_key: undefined,
    acp_stream_log: undefined,
    generator_acp_session_key: undefined,
    generator_acp_stream_log: undefined,
    evaluator_acp_session_key: undefined,
    evaluator_acp_stream_log: undefined,
  });

  return { ok: true, taskId, status: TaskStatus.Pending };
}

export function registerComplete(program: Command): void {
  program
    .command('complete <taskId> <verdict>')
    .description('Process evaluator result (verdict: pass|fail|escalated). Outputs JSON — retry action includes spawn payload for orchestrator.')
    .option('--project <dir>', 'Project directory', process.cwd())
    .action(async (taskId: string, verdict: string, options: { project: string }) => {
      try {
        const result = await runComplete(taskId, verdict, options.project);
        console.log(JSON.stringify(result, null, 2));
      } catch (err) {
        console.error('complete failed:', err instanceof Error ? err.message : err);
        process.exit(1);
      }
    });

  program
    .command('retry <taskId>')
    .description('Reset an escalated task to pending and clear iteration; requires --force.')
    .option('--project <dir>', 'Project directory', process.cwd())
    .option('--force', 'Required to reset escalated task state')
    .action(async (taskId: string, options: { project: string; force?: boolean }) => {
      try {
        const result = await runRetry(taskId, options.project, !!options.force);
        console.log(JSON.stringify(result, null, 2));
      } catch (err) {
        console.error('retry failed:', err instanceof Error ? err.message : err);
        process.exit(1);
      }
    });
}
