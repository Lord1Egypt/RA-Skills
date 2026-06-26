/**
 * Memory Sync Engine
 * Coordinates memory synchronization between sessions
 */
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'fs';
import { join } from 'path';
import { MemoryPrioritizer } from './prioritizer.js';
import { GlobalMemory } from './global-memory.js';
import { SessionMemory } from './session-memory.js';
export class MemorySync {
    globalMemory;
    sessionMemories = new Map();
    api;
    storagePath;
    options;
    initialized = false;
    constructor(api, options = {}) {
        this.api = api;
        this.storagePath = options.storageDir || join(process.cwd(), '.eo-memory');
        this.options = {
            storageDir: this.storagePath,
            maxMemorySize: options.maxMemorySize || 10000,
            autoArchive: options.autoArchive ?? true,
            conflictStrategy: options.conflictStrategy || 'latest',
        };
        this.globalMemory = new GlobalMemory(this.options);
    }
    /**
     * Initialize the memory sync engine
     */
    async init() {
        if (this.initialized)
            return;
        // Ensure storage directory exists
        if (!existsSync(this.storagePath)) {
            mkdirSync(this.storagePath, { recursive: true });
        }
        // Initialize global memory
        await this.globalMemory.init(this.api);
        // Load sync history
        await this.loadSyncHistory();
        this.initialized = true;
        this.api.logger.debug(`[EO MemorySync] Initialized with strategy: ${this.options.conflictStrategy}`);
    }
    /**
     * Load sync history from disk
     */
    async loadSyncHistory() {
        try {
            const historyPath = join(this.storagePath, 'sync-history.json');
            if (existsSync(historyPath)) {
                const data = JSON.parse(readFileSync(historyPath, 'utf-8'));
                this.api.logger.debug(`[EO MemorySync] Loaded sync history: ${data.events?.length || 0} events`);
            }
        }
        catch (error) {
            this.api.logger.warn(`[EO MemorySync] Failed to load sync history: ${error}`);
        }
    }
    /**
     * Save sync event to history
     */
    async saveSyncEvent(event) {
        try {
            const historyPath = join(this.storagePath, 'sync-history.json');
            let history = { events: [] };
            if (existsSync(historyPath)) {
                history = JSON.parse(readFileSync(historyPath, 'utf-8'));
            }
            history.events.push(event);
            // Keep last 1000 events
            if (history.events.length > 1000) {
                history.events = history.events.slice(-1000);
            }
            writeFileSync(historyPath, JSON.stringify(history, null, 2));
        }
        catch (error) {
            this.api.logger.error(`[EO MemorySync] Failed to save sync event: ${error}`);
        }
    }
    /**
     * Get or create session memory
     */
    async getSessionMemory(sessionId) {
        if (!this.sessionMemories.has(sessionId)) {
            const sessionMemory = new SessionMemory(sessionId, this.options);
            await sessionMemory.init(this.api);
            this.sessionMemories.set(sessionId, sessionMemory);
        }
        return this.sessionMemories.get(sessionId);
    }
    /**
     * Session start: Load relevant memory into context
     */
    async onSessionStart(context) {
        const { sessionId, api } = context;
        api.logger.debug(`[EO MemorySync] Session start: ${sessionId}`);
        // Create session memory
        const sessionMemory = await this.getSessionMemory(sessionId);
        // Load user preferences
        const preferences = await this.globalMemory.getPreferences();
        // Load active project contexts
        const projects = await this.globalMemory.getProjectContexts('active');
        // Load pending long-running tasks
        const tasks = await this.globalMemory.getLongRunningTasks()
            .then(allTasks => allTasks.filter(t => t.status !== 'completed'));
        // Load recent memories relevant to this session
        const recentMemories = await this.globalMemory.list()
            .then(entries => entries.slice(0, 20));
        // Save sync event
        await this.saveSyncEvent({
            type: 'load',
            sessionId,
            timestamp: Date.now(),
            entries: recentMemories.map(e => e.key),
        });
        api.logger.debug(`[EO MemorySync] Loaded: ${preferences.length} prefs, ${projects.length} projects, ${tasks.length} tasks`);
        return { preferences, projects, tasks, recentMemories };
    }
    /**
     * Session end: Archive session memories to global
     */
    async onSessionEnd(context, summary) {
        const { sessionId, api } = context;
        api.logger.debug(`[EO MemorySync] Session end: ${sessionId}`);
        const sessionMemory = await this.getSessionMemory(sessionId);
        let archived = 0;
        let cleared = 0;
        let conflicts = 0;
        // Generate session snapshot
        const snapshot = await sessionMemory.generateSnapshot(summary);
        // Get entries to archive
        const entriesToArchive = await sessionMemory.getEntriesForArchival();
        for (const entry of entriesToArchive) {
            if (!MemoryPrioritizer.shouldArchiveToGlobal(entry))
                continue;
            // Check for conflicts with existing global entries
            const existing = await this.globalMemory.get(entry.key);
            if (existing) {
                // Resolve conflict
                const resolved = MemoryPrioritizer.resolveConflict(existing, entry);
                if (resolved !== existing) {
                    conflicts++;
                    api.logger.debug(`[EO MemorySync] Conflict resolved for key: ${entry.key}`);
                }
            }
            // Archive to global
            const success = await this.globalMemory.set(entry.key, entry.value, entry.priority, sessionId, { archivedFrom: sessionId, tags: entry.tags, ...entry.metadata });
            if (success) {
                archived++;
                await sessionMemory.markForArchival(entry.key);
            }
        }
        // Clear temporary entries
        cleared = await sessionMemory.clearTemporary();
        // Save sync event
        await this.saveSyncEvent({
            type: 'archive',
            sessionId,
            timestamp: Date.now(),
            entries: entriesToArchive.map(e => e.key),
            conflictResolved: conflicts > 0,
        });
        // Clean up session memory
        await sessionMemory.destroy();
        this.sessionMemories.delete(sessionId);
        api.logger.debug(`[EO MemorySync] Session end complete: archived=${archived}, cleared=${cleared}, conflicts=${conflicts}`);
        return { archived, cleared, conflicts };
    }
    /**
     * Quick save during session
     */
    async quickSave(context, key, value, priority) {
        const { sessionId } = context;
        const sessionMemory = await this.getSessionMemory(sessionId);
        // Auto-classify priority if not specified
        const p = priority || MemoryPrioritizer.classifyEntry(key, value);
        await sessionMemory.set(key, value, p);
        return true;
    }
    /**
     * Quick load during session
     */
    async quickLoad(context, key) {
        const { sessionId } = context;
        const sessionMemory = await this.getSessionMemory(sessionId);
        const entry = await sessionMemory.get(key);
        return entry?.value ?? null;
    }
    /**
     * Update user preference
     */
    async updatePreference(context, key, value, category) {
        return this.globalMemory.setPreference(key, value, category, context.sessionId);
    }
    /**
     * Update project context
     */
    async updateProjectContext(context, project) {
        project.lastAccessedAt = Date.now();
        return this.globalMemory.setProjectContext(project, context.sessionId);
    }
    /**
     * Update long-running task
     */
    async updateTask(context, task) {
        return this.globalMemory.updateTask(task, context.sessionId);
    }
    /**
     * Get all memory statistics
     */
    async getStats() {
        const globalStats = await this.globalMemory.getStats();
        return {
            global: globalStats,
            sessions: this.sessionMemories.size,
            strategy: this.options.conflictStrategy,
        };
    }
    /**
     * Clear all memory (use with caution)
     */
    async clearAll() {
        await this.globalMemory.clear();
        for (const sessionMemory of this.sessionMemories.values()) {
            await sessionMemory.clear();
        }
        this.sessionMemories.clear();
        this.api.logger.warn(`[EO MemorySync] All memory cleared`);
    }
}
//# sourceMappingURL=memory-sync.js.map