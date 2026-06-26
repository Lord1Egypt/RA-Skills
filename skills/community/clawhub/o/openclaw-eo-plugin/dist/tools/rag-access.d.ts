/**
 * EO RAG Access Control Tool Handler
 * Manage per-agent access to knowledge base (ACL-based)
 */
import type { AgentToolResult } from '@mariozechner/pi-agent-core';
export interface RAGAccessParams {
    action: 'grant' | 'revoke' | 'list' | 'set-default';
    agentId?: string;
    layers?: number[];
    visibility?: 'public' | 'protected' | 'private';
}
export declare function handleRAGAccess(params: RAGAccessParams): Promise<AgentToolResult<unknown>>;
//# sourceMappingURL=rag-access.d.ts.map