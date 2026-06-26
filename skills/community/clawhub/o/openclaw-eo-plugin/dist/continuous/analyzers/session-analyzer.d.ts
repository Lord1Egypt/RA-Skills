/**
 * Session Analyzer
 * Analyzes session data to extract insights for the learning loop
 */
export interface SessionAnalysisInput {
    toolsUsed: string[];
    messageCount: number;
    lastMessage: string;
    context: Record<string, unknown>;
}
export interface AnalyzedSession {
    sessionId: string;
    timestamp: number;
    toolsUsed: string[];
    messageCount: number;
    keyTopics: string[];
    successIndicators: SuccessIndicator[];
    errorIndicators: ErrorIndicator[];
    expertUsage: Map<string, number>;
    workflowType: 'planning' | 'coding' | 'review' | 'debugging' | 'unknown';
}
export interface SuccessIndicator {
    type: 'completion' | 'verification' | 'positive_feedback';
    description: string;
    confidence: number;
}
export interface ErrorIndicator {
    type: 'error_keyword' | 'failed_tool' | 'retry';
    description: string;
    severity: 'low' | 'medium' | 'high';
    count: number;
}
export declare class SessionAnalyzer {
    private sessionHistory;
    /**
     * Analyze a session
     */
    analyze(input: SessionAnalysisInput): Promise<AnalyzedSession>;
    /**
     * Extract key topics from message
     */
    private extractTopics;
    /**
     * Detect success indicators
     */
    private detectSuccessIndicators;
    /**
     * Detect error indicators
     */
    private detectErrorIndicators;
    /**
     * Analyze which experts were used
     */
    private analyzeExpertUsage;
    /**
     * Classify the workflow type
     */
    private classifyWorkflow;
    /**
     * Get recent sessions
     */
    getRecentSessions(count?: number): AnalyzedSession[];
    /**
     * Get session statistics
     */
    getStats(): {
        totalSessions: number;
        avgMessageCount: number;
        topWorkflow: AnalyzedSession['workflowType'] | null;
    };
}
//# sourceMappingURL=session-analyzer.d.ts.map