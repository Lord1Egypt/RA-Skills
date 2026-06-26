// ============================================================================
// EO Agent Coordinator v1.0 - Phase 3: Multi-Agent Collaboration
//
// Coordinates multiple expert agents for collaborative decision-making.
// Handles task distribution, load balancing, conflict resolution, and consensus.
// ============================================================================

import { ExpertResult } from '../skills/multi-expert-orchestrator.js'

// ============================================================================
// Types
// ============================================================================

export interface AgentInfo {
  id: string
  name: string
  role: string
  expertise: string[]
  currentLoad: number  // 0-1, percentage of capacity
  isAvailable: boolean
  lastActive: number   // timestamp
}

export interface CoordinationTask {
  id: string
  type: 'planning' | 'analysis' | 'decision' | 'review' | 'custom'
  priority: 'low' | 'normal' | 'high' | 'critical'
  description: string
  requiredExpertRoles: string[]
  minExperts: number   // minimum experts needed for consensus
  deadline?: number     // timestamp
  payload: any         // task-specific data
}

export interface CoordinatedResult {
  taskId: string
  success: boolean
  consensus: 'unanimous' | 'majority' | 'plurality' | 'none'
  votes?: VoteResult[]
  aggregatedOutput?: string
  conflicts?: ConflictReport[]
  expertContributions: Map<string, ExpertContribution>
  durationMs: number
  timestamp: number
}

export interface VoteResult {
  expertId: string
  expertName: string
  vote: 'approve' | 'reject' | 'abstain'
  confidence: number  // 0-1
  reasoning?: string
}

export interface ConflictReport {
  conflictId: string
  experts: string[]
  disagreement: string
  severity: 'minor' | 'major' | 'critical'
  resolution?: string
}

export interface ExpertContribution {
  expertId: string
  expertName: string
  role: string
  output: string
  keyPoints: string[]
  confidence: number
  timestamp: number
}

export interface CoordinatorConfig {
  enableLoadBalancing: boolean
  enableConflictResolution: boolean
  consensusThreshold: number      // 0-1, required agreement ratio
  maxRetries: number
  taskTimeoutMs: number
  enableVoting: boolean
}

// ============================================================================
// Task Priority Queue
// ============================================================================

class TaskQueue {
  private tasks: CoordinationTask[] = []
  
  add(task: CoordinationTask): void {
    this.tasks.push(task)
    this.tasks.sort((a, b) => this.priorityValue(b) - this.priorityValue(a))
  }
  
  peek(): CoordinationTask | undefined {
    return this.tasks[0]
  }
  
  take(): CoordinationTask | undefined {
    return this.tasks.shift()
  }
  
  remove(taskId: string): boolean {
    const idx = this.tasks.findIndex(t => t.id === taskId)
    if (idx >= 0) {
      this.tasks.splice(idx, 1)
      return true
    }
    return false
  }
  
  isEmpty(): boolean {
    return this.tasks.length === 0
  }
  
  size(): number {
    return this.tasks.length
  }
  
  private priorityValue(task: CoordinationTask): number {
    const priorityMap = { critical: 4, high: 3, normal: 2, low: 1 }
    return priorityMap[task.priority] + (task.deadline ? (task.deadline - Date.now()) / 1000000 : 0)
  }
}

// ============================================================================
// Load Balancer
// ============================================================================

class LoadBalancer {
  private agents: Map<string, AgentInfo> = new Map()
  private config: CoordinatorConfig
  
  constructor(config: CoordinatorConfig) {
    this.config = config
  }
  
  registerAgent(agent: AgentInfo): void {
    this.agents.set(agent.id, agent)
  }
  
  unregisterAgent(agentId: string): void {
    this.agents.delete(agentId)
  }
  
  updateLoad(agentId: string, load: number): void {
    const agent = this.agents.get(agentId)
    if (agent) {
      agent.currentLoad = Math.max(0, Math.min(1, load))
      if (load < 1) agent.isAvailable = true
    }
  }
  
  /**
   * Select the best available agent for a task based on expertise and load.
   */
  selectAgent(requiredRoles: string[]): AgentInfo | undefined {
    if (!this.config.enableLoadBalancing) {
      // Just return any available agent
      return Array.from(this.agents.values()).find(a => a.isAvailable)
    }
    
    // Filter agents with matching expertise
    const candidates = Array.from(this.agents.values())
      .filter(agent => {
        if (!agent.isAvailable || agent.currentLoad >= 0.9) return false
        return requiredRoles.some(role => 
          agent.role.includes(role) || 
          agent.expertise.some(e => e.includes(role))
        )
      })
      .sort((a, b) => {
        // Prefer lower load, then more recent activity
        const loadDiff = a.currentLoad - b.currentLoad
        if (Math.abs(loadDiff) > 0.1) return loadDiff
        return b.lastActive - a.lastActive
      })
    
    return candidates[0]
  }
  
  /**
   * Select multiple agents for a task that requires consensus.
   */
  selectAgents(requiredRoles: string[], count: number): AgentInfo[] {
    const selected: AgentInfo[] = []
    const workingSet = new Map(this.agents)
    
    for (let i = 0; i < count && workingSet.size > 0; i++) {
      const agent = this.selectAgentFromSet(Array.from(workingSet.values()), requiredRoles)
      if (agent) {
        selected.push(agent)
        workingSet.delete(agent.id)
      }
    }
    
    return selected
  }
  
  private selectAgentFromSet(agents: AgentInfo[], requiredRoles: string[]): AgentInfo | undefined {
    return agents
      .filter(a => a.isAvailable && a.currentLoad < 0.9)
      .filter(a => requiredRoles.some(r => a.role.includes(r) || a.expertise.some(e => e.includes(r))))
      .sort((a, b) => a.currentLoad - b.currentLoad)[0]
  }
  
  getAllAgents(): AgentInfo[] {
    return Array.from(this.agents.values())
  }
}

// ============================================================================
// Conflict Resolver
// ============================================================================

class ConflictResolver {
  private config: CoordinatorConfig
  
  constructor(config: CoordinatorConfig) {
    this.config = config
  }
  
  /**
   * Detect conflicts between expert outputs.
   */
  detectConflicts(contributions: Map<string, ExpertContribution>): ConflictReport[] {
    const reports: ConflictReport[] = []
    const entries = Array.from(contributions.entries())
    
    for (let i = 0; i < entries.length; i++) {
      for (let j = i + 1; j < entries.length; j++) {
        const [id1, c1] = entries[i]
        const [id2, c2] = entries[j]
        
        // Simple conflict detection based on key points
        const conflict = this.findDisagreement(c1, c2)
        if (conflict) {
          reports.push({
            conflictId: `conflict-${id1}-${id2}`,
            experts: [id1, id2],
            disagreement: conflict,
            severity: this.assessSeverity(c1, c2),
          })
        }
      }
    }
    
    return reports
  }
  
  private findDisagreement(c1: ExpertContribution, c2: ExpertContribution): string | null {
    // Extract first key point from each
    const p1 = c1.keyPoints[0] || ''
    const p2 = c2.keyPoints[0] || ''
    
    // Simple check: if key points are different, potential disagreement
    if (p1 && p2 && p1 !== p2) {
      return `Expert "${c1.expertName}" suggests "${p1.slice(0, 50)}..." while Expert "${c2.expertName}" suggests "${p2.slice(0, 50)}..."`
    }
    
    // Check confidence difference
    if (Math.abs(c1.confidence - c2.confidence) > 0.4) {
      return `Significant confidence difference: ${c1.expertName} (${(c1.confidence * 100).toFixed(0)}%) vs ${c2.expertName} (${(c2.confidence * 100).toFixed(0)}%)`
    }
    
    return null
  }
  
  private assessSeverity(c1: ExpertContribution, c2: ExpertContribution): 'minor' | 'major' | 'critical' {
    const confidenceDiff = Math.abs(c1.confidence - c2.confidence)
    const contentDiff = c1.keyPoints.length !== c2.keyPoints.length ? 'major' : 'minor'
    
    if (confidenceDiff > 0.6 || contentDiff === 'major') return 'critical'
    if (confidenceDiff > 0.3) return 'major'
    return 'minor'
  }
  
  /**
   * Resolve conflicts through voting.
   */
  resolveThroughVoting(votes: VoteResult[]): { consensus: 'unanimous' | 'majority' | 'plurality' | 'none', decision?: string } {
    const approveVotes = votes.filter(v => v.vote === 'approve').length
    const rejectVotes = votes.filter(v => v.vote === 'reject').length
    const total = votes.length
    
    const ratio = Math.max(approveVotes, rejectVotes) / total
    
    if (ratio >= this.config.consensusThreshold) {
      const decision = approveVotes > rejectVotes ? 'approve' : 'reject'
      return {
        consensus: ratio === 1 ? 'unanimous' : 'majority',
        decision,
      }
    }
    
    return { consensus: 'plurality' }
  }
}

// ============================================================================
// Agent Coordinator (Main Class)
// ============================================================================

export class AgentCoordinator {
  private config: CoordinatorConfig
  private taskQueue: TaskQueue
  private loadBalancer: LoadBalancer
  private conflictResolver: ConflictResolver
  private agents: Map<string, AgentInfo> = new Map()
  
  constructor(config: Partial<CoordinatorConfig> = {}) {
    this.config = {
      enableLoadBalancing: true,
      enableConflictResolution: true,
      consensusThreshold: 0.6,
      maxRetries: 2,
      taskTimeoutMs: 120000,
      enableVoting: true,
      ...config,
    }
    
    this.taskQueue = new TaskQueue()
    this.loadBalancer = new LoadBalancer(this.config)
    this.conflictResolver = new ConflictResolver(this.config)
  }
  
  // ============================================================================
  // Agent Management
  // ============================================================================
  
  registerAgent(agent: Omit<AgentInfo, 'currentLoad' | 'isAvailable' | 'lastActive'>): void {
    const fullAgent: AgentInfo = {
      ...agent,
      currentLoad: 0,
      isAvailable: true,
      lastActive: Date.now(),
    }
    this.agents.set(agent.id, fullAgent)
    this.loadBalancer.registerAgent(fullAgent)
  }
  
  unregisterAgent(agentId: string): void {
    this.agents.delete(agentId)
    this.loadBalancer.unregisterAgent(agentId)
  }
  
  getAgent(agentId: string): AgentInfo | undefined {
    return this.agents.get(agentId)
  }
  
  getAllAgents(): AgentInfo[] {
    return Array.from(this.agents.values())
  }
  
  // ============================================================================
  // Task Management
  // ============================================================================
  
  submitTask(task: CoordinationTask): void {
    this.taskQueue.add(task)
  }
  
  getNextTask(): CoordinationTask | undefined {
    return this.taskQueue.take()
  }
  
  cancelTask(taskId: string): boolean {
    return this.taskQueue.remove(taskId)
  }
  
  getQueueSize(): number {
    return this.taskQueue.size()
  }
  
  // ============================================================================
  // Coordination Logic
  // ============================================================================
  
  /**
   * Coordinate a multi-expert task with consensus building.
   * This is the main entry point for Phase 3 collaboration.
   */
  async coordinate(
    task: CoordinationTask,
    expertOutputs: Map<string, ExpertContribution>
  ): Promise<CoordinatedResult> {
    const startTime = Date.now()
    
    // Detect conflicts
    let conflicts: ConflictReport[] = []
    if (this.config.enableConflictResolution) {
      conflicts = this.conflictResolver.detectConflicts(expertOutputs)
    }
    
    // Build consensus
    let consensus: 'unanimous' | 'majority' | 'plurality' | 'none' = 'none'
    let votes: VoteResult[] = []
    
    if (this.config.enableVoting && conflicts.length > 0) {
      // Auto-generate votes based on contributions
      votes = this.generateVotes(expertOutputs)
      const voteResult = this.conflictResolver.resolveThroughVoting(votes)
      consensus = voteResult.consensus
    } else if (expertOutputs.size >= task.minExperts) {
      // No conflicts but enough experts - unanimous
      consensus = 'unanimous'
    }
    
    // Aggregate output
    const aggregatedOutput = this.aggregateOutputs(expertOutputs)
    
    // Resolve conflict descriptions
    if (conflicts.length > 0) {
      conflicts = conflicts.map(c => ({
        ...c,
        resolution: this.resolveConflictDescription(c),
      }))
    }
    
    return {
      taskId: task.id,
      success: consensus !== 'none',
      consensus,
      votes,
      aggregatedOutput,
      conflicts,
      expertContributions: expertOutputs,
      durationMs: Date.now() - startTime,
      timestamp: Date.now(),
    }
  }
  
  /**
   * Auto-generate votes from expert contributions.
   */
  private generateVotes(contributions: Map<string, ExpertContribution>): VoteResult[] {
    return Array.from(contributions.entries()).map(([id, c]) => ({
      expertId: id,
      expertName: c.expertName,
      vote: c.confidence >= 0.6 ? 'approve' : c.confidence >= 0.3 ? 'abstain' : 'reject',
      confidence: c.confidence,
      reasoning: c.keyPoints[0],
    }))
  }
  
  /**
   * Aggregate multiple expert outputs into a coherent result.
   */
  private aggregateOutputs(contributions: Map<string, ExpertContribution>): string {
    const entries = Array.from(contributions.entries())
    
    // Simple aggregation: concatenate key points
    const allKeyPoints: { expert: string; point: string; confidence: number }[] = []
    
    entries.forEach(([id, c]) => {
      c.keyPoints.forEach(point => {
        allKeyPoints.push({
          expert: c.expertName,
          point,
          confidence: c.confidence,
        })
      })
    })
    
    // Sort by confidence and deduplicate
    const unique = allKeyPoints
      .sort((a, b) => b.confidence - a.confidence)
      .filter((p, idx, arr) => 
        arr.findIndex(x => x.point === p.point) === idx
      )
      .slice(0, 10) // Top 10 points
    
    if (unique.length === 0) return 'No consensus reached.'
    
    return unique.map(p => `[${(p.confidence * 100).toFixed(0)}%] ${p.point}`).join('\n')
  }
  
  private resolveConflictDescription(conflict: ConflictReport): string {
    if (conflict.severity === 'minor') {
      return 'Minor disagreement noted but acceptable.'
    } else if (conflict.severity === 'major') {
      return 'Significant conflict detected. Recommend further analysis.'
    } else {
      return 'Critical conflict requires human review.'
    }
  }
  
  // ============================================================================
  // Load Management
  // ============================================================================
  
  assignTaskToAgent(taskId: string, agentId: string): boolean {
    const agent = this.agents.get(agentId)
    if (agent && agent.isAvailable) {
      agent.currentLoad = Math.min(1, agent.currentLoad + 0.2)
      agent.lastActive = Date.now()
      return true
    }
    return false
  }
  
  releaseAgent(agentId: string): void {
    const agent = this.agents.get(agentId)
    if (agent) {
      agent.currentLoad = Math.max(0, agent.currentLoad - 0.2)
      if (agent.currentLoad < 0.3) agent.isAvailable = true
    }
  }
  
  // ============================================================================
  // Status
  // ============================================================================
  
  getStatus(): {
    queueSize: number
    agentCount: number
    availableAgents: number
    averageLoad: number
  } {
    const agents = this.getAllAgents()
    const avgLoad = agents.length > 0 
      ? agents.reduce((sum, a) => sum + a.currentLoad, 0) / agents.length 
      : 0
    
    return {
      queueSize: this.taskQueue.size(),
      agentCount: agents.length,
      availableAgents: agents.filter(a => a.isAvailable).length,
      averageLoad: avgLoad,
    }
  }
}

// ============================================================================
// Convenience Factory
// ============================================================================

export function createCoordinator(config?: Partial<CoordinatorConfig>): AgentCoordinator {
  return new AgentCoordinator(config)
}

// ============================================================================
// Built-in Expert Templates for Phase 3
// ============================================================================

export const PHASE3_EXPERTS = {
  coordinator: {
    id: 'coordinator-001',
    name: 'Task Coordinator',
    role: 'coordinator',
    expertise: ['task management', 'resource allocation', 'conflict resolution'],
  },
  synthesizer: {
    id: 'synthesizer-001',
    name: 'Result Synthesizer',
    role: 'synthesizer',
    expertise: ['aggregation', 'consensus building', 'summarization'],
  },
  monitor: {
    id: 'monitor-001',
    name: 'Quality Monitor',
    role: 'monitor',
    expertise: ['quality assurance', 'conflict detection', 'standards compliance'],
  },
}

export default AgentCoordinator
