export type IndexLayer = 1 | 2 | 3 | 4 | 5;
export interface RAGConfig {
    enabled: boolean;
    vectorStore: {
        type: 'lancedb' | 'chromadb' | 'memory';
        persistPath?: string;
        embeddingDimension?: number;
    };
    embedding?: {
        model?: string;
        provider?: 'openai' | 'local';
    };
    retrieval: {
        defaultTopK: number;
        rerankTopK?: number;
        hybridAlpha: number;
        enableReranking: boolean;
    };
    indexUpdate?: {
        autoIndex?: boolean;
        indexOnStartup?: boolean;
    };
    conflictResolution?: {
        recency?: number;
        successRate?: number;
        expertAuthority?: number;
        contextSimilarity?: number;
    };
}
export interface RetrievalQuery {
    query: string;
    topK?: number;
    strategy?: 'expert_retrieval' | 'pattern_retrieval' | 'checkpoint_retrieval' | 'decision_retrieval' | 'history_retrieval' | 'hybrid';
}
export interface RetrievalResult {
    chunks: KnowledgeChunk[];
    scores: number[];
    strategy: string;
    queryTimeMs: number;
}
export interface KnowledgeChunk {
    id: string;
    layer: IndexLayer;
    content: string;
    metadata: ChunkMetadata;
    score?: number;
}
export interface ChunkMetadata {
    source: string;
    expertId?: string;
    patternName?: string;
    taskId?: string;
    checkpointId?: string;
    decisionId?: string;
    sessionId?: string;
    timestamp?: number;
    tags?: string[];
}
export interface ContextInjectionRequest {
    query: string;
    taskType?: string;
    topK?: number;
    domains?: string[];
    techStack?: string[];
}
export interface ContextInjectionResult {
    chunks: KnowledgeChunk[];
    injection: string;
    sources: string[];
}
export interface ETPRecord {
    protocolVersion: string;
    timestamp: number;
    taskId: string;
    taskType: string;
    taskDescription: string;
    participatingExperts: string[];
    durationMs: number;
    outcome: 'success' | 'partial' | 'failed';
    keyDecisions: ETPDecision[];
    lessons: string[];
    checkpointsPassed: string[];
    checkpointsFailed: string[];
}
export interface ETPDecision {
    point: string;
    alternatives: string[];
    chosen: string;
    rationale: string;
    timestamp: number;
}
export interface CheckpointResult {
    checkpointId: string;
    checkpointName: string;
    passed: boolean;
    failedItems?: string[];
    warnings?: number;
    durationMs: number;
    timestamp: number;
}
//# sourceMappingURL=types.d.ts.map