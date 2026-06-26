/**
 * Context Management Hook
 * on_message hook that monitors context usage and triggers workflows
 */
import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
import { ContextManager } from '../context/manager.js';
export declare function initContextWorkflowHooks(api: OpenClawPluginApi): void;
export declare function onMessageHook(api: OpenClawPluginApi, event: any): Promise<void>;
/**
 * after_tool_call hook handler
 * 1. Check context changes
 * 2. Update workflow state
 * 3. Decide next steps
 */
export declare function afterToolCallHook(api: OpenClawPluginApi, event: any): Promise<void>;
/**
 * Get context manager for external access
 */
export declare function getContextManager(): ContextManager | null;
/**
 * Get active workflows
 */
export declare function getActiveWorkflows(): Map<string, any>;
//# sourceMappingURL=context-workflow.d.ts.map