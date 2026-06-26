export interface SubagentRuntime {
    subagent: {
        run(params: {
            sessionKey: string;
            message: string;
            extraSystemPrompt?: string;
            provider?: string;
            model?: string;
        }): Promise<{
            runId: string;
        }>;
        waitForRun(params: {
            runId: string;
            timeoutMs?: number;
        }): Promise<{
            status: string;
            error?: string;
        }>;
        getSessionMessages(params: {
            sessionKey: string;
            limit?: number;
        }): Promise<{
            messages: unknown[];
        }>;
    };
}
export declare function createLogger(prefix: string): {
    info: (msg: string) => void;
    warn: (msg: string) => void;
    error: (msg: string) => void;
};
export interface RuntimeAdapterConfig {
    sessionKey: string;
    defaultTimeoutMs?: number;
}
/**
 * Create a SkillContext-compatible runtime adapter for OpenClaw plugin tools.
 *
 * This wraps the OpenClaw spawning API (sessions_spawn, sessions_yield, etc.)
 * into the SkillContext.runtime.subagent interface expected by EO skills.
 */
export declare function createRuntimeAdapter(config: RuntimeAdapterConfig): SubagentRuntime;
export declare function storeSessionMessage(sessionKey: string, message: unknown): void;
export declare function completeSession(runId: string, result: unknown, error?: string): void;
export interface SimpleSkillContext {
    runtime: SubagentRuntime;
    logger: ReturnType<typeof createLogger>;
    sessionId?: string;
}
export declare function buildSkillContext(sessionId?: string, loggerPrefix?: string): SimpleSkillContext;
//# sourceMappingURL=runtime-adapter.d.ts.map