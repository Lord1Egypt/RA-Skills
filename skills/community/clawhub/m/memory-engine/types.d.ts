export type MemoryType = 'fact' | 'experience' | 'lesson' | 'preference' | 'skill';
export type MemoryStatus = 'active' | 'archived';
export interface MemoryRecord {
    id: string;
    content: string;
    type: MemoryType;
    status: MemoryStatus;
    importance: number;
    tags: string[];
    userId?: string;
    agentId?: string;
    createdAt: number;
    updatedAt: number;
    accessedAt: number;
    accessCount: number;
    version: number;
    metadata?: Record<string, unknown>;
    embedding?: number[];
}
export interface MemoryCreateInput {
    content: string;
    type?: MemoryType;
    importance?: number;
    tags?: string[];
    userId?: string;
    agentId?: string;
    metadata?: Record<string, unknown>;
    embedding?: number[];
}
export interface SearchOptions {
    query?: string;
    limit?: number;
    offset?: number;
    userId?: string;
    type?: MemoryType;
    tags?: string[];
    status?: MemoryStatus;
}
export interface SearchResult {
    memory: MemoryRecord;
    score: number;
}
export interface ContextMessage {
    role: 'user' | 'assistant' | 'system';
    content: string;
}
export interface CompressedMessage {
    role: 'user' | 'assistant' | 'system';
    content: string;
    originalIndex: number;
    preserved: boolean;
    summary?: string;
}
export interface CompressionResult {
    messages: CompressedMessage[];
    originalCount: number;
    compressedCount: number;
    compressionRate: number;
    removedCount: number;
}
export interface KnowledgeExtractionResult {
    shouldExtract: boolean;
    content: string;
    knowledgeType: MemoryType;
    importance: number;
    tags: string[];
    metadata?: Record<string, any>;
}
export interface AfterTurnParams {
    sessionId: string;
    sessionFile: string;
    messages: any[];
    prePromptMessageCount: number;
}
export interface AfterTurnResult {
    processed: boolean;
    totalTokens?: number;
    tokenEstimate?: number;
}
export interface AssembleParams {
    sessionId: string;
    sessionFile: string;
    messages: any[];
    tokenBudget?: number;
}
export interface CompactParams {
    sessionId: string;
    sessionFile: string;
    tokenBudget?: number;
    force?: boolean;
}
export interface AssembleResult {
    system: string;
    messages: ContextMessage[];
    tokenEstimate?: number;
    totalTokens?: number;
    systemPromptAddition?: string;
    activeRecallPrompts?: string[];
}
export interface PluginConfig {
    dbPath?: string;
}
//# sourceMappingURL=types.d.ts.map