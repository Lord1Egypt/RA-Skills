import { type SkillName, type SkillContext } from '../skills/index.js';
export interface ProgressUpdate {
    skillName: SkillName;
    stage: 'initialized' | 'analyzing' | 'executing' | 'finalizing' | 'completed' | 'timeout_wait';
    elapsedMs: number;
    progress: number;
    message: string;
    canExtend: boolean;
}
export interface ExecuteWithProgressOptions {
    skillName: SkillName;
    args: string;
    context: SkillContext;
    /** Base timeout in ms (default: 300000 = 5 minutes) */
    timeoutMs?: number;
    /** Progress report interval in ms (default: 30000 = 30 seconds) */
    progressIntervalMs?: number;
    /** Maximum total wait time including extensions (default: 600000 = 10 minutes) */
    maxTimeoutMs?: number;
    /** Callback for progress updates */
    onProgress?: (update: ProgressUpdate) => void;
    /** Enable chain signal (default: true) */
    enableChainSignal?: boolean;
}
export interface ExecuteResult {
    success: boolean;
    output: string;
    skillName: SkillName;
    durationMs: number;
    expertUsed: string[];
    error?: string;
    timedOut: boolean;
    runId?: string;
}
export interface ChainSignal {
    taskId: string;
    status: 'pending' | 'running' | 'completed' | 'failed';
    stages: Map<string, {
        completed: boolean;
        output?: any;
    }>;
    listeners: Set<(signal: ChainSignal) => void>;
    maxStages: number;
}
export interface ChainTaskOptions {
    taskId: string;
    skillName: SkillName;
    args: string;
    context: SkillContext;
    /** Stages that dependent tasks can hook into */
    stages?: string[];
    /** Timeout for each stage */
    stageTimeoutMs?: number;
}
export declare class ProgressExecutor {
    private activeTasks;
    /**
     * Execute a skill with progress reporting and adaptive timeout
     */
    executeWithProgress(options: ExecuteWithProgressOptions): Promise<ExecuteResult>;
    /**
     * Get status of all active tasks
     */
    getActiveTasks(): Array<{
        taskId: string;
        skillName: SkillName;
        elapsedMs: number;
        status: string;
        lastProgress: number;
    }>;
    /**
     * Check if a task is still running
     */
    isTaskRunning(taskId: string): boolean;
    /**
     * Resolve expert ID to name(s)
     */
    private resolveExpert;
}
export declare class ChainSignalManager {
    private signals;
    private logger;
    /**
     * Create a new chain signal for a task
     */
    createSignal(taskId: string, stages?: string[]): ChainSignal;
    /**
     * Get a chain signal
     */
    getSignal(taskId: string): ChainSignal | undefined;
    /**
     * Update signal stage - call this from the executing task
     */
    updateStage(taskId: string, stageName: string, output?: any): boolean;
    /**
     * Subscribe to signal changes - for dependent tasks
     */
    subscribe(taskId: string, callback: (signal: ChainSignal) => void): () => void;
    /**
     * Wait for a specific stage to complete
     */
    waitForStage(taskId: string, stageName: string, timeoutMs?: number): Promise<{
        completed: boolean;
        output?: any;
    }>;
    /**
     * Clean up completed signals
     */
    cleanup(olderThanMs?: number): void;
}
export declare const progressExecutor: ProgressExecutor;
export declare const chainSignalManager: ChainSignalManager;
/**
 * Execute a skill with standard timeout and progress reporting
 * Simple wrapper for backwards compatibility
 */
export declare function executeWithProgressReporting(options: Omit<ExecuteWithProgressOptions, 'onProgress'> & {
    onProgress?: ExecuteWithProgressOptions['onProgress'];
}): Promise<ExecuteResult>;
/**
 * Create a chain signal and return stage trigger functions
 */
export declare function createChainTask(options: ChainTaskOptions): {
    signal: ChainSignal;
    triggerStage: (stageName: string, output?: any) => boolean;
    waitForStage: (stageName: string, timeoutMs?: number) => Promise<{
        completed: boolean;
        output?: any;
    }>;
};
//# sourceMappingURL=progress-executor.d.ts.map