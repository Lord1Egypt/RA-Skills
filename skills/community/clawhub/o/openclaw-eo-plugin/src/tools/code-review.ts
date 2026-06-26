/**
 * EO Code Review Tool Handler
 * Reviews code using MultiExpertOrchestrator
 */

import type { AgentToolResult } from '@mariozechner/pi-agent-core'
import { executeExperts } from '../skills/multi-expert-orchestrator.js'
import { textResult } from '../formatters/index.js'
import { formatReviewOutput, formatReviewFallback } from '../formatters/review-formatter.js'
import { buildReviewTasks } from '../tasks/review-tasks.js'
import { toolLogger } from '../utils/logger.js'

export async function handleCodeReview(params: { path?: string; depth?: string; focus?: string }): Promise<AgentToolResult<unknown>> {
  const path = params?.path || './src'
  const depth = params?.depth || 'standard'
  const focus = params?.focus || ''

  try {
    toolLogger.log(`Starting ${depth} code review for: ${path}`);

    // Build review team based on depth
    const reviewTasks = buildReviewTasks(path, depth, focus)
    const { results, summary } = await executeExperts(reviewTasks)

    const reviewOutput = formatReviewOutput(path, depth, results, summary)

    return textResult(reviewOutput, {
      success: true,
      depth,
      durationMs: summary.totalDurationMs,
    })
  } catch (err) {
    const errorMsg = err instanceof Error ? err.message : String(err)
    console.error(`[eo_code_review] Error: ${errorMsg}`)

    return textResult(formatReviewFallback(path, depth), {
      success: false,
      error: errorMsg,
      fallback: true,
    })
  }
}
