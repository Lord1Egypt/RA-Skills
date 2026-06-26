/**
 * Verify Tasks Builder
 * Builds expert tasks for checkpoint verification
 */

import type { ExpertTask } from '../skills/multi-expert-orchestrator.js'

export function buildVerifyTasks(checkpoint: string, type: string, criteria: string): ExpertTask[] {
  const criteriaStr = criteria ? `\n\nCriteria:\n${criteria}` : ''

  return [
    {
      id: 'verify-qa',
      name: 'QA Engineer',
      prompt: `Verify checkpoint "${checkpoint}" for type "${type}":\n\nProvide verification results with pass/fail status for key items.${criteriaStr}`,
      timeoutMs: 120000,
    },
    {
      id: 'verify-reviewer',
      name: 'Code Reviewer',
      prompt: `Review code quality for checkpoint "${checkpoint}":\n\nCheck for code quality, maintainability, and best practices.${criteriaStr}`,
      timeoutMs: 120000,
    },
  ]
}
