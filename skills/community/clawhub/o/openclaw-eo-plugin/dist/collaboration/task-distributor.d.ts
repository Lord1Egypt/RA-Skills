import { AgentKnowledgeGraph } from './knowledge-graph.js';
import { AgentCoordinator, AgentInfo } from '../autonomy/agent-coordinator.js';
import { type ChainSignal } from '../workflow/progress-executor.js';
export type TaskPriority = 'low' | 'normal' | 'high' | 'critical';
export type TaskStatus = 'pending' | 'distributing' | 'in_progress' | 'aggregating' | 'completed' | 'failed';
export interface TaskSpec {
    id: string;
    name: string;
    description: string;
    type: 'planning' | 'analysis' | 'implementation' | 'review' | 'research' | 'custom';
    priority: TaskPriority;
    requiredExpertTypes: string[];
    minExperts: number;
    maxExperts: number;
    timeoutMs: number;
    payload: any;
    dependencies?: string[];
    preferredExpertIds?: string[];
    createdAt: number;
    deadline?: number;
}
export interface DistributedTask extends TaskSpec {
    status: TaskStatus;
    assignedExperts: string[];
    pendingExperts: string[];
    completedExperts: string[];
    results: Map<string, TaskResult>;
    progress: number;
    startedAt?: number;
    completedAt?: number;
    error?: string;
}
export interface TaskResult {
    expertId: string;
    expertName: string;
    expertRole: string;
    success: boolean;
    output?: string;
    error?: string;
    confidence: number;
    durationMs: number;
    keyPoints: string[];
    suggestions?: string[];
    timestamp: number;
}
export interface DistributionResult {
    taskId: string;
    success: boolean;
    assignedExperts: AgentInfo[];
    pendingAssignments: string[];
    loadAfterDistribution: Map<string, number>;
    estimatedCompletionMs: number;
}
export interface AggregationConfig {
    method: 'concatenate' | 'weighted' | 'consensus' | 'hierarchical';
    maxOutputLength: number;
    includeConfidences: boolean;
    includeMinorityOpinions: boolean;
}
export interface AggregatedResult {
    taskId: string;
    success: boolean;
    primaryOutput: string;
    expertOutputs: TaskResult[];
    consensus?: {
        level: 'unanimous' | 'strong' | 'majority' | 'plurality';
        agreement: number;
        conflicts?: string[];
    };
    confidence: number;
    recommendations: string[];
    durationMs: number;
    timestamp: number;
}
export declare class TaskDistributor {
    private taskQueue;
    private coordinator;
    private knowledgeGraph;
    private aggregationConfig;
    constructor(coordinator: AgentCoordinator, knowledgeGraph: AgentKnowledgeGraph, aggregationConfig?: Partial<AggregationConfig>);
    /**
     * Submit a new task for distribution.
     */
    submitTask(task: Omit<TaskSpec, 'id' | 'createdAt'>): DistributedTask;
    /**
     * Submit multiple tasks.
     */
    submitTasks(tasks: Omit<TaskSpec, 'id' | 'createdAt'>[]): DistributedTask[];
    /**
     * Submit a task with chain signal stages for dependent task coordination.
     * This allows downstream tasks to start preparation when upstream stages complete.
     *
     * @param task - Task specification
     * @param stages - Array of stage names that dependent tasks can wait on
     * @returns Object with task info and chain signal controls
     */
    submitChainTask(task: Omit<TaskSpec, 'id' | 'createdAt'>, stages?: string[]): {
        distributedTask: DistributedTask;
        chainSignal: ChainSignal;
        triggerStage: (stageName: string, output?: any) => boolean;
        waitForStage: (stageName: string, timeoutMs?: number) => Promise<{
            completed: boolean;
            output?: any;
        }>;
        cleanup: () => void;
    };
    /**
     * Wait for a dependency task to reach a specific stage before proceeding.
     * This enables "partial completion" where dependent tasks can start once a
     * critical stage (e.g., 'analyze') is done, without waiting for full completion.
     *
     * @param dependencyTaskId - The task ID to wait on
     * @param stageName - The stage name to wait for
     * @param timeoutMs - Max time to wait (default: 120000ms)
     * @returns Stage result if completed, or timeout indicator
     */
    waitForDependencyStage(dependencyTaskId: string, stageName: string, timeoutMs?: number): Promise<{
        ready: boolean;
        output?: any;
        timedOut: boolean;
    }>;
    /**
     * Create a dependency chain between tasks where Task B can start its
     * preparation when Task A reaches a specific stage.
     *
     * @param taskA - First task (upstream)
     * @param taskB - Second task (downstream, depends on A)
     * @param unlockStageA - Stage in taskA that unlocks taskB
     * @param stagesA - Stages for taskA's chain signal
     * @returns Both chain task handles
     */
    createDependencyChain(taskA: Omit<TaskSpec, 'id' | 'createdAt'>, taskB: Omit<TaskSpec, 'id' | 'createdAt'>, unlockStageA?: string, stagesA?: string[]): {
        chainA: ReturnType<typeof this.submitChainTask>;
        chainB: ReturnType<typeof this.submitChainTask>;
        unlockTaskB: () => Promise<void>;
    };
    /**
     * Distribute a task to available experts.
     */
    distribute(taskId: string): DistributionResult | null;
    /**
     * Auto-distribute all pending tasks.
     */
    autoDistribute(): DistributionResult[];
    /**
     * Select best experts for a task based on requirements and load.
     */
    private selectExperts;
    /**
     * Calculate how well an agent matches a task (relevance score).
     */
    private matchScore;
    /**
     * Submit a result for a task.
     */
    submitResult(taskId: string, result: Omit<TaskResult, 'timestamp'>): boolean;
    /**
     * Aggregate results from all experts into a final output.
     */
    aggregate(taskId: string): AggregatedResult | null;
    private aggregateConcatenate;
    private aggregateWeighted;
    private aggregateConsensus;
    private aggregateHierarchical;
    private collectRecommendations;
    /**
     * Get task status.
     */
    getTaskStatus(taskId: string): DistributedTask | undefined;
    /**
     * Get all tasks.
     */
    getAllTasks(): DistributedTask[];
    /**
     * Get pending tasks count.
     */
    getPendingCount(): number;
    /**
     * Get in-progress tasks count.
     */
    getInProgressCount(): number;
    /**
     * Cancel a task.
     */
    cancel(taskId: string): boolean;
}
export declare const taskDistributor: TaskDistributor;
export default TaskDistributor;
//# sourceMappingURL=task-distributor.d.ts.map