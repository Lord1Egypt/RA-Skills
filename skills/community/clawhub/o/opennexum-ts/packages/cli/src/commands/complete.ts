import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import type { Command } from 'commander';
import {
  parseContract,
  getTask,
  readTasks,
  updateTask,
  TaskStatus,
  getHeadCommit,
  loadConfig,
  resolveAgentCli,
} from '@nexum/core';
import type { EvalVerdict, AgentCli } from '@nexum/core';
import { renderRetryPrompt } from '@nexum/prompts';
import { formatComplete, formatFail, sendMessage, getChatId, getBotToken } from '@nexum/notify';

export interface RetryPayload {
  action: 'retry';
  taskId: string;
  taskName: string;
  agentId: string;
  agentCli: AgentCli;
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
}

interface EvalSummary {
  feedback: string;
  failedCriteria: string[];
  passCount: number;
  totalCount: number;
}

async function readEvalSummary(evalResultPath: string): Promise<EvalSummary> {
  try {
    const content = await readFile(evalResultPath, 'utf8');
    const feedbackMatch = content.match(/^feedback:\s*["']?(.*?)["']?\s*$/m);
    const feedback = feedbackMatch?.[1]?.trim() ?? '';

    const passMatches = [...content.matchAll(/result:\s*pass/g)];
    const failMatches = [...content.matchAll(/result:\s*fail/g)];
    const passCount = passMatches.length;
    const failCount = failMatches.length;
    const totalCount = passCount + failCount;

    const failedCriteria: string[] = [];
    const criteriaBlocks = content.split(/\n\s*-\s*id:\s*/);
    for (const block of criteriaBlocks.slice(1)) {
      const idMatch = block.match(/^(\S+)/);
      if (idMatch && /result:\s*fail/.test(block)) {
        failedCriteria.push(idMatch[1]);
      }
    }

    return { feedback, failedCriteria, passCount, totalCount };
  } catch {
    return { feedback: '', failedCriteria: [], passCount: 0, totalCount: 0 };
  }
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

  const task = await getTask(projectDir, taskId);
  if (!task) {
    throw new Error(`Task not found: ${taskId}`);
  }

  const contractAbsPath = path.isAbsolute(task.contract_path)
    ? task.contract_path
    : path.join(projectDir, task.contract_path);
  const contract = await parseContract(contractAbsPath);

  const startedAt = task.started_at ? new Date(task.started_at).getTime() : Date.now();
  const elapsedMs = Date.now() - startedAt;
  const iteration = task.iteration ?? 0;

  const evalSummary = task.eval_result_path
    ? await readEvalSummary(task.eval_result_path)
    : { feedback: '', failedCriteria: [], passCount: 0, totalCount: 0 };

  const chatId = getChatId();
  const botToken = getBotToken();

  // ── PASS ──
  if (normalizedVerdict === 'pass') {
    const now = new Date().toISOString();
    await updateTask(projectDir, taskId, {
      status: TaskStatus.Done,
      completed_at: now,
    });

    const unlockedIds = await unlockDownstreamTasks(projectDir, taskId);

    if (chatId && botToken) {
      const tasks = await readTasks(projectDir);
      const doneCount = tasks.filter((t) => t.status === TaskStatus.Done).length;
      const msg = formatComplete(
        taskId,
        contract.name,
        elapsedMs,
        iteration,
        evalSummary.passCount,
        evalSummary.totalCount,
        unlockedIds,
        `${doneCount}/${tasks.length}`
      );
      await sendMessage(chatId, msg, botToken).catch(() => {});
    }

    return { action: 'done', taskId, unlockedTasks: unlockedIds };
  }

  // ── FAIL + can retry ──
  if (normalizedVerdict === 'fail' && iteration < contract.max_iterations) {
    const nextIteration = iteration + 1;
    const nextEvalResultPath = path.join(
      projectDir,
      'nexum',
      'runtime',
      'eval',
      `${taskId}-iter-${nextIteration}.yaml`
    );

    const gitCommitCmd = [
      `git add -- ${contract.scope.files.join(' ')}`,
      `git commit -m "feat(${taskId.toLowerCase()}): implement ${contract.name} (iter ${nextIteration})"`,
    ].join(' && ');

    const promptContent = renderRetryPrompt(
      {
        contract,
        task: { id: task.id, name: task.name },
        gitCommitCmd,
        evalResultPath: nextEvalResultPath,
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

    const baseCommit = await getHeadCommit(projectDir).catch(() => '');
    await updateTask(projectDir, taskId, {
      status: TaskStatus.Running,
      iteration: nextIteration,
      eval_result_path: nextEvalResultPath,
      ...(baseCommit ? { base_commit: baseCommit } : {}),
    });

    const config = await loadConfig(projectDir);
    const agentCli = resolveAgentCli(config, contract.generator);
    const label = `nexum-${taskId.toLowerCase()}-${contract.generator}-retry-${nextIteration}`;

    if (chatId && botToken) {
      const msg = formatFail(
        taskId,
        contract.name,
        iteration,
        evalSummary.passCount,
        evalSummary.totalCount,
        evalSummary.failedCriteria.length,
        evalSummary.failedCriteria,
        evalSummary.feedback.slice(0, 200)
      );
      await sendMessage(chatId, msg, botToken).catch(() => {});
    }

    const retryPayload: RetryPayload = {
      action: 'retry',
      taskId,
      taskName: contract.name,
      agentId: contract.generator,
      agentCli,
      promptFile,
      promptContent,
      label,
      cwd: projectDir,
      nextIteration,
    };

    return { action: 'retry', taskId, retryPayload };
  }

  // ── ESCALATED or max iterations reached ──
  const reason =
    normalizedVerdict === 'escalated'
      ? 'Escalated: requires human intervention'
      : `Failed after ${iteration} iterations`;

  await updateTask(projectDir, taskId, {
    status: TaskStatus.Failed,
    last_error: reason,
  });

  if (chatId && botToken) {
    const msg = formatFail(
      taskId,
      contract.name,
      iteration,
      evalSummary.passCount,
      evalSummary.totalCount,
      evalSummary.failedCriteria.length,
      evalSummary.failedCriteria,
      normalizedVerdict === 'escalated' ? reason : evalSummary.feedback.slice(0, 200)
    );
    await sendMessage(chatId, msg, botToken).catch(() => {});
  }

  return {
    action: normalizedVerdict === 'escalated' ? 'escalated' : 'failed',
    taskId,
  };
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
}
