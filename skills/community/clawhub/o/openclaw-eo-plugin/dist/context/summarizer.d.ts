/**
 * Smart Context Summarizer
 * Compresses old conversation into key points while preserving critical info
 */
import type { SummarizableItem, Summary } from './types.js';
export declare class ContextSummarizer {
    private minImportanceThreshold;
    constructor(minImportanceThreshold?: number);
    /**
     * Generate a unique ID
     */
    private generateId;
    /**
     * Extract key information from items
     */
    extractKeyInfo(items: SummarizableItem[]): string[];
    /**
     * Identify key decisions from conversation
     */
    extractDecisions(items: SummarizableItem[]): string[];
    /**
     * Extract user preferences from conversation
     */
    extractPreferences(items: SummarizableItem[]): Record<string, string>;
    /**
     * Determine current task state from recent items
     */
    extractTaskState(items: SummarizableItem[]): string;
    /**
     * Create a summary from a list of items
     */
    summarize(items: SummarizableItem[]): Summary;
    /**
     * Mark a message as having key info
     */
    static markAsKeyInfo(item: SummarizableItem, keyInfo: string[]): SummarizableItem;
}
//# sourceMappingURL=summarizer.d.ts.map