/**
 * Global Memory
 * Shared memory accessible across all sessions with locking mechanism
 */

import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'fs'
import { join } from 'path'
import {
  MemoryPriority,
  RETENTION_PERIODS,
  type GlobalMemoryEntry,
  type UserPreference,
  type ProjectContext,
  type LongRunningTask,
  type MemorySystemOptions,
} from './memory-types.js'
import { MemoryPrioritizer } from './prioritizer.js'

export class GlobalMemory {
  private storagePath: string
  private entries: Map<string, GlobalMemoryEntry> = new Map()
  private locks: Map<string, string> = new Map() // key -> sessionId
  private api?: any
  private initialized = false

  constructor(options: MemorySystemOptions = {}) {
    this.storagePath = options.storageDir || join(process.cwd(), '.eo-memory', 'global')
  }

  /**
   * Initialize global memory store
   */
  async init(api?: any): Promise<void> {
    this.api = api
    if (this.initialized) return

    // Ensure storage directory exists
    if (!existsSync(this.storagePath)) {
      mkdirSync(this.storagePath, { recursive: true })
    }

    // Load existing entries from disk
    await this.loadFromDisk()
    this.initialized = true
    api?.logger?.debug(`[EO GlobalMemory] Initialized at ${this.storagePath}`)
  }

  /**
   * Load entries from disk
   */
  private async loadFromDisk(): Promise<void> {
    try {
      const indexPath = join(this.storagePath, 'index.json')
      if (existsSync(indexPath)) {
        const data = JSON.parse(readFileSync(indexPath, 'utf-8'))
        for (const entry of data.entries || []) {
          this.entries.set(entry.key, entry)
        }
        this.api?.logger?.debug(`[EO GlobalMemory] Loaded ${this.entries.size} entries from disk`)
      }
    } catch (error) {
      this.api?.logger?.warn(`[EO GlobalMemory] Failed to load from disk: ${error}`)
    }
  }

  /**
   * Save entries to disk
   */
  private async saveToDisk(): Promise<void> {
    try {
      const indexPath = join(this.storagePath, 'index.json')
      const data = {
        version: '1.0',
        updatedAt: Date.now(),
        entries: Array.from(this.entries.values()),
      }
      writeFileSync(indexPath, JSON.stringify(data, null, 2))
    } catch (error) {
      this.api?.logger?.error(`[EO GlobalMemory] Failed to save to disk: ${error}`)
    }
  }

  /**
   * Acquire lock for a key (for write operations)
   */
  private acquireLock(key: string, sessionId: string): boolean {
    if (this.locks.has(key)) {
      if (this.locks.get(key) === sessionId) {
        return true // Already locked by same session
      }
      return false // Locked by another session
    }
    this.locks.set(key, sessionId)
    return true
  }

  /**
   * Release lock for a key
   */
  private releaseLock(key: string, sessionId: string): void {
    if (this.locks.get(key) === sessionId) {
      this.locks.delete(key)
    }
  }

  /**
   * Get a global memory entry
   */
  async get<T = unknown>(key: string): Promise<GlobalMemoryEntry<T> | null> {
    const entry = this.entries.get(key)
    if (!entry) return null

    // Check expiration
    if (MemoryPrioritizer.isExpired(entry)) {
      await this.delete(key)
      return null
    }

    return entry as GlobalMemoryEntry<T>
  }

  /**
   * Set a global memory entry (requires lock)
   */
  async set<T = unknown>(key: string, value: T, priority: MemoryPriority, sessionId: string, metadata: Record<string, unknown> = {}): Promise<boolean> {
    if (!this.acquireLock(key, sessionId)) {
      this.api?.logger?.debug(`[EO GlobalMemory] Lock conflict for key: ${key}`)
      return false
    }

    try {
      const now = Date.now()
      const existing = this.entries.get(key)

      const entry: GlobalMemoryEntry<T> = {
        id: existing?.id || `gm_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`,
        key,
        value,
        priority: priority as MemoryPriority.P0_CRITICAL | MemoryPriority.P1_CONTEXT,
        createdAt: existing?.createdAt || now,
        updatedAt: now,
        expiresAt: MemoryPrioritizer.calculateExpiresAt(priority),
        tags: (Array.isArray(metadata.tags) ? metadata.tags : []) as string[],
        metadata,
        locked: false,
        lockSessionId: undefined,
      }

      this.entries.set(key, entry)
      await this.saveToDisk()
      return true
    } finally {
      this.releaseLock(key, sessionId)
    }
  }

  /**
   * Delete a global memory entry
   */
  async delete(key: string): Promise<boolean> {
    const deleted = this.entries.delete(key)
    if (deleted) {
      await this.saveToDisk()
    }
    return deleted
  }

  /**
   * List all global entries with optional filter
   */
  async list(filter?: { priority?: MemoryPriority; tags?: string[]; prefix?: string }): Promise<GlobalMemoryEntry[]> {
    let entries = Array.from(this.entries.values())

    // Apply filters
    if (filter?.priority !== undefined) {
      entries = entries.filter(e => e.priority === filter.priority)
    }
    if (filter?.tags?.length) {
      entries = entries.filter(e => filter.tags!.some(t => e.tags.includes(t)))
    }
    if (filter?.prefix) {
      entries = entries.filter(e => e.key.startsWith(filter.prefix!))
    }

    // Filter expired
    entries = MemoryPrioritizer.filterExpired(entries)

    // Sort by priority then recency
    return MemoryPrioritizer.sortByPriority(entries)
  }

  /**
   * Get user preferences
   */
  async getPreferences(category?: UserPreference['category']): Promise<UserPreference[]> {
    const entries = await this.list({ prefix: 'pref:' })
    const prefs = entries.map(e => e.value as UserPreference)
    if (category) {
      return prefs.filter(p => p.category === category)
    }
    return prefs
  }

  /**
   * Set user preference
   */
  async setPreference(key: string, value: unknown, category: UserPreference['category'], sessionId: string): Promise<boolean> {
    const prefKey = `pref:${category}:${key}`
    return this.set(prefKey, { key, value, category, updatedAt: Date.now() } as UserPreference, MemoryPriority.P1_CONTEXT, sessionId)
  }

  /**
   * Get project contexts
   */
  async getProjectContexts(status?: ProjectContext['status']): Promise<ProjectContext[]> {
    const entries = await this.list({ prefix: 'project:' })
    const projects = entries.map(e => e.value as ProjectContext)
    if (status) {
      return projects.filter(p => p.status === status)
    }
    return projects
  }

  /**
   * Set project context
   */
  async setProjectContext(project: ProjectContext, sessionId: string): Promise<boolean> {
    const key = `project:${project.projectId}`
    return this.set(key, project, MemoryPriority.P1_CONTEXT, sessionId, { tags: ['project-context'] })
  }

  /**
   * Get long-running tasks
   */
  async getLongRunningTasks(status?: LongRunningTask['status']): Promise<LongRunningTask[]> {
    const entries = await this.list({ prefix: 'task:' })
    const tasks = entries.map(e => e.value as LongRunningTask)
    if (status) {
      return tasks.filter(t => t.status === status)
    }
    return tasks
  }

  /**
   * Update long-running task
   */
  async updateTask(task: LongRunningTask, sessionId: string): Promise<boolean> {
    const key = `task:${task.taskId}`
    task.updatedAt = Date.now()
    return this.set(key, task, MemoryPriority.P1_CONTEXT, sessionId, { tags: ['task'] })
  }

  /**
   * Check if a key is locked
   */
  isLocked(key: string): boolean {
    return this.locks.has(key)
  }

  /**
   * Get lock holder session ID
   */
  getLockHolder(key: string): string | undefined {
    return this.locks.get(key)
  }

  /**
   * Get memory statistics
   */
  async getStats(): Promise<{ total: number; byPriority: Record<number, number>; locked: number }> {
    const entries = Array.from(this.entries.values())
    const byPriority: Record<number, number> = {}

    for (const entry of entries) {
      byPriority[entry.priority] = (byPriority[entry.priority] || 0) + 1
    }

    return {
      total: entries.length,
      byPriority,
      locked: this.locks.size,
    }
  }

  /**
   * Clear all global memory (use with caution)
   */
  async clear(): Promise<void> {
    this.entries.clear()
    this.locks.clear()
    await this.saveToDisk()
    this.api?.logger?.warn(`[EO GlobalMemory] All entries cleared`)
  }
}
