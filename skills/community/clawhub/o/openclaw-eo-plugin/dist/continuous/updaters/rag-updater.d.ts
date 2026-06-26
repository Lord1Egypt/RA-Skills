/**
 * RAG Updater
 * Updates the RAG knowledge base with new patterns and knowledge
 */
import { EORAGSystem } from '../../rag/rag-system.js';
import type { ExtractedPattern } from '../analyzers/pattern-extractor.js';
import type { AnalyzedSession } from '../analyzers/session-analyzer.js';
export interface RAGUpdateResult {
    success: boolean;
    chunksAdded: number;
    chunksRemoved: number;
    errors: string[];
}
export declare class RAGUpdater {
    private rag;
    private updateLog;
    constructor(rag: EORAGSystem);
    /**
     * Update RAG with extracted patterns
     */
    update(patterns: ExtractedPattern[]): Promise<RAGUpdateResult>;
    /**
     * Update RAG with session data
     */
    updateWithSession(session: AnalyzedSession): Promise<RAGUpdateResult>;
    /**
     * Index expert knowledge
     */
    indexExpertKnowledge(expertId: string, knowledge: string): Promise<void>;
    /**
     * Index ETP (Experience Transfer Protocol) record
     */
    indexETPRecord(taskId: string, taskDescription: string, outcome: string, lessons?: string[]): Promise<void>;
    /**
     * Format pattern content for RAG
     */
    private formatPatternContent;
    /**
     * Format session content for RAG
     */
    private formatSessionContent;
    /**
     * Log update operation
     */
    private logUpdate;
    /**
     * Get update statistics
     */
    getStats(): {
        totalUpdates: number;
        recentUpdates: number;
    };
    /**
     * Clear stale entries (placeholder for actual cleanup logic)
     */
    clearStaleEntries(_maxAgeMs?: number): Promise<number>;
}
//# sourceMappingURL=rag-updater.d.ts.map