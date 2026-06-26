import { mkdir, open, readFile, rename, unlink, writeFile } from 'node:fs/promises';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import path from 'node:path';
import type { Command } from 'commander';
import {
  getActiveBatch,
  getBatchProgress,
  getTask,
  readTasks,
  resolveAgentExecution,
  syncTasksWithContracts,
  updateTask,
  TaskStatus,
  loadConfig,
  getHeadCommit,
  parseContract,
  parseEvalResult,
  type EvalVerdict,
  type NexumConfig,
} from '@nexum/core';
import {
  formatGeneratorDone,
  formatReviewPassed,
  formatReviewFailed,
  formatEscalation,
  formatCommitMissing,
  formatBatchDone,
  sendMessage,
} from '@nexum/notify';
import { runComplete } from './complete.js';
import { enqueueDispatchEntry } from '../lib/dispatch-queue.js';
import { dispatchAgentWebhook } from '../lib/webhook.js';
import { resolveContractAgents } from '../lib/resolve-contract-agents.js';
import type { AgentCli } from '@nexum/core';

const execFileAsync = promisify(execFile);
const SESSION_COUNTER_FILENAME = 'session-counter.json';
const SESSION_COUNTER_LOCK_SUFFIX = '.lock';

// ─── Types ───────────────────────────────────────────────────────────────────

interface CallbackOptions {
  project: string;
  model?: string;
  inputTokens?: string;
  outputTokens?: string;
  role?: 'generator' | 'evaluator';
}

type SessionRole = 'gen' | 'eval';

// ─── Entry Point ─────────────────────────────────────────────────────────────

export async function runCallback(taskId: string, options: CallbackOptions): Promise<void> {
  const role = options.role ?? 'generator';

  if (role === 'generator') {
    await runGeneratorCallback(taskId, options);
  } else if (role === 'evaluator') {
    await runEvaluatorCallback(taskId, options);
  } else {
    throw new Error(`Invalid role: ${role}. Must be generator or evaluator.`);
  }
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

/** Resolve the actual model name from config agents map */
function resolveModelName(config: NexumConfig, agentId: string, reportedModel?: string): string {
  // If generator reported a standard model name, use it
  if (reportedModel && !['codex', 'claude', 'auto'].includes(reportedModel.toLowerCase())) {
    return reportedModel;
  }
  // Otherwise look up from config
  const agentConfig = config.agents?.[agentId];
  if (agentConfig?.model) return agentConfig.model;
  // Fallback: derive from agentId prefix
  if (agentId.startsWith('codex-')) return 'gpt-5.4';
  if (agentId.startsWith('claude-')) return 'claude-sonnet-4-6';
  return reportedModel || 'unknown';
}

/** Get the latest commit message from git log */
async function getLastCommitMessage(projectDir: string): Promise<string> {
  try {
    const { stdout } = await execFileAsync('git', ['-C', projectDir, 'log', '-1', '--pretty=%s'], { encoding: 'utf8' });
    return stdout.trim();
  } catch {
    return '';
  }
}

async function getNextSessionName(
  sessionFamily: AgentCli,
  role: SessionRole,
  projectDir: string
): Promise<string> {
  const nexumDir = path.join(projectDir, 'nexum');
  const counterPath = path.join(nexumDir, SESSION_COUNTER_FILENAME);
  const lockPath = `${counterPath}${SESSION_COUNTER_LOCK_SUFFIX}`;

  await mkdir(nexumDir, { recursive: true });
  const releaseLock = await acquireSessionCounterLock(lockPath);

  try {
    const nextNumber = await readAndBumpSessionCounter(counterPath);
    const paddedNumber = String(nextNumber).padStart(2, '0');
    return `${sessionFamily}-${role === 'gen' ? 'gen' : 'eval'}-${paddedNumber}`;
  } finally {
    await releaseLock();
  }
}

async function acquireSessionCounterLock(lockPath: string): Promise<() => Promise<void>> {
  for (let attempt = 0; attempt < 100; attempt += 1) {
    try {
      const handle = await open(lockPath, 'wx');
      return async () => {
        await handle.close().catch(() => {});
        await unlink(lockPath).catch(() => {});
      };
    } catch (err) {
      if ((err as NodeJS.ErrnoException).code !== 'EEXIST') {
        throw err;
      }
      await new Promise((resolve) => setTimeout(resolve, 25));
    }
  }

  throw new Error(`Timed out waiting for session counter lock: ${lockPath}`);
}

async function readAndBumpSessionCounter(counterPath: string): Promise<number> {
  const raw = await readFile(counterPath, 'utf8').catch((err: NodeJS.ErrnoException) => {
    if (err.code === 'ENOENT') {
      return '';
    }
    throw err;
  });
  const currentState = parseSessionCounter(raw, counterPath);
  const nextNumber = currentState.next;
  const nextState = { next: nextNumber + 1 };
  const tempPath = `${counterPath}.${process.pid}.${Date.now()}.tmp`;
  await writeFile(tempPath, `${JSON.stringify(nextState, null, 2)}\n`, 'utf8');
  await rename(tempPath, counterPath);
  return nextNumber;
}

function parseSessionCounter(raw: string, counterPath: string): { next: number } {
  if (!raw.trim()) {
    return { next: 1 };
  }

  const parsed = JSON.parse(raw) as { next?: unknown };
  if (!Number.isInteger(parsed.next) || (parsed.next as number) < 1) {
    throw new Error(`Invalid session counter in ${counterPath}`);
  }

  return { next: parsed.next as number };
}

// ─── Generator Callback ──────────────────────────────────────────────────────

async function runGeneratorCallback(taskId: string, options: CallbackOptions): Promise<void> {
  const projectDir = options.project;
  await syncTasksWithContracts(projectDir, { taskId });
  const task = await getTask(projectDir, taskId);
  if (!task) throw new Error(`Task not found: ${taskId}`);

  if (shouldIgnoreGeneratorCallback(task.status)) {
    console.log(JSON.stringify({ ok: true, taskId, status: task.status, ignored: true }));
    return;
  }

  if (task.status !== TaskStatus.Pending && task.status !== TaskStatus.Running) {
    throw new Error(`Task ${taskId} cannot process generator callback from status ${task.status}.`);
  }

  const contract = await loadContract(projectDir, task.contract_path);
  const config = await loadConfig(projectDir);
  const resolvedContract = resolveContractAgents(contract, config);
  const generatorAgentId = resolvedContract.generator;

  const inputTokens = parseInt(options.inputTokens ?? '0', 10) || 0;
  const outputTokens = parseInt(options.outputTokens ?? '0', 10) || 0;
  const model = resolveModelName(config, generatorAgentId, options.model);

  const currentHead = await getHeadCommit(projectDir).catch(() => '');
  const hasRemote = !!(config.git?.remote);
  const commitMissing = hasRemote && task.base_commit && currentHead && currentHead === task.base_commit;

  const startedAt = task.started_at ? new Date(task.started_at).getTime() : Date.now();
  const elapsedMs = Date.now() - startedAt;
  const commitMessage = commitMissing ? '' : await getLastCommitMessage(projectDir);

  // ── Step 1: Update status ──
  await updateTask(projectDir, taskId, {
    status: TaskStatus.GeneratorDone,
    ...(currentHead ? { commit_hash: currentHead } : {}),
  });

  // ── Step 2: Notify ──
  const target = config.notify?.target;
  if (target) {
    const msg = commitMissing
      ? formatCommitMissing({ taskId, taskName: task.name, headHash: currentHead })
      : formatGeneratorDone({
          taskId,
          taskName: task.name,
          agent: generatorAgentId,
          model,
          inputTokens,
          outputTokens,
          scopeFiles: resolvedContract.scope.files,
          commitHash: currentHead,
          commitMessage,
          iteration: task.iteration,
          elapsedMs,
        });

    await sendMessage(target, msg).catch(() => {});
  }

  // ── Step 3: Auto-dispatch evaluator ──
  try {
    const evaluatorExecution = resolveAgentExecution(config, resolvedContract.evaluator);
    const sessionName = await getNextSessionName(evaluatorExecution.cli, 'eval', projectDir);
    await enqueueDispatchEntry(projectDir, {
      taskId,
      action: 'spawn-evaluator',
      role: 'evaluator',
      projectDir,
      sessionName,
    });
    const dispatched = await dispatchAgentWebhook(taskId, 'evaluator', projectDir, sessionName);
    if (dispatched) {
      console.log(`[callback] auto-dispatched evaluator for ${taskId} via webhook`);
    }
  } catch (err) {
    console.warn(`[callback] auto-dispatch evaluator failed for ${taskId}: ${err instanceof Error ? err.message : err}`);
  }

  console.log(JSON.stringify({ ok: true, taskId, status: 'generator_done', commitMissing: !!commitMissing, model, inputTokens, outputTokens }));
}

// ─── Evaluator Callback ──────────────────────────────────────────────────────

async function runEvaluatorCallback(taskId: string, options: CallbackOptions): Promise<void> {
  const projectDir = options.project;
  await syncTasksWithContracts(projectDir, { taskId });
  const task = await getTask(projectDir, taskId);
  if (!task) throw new Error(`Task not found: ${taskId}`);

  if (shouldIgnoreEvaluatorCallback(task.status)) {
    console.log(JSON.stringify({ ok: true, taskId, role: 'evaluator', status: task.status, ignored: true }));
    return;
  }

  if (task.status !== TaskStatus.GeneratorDone && task.status !== TaskStatus.Evaluating) {
    throw new Error(`Task ${taskId} cannot process evaluator callback from status ${task.status}.`);
  }
  if (!task.eval_result_path) throw new Error(`Task ${taskId} has no eval_result_path`);

  const contract = await loadContract(projectDir, task.contract_path);
  const config = await loadConfig(projectDir);
  const target = config.notify?.target;
  const resolvedContract = resolveContractAgents(contract, config);
  const evaluatorAgentId = resolvedContract.evaluator;

  const evalResultPath = resolvePath(projectDir, task.eval_result_path);
  const verdict = await readEvalVerdict(evalResultPath);
  const evalSummary = await parseEvalResult(evalResultPath);
  const iteration = task.iteration ?? 0;
  const startedAt = task.started_at ? new Date(task.started_at).getTime() : Date.now();
  const elapsedMs = Date.now() - startedAt;
  const evalModel = resolveModelName(config, evaluatorAgentId);

  // ── Step 1+2: Run complete ──
  const result = await runComplete(taskId, verdict, projectDir);
  if (result.noop) {
    console.log(JSON.stringify({ ok: true, taskId, role: 'evaluator', verdict, action: result.action, ignored: true }));
    return;
  }

  // ── Step 3: Notify ──
  if (target) {
    if (result.action === 'done') {
      const tasks = await readTasks(projectDir);
      const overallDone = tasks.filter((t) => t.status === TaskStatus.Done).length;
      const activeBatch = await getActiveBatch(projectDir);
      const batchProgress = activeBatch ? await getBatchProgress(projectDir, activeBatch) : null;

      const msg = formatReviewPassed({
        taskId,
        taskName: resolvedContract.name,
        evaluator: evaluatorAgentId,
        model: evalModel,
        elapsedMs,
        iteration,
        passCount: evalSummary.passCount,
        totalCount: evalSummary.totalCount,
        unlockedTasks: result.unlockedTasks ?? [],
        progress: `${overallDone}/${tasks.length}`,
        batchProgress: batchProgress
          ? `${batchProgress.batch}: ${batchProgress.done}/${batchProgress.total}`
          : undefined,
      });
      await sendMessage(target, msg).catch(() => {});

      // ── Batch done summary ──
      if (activeBatch && batchProgress && batchProgress.done === batchProgress.total) {
        const batchTasks = tasks.filter((t) => t.batch === activeBatch);
        const batchStartTime = batchTasks.reduce((earliest, t) => {
          const ts = t.started_at ? new Date(t.started_at).getTime() : Date.now();
          return ts < earliest ? ts : earliest;
        }, Date.now());

        const batchMsg = formatBatchDone({
          batchName: activeBatch,
          tasks: batchTasks.map((t) => ({
            taskId: t.id,
            taskName: t.name,
            status: t.status === TaskStatus.Done ? 'done' : 'fail',
            elapsedMs: t.started_at ? Date.now() - new Date(t.started_at).getTime() : 0,
          })),
          totalElapsedMs: Date.now() - batchStartTime,
        });
        await sendMessage(target, batchMsg).catch(() => {});
      }

    } else if (result.action === 'retry') {
      const msg = formatReviewFailed({
        taskId,
        taskName: resolvedContract.name,
        evaluator: evaluatorAgentId,
        model: evalModel,
        iteration,
        passCount: evalSummary.passCount,
        totalCount: evalSummary.totalCount,
        criteriaResults: evalSummary.criteriaResults,
        feedback: evalSummary.feedback,
        autoRetryHint: `自动重试中，第${iteration + 2}次迭代`,
      });
      await sendMessage(target, msg).catch(() => {});

    } else if (result.action === 'escalated') {
      const history = evalSummary.criteriaResults.length > 0
        ? [{ iteration, feedback: evalSummary.feedback, criteriaResults: evalSummary.criteriaResults }]
        : [];
      const msg = formatEscalation({
        taskId,
        taskName: resolvedContract.name,
        evaluator: evaluatorAgentId,
        history,
        retryCommand: `nexum retry ${taskId} --force`,
      });
      await sendMessage(target, msg).catch(() => {});
    }
  }

  // ── Step 4: Auto-dispatch next step ──
  if (result.action === 'retry' && result.retryPayload) {
    try {
      const generatorExecution = resolveAgentExecution(config, resolvedContract.generator);
      const sessionName = await getNextSessionName(generatorExecution.cli, 'gen', projectDir);
      await enqueueDispatchEntry(projectDir, {
        taskId,
        action: 'spawn-retry',
        role: 'generator',
        projectDir,
        sessionName,
      });
      const dispatched = await dispatchAgentWebhook(taskId, 'generator', projectDir, sessionName);
      if (dispatched) {
        console.log(`[callback] auto-dispatched retry generator for ${taskId} via webhook`);
      }
    } catch (err) {
      console.warn(`[callback] auto-dispatch retry failed for ${taskId}: ${err instanceof Error ? err.message : err}`);
    }
  }

  if (result.action === 'done') {
    await autoDispatchUnlockedTasks(projectDir, result.unlockedTasks ?? [], config);
  }

  console.log(JSON.stringify({ ok: true, taskId, role: 'evaluator', verdict, action: result.action }));
}

// ─── Auto-dispatch ───────────────────────────────────────────────────────────

async function autoDispatchUnlockedTasks(
  projectDir: string,
  unlockedIds: string[],
  config: NexumConfig
): Promise<void> {
  if (unlockedIds.length === 0) return;
  const tasks = await readTasks(projectDir);

  for (const id of unlockedIds) {
    const task = tasks.find((t) => t.id === id && t.status === TaskStatus.Pending);
    if (!task) continue;

    try {
      const contract = await loadContract(projectDir, task.contract_path);
      const resolvedContract = resolveContractAgents(contract, config);
      const generatorExecution = resolveAgentExecution(config, resolvedContract.generator);
      const sessionName = await getNextSessionName(generatorExecution.cli, 'gen', projectDir);
      await enqueueDispatchEntry(projectDir, {
        taskId: id,
        action: 'spawn-next',
        role: 'generator',
        projectDir,
        sessionName,
      });
      const dispatched = await dispatchAgentWebhook(id, 'generator', projectDir, sessionName);
      if (dispatched) {
        console.log(`[callback] auto-dispatched next generator for ${id} via webhook`);
      }
    } catch (err) {
      console.warn(`[callback] auto-dispatch generator failed for ${id}: ${err instanceof Error ? err.message : err}`);
    }
  }
}

async function readEvalVerdict(evalResultPath: string): Promise<EvalVerdict> {
  const content = await readFile(evalResultPath, 'utf8');
  const match = content.match(/^\s*verdict:\s*(pass|fail|escalated)\s*(?:#.*)?$/m);
  if (!match?.[1]) throw new Error(`Unable to parse verdict from ${evalResultPath}`);
  return match[1] as EvalVerdict;
}

// ─── Shared Helpers ──────────────────────────────────────────────────────────

async function loadContract(projectDir: string, contractPath: string) {
  const absPath = path.isAbsolute(contractPath) ? contractPath : path.join(projectDir, contractPath);
  return parseContract(absPath);
}

function resolvePath(projectDir: string, filePath: string): string {
  return path.isAbsolute(filePath) ? filePath : path.join(projectDir, filePath);
}

function shouldIgnoreGeneratorCallback(status: TaskStatus): boolean {
  return (
    status === TaskStatus.GeneratorDone ||
    status === TaskStatus.Evaluating ||
    status === TaskStatus.Done ||
    status === TaskStatus.Escalated ||
    status === TaskStatus.Cancelled
  );
}

function shouldIgnoreEvaluatorCallback(status: TaskStatus): boolean {
  return (
    status === TaskStatus.Pending ||
    status === TaskStatus.Done ||
    status === TaskStatus.Escalated ||
    status === TaskStatus.Cancelled
  );
}

// ─── CLI ─────────────────────────────────────────────────────────────────────

export function registerCallback(program: Command): void {
  program
    .command('callback <taskId>')
    .description('Process generator/evaluator callback: update status, notify, auto-dispatch')
    .option('--project <dir>', 'Project directory', process.cwd())
    .option('--role <role>', 'generator | evaluator', 'generator')
    .option('--model <name>', 'Model used by generator')
    .option('--input-tokens <n>', 'Input tokens consumed')
    .option('--output-tokens <n>', 'Output tokens consumed')
    .action(async (taskId: string, options: CallbackOptions) => {
      try {
        await runCallback(taskId, options);
      } catch (err) {
        console.error('callback failed:', err instanceof Error ? err.message : err);
        process.exit(1);
      }
    });
}
