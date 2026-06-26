/**
 * Memory Auto-Trigger System
 * 
 * Provides deterministic (LLM-independent) memory triggers based on rules.
 * These triggers fire automatically without requiring LLM judgment.
 * 
 * Triggers are categorized as:
 * - Event-based: session_start, session_end, task_complete, error, etc.
 * - Keyword-based: user explicitly says "记住", "record", etc.
 * - Threshold-based: context usage > 70%, repeated failures, etc.
 */

import type { OpenClawPluginApi } from 'openclaw/plugin-sdk'
import * as fs from 'fs'
import * as path from 'path'
import { PLUGIN_VERSION } from '../config.js'

// ============================================================================
// Types
// ============================================================================

export interface AutoTriggerConfig {
  enabled: boolean
  // Event-based triggers
  triggers: TriggerRule[]
  // Keyword patterns that indicate explicit memory requests
  explicitKeywords: string[]
  // Threshold triggers
  thresholds: ThresholdRule[]
}

export interface TriggerRule {
  id: string
  name: string
  event: TriggerEvent
  action: TriggerAction
  enabled: boolean
  priority: 'high' | 'low'
  metadata?: Record<string, unknown>
}

export type TriggerEvent = 
  | 'session_start'
  | 'session_end'
  | 'task_complete'
  | 'task_failed'
  | 'error'
  | 'gateway_restart'
  | 'explicit_keyword'
  | 'context_threshold'
  | 'pattern_detected'

export interface TriggerAction {
  type: 'archive_session' | 'record_decision' | 'record_lesson' | 'sync_memory' | 'notify' | 'custom'
  params?: Record<string, unknown>
}

export interface ThresholdRule {
  id: string
  name: string
  metric: ThresholdMetric
  operator: 'gt' | 'lt' | 'eq'
  value: number
  action: TriggerAction
  enabled: boolean
}

export type ThresholdMetric = 
  | 'context_usage_percent'
  | 'error_rate'
  | 'response_time_ms'
  | 'task_queue_depth'
  | 'session_count'

// Default auto-trigger rules
const DEFAULT_AUTO_TRIGGERS: TriggerRule[] = [
  {
    id: 'session_end_archive',
    name: 'Session End Archive',
    event: 'session_end',
    action: { type: 'archive_session' },
    enabled: true,
    priority: 'high'
  },
  {
    id: 'task_complete_record',
    name: 'Task Complete Record',
    event: 'task_complete',
    action: { type: 'record_decision', params: { source: 'task_complete' } },
    enabled: true,
    priority: 'high'
  },
  {
    id: 'task_failed_lesson',
    name: 'Task Failed Lesson',
    event: 'task_failed',
    action: { type: 'record_lesson', params: { category: 'task_failure' } },
    enabled: true,
    priority: 'high'
  },
  {
    id: 'gateway_restart_notify',
    name: 'Gateway Restart Notify',
    event: 'gateway_restart',
    action: { type: 'notify', params: { message: 'Gateway restarted' } },
    enabled: true,
    priority: 'low'
  }
]

const DEFAULT_EXPLICIT_KEYWORDS = [
  '记住', 'record', 'note', '别忘', '记得', '收藏',
  '重要', '关键', '保留', '保存'
]

const DEFAULT_THRESHOLDS: ThresholdRule[] = [
  {
    id: 'context_high_usage',
    name: 'High Context Usage',
    metric: 'context_usage_percent',
    operator: 'gt',
    value: 70,
    action: { type: 'notify', params: { message: 'Context usage > 70%' } },
    enabled: true
  }
]

const DEFAULT_CONFIG: AutoTriggerConfig = {
  enabled: true,
  triggers: DEFAULT_AUTO_TRIGGERS,
  explicitKeywords: DEFAULT_EXPLICIT_KEYWORDS,
  thresholds: DEFAULT_THRESHOLDS
}

// ============================================================================
// Auto Trigger Manager
// ============================================================================

export class MemoryAutoTrigger {
  private config: AutoTriggerConfig
  private api: OpenClawPluginApi
  private workspaceRoot: string
  private memoryPath: string

  constructor(api: OpenClawPluginApi, workspaceRoot: string, config?: Partial<AutoTriggerConfig>) {
    this.api = api
    this.workspaceRoot = workspaceRoot
    this.memoryPath = path.join(workspaceRoot, '.eo-sessions', 'auto-triggers.json')
    this.config = { ...DEFAULT_CONFIG, ...config }
  }

  /**
   * Check if message contains explicit memory keywords
   */
  hasExplicitKeyword(message: string): boolean {
    const lower = message.toLowerCase()
    return this.config.explicitKeywords.some(kw => lower.includes(kw.toLowerCase()))
  }

  /**
   * Extract explicit memory content from message
   */
  extractExplicitContent(message: string): string | null {
    if (!this.hasExplicitKeyword(message)) return null
    
    // Simple extraction - take the sentence containing the keyword
    const sentences = message.split(/[.!?。]/)
    for (const sentence of sentences) {
      if (this.hasExplicitKeyword(sentence)) {
        return sentence.trim()
      }
    }
    return message.trim()
  }

  /**
   * Check if event matches any trigger conditions
   */
  matchTrigger(event: TriggerEvent, metadata?: Record<string, unknown>): TriggerRule | null {
    const enabledTriggers = this.config.triggers.filter(t => t.enabled && t.event === event)
    
    if (enabledTriggers.length === 0) return null
    
    // Return highest priority match
    return enabledTriggers.sort((a, b) => 
      a.priority === 'high' && b.priority === 'low' ? -1 : 1
    )[0]
  }

  /**
   * Check threshold conditions
   */
  checkThresholds(metrics: Record<ThresholdMetric, number>): ThresholdRule[] {
    const matched: ThresholdRule[] = []
    
    for (const threshold of this.config.thresholds) {
      if (!threshold.enabled) continue
      
      const currentValue = metrics[threshold.metric]
      if (currentValue === undefined) continue
      
      let triggered = false
      switch (threshold.operator) {
        case 'gt': triggered = currentValue > threshold.value; break
        case 'lt': triggered = currentValue < threshold.value; break
        case 'eq': triggered = currentValue === threshold.value; break
      }
      
      if (triggered) {
        matched.push(threshold)
      }
    }
    
    return matched
  }

  /**
   * Execute trigger action
   */
  async executeAction(action: TriggerAction, context: Record<string, unknown>): Promise<void> {
    try {
      switch (action.type) {
        case 'archive_session':
          await this.archiveCurrentSession()
          break
        
        case 'record_decision':
          await this.recordDecision(action.params || {}, context)
          break
        
        case 'record_lesson':
          await this.recordLesson(action.params || {}, context)
          break
        
        case 'sync_memory':
          await this.syncToMemory()
          break
        
        case 'notify':
          this.api.logger.info(`[EO AutoTrigger] Notification: ${action.params?.message}`)
          break
        
        case 'custom':
          this.api.logger.debug(`[EO AutoTrigger] Custom action: ${JSON.stringify(action.params)}`)
          break
      }
    } catch (err) {
      this.api.logger.error(`[EO AutoTrigger] Action failed: ${err}`)
    }
  }

  /**
   * Archive current session (called on session_end)
   */
  private async archiveCurrentSession(): Promise<void> {
    const archiveDir = path.join(this.workspaceRoot, '.eo-sessions')
    const archiveFile = path.join(archiveDir, 'last-session-archive.json')
    
    // Create minimal archive
    const archive = {
      archivedAt: Date.now(),
      version: PLUGIN_VERSION,
      note: 'Archived by auto-trigger on session_end'
    }
    
    try {
      if (!fs.existsSync(archiveDir)) {
        fs.mkdirSync(archiveDir, { recursive: true })
      }
      fs.writeFileSync(archiveFile, JSON.stringify(archive, null, 2))
      this.api.logger.debug(`[EO AutoTrigger] Session archived`)
    } catch (err) {
      this.api.logger.error(`[EO AutoTrigger] Archive failed: ${err}`)
    }
  }

  /**
   * Record a decision to MEMORY.md
   */
  private async recordDecision(params: Record<string, unknown>, context: Record<string, unknown>): Promise<void> {
    const memoryFile = path.join(this.workspaceRoot, 'MEMORY.md')
    
    if (!fs.existsSync(memoryFile)) return
    
    try {
      const content = fs.readFileSync(memoryFile, 'utf-8')
      const timestamp = new Date().toISOString().replace('T', ' ').slice(0, 19)
      
      const decisionSection = `

---

## 📋 决策记录 (${timestamp})

**来源**: ${params.source || 'auto-trigger'}

**决策内容**: ${context.summary || '自动记录的决策'}

**上下文**: ${JSON.stringify(context.metadata || {})}

`
      
      fs.writeFileSync(memoryFile, content.trimEnd() + decisionSection, 'utf-8')
      this.api.logger.debug(`[EO AutoTrigger] Decision recorded`)
    } catch (err) {
      this.api.logger.error(`[EO AutoTrigger] Record decision failed: ${err}`)
    }
  }

  /**
   * Record a lesson (from task failure or error)
   */
  private async recordLesson(params: Record<string, unknown>, context: Record<string, unknown>): Promise<void> {
    const memoryFile = path.join(this.workspaceRoot, 'MEMORY.md')
    
    if (!fs.existsSync(memoryFile)) return
    
    try {
      const content = fs.readFileSync(memoryFile, 'utf-8')
      const timestamp = new Date().toISOString().replace('T', ' ').slice(0, 19)
      
      const lessonSection = `

---

## ⚠️ 教训记录 (${timestamp})

**类别**: ${params.category || 'general'}

**事件**: ${context.event || '自动记录'}

**教训**: ${context.lesson || context.error || '从经验中学习'}

**建议**: ${context.suggestion || '已记录教训，避免重复'}

`
      
      fs.writeFileSync(memoryFile, content.trimEnd() + lessonSection, 'utf-8')
      this.api.logger.debug(`[EO AutoTrigger] Lesson recorded`)
    } catch (err) {
      this.api.logger.error(`[EO AutoTrigger] Record lesson failed: ${err}`)
    }
  }

  /**
   * Sync current state to memory
   */
  private async syncToMemory(): Promise<void> {
    // This could integrate with DreamModule's syncToLongTermMemory
    this.api.logger.debug(`[EO AutoTrigger] Sync to memory triggered`)
  }

  /**
   * Process an incoming event - main entry point
   */
  async processEvent(event: TriggerEvent, metadata?: Record<string, unknown>): Promise<void> {
    if (!this.config.enabled) return
    
    // Check for explicit keywords in message
    if (event === 'explicit_keyword' && metadata?.message) {
      const content = this.extractExplicitContent(metadata.message as string)
      if (content) {
        metadata.explicitContent = content
        await this.executeAction({ type: 'record_decision', params: { source: 'explicit_keyword' } }, { summary: content })
      }
      return
    }
    
    // Match trigger rules
    const matchedRule = this.matchTrigger(event, metadata)
    if (matchedRule) {
      this.api.logger.debug(`[EO AutoTrigger] Matched rule: ${matchedRule.id}`)
      await this.executeAction(matchedRule.action, metadata || {})
    }
    
    // Check thresholds if metrics provided
    if (metadata?.metrics) {
      const matchedThresholds = this.checkThresholds(metadata.metrics as Record<ThresholdMetric, number>)
      for (const threshold of matchedThresholds) {
        this.api.logger.debug(`[EO AutoTrigger] Threshold triggered: ${threshold.id}`)
        await this.executeAction(threshold.action, metadata)
      }
    }
  }

  /**
   * Get current config
   */
  getConfig(): AutoTriggerConfig {
    return { ...this.config }
  }

  /**
   * Update config
   */
  updateConfig(updates: Partial<AutoTriggerConfig>): void {
    this.config = { ...this.config, ...updates }
  }

  /**
   * Add a custom trigger
   */
  addTrigger(rule: TriggerRule): void {
    const existing = this.config.triggers.findIndex(t => t.id === rule.id)
    if (existing >= 0) {
      this.config.triggers[existing] = rule
    } else {
      this.config.triggers.push(rule)
    }
  }
}

// ============================================================================
// Factory
// ============================================================================

let globalAutoTrigger: MemoryAutoTrigger | null = null

export function createMemoryAutoTrigger(
  api: OpenClawPluginApi, 
  workspaceRoot: string,
  config?: Partial<AutoTriggerConfig>
): MemoryAutoTrigger {
  globalAutoTrigger = new MemoryAutoTrigger(api, workspaceRoot, config)
  return globalAutoTrigger
}

export function getMemoryAutoTrigger(): MemoryAutoTrigger | null {
  return globalAutoTrigger
}
