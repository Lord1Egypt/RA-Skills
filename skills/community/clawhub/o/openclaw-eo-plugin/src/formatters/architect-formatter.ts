/**
 * Architect Formatter
 * Formats system architecture design output
 */

import type { ExpertResult } from '../skills/multi-expert-orchestrator.js'
import { formatDuration, formatExpertResults, formatSucceededSection, formatNextSteps, formatHeader } from './common.js'

export function formatArchitectOutput(task: string, style: string, language: string, results: ExpertResult[], summary: any): string {
  const lines: string[] = []

  formatHeader('🏗️ EO Architecture Design', {
    Task: task,
    Style: style.toUpperCase(),
    Language: language,
    Duration: formatDuration(summary.totalDurationMs),
  }, lines)

  const { succeeded } = formatExpertResults(results)
  formatSucceededSection(succeeded, lines)

  // Add architecture template
  lines.push(`### 📐 Architecture Summary`)
  lines.push('')
  lines.push('| Layer | Technology | Reason |')
  lines.push('|-------|------------|--------|')
  lines.push('| Frontend | React 18 + TypeScript | Type safety, ecosystem |')
  lines.push('| Backend | Node.js/Fastify | Performance, TypeScript |')
  lines.push('| Database | PostgreSQL 15 | Reliability, JSONB |')
  lines.push('| Cache | Redis 7 | Performance |')
  lines.push('| Deploy | Docker + K8s | Container orchestration |')
  lines.push('')

  lines.push(`### ⚠️ Risk Assessment`)
  lines.push('')
  lines.push('| Risk | Impact | Probability | Mitigation |')
  lines.push('|------|--------|-------------|------------|')
  lines.push('| High concurrency | Medium | High | Auto-scaling |')
  lines.push('| Data loss | High | Low | Daily backups |')
  lines.push('| Security breach | High | Medium | Auth + HTTPS |')
  lines.push('')

  formatNextSteps([
    'Review architecture with your team',
    "Use 'eo_verify checkpoint=milestone1 type=architecture' to validate",
    "Use 'eo_code_review' after implementing core modules",
  ], lines)

  return lines.join('\n')
}

export function formatArchitectFallback(task: string, style: string, language: string): string {
  return `## 🏗️ EO Architecture Design

**Task:** ${task}
**Style:** ${style.toUpperCase()}
**Language:** ${language}
**Note:** Orchestrator unavailable - showing template

### Tech Stack

| Layer | Technology | Reason |
|-------|------------|--------|
| Frontend | React 18 + TypeScript | Type safety, ecosystem |
| Backend | Node.js/Fastify | Performance, TypeScript |
| Database | PostgreSQL 15 | Reliability, JSONB |
| Cache | Redis 7 | Performance |
| Deploy | Docker + K8s | Container orchestration |

### Module Structure

\`\`\`
src/
├── api/              # REST API layer
├── services/         # Business logic
├── models/           # Data models
├── repositories/    # Database access
└── utils/            # Shared utilities
\`\`\`

### Expert Team
- **System Architect (arch-001)**: Overall system design
- **Data Architect (arch-003)**: Database & caching design
- **API Developer (be-001)**: API contract design
- **CI/CD Engineer (devops-001)**: Deployment pipeline

### Next Steps
1. Review and validate the architecture with your team
2. Use 'eo_verify checkpoint=milestone1 type=architecture' to validate`
}
