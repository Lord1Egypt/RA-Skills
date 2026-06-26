/**
 * EO Code Review Tool Handler
 * Reviews code using MultiExpertOrchestrator
 */
import type { AgentToolResult } from '@mariozechner/pi-agent-core';
export declare function handleCodeReview(params: {
    path?: string;
    depth?: string;
    focus?: string;
}): Promise<AgentToolResult<unknown>>;
//# sourceMappingURL=code-review.d.ts.map