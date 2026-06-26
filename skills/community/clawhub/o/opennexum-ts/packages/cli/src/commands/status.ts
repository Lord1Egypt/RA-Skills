import { readFile } from 'node:fs/promises';
import type { Command } from 'commander';
import { readTasks, TaskStatus, NexumError, ErrorCode } from '@nexum/core';
import { getSessionStatus } from '@nexum/spawn';

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

export async function runStatus(projectDir: string, options: { json?: boolean } = {}): Promise<void> {
  const tasks = await readTasks(projectDir);

  if (options.json) {
    const output = tasks.map((task) => ({
      id: task.id,
      name: task.name,
      status: task.status,
      iteration: task.iteration,
      acp_session_key: task.acp_session_key,
      acp_stream_log: task.acp_stream_log,
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

  for (const task of tasks) {
    const icon = STATUS_ICONS[task.status] ?? '❓';
    const sessionInfo = task.acp_session_key
      ? ` [${task.acp_session_key.slice(-8)}]`
      : '';

    let activityLine = '';
    if (
      (task.status === TaskStatus.Running || task.status === TaskStatus.Evaluating) &&
      task.acp_stream_log
    ) {
      const activity = await getStreamActivity(task.acp_stream_log);
      if (activity) {
        activityLine = `\n    💬 ${activity}`;
      }
    }

    let sessionStatus = '';
    if (task.status === TaskStatus.Running && task.acp_session_key) {
      try {
        const s = await getSessionStatus(task.acp_session_key);
        sessionStatus = s !== 'running' ? ` (ACP: ${s})` : '';
      } catch { /* ignore */ }
    }

    console.log(
      `${icon} ${task.id}  ${task.name.slice(0, 50)}${sessionInfo}${sessionStatus}${activityLine}`
    );
  }

  const done = tasks.filter((t) => t.status === TaskStatus.Done).length;
  console.log(`\n📊 进度: ${done}/${tasks.length} done`);
}

export function registerStatus(program: Command): void {
  program
    .command('status')
    .description('Show status of all tasks with live ACP activity')
    .option('--project <dir>', 'Project directory', process.cwd())
    .option('--json', 'Output task list as JSON')
    .action(async (options: { project: string; json?: boolean }) => {
      try {
        await runStatus(options.project, { json: options.json });
      } catch (err) {
        if (err instanceof NexumError) {
          console.error(`status failed [${err.code}]: ${err.message}`);
        } else {
          console.error('status failed:', err instanceof Error ? err.message : err);
        }
        process.exit(1);
      }
    });
}
