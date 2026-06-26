/**
 * Session Start Hook
 * Loads relevant memory and context when a session begins
 */
import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
import { MemorySync } from '../memory/index.js';
/**
 * Initialize memory sync engine
 */
export declare function initMemorySync(api: OpenClawPluginApi): MemorySync;
/**
 * Get or create memory sync instance
 */
export declare function getMemorySync(): MemorySync | null;
export interface SessionStartContext {
    recentTopics: string[];
    pendingTasks: string[];
    lastSessionSummary?: string;
    preferences?: unknown[];
    projects?: unknown[];
    tasks?: unknown[];
}
export declare function createSessionStartHook(api: OpenClawPluginApi): {
    id: string;
    name: string;
    description: string;
    handle: (event: any) => Promise<void>;
};
//# sourceMappingURL=session-start.d.ts.map