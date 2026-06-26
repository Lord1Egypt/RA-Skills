/**
 * Review Tasks Builder
 * Builds expert tasks for code review
 */

import type { ExpertTask } from '../skills/multi-expert-orchestrator.js'

const DEPTH_EXPERTS: Record<string, string[]> = {
  quick: ['rev-001'],
  standard: ['rev-001', 'rev-002'],
  deep: ['rev-001', 'rev-002', 'sec-001'],
}

const EXPERT_NAMES: Record<string, string> = {
  'rev-001': 'Code Quality Reviewer',
  'rev-002': 'Security Code Reviewer',
  'sec-001': 'Security Engineer',
}

export function buildReviewTasks(path: string, depth: string, focus: string): ExpertTask[] {
  const focusStr = focus ? `\n\nFocus areas: ${focus}` : ''
  const expertIds = DEPTH_EXPERTS[depth] || DEPTH_EXPERTS['standard']

  return expertIds.map((id, idx) => ({
    id: `review-${idx + 1}`,
    name: EXPERT_NAMES[id] || 'Code Reviewer',
    prompt: `Review code at "${path}" with ${depth} depth${focusStr}:\n\nProvide a structured review with findings and recommendations.`,
    timeoutMs: 180000,
  }))
}
