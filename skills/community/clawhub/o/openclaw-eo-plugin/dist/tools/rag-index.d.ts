/**
 * EO RAG Index Tool Handler
 * Bulk index documents into shared knowledge base
 */
import type { AgentToolResult } from '@mariozechner/pi-agent-core';
export interface RAGIndexParams {
    action: 'add' | 'remove' | 'list' | 'stats' | 'clear';
    source?: string;
    content?: string;
    filePath?: string;
    layer?: 1 | 2 | 3 | 4 | 5;
    tags?: string[];
    visibility?: 'public' | 'protected' | 'private';
}
export declare function handleRAGIndex(params: RAGIndexParams, agentId?: string): Promise<AgentToolResult<unknown>>;
//# sourceMappingURL=rag-index.d.ts.map