import type { PluginHookSessionEndEvent, PluginHookSessionStartEvent, PluginHookToolContext } from 'openclaw/plugin-sdk';
export declare const MEMORY_TYPES: readonly ["user", "feedback", "project", "reference"];
export type MemoryType = (typeof MEMORY_TYPES)[number];
/**
 * session_end hook
 *
 * Proactively saves key information from the session to memory.
 */
export declare function handleSessionEnd(event: PluginHookSessionEndEvent, ctx: PluginHookToolContext): Promise<void>;
/**
 * session_start hook
 *
 * Loads relevant memories when a session starts.
 */
export declare function handleSessionStart(event: PluginHookSessionStartEvent, ctx: PluginHookToolContext): Promise<void>;
export declare function getMemoryStats(): {
    totalEntries: number;
    byType: Record<string, number>;
    lastSaveTime: number;
    sizeBytes: number;
};
export declare const eoMemoryHookHandlers: {
    session_end: typeof handleSessionEnd;
    session_start: typeof handleSessionStart;
};
//# sourceMappingURL=handler.d.ts.map