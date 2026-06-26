/**
 * Context Module Types
 * Type definitions for proactive context management
 */

export interface ContextMetrics {
  /** Current token count (approximate) */
  tokenCount: number
  /** Token limit threshold */
  tokenLimit: number
  /** Usage percentage 0-100 */
  usagePercent: number
  /** Message count in current session */
  messageCount: number
  /** Timestamp of last check */
  timestamp: number
}

export interface ContextThresholds {
  warning: number   // 70% - yellow alert
  compress: number // 85% - need summarization
  critical: number  // 95% - emergency eviction
}

export const DEFAULT_THRESHOLDS: ContextThresholds = {
  warning: 70,
  compress: 85,
  critical: 95,
}

export enum ContextLevel {
  NORMAL = 'normal',
  WARNING = 'warning',
  COMPRESS = 'compress',
  CRITICAL = 'critical',
}

export interface SummarizableItem {
  id: string
  type: 'message' | 'tool_call' | 'result' | 'system'
  content: string
  timestamp: number
  importance: number // 0-100
  keyInfo?: string[]  // Extracted key points
}

export interface Summary {
  id: string
  originalCount: number
  condensedCount: number
  keyPoints: string[]
  preservedDecisions: string[]
  userPreferences: Record<string, string>
  currentTaskState: string
  timestamp: number
}

export interface EvictionCandidate {
  item: SummarizableItem
  score: number  // Lower = more likely to evict
  reason: string
}

export interface EvictionPolicy {
  name: string
  minImportance: number  // Minimum importance to keep
  maxAge: number        // Max age in ms before considering eviction
  preserveRecent: number // Keep last N items regardless
}

export const DEFAULT_EVICTION_POLICY: EvictionPolicy = {
  name: 'default',
  minImportance: 30,
  maxAge: 30 * 60 * 1000, // 30 minutes
  preserveRecent: 5,
}

export interface ContextState {
  metrics: ContextMetrics
  level: ContextLevel
  recentSummary?: Summary
  pendingItems: SummarizableItem[]
  lastReportTime: number
}

export interface MonitorConfig {
  thresholds: ContextThresholds
  checkIntervalMs: number  // Minimum time between checks
  reportIntervalMs: number // How often to report to SelfLearning
}
