import type { PlanOptions, EOCommandResult } from '../types/index.js';
export interface PlanCommandContext {
    runtime: {
        subagent: {
            run: (params: {
                sessionKey: string;
                message: string;
                extraSystemPrompt?: string;
                provider?: string;
                model?: string;
            }) => Promise<{
                runId: string;
            }>;
            waitForRun: (params: {
                runId: string;
                timeoutMs?: number;
            }) => Promise<{
                status: string;
                error?: string;
            }>;
            getSessionMessages: (params: {
                sessionKey: string;
                limit?: number;
            }) => Promise<{
                messages: unknown[];
            }>;
        };
    };
    logger: {
        info: (msg: string) => void;
        warn: (msg: string) => void;
        error: (msg: string) => void;
    };
    sessionId?: string;
}
/**
 * Execute the /plan command
 *
 * Creates a project plan by assembling a PM + Engineer + QA team,
 * then coordinating their analysis through subagent sessions.
 */
export declare function executePlan(options: PlanOptions, ctx: PlanCommandContext): Promise<EOCommandResult>;
//# sourceMappingURL=plan.d.ts.map