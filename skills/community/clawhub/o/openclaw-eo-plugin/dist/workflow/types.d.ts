/**
 * Workflow Module Types
 * Type definitions for workflow orchestration engine
 */
export interface Workflow {
    id: string;
    name: string;
    description?: string;
    steps: WorkflowStep[];
    trigger?: TriggerCondition;
    context: Record<string, any>;
    status: WorkflowStatus;
    createdAt: number;
    updatedAt?: number;
    currentStepIndex?: number;
}
export type WorkflowStatus = 'idle' | 'running' | 'paused' | 'completed' | 'failed' | 'cancelled';
export interface WorkflowStep {
    id: string;
    name: string;
    type: StepType;
    config: StepConfig;
    next?: string;
    onError?: string;
    parallelGroup?: string;
}
export type StepType = 'expert' | 'tool' | 'condition' | 'loop' | 'input' | 'output';
export interface StepConfig {
    expertId?: string;
    expertRole?: string;
    prompt?: string;
    toolName?: string;
    toolParams?: Record<string, any>;
    condition?: string;
    conditionFn?: string;
    loopItems?: any[];
    loopVar?: string;
    loopMaxIterations?: number;
    timeoutMs?: number;
    retryCount?: number;
}
export interface TriggerCondition {
    type: TriggerType;
    pattern?: string;
    keywords?: string[];
    toolCall?: string;
    schedule?: string;
    custom?: string;
}
export type TriggerType = 'message' | 'tool_call' | 'schedule' | 'manual' | 'context_level';
export interface WorkflowExecution {
    workflowId: string;
    stepResults: StepResult[];
    status: WorkflowStatus;
    startedAt: number;
    completedAt?: number;
    error?: string;
    context: Record<string, any>;
}
export interface StepResult {
    stepId: string;
    success: boolean;
    output?: any;
    error?: string;
    durationMs: number;
    timestamp: number;
}
export interface WorkflowInstance {
    workflow: Workflow;
    execution: WorkflowExecution;
}
/**
 * Preset Workflow Templates
 */
export interface PresetWorkflowTemplate {
    id: string;
    name: string;
    description: string;
    steps: Omit<WorkflowStep, 'id'>[];
    trigger?: TriggerCondition;
}
//# sourceMappingURL=types.d.ts.map