// ============================================================================
// EO Multi-Expert Trigger Engine - Phase 3.2: Collaborative Decision Making
//
// Implements multi-agent voting, debate/discussion mode, and consensus building.
// ============================================================================

import { AgentKnowledgeGraph, knowledgeGraph, Experience, experienceTracker } from './knowledge-graph.js'

// ============================================================================
// Types
// ============================================================================

export type DecisionOption = {
  id: string
  label: string
  description: string
  pros?: string[]
  cons?: string[]
  confidence: number
  votes?: number
}

export interface ExpertOpinion {
  expertId: string
  expertName: string
  expertRole: string
  recommendation: 'approve' | 'reject' | 'abstain' | 'modify'
  confidence: number
  reasoning: string
  concerns?: string[]
  suggestions?: string[]
  alternative?: string
}

export interface DebateSession {
  id: string
  topic: string
  options: DecisionOption[]
  experts: string[]
  opinions: ExpertOpinion[]
  currentRound: number
  maxRounds: number
  status: 'collecting' | 'debating' | 'voting' | 'decided'
  consensusLevel: 'unanimous' | 'strong' | 'majority' | 'plurality' | 'deadlock'
  decision?: string
  createdAt: number
  updatedAt: number
}

export interface VotingResult {
  optionId: string
  optionLabel: string
  votes: { expertId: string; expertName: string; weight: number }[]
  totalWeight: number
  percentage: number
}

export interface ConsensusResult {
  success: boolean
  consensusLevel: DebateSession['consensusLevel']
  winningOption?: DecisionOption
  votingResults: VotingResult[]
  summary: string
  minorityConcerns?: ExpertOpinion[]
  recommendations?: string[]
}

export interface TriggerConfig {
  votingThreshold: number          // 0-1, required agreement ratio
  minDebateRounds: number
  maxDebateRounds: number
  enableAutoTrigger: boolean
  consensusTimeoutMs: number
  weightByExpertise: boolean       // weight votes by relevant expertise
  weightByConfidence: boolean      // weight votes by confidence
}

// ============================================================================
// Debate Manager
// ============================================================================

export class DebateManager {
  private sessions: Map<string, DebateSession> = new Map()
  private knowledgeGraph: AgentKnowledgeGraph
  private config: TriggerConfig
  
  constructor(
    knowledgeGraph: AgentKnowledgeGraph,
    config: Partial<TriggerConfig> = {}
  ) {
    this.knowledgeGraph = knowledgeGraph
    this.config = {
      votingThreshold: 0.6,
      minDebateRounds: 1,
      maxDebateRounds: 3,
      enableAutoTrigger: true,
      consensusTimeoutMs: 60000,
      weightByExpertise: true,
      weightByConfidence: true,
      ...config,
    }
  }
  
  // ============================================================================
  // Session Management
  // ============================================================================
  
  /**
   * Create a new debate session.
   */
  createSession(
    topic: string,
    options: DecisionOption[],
    expertIds: string[]
  ): DebateSession {
    const id = 'debate-' + Date.now() + '-' + Math.random().toString(36).slice(2, 6)
    
    const session: DebateSession = {
      id,
      topic,
      options,
      experts: expertIds,
      opinions: [],
      currentRound: 0,
      maxRounds: this.config.maxDebateRounds,
      status: 'collecting',
      consensusLevel: 'deadlock',
      createdAt: Date.now(),
      updatedAt: Date.now(),
    }
    
    this.sessions.set(id, session)
    return session
  }
  
  /**
   * Get session by ID.
   */
  getSession(id: string): DebateSession | undefined {
    return this.sessions.get(id)
  }
  
  /**
   * Add an expert opinion to a session.
   */
  addOpinion(
    sessionId: string,
    opinion: Omit<ExpertOpinion, 'expertName' | 'expertRole'>
  ): boolean {
    const session = this.sessions.get(sessionId)
    if (!session || session.status === 'decided') return false
    
    // Get expert info (simplified - in production would look up from expert registry)
    const expertInfo = this.getExpertInfo(opinion.expertId)
    
    const fullOpinion: ExpertOpinion = {
      ...opinion,
      expertName: expertInfo.name,
      expertRole: expertInfo.role,
    }
    
    session.opinions.push(fullOpinion)
    session.updatedAt = Date.now()
    
    // Record experience
    this.recordDebateExperience(session, fullOpinion)
    
    return true
  }
  
  /**
   * Progress to next debate round.
   */
  nextRound(sessionId: string): DebateSession | null {
    const session = this.sessions.get(sessionId)
    if (!session) return null
    
    session.currentRound++
    session.updatedAt = Date.now()
    
    if (session.currentRound >= session.maxRounds) {
      session.status = 'voting'
    } else {
      session.status = 'debating'
    }
    
    return session
  }
  
  // ============================================================================
  // Voting & Consensus
  // ============================================================================
  
  /**
   * Conduct voting on current options.
   */
  vote(sessionId: string): VotingResult[] {
    const session = this.sessions.get(sessionId)
    if (!session) return []
    
    const results: VotingResult[] = session.options.map(option => {
      const votes: { expertId: string; expertName: string; weight: number }[] = []
      
      session.opinions.forEach(opinion => {
        let weight = 1.0
        
        // Weight by expertise relevance
        if (this.config.weightByExpertise) {
          weight *= this.calculateExpertiseWeight(opinion, option)
        }
        
        // Weight by confidence
        if (this.config.weightByConfidence) {
          weight *= opinion.confidence
        }
        
        // Check if expert recommends this option
        if (opinion.recommendation === 'approve' && opinion.alternative === option.id) {
          votes.push({
            expertId: opinion.expertId,
            expertName: opinion.expertName,
            weight,
          })
        } else if (opinion.recommendation === 'modify' && opinion.suggestions?.includes(option.id)) {
          votes.push({
            expertId: opinion.expertId,
            expertName: opinion.expertName,
            weight: weight * 0.8, // Modify gets slightly less weight
          })
        }
      })
      
      const totalWeight = votes.reduce((sum, v) => sum + v.weight, 0)
      const totalPossibleWeight = session.opinions.reduce((sum, o) => {
        let w = 1.0
        if (this.config.weightByExpertise) w *= 0.5
        if (this.config.weightByConfidence) w *= o.confidence
        return sum + w
      }, 0)
      
      return {
        optionId: option.id,
        optionLabel: option.label,
        votes,
        totalWeight,
        percentage: totalPossibleWeight > 0 ? totalWeight / totalPossibleWeight : 0,
      }
    })
    
    return results.sort((a, b) => b.totalWeight - a.totalWeight)
  }
  
  /**
   * Determine consensus from voting results.
   */
  determineConsensus(sessionId: string): ConsensusResult {
    const session = this.sessions.get(sessionId)
    if (!session) {
      return {
        success: false,
        consensusLevel: 'deadlock',
        votingResults: [],
        summary: 'Session not found',
      }
    }
    
    const votingResults = this.vote(sessionId)
    session.status = 'decided'
    
    if (votingResults.length === 0) {
      session.consensusLevel = 'deadlock'
      return {
        success: false,
        consensusLevel: 'deadlock',
        votingResults: [],
        summary: 'No votes cast',
      }
    }
    
    const winner = votingResults[0]
    const winnerPercentage = winner.percentage
    
    // Determine consensus level
    let consensusLevel: DebateSession['consensusLevel'] = 'deadlock'
    if (winnerPercentage >= this.config.votingThreshold) {
      if (winnerPercentage >= 0.9) {
        consensusLevel = 'unanimous'
      } else if (winnerPercentage >= 0.75) {
        consensusLevel = 'strong'
      } else {
        consensusLevel = 'majority'
      }
    } else if (winnerPercentage >= 0.4) {
      consensusLevel = 'plurality'
    }
    
    session.consensusLevel = consensusLevel
    session.decision = winner.optionId
    session.updatedAt = Date.now()
    
    // Collect minority concerns
    const minorityConcerns = session.opinions.filter(opinion => {
      const isWinnerOption = opinion.alternative === winner.optionId ||
                            opinion.recommendation === 'reject'
      return isWinnerOption && opinion.concerns && opinion.concerns.length > 0
    })
    
    // Generate recommendations
    const recommendations = this.generateRecommendations(session, winner)
    
    const summary = this.generateSummary(session, consensusLevel, winner, minorityConcerns)
    
    return {
      success: consensusLevel !== 'deadlock',
      consensusLevel,
      winningOption: session.options.find(o => o.id === winner.optionId),
      votingResults,
      summary,
      minorityConcerns: minorityConcerns.length > 0 ? minorityConcerns : undefined,
      recommendations,
    }
  }
  
  // ============================================================================
  // Helper Methods
  // ============================================================================
  
  private getExpertInfo(expertId: string): { name: string; role: string } {
    // Simplified - would look up from expert registry
    const knownExperts: Record<string, { name: string; role: string }> = {
      'arch-001': { name: 'System Architect', role: 'architect' },
      'plan-001': { name: 'Project Planner', role: 'planner' },
      'fe-001': { name: 'Frontend Developer', role: 'frontend' },
      'be-001': { name: 'Backend Developer', role: 'backend' },
      'qa-001': { name: 'QA Engineer', role: 'qa' },
    }
    return knownExperts[expertId] || { name: expertId, role: 'expert' }
  }
  
  private calculateExpertiseWeight(opinion: ExpertOpinion, option: DecisionOption): number {
    // In production, would analyze option tags/domains vs expert expertise
    // Simplified: role-based weights
    const roleWeights: Record<string, Record<string, number>> = {
      architect: { technical: 1.0, design: 0.8, business: 0.5 },
      planner: { planning: 1.0, business: 0.9, technical: 0.6 },
      frontend: { ui: 1.0, ux: 0.9, technical: 0.7 },
      backend: { technical: 1.0, scalability: 0.9, business: 0.5 },
      qa: { quality: 1.0, testing: 1.0, technical: 0.6 },
    }
    
    const weights = roleWeights[opinion.expertRole] || { default: 0.7 }
    const maxWeight = Math.max(...Object.values(weights))
    return maxWeight || 0.7
  }
  
  private recordDebateExperience(session: DebateSession, opinion: ExpertOpinion): void {
    // Extract key insights from the opinion
    const insights: string[] = []
    
    if (opinion.reasoning) insights.push(opinion.reasoning)
    if (opinion.concerns) insights.push(...opinion.concerns)
    if (opinion.suggestions) insights.push(...opinion.suggestions)
    
    if (insights.length > 0) {
      experienceTracker.record({
        taskType: 'debate:' + session.topic.slice(0, 30),
        context: session.topic,
        actions: [opinion.recommendation],
        outcome: 'success', // Debates always succeed in generating insights
        outcomeDetails: opinion.reasoning,
        keyInsights: insights,
        expertId: opinion.expertId,
        applicableDomains: [opinion.expertRole, 'collaboration'],
      })
    }
  }
  
  private generateRecommendations(session: DebateSession, winner: VotingResult): string[] | undefined {
    const recommendations: string[] = []
    
    // Collect suggestions from winning option supporters
    session.opinions
      .filter(op => op.alternative === winner.optionId || op.recommendation === 'approve')
      .forEach(op => {
        if (op.suggestions) {
          recommendations.push(...op.suggestions)
        }
      })
    
    return recommendations.length > 0 ? [...new Set(recommendations)] : undefined
  }
  
  private generateSummary(
    session: DebateSession,
    consensusLevel: DebateSession['consensusLevel'],
    winner: VotingResult,
    minorityConcerns: ExpertOpinion[]
  ): string {
    const levelDescriptions = {
      unanimous: '所有专家达成一致',
      strong: '绝大多数专家支持',
      majority: '多数专家支持',
      plurality: '部分专家支持',
      deadlock: '专家意见分歧较大',
    }
    
    let summary = `${levelDescriptions[consensusLevel]}「${winner.optionLabel}」`
    
    if (minorityConcerns.length > 0) {
      summary += `。但有 ${minorityConcerns.length} 位专家持不同意见，建议关注其关切点。`
    }
    
    return summary
  }
  
  // ============================================================================
  // Auto-trigger Logic
  // ============================================================================
  
  /**
   * Check if a new message should trigger multi-expert collaboration.
   */
  shouldTrigger(context: {
    messageLength: number
    hasTechnicalTerms: boolean
    hasDecisionKeywords: boolean
    isComplexTask: boolean
  }): boolean {
    if (!this.config.enableAutoTrigger) return false
    
    // Trigger on complex tasks or decision requests
    const complexityScore = 
      (context.messageLength > 500 ? 0.3 : 0) +
      (context.hasTechnicalTerms ? 0.2 : 0) +
      (context.hasDecisionKeywords ? 0.3 : 0) +
      (context.isComplexTask ? 0.4 : 0)
    
    return complexityScore >= 0.5
  }
  
  /**
   * Analyze message to detect if it's a decision request.
   */
  analyzeMessage(message: string): {
    isDecisionRequest: boolean
    decisionType?: string
    urgency?: 'low' | 'normal' | 'high'
    complexity?: 'low' | 'medium' | 'high'
  } {
    const decisionKeywords = ['应该', '要不要', '选哪个', '建议', '方案', '如何决定', 'choose', 'should', 'recommend']
    const urgencyKeywords = ['紧急', '重要', '马上', '尽快', 'ASAP', 'urgent']
    const technicalKeywords = ['架构', '设计', '方案', '技术', 'architecture', 'design', 'technical']
    
    const hasDecision = decisionKeywords.some(k => message.includes(k))
    const hasUrgency = urgencyKeywords.some(k => message.includes(k))
    const hasTechnical = technicalKeywords.some(k => message.includes(k))
    
    if (!hasDecision) {
      return { isDecisionRequest: false }
    }
    
    let complexity: 'low' | 'medium' | 'high' = 'medium'
    if (message.length > 1000 || hasTechnical) complexity = 'high'
    if (message.length < 200) complexity = 'low'
    
    let urgency: 'low' | 'normal' | 'high' = 'normal'
    if (hasUrgency) urgency = 'high'
    
    const decisionTypes = ['选择', '方案', '设计', '技术选型', '优先级']
    const decisionType = decisionTypes.find(t => message.includes(t)) || 'general'
    
    return {
      isDecisionRequest: true,
      decisionType,
      urgency,
      complexity,
    }
  }
}

// ============================================================================
// Global Instance
// ============================================================================

export const debateManager = new DebateManager(knowledgeGraph)

export default DebateManager
