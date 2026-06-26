// ============================================================================
// EO Runtime Adapter - Bridge OpenClaw Plugin API → SkillContext
//
// Provides the SkillContext.runtime.subagent interface for EO skill implementations
// by wrapping OpenClaw's sessions API (sessions_spawn, sessions_yield, etc.)
// ============================================================================
// ---------------------------------------------------------------------------
// Runtime Adapter Interface (what skill executors need)
// ---------------------------------------------------------------------------
import { logger } from './utils/logger.js';
// ---------------------------------------------------------------------------
// Default Logger
// ---------------------------------------------------------------------------
export function createLogger(prefix) {
    return {
        info: (msg) => logger.info(`[${prefix}] INFO: ${msg}`),
        warn: (msg) => console.warn(`[${prefix}] WARN: ${msg}`),
        error: (msg) => console.error(`[${prefix}] ERROR: ${msg}`),
    };
}
/**
 * Create a SkillContext-compatible runtime adapter for OpenClaw plugin tools.
 *
 * This wraps the OpenClaw spawning API (sessions_spawn, sessions_yield, etc.)
 * into the SkillContext.runtime.subagent interface expected by EO skills.
 */
export function createRuntimeAdapter(config) {
    const { sessionKey, defaultTimeoutMs = 300000 } = config;
    // Track running sessions
    const runningSessions = new Map();
    return {
        subagent: {
            async run(params) {
                const runId = `run-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
                runningSessions.set(runId, { status: 'running' });
                logger.debug(`Spawning subagent runId=${runId} sessionKey=${params.sessionKey}`);
                logger.debug(`message length: ${params.message.length} chars`);
                globalThis.__eoRuntimeTasks = globalThis.__eoRuntimeTasks || {};
                globalThis.__eoRuntimeTasks[runId] = {
                    runId,
                    sessionKey: params.sessionKey,
                    message: params.message,
                    extraSystemPrompt: params.extraSystemPrompt,
                    provider: params.provider,
                    model: params.model,
                    createdAt: Date.now(),
                };
                return { runId };
            },
            async waitForRun(params) {
                const timeoutMs = params.timeoutMs ?? defaultTimeoutMs;
                const startTime = Date.now();
                const runId = params.runId;
                logger.debug(`Waiting for runId=${runId} timeout=${timeoutMs}ms`);
                while (Date.now() - startTime < timeoutMs) {
                    const session = runningSessions.get(runId);
                    if (session?.status === 'completed') {
                        runningSessions.delete(runId);
                        return { status: 'completed' };
                    }
                    if (session?.status === 'failed') {
                        runningSessions.delete(runId);
                        return { status: 'failed', error: 'Expert task failed' };
                    }
                    await new Promise(resolve => setTimeout(resolve, 500));
                }
                runningSessions.delete(runId);
                return { status: 'timeout', error: `Task ${runId} timed out after ${timeoutMs}ms` };
            },
            async getSessionMessages(params) {
                const limit = params.limit ?? 10;
                const key = params.sessionKey;
                globalThis.__eoSessionMessages = globalThis.__eoSessionMessages || {};
                const sessionMessages = globalThis.__eoSessionMessages[key] || [];
                const messages = sessionMessages.slice(-limit);
                logger.debug(`getSessionMessages sessionKey=${key} count=${messages.length}`);
                return { messages };
            },
        },
    };
}
// ---------------------------------------------------------------------------
// Message Accumulation Helper
// ---------------------------------------------------------------------------
export function storeSessionMessage(sessionKey, message) {
    ;
    globalThis.__eoSessionMessages = globalThis.__eoSessionMessages || {};
    globalThis.__eoSessionMessages[sessionKey] = globalThis.__eoSessionMessages[sessionKey] || [];
    globalThis.__eoSessionMessages[sessionKey].push(message);
}
export function completeSession(runId, result, error) {
    const tasks = globalThis.__eoRuntimeTasks || {};
    const task = tasks[runId];
    if (task) {
        ;
        globalThis.__eoSessionResults = globalThis.__eoSessionResults || {};
        globalThis.__eoSessionResults[runId] = { result, error, completedAt: Date.now() };
        storeSessionMessage(task.sessionKey, {
            role: 'assistant',
            content: typeof result === 'string' ? result : JSON.stringify(result),
            runId,
        });
    }
}
export function buildSkillContext(sessionId, loggerPrefix = 'skill') {
    const logger = createLogger(loggerPrefix);
    const runtime = createRuntimeAdapter({ sessionKey: sessionId ?? 'default' });
    return { runtime, logger, sessionId };
}
//# sourceMappingURL=runtime-adapter.js.map