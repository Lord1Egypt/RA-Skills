import { readFile } from 'node:fs/promises';
import type { Command } from 'commander';
import {
  getActiveBatch,
  getBatchProgress,
  readTasks,
  syncTasksWithContracts,
  TaskStatus,
  type Task,
  NexumError,
} from '@nexum/core';
import { getSessionStatus } from '@nexum/spawn';
import { archiveDoneTasks } from '../lib/archive.js';
import { getDisplaySession, getTrackedSessions } from '../lib/task-session.js';

/** Read the last N non-empty lines from an ACP stream log JSONL file */
async function getStreamActivity(streamLogPath: string, lines = 2): Promise<string> {
  try {
    const content = await readFile(streamLogPath, 'utf8');
    const entries = content
      .split('\n')
      .filter((l) => l.trim())
      .map((l) => {
        try { return JSON.parse(l) as Record<string, unknown>; } catch { return null; }
      })
      .filter(Boolean) as Record<string, unknown>[];

    const textEntries = entries
      .filter((e) => typeof e.text === 'string' && (e.text as string).trim())
      .slice(-lines);

    if (textEntries.length === 0) return '';
    return textEntries
      .map((e) => (e.text as string).trim().slice(0, 80))
      .join(' / ');
  } catch {
    return '';
  }
}

export async function runStatus(
  projectDir: string,
  options: { json?: boolean; batch?: string } = {}
): Promise<void> {
  await syncTasksWithContracts(projectDir);
  const tasks = await readTasks(projectDir);
  const currentBatch = options.batch ?? await getActiveBatch(projectDir);
  const visibleTasks =
    options.batch === undefined ? tasks : tasks.filter((task) => task.batch === options.batch);

  if (options.json) {
    const output = visibleTasks.map((task) => ({
      id: task.id,
      name: task.name,
      status: task.status,
      batch: task.batch,
      iteration: task.iteration,
      acp_session_key: task.acp_session_key,
      acp_stream_log: task.acp_stream_log,
      generator_acp_session_key: task.generator_acp_session_key,
      generator_acp_stream_log: task.generator_acp_stream_log,
      evaluator_acp_session_key: task.evaluator_acp_session_key,
      evaluator_acp_stream_log: task.evaluator_acp_stream_log,
    }));
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  if (tasks.length === 0) {
    console.log('No tasks found.');
    return;
  }

  const STATUS_ICONS: Record<string, string> = {
    done:       '✅',
    running:    '🔄',
    evaluating: '🔍',
    pending:    '⏳',
    blocked:    '🔒',
    failed:     '🔴',
    escalated:  '🚨',
    cancelled:  '⛔',
  };

  for (const task of visibleTasks) {
    const icon = STATUS_ICONS[task.status] ?? '❓';
    const displaySession = getDisplaySession(task);
    const sessionInfo = displaySession.sessionKey
      ? ` [${displaySession.sessionKey.slice(-8)}]`
      : '';

    let activityLine = '';
    if (
      (task.status === TaskStatus.Running || task.status === TaskStatus.Evaluating) &&
      displaySession.streamLog
    ) {
      const activity = await getStreamActivity(displaySession.streamLog);
      if (activity) {
        activityLine = `\n    💬 ${activity}`;
      }
    }

    let sessionStatus = '';
    if (
      (task.status === TaskStatus.Running || task.status === TaskStatus.Evaluating) &&
      displaySession.sessionKey
    ) {
      try {
        const s = await getSessionStatus(displaySession.sessionKey);
        sessionStatus = s !== 'running' ? ` (ACP: ${s})` : '';
      } catch { /* ignore */ }
    }

    const trackedSessions = getTrackedSessions(task)
      .filter((session) => session.sessionKey && session.sessionKey !== displaySession.sessionKey)
      .map((session) => {
        const icon = session.role === 'generator' ? '🔨' : '🔍';
        return `\n    ${icon} ${session.role}: [${session.sessionKey?.slice(-8)}]`;
      })
      .join('');

    console.log(
      `${icon} ${task.id}  ${task.name.slice(0, 50)}${sessionInfo}${sessionStatus}${trackedSessions}${activityLine}`
    );
  }

  const overallDone = tasks.filter((task) => task.status === TaskStatus.Done).length;

  if (currentBatch) {
    const batchProgress = await getBatchProgress(projectDir, currentBatch);
    console.log(`\n📊 ${batchProgress.batch}: ${batchProgress.done}/${batchProgress.total}  |  总体: ${overallDone}/${tasks.length}`);
  } else {
    console.log(`\n📊 总体: ${overallDone}/${tasks.length}`);
  }
}

export function registerStatus(program: Command): void {
  program
    .command('status')
    .description('Show status of all tasks with live ACP activity')
    .option('--project <dir>', 'Project directory', process.cwd())
    .option('--batch <name>', 'Filter displayed tasks to one batch')
    .option('--json', 'Output task list as JSON')
    .action(async (options: { project: string; json?: boolean; batch?: string }) => {
      try {
        await runStatus(options.project, { json: options.json, batch: options.batch });
      } catch (err) {
        if (err instanceof NexumError) {
          console.error(`status failed [${err.code}]: ${err.message}`);
        } else {
          console.error('status failed:', err instanceof Error ? err.message : err);
        }
        process.exit(1);
      }
    });

  program
    .command('archive')
    .description('Archive done tasks into nexum/history')
    .option('--project <dir>', 'Project directory', process.cwd())
    .option('--batch <name>', 'Archive done tasks for one batch')
    .action(async (options: { project: string; batch?: string }) => {
      try {
        const result = await archiveDoneTasks(options.project, options.batch);

        if (result.archivedCount === 0) {
          console.log('No done tasks to archive.');
          return;
        }

        console.log(`Archived ${result.archivedCount} task(s) to ${result.archivePath}`);
      } catch (err) {
        console.error('archive failed:', err instanceof Error ? err.message : err);
        process.exit(1);
      }
    });
}
