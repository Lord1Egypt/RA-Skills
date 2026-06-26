/**
 * Memory Types - Cross-Session Memory System
 * Defines all types for the EO memory architecture
 */

import type { OpenClawPluginApi } from 'openclaw/plugin-sdk'

// Memory Priority Levels
export enum MemoryPriority {
  P0_CRITICAL = 0,   // Critical decisions - permanent retention
  P1_CONTEXT = 1,     // Project context - 30 days retention
  P2_SUMMARY = 2,     // Conversation summary - 7 days retention
  P3_TEMPORARY = 3,   // Temporary state - cleared on session end
}

// Retention periods in milliseconds
export const RETENTION_PERIODS: Record<MemoryPriority, number | null> = {
  [MemoryPriority.P0_CRITICAL]: null,                    // Permanent
  [MemoryPriority.P1_CONTEXT]: 30 * 24 * 60 * 60 * 1000, // 30 days
  [MemoryPriority.P2_SUMMARY]: 7 * 24 * 60 * 60 * 1000,  // 7 days
  [MemoryPriority.P3_TEMPORARY]: null,                    // Session only
}

// Base memory entry interface
export interface MemoryEntry<T = unknown> {
  id: string
  key: string
  value: T
  priority: MemoryPriority
  createdAt: number
  updatedAt: number
  expiresAt: number | null
  sessionId?: string
  tags: string[]
  metadata: Record<string, unknown>
}

// Global memory entry - shared across all sessions
export interface GlobalMemoryEntry<T = unknown> extends MemoryEntry<T> {
  priority: MemoryPriority.P0_CRITICAL | MemoryPriority.P1_CONTEXT
  locked: boolean
  lockSessionId?: string
}

// Session memory entry - single session only
export interface SessionMemoryEntry<T = unknown> extends MemoryEntry<T> {
  priority: MemoryPriority
  archived: boolean
}

// User preference entry
export interface UserPreference {
  key: string
  value: unknown
  category: 'ui' | 'behavior' | 'project' | 'system'
  updatedAt: number
}

// Project context entry
export interface ProjectContext {
  projectId: string
  projectName: string
  status: 'active' | 'paused' | 'completed'
  lastAccessedAt: number
  metadata: Record<string, unknown>
}

// Long-running task entry
export interface LongRunningTask {
  taskId: string
  description: string
  status: 'pending' | 'in_progress' | 'blocked' | 'completed'
  createdAt: number
  updatedAt: number
  blockedBy?: string[]
}

// Memory sync event
export interface MemorySyncEvent {
  type: 'load' | 'save' | 'archive' | 'clear' | 'conflict'
  sessionId: string
  timestamp: number
  entries: string[]  // entry keys
  conflictResolved?: boolean
}

// Session memory snapshot (for archiving)
export interface SessionSnapshot {
  sessionId: string
  startedAt: number
  endedAt: number
  summary: string
  decisions: GlobalMemoryEntry[]
  context: ProjectContext[]
  tasks: LongRunningTask[]
  preferences: UserPreference[]
}

// Memory system options
export interface MemorySystemOptions {
  storageDir?: string
  maxMemorySize?: number
  autoArchive?: boolean
  conflictStrategy?: 'latest' | 'priority' | 'merge'
}

// Memory store interface
export interface IMemoryStore {
  get<T>(key: string): Promise<MemoryEntry<T> | null>
  set<T>(key: string, entry: MemoryEntry<T>): Promise<void>
  delete(key: string): Promise<boolean>
  list(filter?: Partial<MemoryEntry>): Promise<MemoryEntry[]>
  clear(): Promise<void>
}

// API context passed to hooks
export interface MemoryContext {
  sessionId: string
  userId?: string
  channel?: string
  api: OpenClawPluginApi
}
