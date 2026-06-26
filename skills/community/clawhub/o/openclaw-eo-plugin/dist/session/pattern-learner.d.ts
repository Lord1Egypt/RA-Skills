/**
 * Pattern Learner - Learn from Successful Execution Paths
 *
 * Analyzes historical sessions to extract successful patterns
 * and stores them in RAG L2 for reuse.
 *
 * This enables:
 * - Learning from successes (not just failures)
 * - Reducing user intervention by following proven paths
 * - Building a reusable pattern library
 */
export interface PatternRecord {
    id: string;
    taskType: string;
    taskDescription: string;
    steps: string[];
    tools: string[];
    outcome: 'success' | 'partial' | 'failed';
    userFeedback?: 'positive' | 'neutral' | 'negative';
    duration?: number;
    timestamp: number;
    sessionId: string;
}
export interface LearnedPattern {
    id: string;
    name: string;
    taskType: string;
    description: string;
    pattern: string;
    tools: string[];
    successIndicators: string[];
    适用场景: string[];
    示例Task?: string;
    confidence: number;
    lastUsed: string;
}
/**
 * Pattern Learner - Extracts and stores successful patterns
 */
export declare class PatternLearner {
    private ragSystem;
    private patterns;
    /**
     * Analyze a session and extract successful patterns
     */
    analyzeSession(sessionKey: string, sessionData: any): Promise<LearnedPattern[]>;
    /**
     * Analyze multiple sessions and build pattern library
     */
    learnFromSessions(sessions: Array<{
        key: string;
        data: any;
    }>): Promise<{
        patternsLearned: number;
        highConfidence: number;
    }>;
    /**
     * Store pattern in RAG L2
     */
    private storePattern;
    /**
     * Retrieve relevant patterns for a task
     */
    retrievePatterns(taskQuery: string, topK?: number): Promise<LearnedPattern[]>;
    /**
     * Extract text content from message
     */
    private extractText;
    /**
     * Check if message indicates task start
     */
    private isTaskStart;
    /**
     * Extract task description from message
     */
    private extractTaskDescription;
    /**
     * Create a pattern from task execution
     */
    private createPattern;
    /**
     * Classify task type
     */
    private classifyTask;
    /**
     * Generate pattern name
     */
    private generatePatternName;
    /**
     * Merge similar patterns
     */
    private mergePatterns;
    /**
     * Get stored patterns count
     */
    getStats(): Promise<{
        totalPatterns: number;
        byType: Record<string, number>;
    }>;
}
export declare const patternLearner: PatternLearner;
//# sourceMappingURL=pattern-learner.d.ts.map