/**
 * Common Formatters
 * Shared helper functions for output formatting
 */

import type { ExpertResult } from '../skills/multi-expert-orchestrator.js'

export { textResult, errorResult }

function textResult(text: string, details?: Record<string, unknown>) {
  return {
    content: [{ type: 'text' as const, text }],
    details: details ?? {},
  }
}

function errorResult(text: string) {
  return {
    content: [{ type: 'text' as const, text }],
    details: { success: false },
  }
}

export function formatDuration(durationMs: number): string {
  return `${(durationMs / 1000).toFixed(1)}s`
}

export function formatExpertResults(results: ExpertResult[]): { succeeded: ExpertResult[]; failed: ExpertResult[] } {
  return {
    succeeded: results.filter(r => r.success),
    failed: results.filter(r => !r.success),
  }
}

export function formatSucceededSection(succeeded: ExpertResult[], lines: string[]) {
  if (succeeded.length === 0) return

  lines.push(`### ✅ Expert Analysis (${succeeded.length} succeeded)`)
  lines.push('')
  for (const r of succeeded) {
    lines.push(`#### ${r.name}`)
    lines.push(r.output || '_No output_')
    lines.push('')
  }
}

export function formatFailedSection(failed: ExpertResult[], lines: string[]) {
  if (failed.length === 0) return

  lines.push(`### ❌ Failed Experts (${failed.length})`)
  for (const r of failed) {
    lines.push(`- **${r.name}:** ${r.error || 'Unknown error'}`)
  }
  lines.push('')
}

export function formatNextSteps(steps: string[], lines: string[]) {
  lines.push(`### Next Steps`)
  lines.push('')
  steps.forEach((step, i) => {
    lines.push(`${i + 1}. ${step}`)
  })
  lines.push('')
}

export function formatHeader(title: string, meta: Record<string, string>, lines: string[]) {
  lines.push(`## ${title}`)
  lines.push('')
  for (const [key, value] of Object.entries(meta)) {
    lines.push(`**${key}:** ${value}`)
  }
  lines.push('')
}
