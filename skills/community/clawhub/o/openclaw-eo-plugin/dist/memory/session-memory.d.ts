/**
 * Session Memory
 * Per-session memory that can archive to global on session end
 */
import { MemoryPriority, type SessionMemoryEntry, type SessionSnapshot, type MemorySystemOptions } from './memory-types.js';
export declare class SessionMemory {
    private storagePath;
    private sessionId;
    private entries;
    private api?;
    private initialized;
    private startTime;
    constructor(sessionId: string, options?: MemorySystemOptions);
    /**
     * Initialize session memory store
     */
    init(api?: any): Promise<void>;
    /**
     * Load entries from disk
     */
    private loadFromDisk;
    /**
     * Save entries to disk
     */
    private saveToDisk;
    /**
     * Generate a unique memory ID
     */
    private generateId;
    /**
     * Get a session memory entry
     */
    get<T = unknown>(key: string): Promise<SessionMemoryEntry<T> | null>;
    /**
     * Set a session memory entry
     */
    set<T = unknown>(key: string, value: T, priority: MemoryPriority, metadata?: Record<string, unknown>): Promise<SessionMemoryEntry>;
    /**
     * Update an existing entry
     */
    update<T = unknown>(key: string, updates: Partial<{
        value: T;
        priority: MemoryPriority;
        tags: string[];
        metadata: Record<string, unknown>;
    }>): Promise<SessionMemoryEntry<T> | null>;
    /**
     * Delete a session memory entry
     */
    delete(key: string): Promise<boolean>;
    /**
     * List all session entries with optional filter
     */
    list(filter?: {
        priority?: MemoryPriority;
        tags?: string[];
        prefix?: string;
        includeArchived?: boolean;
    }): Promise<SessionMemoryEntry[]>;
    /**
     * Add a decision to session memory
     */
    addDecision(key: string, decision: unknown, metadata?: Record<string, unknown>): Promise<SessionMemoryEntry>;
    /**
     * Get all decisions from session
     */
    getDecisions(): Promise<SessionMemoryEntry[]>;
    /**
     * Add a conversation summary
     */
    addSummary(key: string, summary: string, metadata?: Record<string, unknown>): Promise<SessionMemoryEntry>;
    /**
     * Get all summaries from session
     */
    getSummaries(): Promise<SessionMemoryEntry[]>;
    /**
     * Mark entry for archival to global memory
     */
    markForArchival(key: string): Promise<boolean>;
    /**
     * Get entries marked for archival
     */
    getEntriesForArchival(): Promise<SessionMemoryEntry[]>;
    /**
     * Generate session snapshot for archiving
     */
    generateSnapshot(summary: string): Promise<SessionSnapshot>;
    /**
     * Clear temporary (P3) entries
     */
    clearTemporary(): Promise<number>;
    /**
     * Clear all session memory
     */
    clear(): Promise<void>;
    /**
     * Clean up session storage from disk
     */
    destroy(): Promise<void>;
    /**
     * Get session memory statistics
     */
    getStats(): Promise<{
        total: number;
        byPriority: Record<number, number>;
        archived: number;
        duration: number;
    }>;
    /**
     * Get session ID
     */
    getSessionId(): string;
}
//# sourceMappingURL=session-memory.d.ts.map