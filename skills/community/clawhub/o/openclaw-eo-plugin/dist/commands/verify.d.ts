import type { VerifyOptions, EOCommandResult } from '../types/index.js';
export interface VerifyCommandContext {
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
 * Execute the /verify command
 *
 * Verifies implementation against specifications using appropriate experts.
 */
export declare function executeVerify(options: VerifyOptions, ctx: VerifyCommandContext): Promise<EOCommandResult>;
//# sourceMappingURL=verify.d.ts.map