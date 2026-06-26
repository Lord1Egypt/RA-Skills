// ============================================================================
// EO Self-Manager - Phase 4.3: Self-Management
//
// Implements automatic memory/context cleanup, session archiving,
// and performance optimization.
// ============================================================================

// ============================================================================
// Types
// ============================================================================

import { logger } from '../utils/logger.js'

export interface MemoryStats {
  heapUsed: number        // MB
  heapTotal: number      // MB
  external: number        // MB
  rss: number           // MB
  arrayBuffers: number   // MB
}

export interface ContextStats {
  currentTokens: number
  maxTokens: number
  oldestMessageAge: number  // ms
  messageCount: number
  compressionRatio: number
}

export interface SessionArchive {
  id: string
  sessionId: string
  startedAt: number
  endedAt: number
  messageCount: number
  keyOutcomes: string[]
  expertContributions: string[]
  totalDuration: number
  compressedSize: number    // bytes
  archivedAt: number
}

export interface CleanupConfig {
  maxHeapMB: number
  maxContextTokens: number
  maxSessionAge: number       // ms
  maxSessionMessages: number
  archiveOldSessions: boolean
  archiveAfterDays: number
  compressionEnabled: boolean
  autoCleanupIntervalMs: number
}

export interface PerformanceProfile {
  avgResponseTime: number    // ms
  avgMemoryUsage: number     // MB
  activeSessions: number
  completedTasks: number
  errorRate: number
  efficiency: number         // 0-1
}

export interface OptimizationAction {
  type: 'gc' | 'compress' | 'archive' | 'flush' | 'restart_component'
  target?: string
  reason: string
  expectedImprovement: string
  executed: boolean
  timestamp: number
}

// ============================================================================
// Memory Manager
// ============================================================================

class MemoryManager {
  private config: CleanupConfig
  private lastGC: number = 0
  
  constructor(config: CleanupConfig) {
    this.config = config
  }
  
  /**
   * Get current memory statistics.
   */
  getStats(): MemoryStats {
    const mem = process.memoryUsage()
    return {
      heapUsed: Math.round(mem.heapUsed / 1024 / 1024),
      heapTotal: Math.round(mem.heapTotal / 1024 / 1024),
      external: Math.round(mem.external / 1024 / 1024),
      rss: Math.round(mem.rss / 1024 / 1024),
      arrayBuffers: Math.round((mem.arrayBuffers || 0) / 1024 / 1024),
    }
  }
  
  /**
   * Check if memory is within healthy limits.
   */
  isHealthy(): boolean {
    const stats = this.getStats()
    return stats.heapUsed < this.config.maxHeapMB * 0.8
  }
  
  /**
   * Get memory usage as percentage.
   */
  getUsagePercent(): number {
    const stats = this.getStats()
    return (stats.heapUsed / this.config.maxHeapMB) * 100
  }
  
  /**
   * Attempt garbage collection.
   */
  async tryGC(): Promise<{ success: boolean; freedMB: number; error?: string }> {
    const before = this.getStats().heapUsed
    
    try {
      if (global.gc) {
        global.gc()
        await new Promise(resolve => setTimeout(resolve, 100))
      }
      
      const after = this.getStats().heapUsed
      const freed = before - after
      this.lastGC = Date.now()
      
      return {
        success: true,
        freedMB: Math.round(freed),
      }
    } catch (e) {
      return {
        success: false,
        freedMB: 0,
        error: e instanceof Error ? e.message : String(e),
      }
    }
  }
  
  /**
   * Suggest cleanup actions based on memory state.
   */
  suggestCleanup(): OptimizationAction[] {
    const actions: OptimizationAction[] = []
    const stats = this.getStats()
    
    // Check heap usage
    const heapPercent = (stats.heapUsed / this.config.maxHeapMB) * 100
    
    if (heapPercent > 90) {
      actions.push({
        type: 'gc',
        reason: `Heap usage critical: ${heapPercent.toFixed(0)}%`,
        expectedImprovement: '~10-30% memory reduction',
        executed: false,
        timestamp: Date.now(),
      })
    } else if (heapPercent > 75) {
      actions.push({
        type: 'gc',
        reason: `Heap usage high: ${heapPercent.toFixed(0)}%`,
        expectedImprovement: '~5-15% memory reduction',
        executed: false,
        timestamp: Date.now(),
      })
    }
    
    // Check if GC was long ago
    if (this.lastGC > 0 && Date.now() - this.lastGC > 300000) { // 5 minutes
      actions.push({
        type: 'gc',
        reason: 'GC not run recently (5+ minutes)',
        expectedImprovement: 'Variable memory reduction',
        executed: false,
        timestamp: Date.now(),
      })
    }
    
    return actions
  }
}

// ============================================================================
// Context Manager
// ============================================================================

class ContextManager {
  private config: CleanupConfig
  private messageCount = 0
  private oldestMessage: number = Date.now()
  
  constructor(config: CleanupConfig) {
    this.config = config
  }
  
  /**
   * Record a new message.
   */
  recordMessage(): void {
    this.messageCount++
    this.oldestMessage = Date.now()
  }
  
  /**
   * Get context statistics.
   */
  getStats(): ContextStats {
    const oldestAge = Date.now() - this.oldestMessage
    
    return {
      currentTokens: this.estimateTokens(),
      maxTokens: this.config.maxContextTokens,
      oldestMessageAge: oldestAge,
      messageCount: this.messageCount,
      compressionRatio: this.messageCount > 100 ? 0.7 : 1.0,
    }
  }
  
  /**
   * Estimate current token count.
   * Simplified: ~4 chars per token average.
   */
  private estimateTokens(): number {
    // This would be replaced with actual token counting in production
    return Math.round(this.messageCount * 50) // ~50 tokens per message average
  }
  
  /**
   * Check if context needs compression.
   */
  needsCompression(): boolean {
    const stats = this.getStats()
    return (
      stats.currentTokens > this.config.maxContextTokens * 0.8 ||
      stats.oldestMessageAge > this.config.maxSessionAge
    )
  }
  
  /**
   * Reset message counter.
   */
  reset(): void {
    this.messageCount = 0
    this.oldestMessage = Date.now()
  }
  
  /**
   * Suggest context optimization actions.
   */
  suggestOptimization(): OptimizationAction[] {
    const actions: OptimizationAction[] = []
    const stats = this.getStats()
    
    if (stats.currentTokens > this.config.maxContextTokens) {
      actions.push({
        type: 'compress',
        reason: `Token count exceeded: ${stats.currentTokens} > ${this.config.maxContextTokens}`,
        expectedImprovement: 'Reduce to ~70% tokens',
        executed: false,
        timestamp: Date.now(),
      })
    }
    
    if (stats.oldestMessageAge > this.config.maxSessionAge) {
      actions.push({
        type: 'compress',
        reason: `Session too old: ${Math.round(stats.oldestMessageAge / 60000)} minutes`,
        expectedImprovement: 'Remove old messages, keep recent context',
        executed: false,
        timestamp: Date.now(),
      })
    }
    
    return actions
  }
}

// ============================================================================
// Session Archive Manager
// ============================================================================

class SessionArchiveManager {
  private config: CleanupConfig
  private archives: Map<string, SessionArchive> = new Map()
  private sessions: Map<string, {
    sessionId: string
    startedAt: number
    messages: number
    outcomes: string[]
    experts: string[]
  }> = new Map()
  
  constructor(config: CleanupConfig) {
    this.config = config
  }
  
  /**
   * Start tracking a session.
   */
  startSession(sessionId: string): void {
    this.sessions.set(sessionId, {
      sessionId,
      startedAt: Date.now(),
      messages: 0,
      outcomes: [],
      experts: [],
    })
  }
  
  /**
   * Record a message in a session.
   */
  recordMessage(sessionId: string): void {
    const session = this.sessions.get(sessionId)
    if (session) session.messages++
  }
  
  /**
   * Record an outcome.
   */
  recordOutcome(sessionId: string, outcome: string): void {
    const session = this.sessions.get(sessionId)
    if (session) session.outcomes.push(outcome)
  }
  
  /**
   * Record expert contribution.
   */
  recordExpertContribution(sessionId: string, expertId: string): void {
    const session = this.sessions.get(sessionId)
    if (session && !session.experts.includes(expertId)) {
      session.experts.push(expertId)
    }
  }
  
  /**
   * End and archive a session.
   */
  archiveSession(sessionId: string): SessionArchive | null {
    const session = this.sessions.get(sessionId)
    if (!session) return null
    
    const archive: SessionArchive = {
      id: 'archive-' + Date.now(),
      sessionId,
      startedAt: session.startedAt,
      endedAt: Date.now(),
      messageCount: session.messages,
      keyOutcomes: session.outcomes.slice(0, 10),
      expertContributions: session.experts,
      totalDuration: Date.now() - session.startedAt,
      compressedSize: this.estimateCompressedSize(session),
      archivedAt: Date.now(),
    }
    
    this.archives.set(sessionId, archive)
    this.sessions.delete(sessionId)
    
    return archive
  }
  
  /**
   * Estimate compressed size of session data.
   */
  private estimateCompressedSize(session: typeof this.sessions extends Map<string, infer V> ? V : never): number {
    // Rough estimate: 100 bytes per message average
    return session.messages * 100
  }
  
  /**
   * Get all archives.
   */
  getArchives(): SessionArchive[] {
    return Array.from(this.archives.values())
  }
  
  /**
   * Get archive for a session.
   */
  getArchive(sessionId: string): SessionArchive | undefined {
    return this.archives.get(sessionId)
  }
  
  /**
   * Delete old archives.
   */
  cleanupOldArchives(beforeDate: number): number {
    let deleted = 0
    
    for (const [id, archive] of this.archives.entries()) {
      if (archive.archivedAt < beforeDate) {
        this.archives.delete(id)
        deleted++
      }
    }
    
    return deleted
  }
  
  /**
   * Get archives that should be archived based on config.
   */
  getSessionsNeedingArchive(): string[] {
    const cutoff = Date.now() - this.config.archiveAfterDays * 24 * 60 * 60 * 1000
    const needingArchive: string[] = []
    
    for (const session of this.sessions.values()) {
      if (session.startedAt < cutoff) {
        needingArchive.push(session.sessionId)
      }
    }
    
    return needingArchive
  }
}

// ============================================================================
// Performance Optimizer
// ============================================================================

class PerformanceOptimizer {
  private history: PerformanceProfile[] = []
  private maxHistory = 100
  
  constructor() {}
  
  /**
   * Record a performance profile snapshot.
   */
  recordProfile(profile: PerformanceProfile): void {
    this.history.push(profile)
    if (this.history.length > this.maxHistory) {
      this.history.shift()
    }
  }
  
  /**
   * Get recent performance trend.
   */
  getTrend(): { direction: 'improving' | 'degrading' | 'stable'; changePercent: number } {
    if (this.history.length < 5) {
      return { direction: 'stable', changePercent: 0 }
    }
    
    const recent = this.history.slice(-5)
    const older = this.history.slice(-10, -5)
    
    const recentAvg = recent.reduce((sum, p) => sum + p.efficiency, 0) / recent.length
    const olderAvg = older.length > 0 
      ? older.reduce((sum, p) => sum + p.efficiency, 0) / older.length 
      : recentAvg
    
    const changePercent = ((recentAvg - olderAvg) / olderAvg) * 100
    
    let direction: 'improving' | 'degrading' | 'stable'
    if (changePercent > 5) direction = 'improving'
    else if (changePercent < -5) direction = 'degrading'
    else direction = 'stable'
    
    return { direction, changePercent }
  }
  
  /**
   * Get current performance score.
   */
  getCurrentScore(): number {
    if (this.history.length === 0) return 0.5
    return this.history[this.history.length - 1].efficiency
  }
  
  /**
   * Suggest performance optimizations.
   */
  suggestOptimizations(memoryStats: MemoryStats, contextStats: ContextStats): OptimizationAction[] {
    const actions: OptimizationAction[] = []
    const trend = this.getTrend()
    
    // Memory-based suggestions
    if (memoryStats.heapUsed / memoryStats.heapTotal > 0.9) {
      actions.push({
        type: 'gc',
        reason: 'Heap utilization critical (>90%)',
        expectedImprovement: 'Reduce heap pressure',
        executed: false,
        timestamp: Date.now(),
      })
    }
    
    // Context-based suggestions
    if (contextStats.currentTokens > contextStats.maxTokens * 0.9) {
      actions.push({
        type: 'compress',
        reason: 'Token usage critical',
        expectedImprovement: 'Prevent context overflow',
        executed: false,
        timestamp: Date.now(),
      })
    }
    
    // Trend-based suggestions
    if (trend.direction === 'degrading') {
      actions.push({
        type: 'restart_component',
        target: 'session_manager',
        reason: `Performance degrading (${trend.changePercent.toFixed(1)}%)`,
        expectedImprovement: 'Restore performance to baseline',
        executed: false,
        timestamp: Date.now(),
      })
    }
    
    return actions
  }
}

// ============================================================================
// Self-Manager (Main Class)
// ============================================================================

export class SelfManager {
  private config: CleanupConfig
  private memory: MemoryManager
  private context: ContextManager
  private archives: SessionArchiveManager
  private optimizer: PerformanceOptimizer
  private cleanupInterval?: NodeJS.Timeout
  private isRunning = false
  
  constructor(config?: Partial<CleanupConfig>) {
    this.config = {
      maxHeapMB: 512,
      maxContextTokens: 100000,
      maxSessionAge: 30 * 60 * 1000,    // 30 minutes
      maxSessionMessages: 500,
      archiveOldSessions: true,
      archiveAfterDays: 7,
      compressionEnabled: true,
      autoCleanupIntervalMs: 60000,      // 1 minute
      ...config,
    }
    
    this.memory = new MemoryManager(this.config)
    this.context = new ContextManager(this.config)
    this.archives = new SessionArchiveManager(this.config)
    this.optimizer = new PerformanceOptimizer()
  }
  
  // ============================================================================
  // Lifecycle
  // ============================================================================
  
  /**
   * Start self-management.
   */
  start(): void {
    if (this.isRunning) return
    this.isRunning = true
    
    // Start cleanup interval
    this.cleanupInterval = setInterval(() => {
      this.runCleanupCycle()
    }, this.config.autoCleanupIntervalMs)
    
    logger.info('SelfManager started')
  }
  
  /**
   * Stop self-management.
   */
  stop(): void {
    this.isRunning = false
    if (this.cleanupInterval) {
      clearInterval(this.cleanupInterval)
      this.cleanupInterval = undefined
    }
    logger.info('SelfManager stopped')
  }
  
  /**
   * Run a single cleanup cycle.
   */
  async runCleanupCycle(): Promise<OptimizationAction[]> {
    const actions: OptimizationAction[] = []
    
    // 1. Check memory and GC if needed
    const memoryActions = this.memory.suggestCleanup()
    for (const action of memoryActions) {
      if (action.type === 'gc' && !action.executed) {
        const result = await this.memory.tryGC()
        if (result.success) {
          action.executed = true
          logger.info(`GC freed ${result.freedMB}MB`)
        }
      }
      actions.push(action)
    }
    
    // 2. Check context and compress if needed
    const contextActions = this.context.suggestOptimization()
    for (const action of contextActions) {
      if (action.type === 'compress' && !action.executed) {
        // Would trigger context compression
        action.executed = true
        this.context.reset()
        logger.debug('Context compressed')
      }
      actions.push(action)
    }
    
    // 3. Check for sessions that need archiving
    if (this.config.archiveOldSessions) {
      const sessionsToArchive = this.archives.getSessionsNeedingArchive()
      for (const sessionId of sessionsToArchive) {
        const archive = this.archives.archiveSession(sessionId)
        if (archive) {
          logger.info(`Archived session ${sessionId}: ${archive.messageCount} messages`)
          actions.push({
            type: 'archive',
            target: sessionId,
            reason: `Session older than ${this.config.archiveAfterDays} days`,
            expectedImprovement: 'Reduced memory footprint',
            executed: true,
            timestamp: Date.now(),
          })
        }
      }
    }
    
    // 4. Record performance profile
    const profile = this.buildProfile()
    this.optimizer.recordProfile(profile)
    
    // 5. Check for performance-based optimizations
    const perfActions = this.optimizer.suggestOptimizations(
      this.memory.getStats(),
      this.context.getStats()
    )
    actions.push(...perfActions)
    
    return actions.filter(a => !a.executed)
  }
  
  /**
   * Build current performance profile.
   */
  private buildProfile(): PerformanceProfile {
    const memStats = this.memory.getStats()
    const contextStats = this.context.getStats()
    
    return {
      avgResponseTime: 0,     // Would be tracked from actual metrics
      avgMemoryUsage: memStats.heapUsed,
      activeSessions: 0,      // Would be tracked from session manager
      completedTasks: 0,      // Would be tracked from task manager
      errorRate: 0,          // Would be tracked from error logger
      efficiency: Math.max(0, 1 - (memStats.heapUsed / this.config.maxHeapMB)),
    }
  }
  
  // ============================================================================
  // Session Management
  // ============================================================================
  
  /**
   * Start tracking a new session.
   */
  startSession(sessionId: string): void {
    this.archives.startSession(sessionId)
  }
  
  /**
   * Record a message.
   */
  recordMessage(sessionId: string): void {
    this.context.recordMessage()
    this.archives.recordMessage(sessionId)
  }
  
  /**
   * Record an outcome.
   */
  recordOutcome(sessionId: string, outcome: string): void {
    this.archives.recordOutcome(sessionId, outcome)
  }
  
  /**
   * Record expert contribution.
   */
  recordExpertContribution(sessionId: string, expertId: string): void {
    this.archives.recordExpertContribution(sessionId, expertId)
  }
  
  /**
   * End a session.
   */
  endSession(sessionId: string): SessionArchive | undefined {
    return this.archives.archiveSession(sessionId)
  }
  
  // ============================================================================
  // Manual Optimization
  // ============================================================================
  
  /**
   * Force garbage collection.
   */
  async forceGC(): Promise<{ success: boolean; freedMB: number }> {
    return this.memory.tryGC()
  }
  
  /**
   * Force context compression.
   */
  forceCompression(): void {
    this.context.reset()
    logger.warn('Context force-compressed')
  }
  
  /**
   * Archive all old sessions.
   */
  archiveAllOldSessions(): number {
    const sessions = this.archives.getSessionsNeedingArchive()
    for (const sessionId of sessions) {
      this.archives.archiveSession(sessionId)
    }
    return sessions.length
  }
  
  // ============================================================================
  // Status
  // ============================================================================
  
  /**
   * Get comprehensive status.
   */
  getStatus(): {
    memory: MemoryStats
    context: ContextStats
    archives: { total: number; oldestAge: number }
    performance: { score: number; trend: string }
    pendingActions: number
  } {
    const memStats = this.memory.getStats()
    const contextStats = this.context.getStats()
    const trend = this.optimizer.getTrend()
    const archives = this.archives.getArchives()
    
    return {
      memory: memStats,
      context: contextStats,
      archives: {
        total: archives.length,
        oldestAge: archives.length > 0 
          ? Date.now() - archives[0].endedAt 
          : 0,
      },
      performance: {
        score: this.optimizer.getCurrentScore(),
        trend: trend.direction,
      },
      pendingActions: this.getPendingActions().length,
    }
  }
  
  /**
   * Get pending optimization actions.
   */
  getPendingActions(): OptimizationAction[] {
    const actions: OptimizationAction[] = []
    actions.push(...this.memory.suggestCleanup())
    actions.push(...this.context.suggestOptimization())
    return actions.filter(a => !a.executed)
  }
}

// ============================================================================
// Global Instance
// ============================================================================

export const selfManager = new SelfManager()

export default SelfManager
