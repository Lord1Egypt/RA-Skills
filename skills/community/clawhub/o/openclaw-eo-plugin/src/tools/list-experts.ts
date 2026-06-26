/**
 * EO List Experts Tool Handler
 * Lists experts from the 141-expert library
 */

import type { AgentToolResult } from '@mariozechner/pi-agent-core'
import { textResult } from '../formatters/index.js'
import { listExpertsAsMarkdown, getAvailableExperts } from '../experts/index.js'

export function handleListExperts(params: { filter?: string }): AgentToolResult<unknown> {
  const filter = params?.filter

  if (filter) {
    const experts = getAvailableExperts().filter(e =>
      e.name.toLowerCase().includes(filter.toLowerCase()) ||
      e.role.toLowerCase().includes(filter.toLowerCase()) ||
      e.description.toLowerCase().includes(filter.toLowerCase())
    )

    if (experts.length === 0) {
      return textResult(`👥 No experts found matching "${filter}"\n\nTry filtering by role (e.g., 'architect', 'planner', 'qa') or name.`)
    }

    const lines = [`## 👥 EO Expert Library - Filtered: "${filter}"`, `Found ${experts.length} experts:\n`]
    for (const e of experts) {
      lines.push(`### ${e.name} (${e.id})`)
      lines.push(`**Role:** ${e.role}`)
      lines.push(`**Available:** ${e.available !== false ? '✅ Yes' : '❌ No'}`)
      lines.push(e.description)
      if (e.capabilities?.length) {
        lines.push(`**Capabilities:** ${e.capabilities.join(', ')}`)
      }
      lines.push('')
    }

    return textResult(lines.join('\n'))
  }

  // Full listing
  return textResult(listExpertsAsMarkdown())
}
