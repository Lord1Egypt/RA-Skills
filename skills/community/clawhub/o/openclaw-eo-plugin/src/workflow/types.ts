/**
 * Workflow Module Types
 * Type definitions for workflow orchestration engine
 */

export interface Workflow {
  id: string
  name: string
  description?: string
  steps: WorkflowStep[]
  trigger?: TriggerCondition
  context: Record<string, any>
  status: WorkflowStatus
  createdAt: number
  updatedAt?: number
  currentStepIndex?: number
}

export type WorkflowStatus = 'idle' | 'running' | 'paused' | 'completed' | 'failed' | 'cancelled'

export interface WorkflowStep {
  id: string
  name: string
  type: StepType
  config: StepConfig
  next?: string           // Next step ID or 'end'
  onError?: string        // Error handling step ID
  parallelGroup?: string  // For parallel execution grouping
}

export type StepType = 'expert' | 'tool' | 'condition' | 'loop' | 'input' | 'output'

export interface StepConfig {
  // For expert type
  expertId?: string
  expertRole?: string
  prompt?: string

  // For tool type
  toolName?: string
  toolParams?: Record<string, any>

  // For condition type
  condition?: string
  conditionFn?: string  // JS expression

  // For loop type
  loopItems?: any[]
  loopVar?: string
  loopMaxIterations?: number

  // Common
  timeoutMs?: number
  retryCount?: number
}

export interface TriggerCondition {
  type: TriggerType
  pattern?: string      // Regex pattern for message matching
  keywords?: string[]   // Keywords that trigger this workflow
  toolCall?: string     // Tool call that triggers
  schedule?: string     // Cron expression
  custom?: string       // Custom trigger function name
}

export type TriggerType = 'message' | 'tool_call' | 'schedule' | 'manual' | 'context_level'

export interface WorkflowExecution {
  workflowId: string
  stepResults: StepResult[]
  status: WorkflowStatus
  startedAt: number
  completedAt?: number
  error?: string
  context: Record<string, any>
}

export interface StepResult {
  stepId: string
  success: boolean
  output?: any
  error?: string
  durationMs: number
  timestamp: number
}

export interface WorkflowInstance {
  workflow: Workflow
  execution: WorkflowExecution
}

/**
 * Preset Workflow Templates
 */
export interface PresetWorkflowTemplate {
  id: string
  name: string
  description: string
  steps: Omit<WorkflowStep, 'id'>[]
  trigger?: TriggerCondition
}
