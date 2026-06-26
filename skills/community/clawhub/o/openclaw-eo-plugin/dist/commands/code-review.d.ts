import type { CodeReviewOptions, EOCommandResult } from '../types/index.js';
export interface CodeReviewCommandContext {
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
 * Execute the /code-review command
 *
 * Performs code review using code-reviewer + senior-dev experts.
 */
export declare function executeCodeReview(options: CodeReviewOptions, ctx: CodeReviewCommandContext): Promise<EOCommandResult>;
//# sourceMappingURL=code-review.d.ts.map