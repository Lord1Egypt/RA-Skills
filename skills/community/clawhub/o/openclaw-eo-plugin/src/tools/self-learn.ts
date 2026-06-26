/**
 * EO Self-Learning Tool Handler
 * Self-Learning Engine for feedback and patterns
 */

import type { AgentToolResult } from '@mariozechner/pi-agent-core'
import { SelfLearningOrchestrator } from '../self-learning/orchestrator.js'
import { textResult } from '../formatters/index.js'
import { WORKSPACE } from '../config.js'

const selfLearning = new SelfLearningOrchestrator(WORKSPACE, { enabled: true })

export function handleSelfLearn(params: any): AgentToolResult<unknown> {
  const s = selfLearning.getStatus()
  return textResult(`Self-Learning: Enabled=${s.enabled}, Feedback=${s.feedbackCount}, Patterns=${s.patternCount}`)
}
