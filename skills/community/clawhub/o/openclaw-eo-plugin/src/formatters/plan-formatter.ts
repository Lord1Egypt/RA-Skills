/**
 * Plan Formatter
 * Formats project planning output
 */

import type { ExpertResult } from '../skills/multi-expert-orchestrator.js'
import { formatDuration, formatExpertResults, formatSucceededSection, formatFailedSection, formatNextSteps, formatHeader } from './common.js'

export function formatPlanOutput(task: string, results: ExpertResult[], summary: any): string {
  const lines: string[] = []

  formatHeader('📋 EO Project Plan', {
    Task: task,
    Duration: formatDuration(summary.totalDurationMs),
    'Expert Team': `${results.length} experts`,
  }, lines)

  const { succeeded, failed } = formatExpertResults(results)
  formatSucceededSection(succeeded, lines)
  formatFailedSection(failed, lines)

  // Add WBS structure
  lines.push(`### 📊 WBS (Work Breakdown Structure)`)
  lines.push('')
  lines.push('| Phase | Tasks | Est. Hours |')
  lines.push('|-------|-------|------------|')
  lines.push('| M1: Requirements & Planning | 4 | 12h |')
  lines.push('| M2: Core Development | 4 | 32h |')
  lines.push('| M3: Testing & QA | 4 | 22h |')
  lines.push('| M4: Deployment & Delivery | 4 | 10h |')
  lines.push('| **Total** | **16** | **76h** |')
  lines.push('')

  formatNextSteps([
    "Review the expert analysis above",
    "Use 'eo_architect' to design system architecture",
    "Use 'eo_verify checkpoint=milestone1' after Phase 1",
    "Use 'eo_code_review' after development",
  ], lines)

  return lines.join('\n')
}

export function formatPlanFallback(task: string, priority: string): string {
  return `## 📋 EO Project Plan

**Task:** ${task}
**Priority:** ${priority}
**Note:** Orchestrator unavailable - showing template

### WBS (Work Breakdown Structure)

| Phase | Tasks | Est. Hours |
|-------|-------|------------|
| M1: Requirements & Planning | 4 | 12h |
| M2: Core Development | 4 | 32h |
| M3: Testing & QA | 4 | 22h |
| M4: Deployment & Delivery | 4 | 10h |
| **Total** | **16** | **76h** |

### Expert Team
- **Planner (plan-001)**: Project planning & WBS creation
- **Frontend (fe-001)**: React/UI implementation analysis
- **Backend (be-001)**: API & service implementation analysis
- **QA (qa-001)**: Testing strategy & coverage planning

### Next Steps
1. Use 'eo_architect' to design system architecture
2. Use 'eo_verify checkpoint=milestone1' after Phase 1
3. Use 'eo_code_review' after development`
}
