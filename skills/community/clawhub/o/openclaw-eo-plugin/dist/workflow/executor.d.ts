/**
 * Workflow Executor
 * Executes workflows step by step with support for parallel, conditional, and loop steps
 */
import type { OpenClawPluginApi } from 'openclaw/plugin-sdk';
import type { Workflow, WorkflowExecution } from './types.js';
export declare class WorkflowExecutor {
    private api;
    private currentExecution?;
    private stepTimeouts;
    constructor(api: OpenClawPluginApi);
    /**
     * Start executing a workflow
     */
    execute(workflow: Workflow): Promise<WorkflowExecution>;
    /**
     * Execute a single step
     */
    private executeStep;
    /**
     * Execute an expert step
     */
    private executeExpertStep;
    /**
     * Execute a tool step
     */
    private executeToolStep;
    /**
     * Execute a condition step
     */
    private executeConditionStep;
    /**
     * Execute a loop step
     */
    private executeLoopStep;
    /**
     * Format output step
     */
    private formatOutput;
    /**
     * Get current execution status
     */
    getCurrentExecution(): WorkflowExecution | undefined;
    /**
     * Cancel current execution
     */
    cancel(): void;
}
//# sourceMappingURL=executor.d.ts.map