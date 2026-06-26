interface ProactiveNotifier {
    notify(severity: 'info' | 'success' | 'warning' | 'error', title: string, message: string, channels?: string[], options?: any): Promise<string | void>;
}
export interface DreamConfig {
    /** Enable dream module */
    enabled: boolean;
    /** Run dream analysis on session end */
    triggerOnSessionEnd: boolean;
    /** Run dream analysis on idle */
    triggerOnIdle: boolean;
    /** Idle time before triggering dream (ms) */
    idleTimeoutMs: number;
    /** Maximum sessions to analyze per dream cycle */
    maxSessionsPerDream: number;
    /** Workspace root for session storage */
    workspaceRoot: string;
    /** Memory file path for persisting learnings */
    memoryPath: string;
    /** Proactive notifier for sending reports */
    notifier?: ProactiveNotifier;
    /** Feishu chat ID for notifications */
    feishuChatId?: string;
    /** Enable proactive report after dream completes */
    enableProactiveReport: boolean;
}
export interface DreamResult {
    sessionsAnalyzed: number;
    patternsExtracted: number;
    insightsGenerated: number;
    memoryUpdated: boolean;
    suggestions: string[];
    durationMs: number;
    errors: string[];
}
export interface DreamInsight {
    id: string;
    category: 'pattern' | 'decision' | 'preference' | 'workflow';
    content: string;
    confidence: number;
    evidenceSessions: string[];
    recommendation?: string;
    createdAt: number;
}
export declare class DreamModule {
    private config;
    private archiver;
    private memory;
    private lastDreamAt;
    private idleSince;
    private isDreaming;
    constructor(config?: Partial<DreamConfig>);
    /**
     * Call this when a session message is received
     */
    recordActivity(): void;
    /**
     * Check if we should trigger idle dream
     */
    shouldDreamOnIdle(): boolean;
    /**
     * Trigger dream analysis
     * Called automatically on session end or idle
     */
    dream(sessionKey?: string): Promise<DreamResult>;
    /**
     * Get list of recent sessions to analyze
     */
    private getRecentSessions;
    private analyzePatterns;
    /**
     * Generate insights from sessions and patterns
     */
    private generateInsights;
    private generateSuggestions;
    /**
     * Send proactive report after dream analysis completes
     */
    private sendProactiveReport;
    /**
     * Sync insights to MEMORY.md for long-term persistence.
     * This ensures learnings survive session resets and influence future behavior.
     */
    private syncToLongTermMemory;
    /**
     * Configure proactive notifier (can be called to update notifier at runtime)
     */
    setNotifier(notifier: ProactiveNotifier, feishuChatId?: string): void;
    getStatus(): {
        enabled: boolean;
        isDreaming: boolean;
        lastDreamAt: number;
        idleForMs: number;
        stats: ReturnType<typeof this.archiver.getStats>;
    };
    /**
     * Get current memory (learnings)
     */
    getMemory(): DreamInsight[];
}
export declare function getDreamModule(config?: Partial<DreamConfig>): DreamModule;
export declare function createDreamModule(config: Partial<DreamConfig>): DreamModule;
export {};
//# sourceMappingURL=eo-dream-enhanced.d.ts.map