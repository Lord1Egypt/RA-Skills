import type { Command } from 'commander';
import { getTask, updateTask, TaskStatus, loadConfig } from '@nexum/core';
import { sendMessage } from '@nexum/notify';

export async function runCallback(taskId: string, projectDir: string): Promise<void> {
  const task = await getTask(projectDir, taskId);
  if (!task) {
    throw new Error(`Task not found: ${taskId}`);
  }

  await updateTask(projectDir, taskId, {
    status: TaskStatus.GeneratorDone,
  });

  // Read Telegram config from nexum/config.json (notify.target = chatId, notify.botToken)
  // Fall back to environment variables for compatibility
  const config = await loadConfig(projectDir).catch(() => ({}));
  const notifyConfig = (config as Record<string, unknown>).notify as Record<string, string> | undefined;
  const chatId = notifyConfig?.target ?? process.env['TELEGRAM_CHAT_ID'];
  const botToken = notifyConfig?.botToken ?? process.env['TELEGRAM_BOT_TOKEN'];

  if (chatId && botToken) {
    const message = [
      '✅ Generator 完成',
      '━━━━━━━━━━━━━━━',
      `📋 任务内容: ${task.name}`,
      `🆔 任务ID: ${taskId}`,
      '💬 等待编排者触发 eval',
    ].join('\n');

    await sendMessage(chatId, message, botToken);
  }

  console.log(JSON.stringify({ ok: true, taskId, status: TaskStatus.GeneratorDone }));
}

export function registerCallback(program: Command): void {
  program
    .command('callback <taskId>')
    .description('Mark generator completion and send callback notification')
    .option('--project <dir>', 'Project directory', process.cwd())
    .action(async (taskId: string, options: { project: string }) => {
      try {
        await runCallback(taskId, options.project);
      } catch (err) {
        console.error('callback failed:', err instanceof Error ? err.message : err);
        process.exit(1);
      }
    });
}
