import { apply as applyMcpClient } from '@deepseek-ai/dsh-mcp-client'
import { mountWritingPlugin } from './adapter.js'

export const name = 'advanced-human-writing'
export const inject = ['tools', 'systemPrompt']

/**
 * DeepSeek Harness bundle adapter. The Python package owns audit planning and
 * state; the adapter mounts it and contributes generation-time writing guidance.
 */
export async function apply(ctx, config = {}) {
  await mountWritingPlugin(ctx, config, applyMcpClient)
}
