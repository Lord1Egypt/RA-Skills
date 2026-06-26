/**
 * Pattern Learning Tool - Extract and retrieve successful patterns
 */
import type { AgentToolResult } from '@mariozechner/pi-agent-core';
export interface PatternLearnParams {
    action: 'learn' | 'retrieve' | 'stats' | 'list';
    taskQuery?: string;
    sessionFile?: string;
}
/**
 * Handle pattern learning operations
 */
export declare function handlePatternLearn(params: PatternLearnParams, agentId?: string): Promise<AgentToolResult<unknown>>;
//# sourceMappingURL=pattern-learn.d.ts.map