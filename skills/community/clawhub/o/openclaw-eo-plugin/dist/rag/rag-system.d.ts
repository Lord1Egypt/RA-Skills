export * from './types.js';
export interface RAGConfig {
    enabled: boolean;
    persistPath: string;
    defaultTopK: number;
    enableReranking: boolean;
    defaultACL: 'public' | 'private' | 'shared';
}
export interface KnowledgeChunk {
    id: string;
    layer: 1 | 2 | 3 | 4 | 5;
    content: string;
    metadata: {
        source: string;
        expertId?: string;
        patternName?: string;
        taskId?: string;
        taskType?: string;
        timestamp?: number;
        acl?: 'public' | 'private' | 'shared';
        allowedAgents?: string[];
        [key: string]: any;
    };
    score?: number;
}
export interface RetrievalQuery {
    query: string;
    topK?: number;
    strategy?: 'expert_retrieval' | 'pattern_retrieval' | 'checkpoint_retrieval' | 'history_retrieval' | 'hybrid';
}
export interface RetrievalResult {
    chunks: KnowledgeChunk[];
    scores: number[];
    strategy: string;
    queryTimeMs: number;
}
export interface ContextInjectionRequest {
    query: string;
    taskType?: string;
    topK?: number;
}
export interface ContextInjectionResult {
    chunks: KnowledgeChunk[];
    injection: string;
    sources: string[];
}
export declare class EORAGSystem {
    private config;
    private chunks;
    private initialized;
    private currentAgentId;
    constructor(config?: Partial<RAGConfig>);
    /**
     * Set the current agent context for access control
     */
    setAgentContext(agentId: string): void;
    /**
     * Check if current agent can access a chunk
     */
    private canAccess;
    /**
     * Initialize the RAG system - load from disk or seed default
     */
    initialize(): Promise<void>;
    /**
     * Seed default knowledge
     */
    private seedDefaultKnowledge;
    /**
     * Persist chunks to disk
     */
    private persist;
    /**
     * Search the knowledge base with access control
     */
    search(query: RetrievalQuery): Promise<RetrievalResult>;
    /**
     * Quick search
     */
    quickSearch(query: string, topK?: number): Promise<RetrievalResult>;
    /**
     * Inject relevant knowledge into context
     */
    injectContext(request: ContextInjectionRequest): Promise<ContextInjectionResult>;
    /**
     * Index a new chunk with access control
     */
    indexChunk(chunk: Omit<KnowledgeChunk, 'id'>, agentId?: string): Promise<string>;
    /**
     * Index a document (batch by paragraphs)
     */
    indexDocument(doc: {
        content: string;
        source: string;
        layer?: 1 | 2 | 3 | 4 | 5;
        acl?: 'public' | 'private' | 'shared';
        allowedAgents?: string[];
    }): Promise<number>;
    /**
     * Get chunks by source
     */
    getChunksBySource(source: string): Promise<KnowledgeChunk[]>;
    /**
     * Delete chunks by source
     */
    deleteBySource(source: string, agentId: string): Promise<number>;
    /**
     * Get system statistics
     */
    getStats(): Promise<{
        enabled: boolean;
        totalChunks: number;
        byLayer: Record<number, number>;
        byACL: Record<string, number>;
        storagePath: string;
    }>;
    isEnabled(): boolean;
    createETP(record: {
        taskId: string;
        taskType: string;
        taskDescription: string;
        participatingExperts: string[];
        durationMs: number;
        outcome: string;
        lessons?: string[];
    }): string;
}
export declare function getSharedRAGSystem(config?: Partial<RAGConfig>): EORAGSystem;
export declare function resetSharedRAGSystem(): void;
export declare function search(query: string, options?: {
    topK?: number;
    strategy?: string;
}): Promise<RetrievalResult>;
export declare function inject(request: ContextInjectionRequest): Promise<ContextInjectionResult>;
//# sourceMappingURL=rag-system.d.ts.map