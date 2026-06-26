export interface MemoryStats {
    heapUsed: number;
    heapTotal: number;
    external: number;
    rss: number;
    arrayBuffers: number;
}
export interface ContextStats {
    currentTokens: number;
    maxTokens: number;
    oldestMessageAge: number;
    messageCount: number;
    compressionRatio: number;
}
export interface SessionArchive {
    id: string;
    sessionId: string;
    startedAt: number;
    endedAt: number;
    messageCount: number;
    keyOutcomes: string[];
    expertContributions: string[];
    totalDuration: number;
    compressedSize: number;
    archivedAt: number;
}
export interface CleanupConfig {
    maxHeapMB: number;
    maxContextTokens: number;
    maxSessionAge: number;
    maxSessionMessages: number;
    archiveOldSessions: boolean;
    archiveAfterDays: number;
    compressionEnabled: boolean;
    autoCleanupIntervalMs: number;
}
export interface PerformanceProfile {
    avgResponseTime: number;
    avgMemoryUsage: number;
    activeSessions: number;
    completedTasks: number;
    errorRate: number;
    efficiency: number;
}
export interface OptimizationAction {
    type: 'gc' | 'compress' | 'archive' | 'flush' | 'restart_component';
    target?: string;
    reason: string;
    expectedImprovement: string;
    executed: boolean;
    timestamp: number;
}
export declare class SelfManager {
    private config;
    private memory;
    private context;
    private archives;
    private optimizer;
    private cleanupInterval?;
    private isRunning;
    constructor(config?: Partial<CleanupConfig>);
    /**
     * Start self-management.
     */
    start(): void;
    /**
     * Stop self-management.
     */
    stop(): void;
    /**
     * Run a single cleanup cycle.
     */
    runCleanupCycle(): Promise<OptimizationAction[]>;
    /**
     * Build current performance profile.
     */
    private buildProfile;
    /**
     * Start tracking a new session.
     */
    startSession(sessionId: string): void;
    /**
     * Record a message.
     */
    recordMessage(sessionId: string): void;
    /**
     * Record an outcome.
     */
    recordOutcome(sessionId: string, outcome: string): void;
    /**
     * Record expert contribution.
     */
    recordExpertContribution(sessionId: string, expertId: string): void;
    /**
     * End a session.
     */
    endSession(sessionId: string): SessionArchive | undefined;
    /**
     * Force garbage collection.
     */
    forceGC(): Promise<{
        success: boolean;
        freedMB: number;
    }>;
    /**
     * Force context compression.
     */
    forceCompression(): void;
    /**
     * Archive all old sessions.
     */
    archiveAllOldSessions(): number;
    /**
     * Get comprehensive status.
     */
    getStatus(): {
        memory: MemoryStats;
        context: ContextStats;
        archives: {
            total: number;
            oldestAge: number;
        };
        performance: {
            score: number;
            trend: string;
        };
        pendingActions: number;
    };
    /**
     * Get pending optimization actions.
     */
    getPendingActions(): OptimizationAction[];
}
export declare const selfManager: SelfManager;
export default SelfManager;
//# sourceMappingURL=self-manager.d.ts.map