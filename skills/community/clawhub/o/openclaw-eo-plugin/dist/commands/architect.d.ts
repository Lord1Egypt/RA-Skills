import type { ArchitectOptions, EOCommandResult } from '../types/index.js';
export interface ArchitectCommandContext {
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
 * Execute the /architect command
 *
 * Designs system architecture by assembling an architect + tech-lead + DBA team.
 */
export declare function executeArchitect(options: ArchitectOptions, ctx: ArchitectCommandContext): Promise<EOCommandResult>;
//# sourceMappingURL=architect.d.ts.map