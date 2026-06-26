export interface ExpertTask {
    id: string;
    name: string;
    prompt: string;
    timeoutMs?: number;
    retries?: number;
    critical?: boolean;
}
export interface ExpertResult {
    id: string;
    name: string;
    success: boolean;
    output?: string;
    error?: string;
    durationMs: number;
    timedOut?: boolean;
}
export interface OrchestratorConfig {
    defaultTimeoutMs: number;
    maxConcurrency: number;
    abortOnCriticalFailure: boolean;
    retryDelayMs: number;
}
declare class ResultAggregator {
    private results;
    private pending;
    private startTime;
    private taskMap;
    constructor(tasks: ExpertTask[]);
    complete(id: string, result: Partial<ExpertResult>): void;
    isComplete(): boolean;
    getPending(): string[];
    getResults(): ExpertResult[];
    getSummary(): {
        total: number;
        succeeded: number;
        failed: number;
        timedOut: number;
        totalDurationMs: number;
    };
    hasCriticalFailure(): boolean;
}
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
export declare class MultiExpertOrchestrator {
    private config;
    private activeHandles;
    constructor(config?: Partial<OrchestratorConfig>);
    /**
     * Execute multiple expert tasks in parallel with robust error handling.
     * Uses OpenClaw's sessions_spawn for actual subagent creation.
     */
    execute(tasks: ExpertTask[]): Promise<{
        results: ExpertResult[];
        summary: ReturnType<ResultAggregator['getSummary']>;
        aborted: boolean;
    }>;
    /**
     * Execute a single expert task with timeout and retry handling.
     * Integrates with OpenClaw's sessions_spawn for subagent creation.
     */
    private executeTask;
    /**
     * Wait for task completion with timeout.
     * Polls the handle status until completion or timeout.
     */
    private waitForCompletion;
    /**
     * Abort all running tasks.
     */
    abortAll(): void;
    private delay;
}
/**
 * Execute multiple expert tasks with default settings.
 */
export declare function executeExperts(tasks: ExpertTask[]): Promise<{
    results: ExpertResult[];
    summary: {
        total: number;
        succeeded: number;
        failed: number;
        timedOut: number;
        totalDurationMs: number;
    };
}>;
/**
 * Build expert tasks for orchestration from a task description and team template.
 */
export declare function buildExpertTasks(taskDescription: string, teamTemplate: string | string[], options?: {
    timeoutMs?: number;
    includePlanner?: boolean;
    includeArchitect?: boolean;
}): ExpertTask[];
export {};
//# sourceMappingURL=multi-expert-orchestrator.d.ts.map