/**
 * EO Collab Tool Handler v4
 */

import type { AgentToolResult } from '@mariozechner/pi-agent-core'
import { textResult } from '../formatters/index.js'
import { EXPERT_STATS } from '../experts/data.js'
import { PLUGIN_VERSION } from '../config.js'
import { EXPERTS } from '../experts/data.js'
import { toolLogger } from '../utils/logger.js'

export async function handleCollab(params: { task?: string }): Promise<AgentToolResult<unknown>> {
  const task = params?.task || 'general'
  const startTime = Date.now()

  toolLogger.log(`Collaboration for: ${task.slice(0, 50)}...`);

  try {
    // Analyze task to determine required experts
    const taskLower = task.toLowerCase()
    let expertNames: string[] = []

    if (taskLower.includes('plan') || taskLower.includes('规划')) {
      expertNames = ['Project Planner', 'Tech Lead', 'QA Engineer']
    } else if (taskLower.includes('architect') || taskLower.includes('架构')) {
      expertNames = ['System Architect', 'Frontend Architect', 'Backend Architect']
    } else if (taskLower.includes('review') || taskLower.includes('审查')) {
      expertNames = ['Code Reviewer', 'Security Auditor']
    } else if (taskLower.includes('security') || taskLower.includes('安全')) {
      expertNames = ['Security Auditor', 'AppSec Engineer']
    } else if (taskLower.includes('deploy') || taskLower.includes('部署')) {
      expertNames = ['DevOps Engineer', 'SRE']
    } else {
      expertNames = ['Project Planner', 'Tech Lead', 'Code Reviewer']
    }

    const experts = expertNames.map(name => {
      const expert = EXPERTS[name]
      return {
        name,
        description: expert?.description || 'Expert description'
      }
    })

    // Build output
    const lines = [
      `🤖 **EO Multi-Expert Collaboration v${PLUGIN_VERSION}**`,
      ``,
      `**Task:** ${task}`,
      ``,
      `**Detected Experts:** ${experts.length}`,
      ``,
      `---`,
      ``
    ]

    for (const expert of experts) {
      lines.push(`### ${expert.name}`)
      lines.push(expert.description)
      lines.push(``)
    }

    lines.push(`---`)
    lines.push(`**Suggested Subagent Spawning:**`)
    lines.push(``)
    lines.push(`\`\`\``)
    for (const expert of experts) {
      lines.push(`sessions_spawn({`)
      lines.push(`  task: "作为 ${expert.name}，请处理以下任务：${task}",`)
      lines.push(`  runtime: "subagent",`)
      lines.push(`  timeout: 180000`)
      lines.push(`})`)
    }
    lines.push(`\`\`\``)
    lines.push(``)
    lines.push(`⏱️ Duration: ${Date.now() - startTime}ms`)

    return textResult(lines.join('\n'), {
      success: true,
      expertCount: experts.length,
      durationMs: Date.now() - startTime
    })

  } catch (err) {
    const errorMsg = err instanceof Error ? err.message : String(err)
    console.error(`[eo_collab v4] Error: ${errorMsg}`)

    return textResult(`❌ **EO Collab Error:** ${errorMsg}`, {
      success: false,
      error: errorMsg
    })
  }
}
