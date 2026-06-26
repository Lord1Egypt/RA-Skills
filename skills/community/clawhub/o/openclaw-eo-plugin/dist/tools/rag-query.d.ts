/**
 * EO RAG Query Tool Handler v2
 * Uses shared RAG system with access control
 */
import type { AgentToolResult } from '@mariozechner/pi-agent-core';
export interface RAGQueryParams {
    query: string;
    topK?: number;
    strategy?: 'expert_retrieval' | 'pattern_retrieval' | 'checkpoint_retrieval' | 'history_retrieval' | 'hybrid';
}
export declare function handleRAGQuery(params: RAGQueryParams, agentId?: string): Promise<AgentToolResult<unknown>>;
//# sourceMappingURL=rag-query.d.ts.map