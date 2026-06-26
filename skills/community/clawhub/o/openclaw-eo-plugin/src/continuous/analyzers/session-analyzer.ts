/**
 * Session Analyzer
 * Analyzes session data to extract insights for the learning loop
 */

export interface SessionAnalysisInput {
  toolsUsed: string[]
  messageCount: number
  lastMessage: string
  context: Record<string, unknown>
}

export interface AnalyzedSession {
  sessionId: string
  timestamp: number
  toolsUsed: string[]
  messageCount: number
  keyTopics: string[]
  successIndicators: SuccessIndicator[]
  errorIndicators: ErrorIndicator[]
  expertUsage: Map<string, number>
  workflowType: 'planning' | 'coding' | 'review' | 'debugging' | 'unknown'
}

export interface SuccessIndicator {
  type: 'completion' | 'verification' | 'positive_feedback'
  description: string
  confidence: number
}

export interface ErrorIndicator {
  type: 'error_keyword' | 'failed_tool' | 'retry'
  description: string
  severity: 'low' | 'medium' | 'high'
  count: number
}

export class SessionAnalyzer {
  private sessionHistory: AnalyzedSession[] = []

  /**
   * Analyze a session
   */
  async analyze(input: SessionAnalysisInput): Promise<AnalyzedSession> {
    const session: AnalyzedSession = {
      sessionId: `sess-${Date.now()}`,
      timestamp: Date.now(),
      toolsUsed: input.toolsUsed,
      messageCount: input.messageCount,
      keyTopics: this.extractTopics(input.lastMessage),
      successIndicators: this.detectSuccessIndicators(input),
      errorIndicators: this.detectErrorIndicators(input),
      expertUsage: this.analyzeExpertUsage(input.toolsUsed),
      workflowType: this.classifyWorkflow(input),
    }

    this.sessionHistory.push(session)
    return session
  }

  /**
   * Extract key topics from message
   */
  private extractTopics(message: string): string[] {
    const topics: string[] = []
    const topicKeywords = [
      { keywords: ['plan', 'wbs', 'milestone', 'roadmap'], topic: 'planning' },
      { keywords: ['code', 'implement', 'function', 'class'], topic: 'coding' },
      { keywords: ['review', 'check', 'verify', 'audit'], topic: 'review' },
      { keywords: ['bug', 'error', 'fix', 'issue'], topic: 'debugging' },
      { keywords: ['deploy', 'release', 'publish'], topic: 'deployment' },
      { keywords: ['test', 'qa', 'quality'], topic: 'testing' },
    ]

    const lowerMessage = message.toLowerCase()
    for (const { keywords, topic } of topicKeywords) {
      if (keywords.some(k => lowerMessage.includes(k))) {
        topics.push(topic)
      }
    }

    return [...new Set(topics)]
  }

  /**
   * Detect success indicators
   */
  private detectSuccessIndicators(input: SessionAnalysisInput): SuccessIndicator[] {
    const indicators: SuccessIndicator[] = []
    const lowerMessage = input.lastMessage.toLowerCase()

    // Completion indicators
    if (lowerMessage.includes('completed') || lowerMessage.includes('done') || lowerMessage.includes('success')) {
      indicators.push({
        type: 'completion',
        description: 'Task completion detected',
        confidence: 0.8,
      })
    }

    // Verification indicators
    if (lowerMessage.includes('verified') || lowerMessage.includes('validated') || lowerMessage.includes('passed')) {
      indicators.push({
        type: 'verification',
        description: 'Verification passed',
        confidence: 0.9,
      })
    }

    return indicators
  }

  /**
   * Detect error indicators
   */
  private detectErrorIndicators(input: SessionAnalysisInput): ErrorIndicator[] {
    const indicators: ErrorIndicator[] = []
    const lowerMessage = input.lastMessage.toLowerCase()

    // Error keyword detection
    const errorWords = ['error', 'failed', 'exception', 'crash', 'bug']
    for (const word of errorWords) {
      const regex = new RegExp(`\\b${word}\\b`, 'gi')
      const matches = lowerMessage.match(regex)
      if (matches) {
        indicators.push({
          type: 'error_keyword',
          description: `Keyword "${word}" detected`,
          severity: word === 'error' || word === 'failed' ? 'high' : 'medium',
          count: matches.length,
        })
      }
    }

    return indicators
  }

  /**
   * Analyze which experts were used
   */
  private analyzeExpertUsage(toolsUsed: string[]): Map<string, number> {
    const usage = new Map<string, number>()

    for (const tool of toolsUsed) {
      if (tool.startsWith('eo_')) {
        const count = usage.get(tool) || 0
        usage.set(tool, count + 1)
      }
    }

    return usage
  }

  /**
   * Classify the workflow type
   */
  private classifyWorkflow(input: SessionAnalysisInput): AnalyzedSession['workflowType'] {
    const lowerMessage = input.lastMessage.toLowerCase()

    if (lowerMessage.includes('plan') || lowerMessage.includes('wbs')) return 'planning'
    if (lowerMessage.includes('code') || lowerMessage.includes('implement')) return 'coding'
    if (lowerMessage.includes('review') || lowerMessage.includes('check')) return 'review'
    if (lowerMessage.includes('bug') || lowerMessage.includes('error') || lowerMessage.includes('fix')) return 'debugging'

    return 'unknown'
  }

  /**
   * Get recent sessions
   */
  getRecentSessions(count: number = 10): AnalyzedSession[] {
    return this.sessionHistory.slice(-count)
  }

  /**
   * Get session statistics
   */
  getStats(): {
    totalSessions: number
    avgMessageCount: number
    topWorkflow: AnalyzedSession['workflowType'] | null
  } {
    if (this.sessionHistory.length === 0) {
      return { totalSessions: 0, avgMessageCount: 0, topWorkflow: null }
    }

    const totalMessages = this.sessionHistory.reduce((sum, s) => sum + s.messageCount, 0)
    const workflowCounts = new Map<AnalyzedSession['workflowType'], number>()

    for (const session of this.sessionHistory) {
      const count = workflowCounts.get(session.workflowType) || 0
      workflowCounts.set(session.workflowType, count + 1)
    }

    let topWorkflow: AnalyzedSession['workflowType'] | null = null
    let maxCount = 0
    for (const [workflow, count] of workflowCounts) {
      if (count > maxCount) {
        maxCount = count
        topWorkflow = workflow
      }
    }

    return {
      totalSessions: this.sessionHistory.length,
      avgMessageCount: totalMessages / this.sessionHistory.length,
      topWorkflow,
    }
  }
}
