export interface DreamTrigger {
    type: 'manual' | 'scheduled' | 'session_end' | 'threshold';
}
export interface DreamResult {
    success: boolean;
    report?: DreamReport;
    error?: string;
    durationMs: number;
}
export interface DreamReport {
    id: string;
    date: string;
    dreamStartTime: string;
    dreamEndTime: string;
    durationMs: number;
    sessionsAnalyzed: number;
    analysis: SessionAnalysis;
    patterns: PatternExtraction;
    evolutionOps: EvolutionOperation[];
    memoryUpdate: string;
}
export interface SessionAnalysis {
    date: string;
    totalSessions: number;
    sessionsWithTask: number;
    taskCompletionRate: number;
    topExpertsUsed: string[];
    topTools: string[];
    errorPatterns: ErrorPattern[];
    successPatterns: SuccessPattern[];
    avgSessionDurationMs: number;
    notableEvents: string[];
}
export interface PatternExtraction {
    crossSessionPatterns: CrossSessionPattern[];
    expertWeaknesses: ExpertWeakness[];
    newExpertNeeds: NewExpertNeed[];
    toolImprovements: ToolImprovement[];
}
export interface CrossSessionPattern {
    name: string;
    description: string;
    evidence: string[];
    severity: 'low' | 'medium' | 'high';
}
export interface ErrorPattern {
    pattern: string;
    frequency: number;
    sessionIds: string[];
    suggestedFix?: string;
}
export interface SuccessPattern {
    pattern: string;
    frequency: number;
    sessionIds: string[];
    recommendedPractice: string;
}
export interface ExpertWeakness {
    expertId: string;
    expertName: string;
    weakness: string;
    evidence: string[];
    suggestedPromptRefinement: string;
    severity: 'low' | 'medium' | 'high';
}
export interface NewExpertNeed {
    domain: string;
    description: string;
    supportingSessions: string[];
    suggestedExpertProfile: string;
    priority: 'low' | 'medium' | 'high';
}
export interface ToolImprovement {
    toolName: string;
    improvement: string;
    evidence: string[];
}
export interface EvolutionOperation {
    type: 'patch' | 'new_expert' | 'memory_update';
    target: string;
    description: string;
    severity: 'low' | 'medium' | 'high';
    status: 'pending' | 'approved' | 'rejected';
    patchFile?: string;
}
export declare class DreamEngine {
    private workspace;
    private memoryUpdate;
    private lastReport;
    private reports;
    constructor(workspace: string);
    /**
     * Execute a dream cycle
     */
    executeDream(trigger?: DreamTrigger): Promise<DreamResult>;
    /**
     * Load sessions from workspace
     */
    private loadSessions;
    /**
     * Analyze sessions
     */
    private analyzeSessions;
    /**
     * Extract patterns from analysis
     */
    private extractPatterns;
    /**
     * Generate evolution operations
     */
    private generateEvolutionOps;
    /**
     * Generate memory update content
     */
    private generateMemoryUpdate;
    /**
     * Get dream status
     */
    getStatus(): {
        lastReport: string | null;
        reportCount: number;
        pendingPatches: number;
    };
    /**
     * List dream reports
     */
    listReports(): {
        date: string;
        summary: string;
    }[];
    /**
     * Get pending evolution operations
     */
    getPendingPatches(): EvolutionOperation[];
    /**
     * Get memory update from last dream
     */
    getMemoryUpdate(): string;
}
export interface SessionData {
    sessionId: string;
    date: string;
    startTime: number;
    endTime: number;
    taskDescription?: string;
    taskCompleted?: boolean;
    messages: SessionMessage[];
}
export interface SessionMessage {
    role: 'user' | 'assistant' | 'system';
    content: string;
    timestamp?: number;
    tools?: {
        name: string;
        input: Record<string, unknown>;
    }[];
}
//# sourceMappingURL=dream-engine.d.ts.map