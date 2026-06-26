/**
 * Pattern Extractor
 * Extracts patterns from analyzed sessions for the learning loop
 */
import type { AnalyzedSession } from './session-analyzer.js';
export interface ExtractedPattern {
    id: string;
    name: string;
    description: string;
    type: 'workflow' | 'expert_sequence' | 'error' | 'topic';
    frequency: number;
    evidence: string[];
    severity: 'low' | 'medium' | 'high';
    suggestedAction?: string;
    timestamp: number;
}
export interface PatternExtractionResult {
    patterns: ExtractedPattern[];
    newPatterns: ExtractedPattern[];
    errorPatterns: ExtractedPattern[];
    recommendedFixes: string[];
}
export declare class PatternExtractor {
    private patternLibrary;
    /**
     * Extract patterns from session analysis
     */
    extract(session: AnalyzedSession): Promise<ExtractedPattern[]>;
    /**
     * Extract workflow pattern
     */
    private extractWorkflowPattern;
    /**
     * Extract expert usage patterns
     */
    private extractExpertPatterns;
    /**
     * Extract error patterns
     */
    private extractErrorPatterns;
    /**
     * Extract topic patterns
     */
    private extractTopicPatterns;
    /**
     * Get suggested fix for error type
     */
    private getSuggestedFix;
    /**
     * Update pattern library
     */
    private updatePatternLibrary;
    /**
     * Get all patterns from library
     */
    getPatterns(): ExtractedPattern[];
    /**
     * Get patterns by type
     */
    getPatternsByType(type: ExtractedPattern['type']): ExtractedPattern[];
    /**
     * Get high severity patterns
     */
    getHighSeverityPatterns(): ExtractedPattern[];
    /**
     * Get pattern summary
     */
    getSummary(): {
        total: number;
        byType: Record<string, number>;
        highSeverity: number;
    };
}
//# sourceMappingURL=pattern-extractor.d.ts.map