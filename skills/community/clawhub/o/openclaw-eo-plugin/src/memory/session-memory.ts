/**
 * Session Memory
 * Per-session memory that can archive to global on session end
 */

import { existsSync, mkdirSync, readFileSync, writeFileSync, unlinkSync } from 'fs'
import { join } from 'path'
import {
  MemoryPriority,
  type SessionMemoryEntry,
  type SessionSnapshot,
  type MemorySystemOptions,
  type MemorySyncEvent,
} from './memory-types.js'
import { MemoryPrioritizer } from './prioritizer.js'

export class SessionMemory {
  private storagePath: string
  private sessionId: string
  private entries: Map<string, SessionMemoryEntry> = new Map()
  private api?: any
  private initialized = false
  private startTime: number

  constructor(sessionId: string, options: MemorySystemOptions = {}) {
    this.sessionId = sessionId
    this.storagePath = options.storageDir || join(process.cwd(), '.eo-memory', 'sessions', sessionId)
    this.startTime = Date.now()
  }

  /**
   * Initialize session memory store
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
    api?.logger?.debug(`[EO SessionMemory] Initialized session ${this.sessionId}`)
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
        this.api?.logger?.debug(`[EO SessionMemory] Loaded ${this.entries.size} entries for session ${this.sessionId}`)
      }
    } catch (error) {
      this.api?.logger?.warn(`[EO SessionMemory] Failed to load from disk: ${error}`)
    }
  }

  /**
   * Save entries to disk
   */
  private async saveToDisk(): Promise<void> {
    try {
      const indexPath = join(this.storagePath, 'index.json')
      const data = {
        sessionId: this.sessionId,
        version: '1.0',
        updatedAt: Date.now(),
        entries: Array.from(this.entries.values()),
      }
      writeFileSync(indexPath, JSON.stringify(data, null, 2))
    } catch (error) {
      this.api?.logger?.error(`[EO SessionMemory] Failed to save to disk: ${error}`)
    }
  }

  /**
   * Generate a unique memory ID
   */
  private generateId(): string {
    return `sm_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`
  }

  /**
   * Get a session memory entry
   */
  async get<T = unknown>(key: string): Promise<SessionMemoryEntry<T> | null> {
    const entry = this.entries.get(key)
    if (!entry) return null

    // Check expiration
    if (MemoryPrioritizer.isExpired(entry)) {
      await this.delete(key)
      return null
    }

    return entry as SessionMemoryEntry<T>
  }

  /**
   * Set a session memory entry
   */
  async set<T = unknown>(key: string, value: T, priority: MemoryPriority, metadata: Record<string, unknown> = {}): Promise<SessionMemoryEntry> {
    const now = Date.now()
    const existing = this.entries.get(key)

    const entry: SessionMemoryEntry<T> = {
      id: existing?.id || this.generateId(),
      key,
      value,
      priority,
      createdAt: existing?.createdAt || now,
      updatedAt: now,
      expiresAt: MemoryPrioritizer.calculateExpiresAt(priority),
      sessionId: this.sessionId,
      tags: (Array.isArray(metadata.tags) ? metadata.tags : []) as string[],
      metadata,
      archived: existing?.archived || false,
    }

    this.entries.set(key, entry)
    await this.saveToDisk()
    return entry as SessionMemoryEntry
  }

  /**
   * Update an existing entry
   */
  async update<T = unknown>(key: string, updates: Partial<{ value: T; priority: MemoryPriority; tags: string[]; metadata: Record<string, unknown> }>): Promise<SessionMemoryEntry<T> | null> {
    const existing = this.entries.get(key)
    if (!existing) return null

    const mergedTags = updates.tags ?? (existing.tags as string[])
    return this.set(key, updates.value ?? existing.value, updates.priority ?? existing.priority, {
      ...existing.metadata,
      ...updates.metadata,
      tags: mergedTags,
    }) as Promise<SessionMemoryEntry<T>>
  }

  /**
   * Delete a session memory entry
   */
  async delete(key: string): Promise<boolean> {
    const deleted = this.entries.delete(key)
    if (deleted) {
      await this.saveToDisk()
    }
    return deleted
  }

  /**
   * List all session entries with optional filter
   */
  async list(filter?: { priority?: MemoryPriority; tags?: string[]; prefix?: string; includeArchived?: boolean }): Promise<SessionMemoryEntry[]> {
    let entries = Array.from(this.entries.values())

    // Filter archived unless explicitly included
    if (!filter?.includeArchived) {
      entries = entries.filter(e => !e.archived)
    }

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
   * Add a decision to session memory
   */
  async addDecision(key: string, decision: unknown, metadata: Record<string, unknown> = {}): Promise<SessionMemoryEntry> {
    return this.set(`decision:${key}`, decision, MemoryPriority.P0_CRITICAL, {
      tags: ['decision', 'critical'],
      ...metadata,
    })
  }

  /**
   * Get all decisions from session
   */
  async getDecisions(): Promise<SessionMemoryEntry[]> {
    return this.list({ prefix: 'decision:' })
  }

  /**
   * Add a conversation summary
   */
  async addSummary(key: string, summary: string, metadata: Record<string, unknown> = {}): Promise<SessionMemoryEntry> {
    return this.set(`summary:${key}`, summary, MemoryPriority.P2_SUMMARY, {
      tags: ['summary'],
      ...metadata,
    })
  }

  /**
   * Get all summaries from session
   */
  async getSummaries(): Promise<SessionMemoryEntry[]> {
    return this.list({ prefix: 'summary:' })
  }

  /**
   * Mark entry for archival to global memory
   */
  async markForArchival(key: string): Promise<boolean> {
    const entry = this.entries.get(key)
    if (!entry) return false

    entry.archived = true
    await this.saveToDisk()
    return true
  }

  /**
   * Get entries marked for archival
   */
  async getEntriesForArchival(): Promise<SessionMemoryEntry[]> {
    return this.list({ includeArchived: true }).then(entries =>
      entries.filter(e => e.archived || MemoryPrioritizer.shouldArchiveToGlobal(e))
    )
  }

  /**
   * Generate session snapshot for archiving
   */
  async generateSnapshot(summary: string): Promise<SessionSnapshot> {
    const decisions = await this.list({ prefix: 'decision:' })
    const tasks = await this.list({ prefix: 'task:' })
    const prefs = await this.list({ prefix: 'pref:' })

    return {
      sessionId: this.sessionId,
      startedAt: this.startTime,
      endedAt: Date.now(),
      summary,
      decisions: decisions.map(d => ({
        ...d,
        priority: d.priority as any, // Cast for compatibility
        locked: false,
      })),
      context: tasks.map(t => t.value as any),
      tasks: tasks.map(t => t.value as any),
      preferences: prefs.map(p => p.value as any),
    }
  }

  /**
   * Clear temporary (P3) entries
   */
  async clearTemporary(): Promise<number> {
    const tempEntries = await this.list({ priority: MemoryPriority.P3_TEMPORARY })
    let cleared = 0

    for (const entry of tempEntries) {
      if (await this.delete(entry.key)) {
        cleared++
      }
    }

    return cleared
  }

  /**
   * Clear all session memory
   */
  async clear(): Promise<void> {
    this.entries.clear()
    await this.saveToDisk()
  }

  /**
   * Clean up session storage from disk
   */
  async destroy(): Promise<void> {
    try {
      const indexPath = join(this.storagePath, 'index.json')
      if (existsSync(indexPath)) {
        unlinkSync(indexPath)
      }
      this.entries.clear()
      this.api?.logger?.debug(`[EO SessionMemory] Destroyed session ${this.sessionId}`)
    } catch (error) {
      this.api?.logger?.error(`[EO SessionMemory] Failed to destroy session: ${error}`)
    }
  }

  /**
   * Get session memory statistics
   */
  async getStats(): Promise<{ total: number; byPriority: Record<number, number>; archived: number; duration: number }> {
    const entries = Array.from(this.entries.values())
    const byPriority: Record<number, number> = {}

    for (const entry of entries) {
      byPriority[entry.priority] = (byPriority[entry.priority] || 0) + 1
    }

    return {
      total: entries.length,
      byPriority,
      archived: entries.filter(e => e.archived).length,
      duration: Date.now() - this.startTime,
    }
  }

  /**
   * Get session ID
   */
  getSessionId(): string {
    return this.sessionId
  }
}
