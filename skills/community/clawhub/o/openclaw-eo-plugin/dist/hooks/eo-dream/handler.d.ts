import type { PluginHookBeforeToolCallEvent, PluginHookBeforeToolCallResult, PluginHookAfterToolCallEvent, PluginHookToolContext, PluginHookSessionEndEvent, PluginHookSessionStartEvent } from 'openclaw/plugin-sdk';
/**
 * session_end hook
 *
 * Triggered when a session ends. Collects session data for dream analysis.
 */
export declare function handleSessionEnd(event: PluginHookSessionEndEvent, ctx: PluginHookToolContext): Promise<void>;
/**
 * session_start hook
 *
 * Triggered when a session starts. Could load relevant memories.
 */
export declare function handleSessionStart(event: PluginHookSessionStartEvent, ctx: PluginHookToolContext): Promise<void>;
/**
 * before_tool_call hook for dream tools
 */
export declare function handleBeforeToolCall(event: PluginHookBeforeToolCallEvent, ctx: PluginHookToolContext): Promise<PluginHookBeforeToolCallResult | void>;
/**
 * after_tool_call hook for dream tools
 */
export declare function handleAfterToolCall(event: PluginHookAfterToolCallEvent, ctx: PluginHookToolContext): Promise<void>;
export declare function getDreamHookStatus(): {
    enabled: boolean;
    pendingDreamTrigger: boolean;
    sessionCount: number;
    lastSessionTime: number;
    timeSinceLastSession: number;
};
export declare function clearPendingDreamTrigger(): void;
export declare const eoDreamHookHandlers: {
    session_end: typeof handleSessionEnd;
    session_start: typeof handleSessionStart;
    before_tool_call: typeof handleBeforeToolCall;
    after_tool_call: typeof handleAfterToolCall;
};
//# sourceMappingURL=handler.d.ts.map