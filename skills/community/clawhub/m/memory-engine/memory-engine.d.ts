import { MemoryRecord, MemoryCreateInput, SearchOptions, SearchResult, ContextMessage, CompressionResult, KnowledgeExtractionResult } from './types';
export interface MemoryEngineConfig {
    dbPath?: string;
    enableCompression?: boolean;
    maxMessages?: number;
    keepRecentCount?: number;
}
export declare class MemoryEngine {
    private store;
    private extractor;
    private compressor;
    private initialized;
    embeddingModel: any;
    constructor(config?: MemoryEngineConfig);
    initialize(): Promise<void>;
    isInitialized(): boolean;
    addMemory(input: MemoryCreateInput): Promise<MemoryRecord>;
    searchMemories(query: string, options?: SearchOptions): Promise<SearchResult[]>;
    getAllMemories(limit?: number): Promise<MemoryRecord[]>;
    extractKnowledge(content: string, messageType?: 'user' | 'ai'): Promise<KnowledgeExtractionResult | null>;
    extractFromConversationPair(userMessage: string, aiMessage: string): Promise<KnowledgeExtractionResult[]>;
    compressContext(messages: ContextMessage[]): CompressionResult;
    getContext(messages: ContextMessage[], _tokenBudget?: number): ContextMessage[];
    getStatistics(): any;
    archiveOldMemories(maxAgeDays: number, minImportance: number): number;
    shutdown(): Promise<void>;
}
export declare function createMemoryEngine(config?: MemoryEngineConfig): Promise<MemoryEngine>;
//# sourceMappingURL=memory-engine.d.ts.map