/**
 * Global Memory
 * Shared memory accessible across all sessions with locking mechanism
 */
import { MemoryPriority, type GlobalMemoryEntry, type UserPreference, type ProjectContext, type LongRunningTask, type MemorySystemOptions } from './memory-types.js';
export declare class GlobalMemory {
    private storagePath;
    private entries;
    private locks;
    private api?;
    private initialized;
    constructor(options?: MemorySystemOptions);
    /**
     * Initialize global memory store
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
     * Acquire lock for a key (for write operations)
     */
    private acquireLock;
    /**
     * Release lock for a key
     */
    private releaseLock;
    /**
     * Get a global memory entry
     */
    get<T = unknown>(key: string): Promise<GlobalMemoryEntry<T> | null>;
    /**
     * Set a global memory entry (requires lock)
     */
    set<T = unknown>(key: string, value: T, priority: MemoryPriority, sessionId: string, metadata?: Record<string, unknown>): Promise<boolean>;
    /**
     * Delete a global memory entry
     */
    delete(key: string): Promise<boolean>;
    /**
     * List all global entries with optional filter
     */
    list(filter?: {
        priority?: MemoryPriority;
        tags?: string[];
        prefix?: string;
    }): Promise<GlobalMemoryEntry[]>;
    /**
     * Get user preferences
     */
    getPreferences(category?: UserPreference['category']): Promise<UserPreference[]>;
    /**
     * Set user preference
     */
    setPreference(key: string, value: unknown, category: UserPreference['category'], sessionId: string): Promise<boolean>;
    /**
     * Get project contexts
     */
    getProjectContexts(status?: ProjectContext['status']): Promise<ProjectContext[]>;
    /**
     * Set project context
     */
    setProjectContext(project: ProjectContext, sessionId: string): Promise<boolean>;
    /**
     * Get long-running tasks
     */
    getLongRunningTasks(status?: LongRunningTask['status']): Promise<LongRunningTask[]>;
    /**
     * Update long-running task
     */
    updateTask(task: LongRunningTask, sessionId: string): Promise<boolean>;
    /**
     * Check if a key is locked
     */
    isLocked(key: string): boolean;
    /**
     * Get lock holder session ID
     */
    getLockHolder(key: string): string | undefined;
    /**
     * Get memory statistics
     */
    getStats(): Promise<{
        total: number;
        byPriority: Record<number, number>;
        locked: number;
    }>;
    /**
     * Clear all global memory (use with caution)
     */
    clear(): Promise<void>;
}
//# sourceMappingURL=global-memory.d.ts.map