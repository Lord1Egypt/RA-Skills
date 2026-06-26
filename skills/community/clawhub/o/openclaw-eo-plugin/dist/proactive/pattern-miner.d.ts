/**
 * Pattern Miner
 * Extracts patterns from session history for learning
 */
export interface SessionPattern {
    toolsUsed: string[];
    commonTopics: string[];
    expertInvocations: number;
    timestamp: number;
}
export interface MinedPattern {
    type: 'tool_sequence' | 'topic' | 'workflow';
    pattern: string;
    frequency: number;
}
export declare function minePatterns(sessions: SessionPattern[]): MinedPattern[];
export declare function extractTopics(message: string): string[];
//# sourceMappingURL=pattern-miner.d.ts.map