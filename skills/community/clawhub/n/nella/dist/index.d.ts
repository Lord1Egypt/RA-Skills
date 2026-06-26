export { AssumptionTracker, AssumptionType, ChangeLedger, Changes, CodeChunk, Constraint, ContextManager, ContextService, DependencyChange, DependencyTracker, FileChange, IndexConfig, IndexManager, McpTool, McpToolCall, McpToolHandler, McpToolResult, NELLA_TOOLS, RawTaskYaml, RunLogger, RunResult, SearchQuery, SearchResponse, SearchResult, SearchService, SessionStore, Task, ToolHandlerConfig, ValidationResult, VerifyCodeRequest, VerifyCodeResult, Workspace, WorkspaceConfig, WorkspaceEntry, WorkspaceOptions, WorkspaceRegistry, WorkspaceService, WorkspaceSwitcher, applyChanges, cleanupTempWorkspace, createCodeVerifier, createHybridSearcher, createIndexManager, createMcpToolHandler, createNellaDir, createTempWorkspace, createWorkspaceRegistry, createWorkspaceSwitcher, generateRunId, getDiff, getModifiedFiles, getWorkspaceRegistry, getWorkspaceSwitcher, validateToolInput, writeArtifacts } from '@usenella/core';
import { ServerContext } from './mcp/server.js';
export { startMcpServer } from './mcp/server.js';
import { Tool } from '@modelcontextprotocol/sdk/types.js';

/**
 * Context Tools
 *
 * MCP tools for stateful context tracking across agent sessions:
 * - Dependency monitoring
 * - Assumption tracking
 * - Change history
 * - Session context
 */

declare function registerContextTools(): Tool[];
interface ToolCallResult {
    content: Array<{
        type: "text";
        text: string;
    }>;
    isError?: boolean;
}
declare function handleContextTool(name: string, args: Record<string, unknown>, context: ServerContext): Promise<ToolCallResult | null>;

export { ServerContext, handleContextTool, registerContextTools };
