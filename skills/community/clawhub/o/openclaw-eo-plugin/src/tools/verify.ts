/**
 * EO Verify Tool Handler
 * Verifies checkpoint using MultiExpertOrchestrator
 */

import type { AgentToolResult } from '@mariozechner/pi-agent-core'
import { executeExperts } from '../skills/multi-expert-orchestrator.js'
import { textResult } from '../formatters/index.js'
import { formatVerifyOutput, formatVerifyFallback } from '../formatters/verify-formatter.js'
import { buildVerifyTasks } from '../tasks/verify-tasks.js'
import { toolLogger } from '../utils/logger.js'

export async function handleVerify(params: { checkpoint?: string; type?: string; criteria?: string }): Promise<AgentToolResult<unknown>> {
  const checkpoint = params?.checkpoint || 'milestone1'
  const type = params?.type || 'code'
  const criteria = params?.criteria || ''

  try {
    toolLogger.log(`Starting ${type} verification for: ${checkpoint}`);

    // Build verification team based on type
    const verifyTasks = buildVerifyTasks(checkpoint, type, criteria)
    const { results, summary } = await executeExperts(verifyTasks)

    const verifyOutput = formatVerifyOutput(checkpoint, type, results, summary)

    return textResult(verifyOutput, {
      success: true,
      type,
      durationMs: summary.totalDurationMs,
    })
  } catch (err) {
    const errorMsg = err instanceof Error ? err.message : String(err)
    console.error(`[eo_verify] Error: ${errorMsg}`)

    return textResult(formatVerifyFallback(checkpoint, type), {
      success: false,
      error: errorMsg,
      fallback: true,
    })
  }
}
