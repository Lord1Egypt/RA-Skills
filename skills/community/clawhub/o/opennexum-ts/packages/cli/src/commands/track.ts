import type { Command } from 'commander';
import {
  getTask,
  updateTask,
  readTasks,
  TaskStatus,
  parseContract,
} from '@nexum/core';
import { formatDispatch, sendMessage, getChatId, getBotToken } from '@nexum/notify';
import path from 'node:path';

/**
 * track: called by the orchestrator (AI agent) after sessions_spawn succeeds.
 * Writes the sessionKey (and optional streamLogPath) to active-tasks.json
 * and sends a Telegram dispatch notification.
 */
export async function runTrack(
  taskId: string,
  sessionKey: string,
  projectDir: string,
  streamLogPath?: string
): Promise<void> {
  const task = await getTask(projectDir, taskId);
  if (!task) {
    throw new Error(`Task not found: ${taskId}`);
  }

  await updateTask(projectDir, taskId, {
    acp_session_key: sessionKey,
    ...(streamLogPath ? { acp_stream_log: streamLogPath } : {}),
    updated_at: new Date().toISOString(),
  });

  // Send dispatch notification
  const chatId = getChatId();
  const botToken = getBotToken();
  if (chatId && botToken) {
    try {
      const contractAbsPath = path.isAbsolute(task.contract_path)
        ? task.contract_path
        : path.join(projectDir, task.contract_path);
      const contract = await parseContract(contractAbsPath);
      const tasks = await readTasks(projectDir);
      const doneCount = tasks.filter((t) => t.status === TaskStatus.Done).length;
      const progress = `${doneCount}/${tasks.length}`;

      const msg = formatDispatch(
        taskId,
        contract.name,
        contract.generator,
        contract.scope.files.length,
        contract.deliverables.length,
        progress
      );
      await sendMessage(chatId, msg, botToken);
    } catch {
      // Notification failure is non-fatal
    }
  }

  console.log(JSON.stringify({ ok: true, taskId, sessionKey, streamLogPath: streamLogPath ?? null }));
}

export function registerTrack(program: Command): void {
  program
    .command('track <taskId> <sessionKey>')
    .description('Record ACP session key for a running task (called by orchestrator after spawn)')
    .option('--project <dir>', 'Project directory', process.cwd())
    .option('--stream-log <path>', 'Path to ACP stream log file (from sessions_spawn streamLogPath)')
    .action(async (taskId: string, sessionKey: string, options: { project: string; streamLog?: string }) => {
      try {
        await runTrack(taskId, sessionKey, options.project, options.streamLog);
      } catch (err) {
        console.error('track failed:', err instanceof Error ? err.message : err);
        process.exit(1);
      }
    });
}
