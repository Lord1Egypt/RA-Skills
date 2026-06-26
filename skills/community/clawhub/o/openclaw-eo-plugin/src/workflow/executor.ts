/**
 * Workflow Executor
 * Executes workflows step by step with support for parallel, conditional, and loop steps
 */

import type { OpenClawPluginApi } from 'openclaw/plugin-sdk'
import type { Workflow, WorkflowStep, WorkflowExecution, StepResult, StepType } from './types.js'

export class WorkflowExecutor {
  private api: OpenClawPluginApi
  private currentExecution?: WorkflowExecution
  private stepTimeouts: Map<string, NodeJS.Timeout> = new Map()

  constructor(api: OpenClawPluginApi) {
    this.api = api
  }

  /**
   * Start executing a workflow
   */
  async execute(workflow: Workflow): Promise<WorkflowExecution> {
    this.api.logger.info(`[WorkflowExecutor] Starting workflow: ${workflow.name} (${workflow.id})`)

    workflow.status = 'running'
    workflow.currentStepIndex = 0

    const execution: WorkflowExecution = {
      workflowId: workflow.id,
      stepResults: [],
      status: 'running',
      startedAt: Date.now(),
      context: { ...workflow.context },
    }

    this.currentExecution = execution

    try {
      // Execute steps sequentially (parallel execution handled within steps)
      for (let i = 0; i < workflow.steps.length; i++) {
        workflow.currentStepIndex = i
        const step = workflow.steps[i]

        this.api.logger.debug(`[WorkflowExecutor] Executing step: ${step.name} (${step.type})`)

        const result = await this.executeStep(step, execution.context)
        execution.stepResults.push(result)

        if (!result.success) {
          // Handle error - go to error step or fail
          if (step.onError) {
            const errorStep = workflow.steps.find(s => s.id === step.onError)
            if (errorStep) {
              const errorResult = await this.executeStep(errorStep, execution.context)
              execution.stepResults.push(errorResult)
            }
          } else {
            execution.status = 'failed'
            execution.error = `Step ${step.id} failed: ${result.error}`
            workflow.status = 'failed'
            break
          }
        }

        // Check if workflow should end early
        if (result.output === 'end' || step.next === 'end') {
          break
        }
      }

      // Check if all steps completed successfully
      if (execution.status === 'running') {
        const allSuccess = execution.stepResults.every(r => r.success)
        execution.status = allSuccess ? 'completed' : 'failed'
        workflow.status = execution.status
      }

    } catch (error) {
      execution.status = 'failed'
      execution.error = error instanceof Error ? error.message : String(error)
      workflow.status = 'failed'
      this.api.logger.error(`[WorkflowExecutor] Workflow failed: ${execution.error}`)
    }

    execution.completedAt = Date.now()
    this.currentExecution = undefined

    this.api.logger.info(
      `[WorkflowExecutor] Workflow ${workflow.name} ${execution.status} ` +
      `(${execution.completedAt - execution.startedAt}ms)`
    )

    return execution
  }

  /**
   * Execute a single step
   */
  private async executeStep(
    step: WorkflowStep,
    context: Record<string, any>
  ): Promise<StepResult> {
    const startTime = Date.now()

    try {
      let output: any

      switch (step.type) {
        case 'expert':
          output = await this.executeExpertStep(step, context)
          break
        case 'tool':
          output = await this.executeToolStep(step, context)
          break
        case 'condition':
          output = await this.executeConditionStep(step, context)
          break
        case 'loop':
          output = await this.executeLoopStep(step, context)
          break
        case 'input':
          output = context.pendingInput
          break
        case 'output':
          output = this.formatOutput(step, context)
          break
        default:
          output = `Unknown step type: ${step.type}`
      }

      return {
        stepId: step.id,
        success: true,
        output,
        durationMs: Date.now() - startTime,
        timestamp: Date.now(),
      }

    } catch (error) {
      return {
        stepId: step.id,
        success: false,
        error: error instanceof Error ? error.message : String(error),
        durationMs: Date.now() - startTime,
        timestamp: Date.now(),
      }
    }
  }

  /**
   * Execute an expert step
   */
  private async executeExpertStep(
    step: WorkflowStep,
    context: Record<string, any>
  ): Promise<string> {
    const { expertRole, prompt } = step.config
    if (!prompt) return 'No prompt specified'

    // In a full implementation, this would invoke the expert library
    // For now, simulate expert execution
    this.api.logger.debug(`[WorkflowExecutor] Invoking expert: ${expertRole}`)

    // Store in context for other steps to use
    context[`${step.id}_output`] = `[Expert: ${expertRole}] ${prompt}`

    return `[Expert: ${expertRole}] Task completed`
  }

  /**
   * Execute a tool step
   */
  private async executeToolStep(
    step: WorkflowStep,
    context: Record<string, any>
  ): Promise<string> {
    const { toolName, toolParams } = step.config
    if (!toolName) return 'No tool specified'

    this.api.logger.debug(`[WorkflowExecutor] Calling tool: ${toolName}`)

    // In a full implementation, this would call the actual tool
    // For now, simulate tool execution
    context[`${step.id}_output`] = `[Tool: ${toolName}] Executed with params: ${JSON.stringify(toolParams || {})}`

    return `[Tool: ${toolName}] Completed`
  }

  /**
   * Execute a condition step
   */
  private async executeConditionStep(
    step: WorkflowStep,
    context: Record<string, any>
  ): Promise<string> {
    const { condition } = step.config
    if (!condition) return 'no_condition'

    // Simple condition evaluation
    // In production, this would be more sophisticated
    this.api.logger.debug(`[WorkflowExecutor] Evaluating condition: ${condition}`)

    // Default: proceed to next step
    context[`${step.id}_result`] = true
    return 'proceed'
  }

  /**
   * Execute a loop step
   */
  private async executeLoopStep(
    step: WorkflowStep,
    context: Record<string, any>
  ): Promise<string> {
    const { loopItems, loopVar, loopMaxIterations } = step.config
    if (!loopItems || !Array.isArray(loopItems)) {
      return 'no_loop_items'
    }

    const maxIter = loopMaxIterations || loopItems.length
    const items = loopItems.slice(0, maxIter)

    this.api.logger.debug(`[WorkflowExecutor] Looping over ${items.length} items`)

    let iteration = 0
    for (const item of items) {
      if (loopVar) {
        context[loopVar] = item
      }
      iteration++
      this.api.logger.debug(`[WorkflowExecutor] Loop iteration ${iteration}/${items.length}`)
    }

    context[`${step.id}_iterations`] = iteration
    return `completed_${iteration}_iterations`
  }

  /**
   * Format output step
   */
  private formatOutput(
    step: WorkflowStep,
    context: Record<string, any>
  ): string {
    const { prompt } = step.config
    if (!prompt) return 'Output step completed'

    // Gather outputs from previous steps
    const outputs = Object.entries(context)
      .filter(([k]) => k.endsWith('_output'))
      .map(([k, v]) => `${k}: ${v}`)
      .join('\n')

    return `Output: ${prompt}\n\n${outputs}`
  }

  /**
   * Get current execution status
   */
  getCurrentExecution(): WorkflowExecution | undefined {
    return this.currentExecution
  }

  /**
   * Cancel current execution
   */
  cancel(): void {
    if (this.currentExecution) {
      this.currentExecution.status = 'cancelled'
      this.api.logger.warn('[WorkflowExecutor] Workflow cancelled')
    }

    // Clear all pending timeouts
    for (const timeout of this.stepTimeouts.values()) {
      clearTimeout(timeout)
    }
    this.stepTimeouts.clear()
  }
}
