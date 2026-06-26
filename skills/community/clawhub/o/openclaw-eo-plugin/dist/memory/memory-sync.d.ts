/**
 * Memory Sync Engine
 * Coordinates memory synchronization between sessions
 */
import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
import { MemoryPriority, type GlobalMemoryEntry, type MemorySystemOptions, type MemoryContext, type UserPreference, type ProjectContext, type LongRunningTask } from './memory-types.js';
import { SessionMemory } from './session-memory.js';
export declare class MemorySync {
    private globalMemory;
    private sessionMemories;
    private api;
    private storagePath;
    private options;
    private initialized;
    constructor(api: OpenClawPluginApi, options?: MemorySystemOptions);
    /**
     * Initialize the memory sync engine
     */
    init(): Promise<void>;
    /**
     * Load sync history from disk
     */
    private loadSyncHistory;
    /**
     * Save sync event to history
     */
    private saveSyncEvent;
    /**
     * Get or create session memory
     */
    getSessionMemory(sessionId: string): Promise<SessionMemory>;
    /**
     * Session start: Load relevant memory into context
     */
    onSessionStart(context: MemoryContext): Promise<{
        preferences: UserPreference[];
        projects: ProjectContext[];
        tasks: LongRunningTask[];
        recentMemories: GlobalMemoryEntry[];
    }>;
    /**
     * Session end: Archive session memories to global
     */
    onSessionEnd(context: MemoryContext, summary: string): Promise<{
        archived: number;
        cleared: number;
        conflicts: number;
    }>;
    /**
     * Quick save during session
     */
    quickSave(context: MemoryContext, key: string, value: unknown, priority?: MemoryPriority): Promise<boolean>;
    /**
     * Quick load during session
     */
    quickLoad<T = unknown>(context: MemoryContext, key: string): Promise<T | null>;
    /**
     * Update user preference
     */
    updatePreference(context: MemoryContext, key: string, value: unknown, category: UserPreference['category']): Promise<boolean>;
    /**
     * Update project context
     */
    updateProjectContext(context: MemoryContext, project: ProjectContext): Promise<boolean>;
    /**
     * Update long-running task
     */
    updateTask(context: MemoryContext, task: LongRunningTask): Promise<boolean>;
    /**
     * Get all memory statistics
     */
    getStats(): Promise<{
        global: {
            total: number;
            byPriority: Record<number, number>;
            locked: number;
        };
        sessions: number;
        strategy: string;
    }>;
    /**
     * Clear all memory (use with caution)
     */
    clearAll(): Promise<void>;
}
//# sourceMappingURL=memory-sync.d.ts.map