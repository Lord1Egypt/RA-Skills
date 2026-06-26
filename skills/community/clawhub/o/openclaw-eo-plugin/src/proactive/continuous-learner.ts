/**
 * Continuous Learner
 * Ongoing learning loop that improves EO performance
 */

import { minePatterns, extractTopics, type SessionPattern, type MinedPattern } from './pattern-miner.js'

export interface LearningReport {
  sessionsAnalyzed: number
  newPatterns: number
  topicsLearned: string[]
  suggestions: string[]
}

export class ContinuousLearner {
  private sessions: SessionPattern[] = []
  private patterns: MinedPattern[] = []
  private workspace: string

  constructor(workspace: string) {
    this.workspace = workspace
  }

  addSession(toolsUsed: string[], message: string): void {
    const topics = extractTopics(message)
    this.sessions.push({
      toolsUsed,
      commonTopics: topics,
      expertInvocations: toolsUsed.filter(t => t.startsWith('eo_') && t !== 'eo_collab' && t !== 'eo_list_experts').length,
      timestamp: Date.now(),
    })

    // Re-mine patterns periodically
    if (this.sessions.length % 5 === 0) {
      this.patterns = minePatterns(this.sessions)
    }
  }

  getPatterns(): MinedPattern[] {
    return this.patterns
  }

  getReport(): LearningReport {
    const topicsLearned = [...new Set(this.sessions.flatMap(s => s.commonTopics))]
    return {
      sessionsAnalyzed: this.sessions.length,
      newPatterns: this.patterns.length,
      topicsLearned,
      suggestions: this.generateSuggestions(),
    }
  }

  private generateSuggestions(): string[] {
    const suggestions: string[] = []

    // Suggest based on common tool sequences
    const toolSeqs = this.patterns.filter(p => p.type === 'tool_sequence')
    if (toolSeqs.length > 0) {
      suggestions.push(`Common workflow: ${toolSeqs[0].pattern}`)
    }

    // Suggest based on frequent topics
    const topics = this.patterns.filter(p => p.type === 'topic')
    if (topics.length > 0) {
      suggestions.push(`Frequently worked on: ${topics.map(t => t.pattern).join(', ')}`)
    }

    return suggestions
  }
}
