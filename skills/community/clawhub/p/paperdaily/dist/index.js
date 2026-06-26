/**
 * PaperDaily OpenClaw Skill
 * 
 * Entry point for OpenClaw skill system.
 * Delegates to openclaw-paperdaily package.
 */

import { processCommand } from '../node_modules/openclaw-paperdaily/dist/src/index.js';

/**
 * OpenClaw skill handler
 */
export async function handler(context) {
  const message = context.message?.text || context.input?.text || '';

  // Check if message is a PaperDaily command
  if (message === '今日文献' || message === '刷新文献') {
    const result = await processCommand(message);
    return result;
  }

  // Not a PaperDaily command, return null to let other handlers process
  return null;
}

export default handler;
