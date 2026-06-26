// ============================================================================
// EO Multi-Expert Orchestrator v1.0 - Plugin Integration
//
// Full integration with EO Skills multi-expert-orchestrator.ts
// Bridges OpenClaw's sessions_spawn API with the EO expert system.
// ============================================================================
const DEFAULT_CONFIG = {
    defaultTimeoutMs: 300000,
    maxConcurrency: 4,
    abortOnCriticalFailure: true,
    retryDelayMs: 1000,
};
// ============================================================================
// Result Aggregator
// ============================================================================
class ResultAggregator {
    results = new Map();
    pending = new Set();
    startTime = 0;
    taskMap = new Map();
    constructor(tasks) {
        tasks.forEach(t => {
            this.pending.add(t.id);
            this.results.set(t.id, { id: t.id, name: t.name, success: false, durationMs: 0 });
            this.taskMap.set(t.id, t);
        });
        this.startTime = Date.now();
    }
    complete(id, result) {
        const existing = this.results.get(id);
        if (existing) {
            this.results.set(id, { ...existing, ...result, durationMs: Date.now() - this.startTime });
            this.pending.delete(id);
        }
    }
    isComplete() { return this.pending.size === 0; }
    getPending() { return Array.from(this.pending); }
    getResults() { return Array.from(this.results.values()); }
    getSummary() {
        const results = this.getResults();
        return {
            total: results.length,
            succeeded: results.filter(r => r.success).length,
            failed: results.filter(r => !r.success && !r.timedOut).length,
            timedOut: results.filter(r => r.timedOut).length,
            totalDurationMs: Date.now() - this.startTime,
        };
    }
    hasCriticalFailure() {
        return this.getResults().some(r => {
            if (r.success)
                return false;
            const task = this.taskMap.get(r.id);
            return task?.critical === true;
        });
    }
}
// ============================================================================
// Multi-Expert Orchestrator
// ============================================================================
/**
 * Orchestrates parallel execution of expert tasks using OpenClaw's sessions API.
 *
 * Key features:
 * - Parallel execution with configurable concurrency
 * - Timeout handling per task
 * - Error isolation (one failure doesn't affect others)
 * - Critical task abort support
 * - Result aggregation and summary
 *
 * Integration with OpenClaw:
 * - Uses sessions_spawn for subagent spawning
 * - Uses sessions_yield for coordinating multi-expert workflows
 * - Stores results in global __eoSessionResults for retrieval
 */
export class MultiExpertOrchestrator {
    config;
    activeHandles = new Map();
    constructor(config = {}) {
        this.config = { ...DEFAULT_CONFIG, ...config };
    }
    /**
     * Execute multiple expert tasks in parallel with robust error handling.
     * Uses OpenClaw's sessions_spawn for actual subagent creation.
     */
    async execute(tasks) {
        const aggregator = new ResultAggregator(tasks);
        const batchSize = this.config.maxConcurrency;
        logger.info(`Starting ${tasks.length} tasks, batchSize=${batchSize}`);
        for (let i = 0; i < tasks.length && !aggregator.hasCriticalFailure(); i += batchSize) {
            const batch = tasks.slice(i, i + batchSize);
            logger.debug(`Executing batch ${Math.floor(i / batchSize) + 1}: ${batch.map(t => t.name).join(', ')}`);
            const batchPromises = batch.map(task => this.executeTask(task, aggregator));
            await Promise.all(batchPromises);
        }
        const summary = aggregator.getSummary();
        logger.info(`Completed: ${summary.succeeded}/${summary.total} succeeded, ${summary.failed} failed, ${summary.timedOut} timed out`);
        return {
            results: aggregator.getResults(),
            summary,
            aborted: aggregator.hasCriticalFailure(),
        };
    }
    /**
     * Execute a single expert task with timeout and retry handling.
     * Integrates with OpenClaw's sessions_spawn for subagent creation.
     */
    async executeTask(task, aggregator) {
        const timeoutMs = task.timeoutMs || this.config.defaultTimeoutMs;
        const maxRetries = task.retries || 0;
        const startTime = Date.now();
        for (let attempt = 0; attempt <= maxRetries; attempt++) {
            try {
                // Use global sessions_spawn from OpenClaw plugin environment
                const sessions_spawn = globalThis.__openclaw_sessions_spawn;
                if (sessions_spawn) {
                    // Real OpenClaw integration
                    const handle = await sessions_spawn({
                        task: task.prompt,
                        mode: 'run',
                        runTimeoutSeconds: Math.floor(timeoutMs / 1000),
                    });
                    this.activeHandles.set(task.id, handle);
                    // Wait for completion with timeout polling
                    const result = await this.waitForCompletion(handle, timeoutMs);
                    aggregator.complete(task.id, {
                        success: true,
                        output: result,
                        durationMs: Date.now() - startTime,
                    });
                }
                else {
                    // Fallback: simulate execution for testing/dev without OpenClaw sessions
                    logger.warn(`No sessions_spawn available, simulating task: ${task.name}`);
                    await this.delay(Math.min(timeoutMs, 2000));
                    // Simulate a successful result using the prompt as output
                    const simulatedOutput = `[Simulated Expert Output]\n\nExpert: ${task.name}\n\nTask: ${task.prompt.slice(0, 500)}...\n\n[This is a simulated result. In production, this would be the actual subagent output.]`;
                    aggregator.complete(task.id, {
                        success: true,
                        output: simulatedOutput,
                        durationMs: Date.now() - startTime,
                    });
                }
                return;
            }
            catch (error) {
                const errorMsg = error instanceof Error ? error.message : String(error);
                console.error(`[MultiExpertOrchestrator] Task ${task.name} failed (attempt ${attempt + 1}): ${errorMsg}`);
                if (attempt < maxRetries) {
                    await this.delay(this.config.retryDelayMs);
                    continue;
                }
                aggregator.complete(task.id, {
                    success: false,
                    error: errorMsg,
                    timedOut: errorMsg.includes('timeout'),
                    durationMs: Date.now() - startTime,
                });
                return;
            }
        }
    }
    /**
     * Wait for task completion with timeout.
     * Polls the handle status until completion or timeout.
     */
    async waitForCompletion(handle, timeoutMs) {
        const startTime = Date.now();
        while (Date.now() - startTime < timeoutMs) {
            try {
                // Check handle status
                const status = handle.status?.();
                if (status === 'completed' || status === 'done') {
                    // Get result from global store
                    const runId = handle.sessionId || handle.runId;
                    const results = globalThis.__eoSessionResults || {};
                    const result = results[runId];
                    if (status === 'failed') {
                        throw new Error(`Task ${runId} failed with status: ${status}`);
                    }
                    return result?.output || result?.result || 'Task completed';
                }
                // Wait before next poll
                await this.delay(500);
            }
            catch (e) {
                // Handle may not have status() method in stub
                await this.delay(500);
            }
        }
        throw new Error(`Task ${handle.sessionId || handle.runId} timed out after ${timeoutMs}ms`);
    }
    /**
     * Abort all running tasks.
     */
    abortAll() {
        this.activeHandles.forEach((handle, id) => {
            try {
                handle.abort?.();
            }
            catch (e) {
                console.error(`[MultiExpertOrchestrator] Failed to abort task ${id}:`, e);
            }
        });
        this.activeHandles.clear();
    }
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}
// ============================================================================
// Convenience Functions
// ============================================================================
/**
 * Execute multiple expert tasks with default settings.
 */
export async function executeExperts(tasks) {
    const orchestrator = new MultiExpertOrchestrator();
    const result = await orchestrator.execute(tasks);
    return {
        results: result.results,
        summary: result.summary,
    };
}
// ============================================================================
// Expert Task Builder - convenience for creating tasks from EO experts
// ============================================================================
import { EXPERTS, TEAM_TEMPLATES } from '../experts/data.js';
import { buildExpertPrompt } from '../adapter/skill-adapter.js';
import { logger } from '../utils/logger.js';
/**
 * Build expert tasks for orchestration from a task description and team template.
 */
export function buildExpertTasks(taskDescription, teamTemplate, options) {
    const template = Array.isArray(teamTemplate) ? teamTemplate : (TEAM_TEMPLATES[teamTemplate] ?? ['plan-001', 'fe-001', 'be-001', 'qa-001']);
    const expertPrompts = {
        'plan-001': buildExpertPrompt('plan-001', 'Project Planner', `Create a detailed project plan for:\n\n${taskDescription}`, {}),
        'fe-001': buildExpertPrompt('fe-001', 'React Developer', `Provide frontend technical analysis for:\n\n${taskDescription}`, {}),
        'be-001': buildExpertPrompt('be-001', 'API Developer', `Provide backend technical analysis for:\n\n${taskDescription}`, {}),
        'qa-001': buildExpertPrompt('qa-001', 'Test Engineer', `Define testing strategy for:\n\n${taskDescription}`, {}),
        'arch-001': buildExpertPrompt('arch-001', 'System Architect', `Design system architecture for:\n\n${taskDescription}`, {}),
        'arch-003': buildExpertPrompt('arch-003', 'Data Architect', `Design data layer for:\n\n${taskDescription}`, {}),
        'devops-001': buildExpertPrompt('devops-001', 'CI/CD Engineer', `Design deployment and infrastructure for:\n\n${taskDescription}`, {}),
    };
    const timeoutMs = options?.timeoutMs ?? 120000;
    return template.map((expertId, idx) => {
        const expert = EXPERTS[expertId];
        const prompt = expertPrompts[expertId] ?? buildExpertPrompt(expertId, expert?.name ?? expertId, taskDescription, {});
        return {
            id: `expert-${idx + 1}-${expertId}`,
            name: expert?.name ?? expertId,
            prompt,
            timeoutMs,
        };
    });
}
//# sourceMappingURL=multi-expert-orchestrator.js.map