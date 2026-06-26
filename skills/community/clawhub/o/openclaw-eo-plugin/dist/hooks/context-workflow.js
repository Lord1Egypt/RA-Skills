/**
 * Context Management Hook
 * on_message hook that monitors context usage and triggers workflows
 */
import { ContextManager } from '../context/manager.js';
import { WorkflowTrigger } from '../workflow/trigger.js';
import { createWorkflowFromPreset, PRESET_WORKFLOWS } from '../workflow/presets.js';
import { WorkflowExecutor } from '../workflow/executor.js';
let contextManager = null;
let workflowExecutor = null;
let activeWorkflows = new Map();
export function initContextWorkflowHooks(api) {
    contextManager = new ContextManager(api, {
        monitor: {
            thresholds: { warning: 70, compress: 85, critical: 95 },
            checkIntervalMs: 60000,
            reportIntervalMs: 300000,
        },
    });
    workflowExecutor = new WorkflowExecutor(api);
    api.logger.info('[EO ContextWorkflow] Context and workflow hooks initialized');
}
/**
 * on_message hook handler
 * 1. Detect workflow triggers
 * 2. Check context usage
 * 3. Trigger summarization if needed
 */
// Performance optimization: throttle expensive operations
let lastProcessTime = 0;
const PROCESS_INTERVAL_MS = 5000; // Only process context every 5 seconds
let lastWorkflowCheck = 0;
const WORKFLOW_CHECK_INTERVAL_MS = 10000; // Only check workflows every 10 seconds
export async function onMessageHook(api, event) {
    if (!contextManager || !workflowExecutor) {
        initContextWorkflowHooks(api);
    }
    const now = Date.now();
    const message = event?.context?.message || event?.context?.content || '';
    // Check context state periodically (not every message)
    if (now - lastProcessTime > PROCESS_INTERVAL_MS) {
        lastProcessTime = now;
        try {
            const contextState = await contextManager.process();
            // If context is getting high, log warning
            if (contextState.level !== 'normal') {
                api.logger.info(`[EO ContextWorkflow] Context level: ${contextState.level} ` +
                    `(${contextState.metrics.usagePercent.toFixed(1)}%)`);
            }
        }
        catch (e) {
            api.logger.warn(`[EO ContextWorkflow] Context process error: ${e}`);
        }
    }
    // Check for workflow triggers periodically (not every message)
    if (now - lastWorkflowCheck > WORKFLOW_CHECK_INTERVAL_MS) {
        lastWorkflowCheck = now;
        // Check for workflow triggers
        const matchingWorkflows = WorkflowTrigger.findMatchingWorkflows(PRESET_WORKFLOWS.map(p => createWorkflowFromPreset(p.id, {})).filter(Boolean), { message, type: 'message' });
        // Auto-trigger first matching workflow (only if no active workflows)
        if (matchingWorkflows.length > 0 && activeWorkflows.size === 0) {
            const workflow = matchingWorkflows[0];
            api.logger.info(`[EO ContextWorkflow] Triggering workflow: ${workflow.name}`);
            activeWorkflows.set(workflow.id, workflow);
            try {
                const execution = await workflowExecutor.execute(workflow);
                activeWorkflows.delete(workflow.id);
                if (execution.status === 'completed') {
                    api.logger.info(`[EO ContextWorkflow] Workflow ${workflow.name} completed successfully`);
                }
                else {
                    api.logger.warn(`[EO ContextWorkflow] Workflow ${workflow.name} ${execution.status}`);
                }
            }
            catch (e) {
                activeWorkflows.delete(workflow.id);
                api.logger.warn(`[EO ContextWorkflow] Workflow execution error: ${e}`);
            }
        }
    }
}
/**
 * after_tool_call hook handler
 * 1. Check context changes
 * 2. Update workflow state
 * 3. Decide next steps
 */
export async function afterToolCallHook(api, event) {
    if (!contextManager || !workflowExecutor)
        return;
    const toolName = event?.toolName || '';
    // Log tool call for context tracking
    if (toolName.startsWith('eo_')) {
        api.logger.debug(`[EO ContextWorkflow] EO tool called: ${toolName}`);
    }
    // Check if any active workflow needs this tool result
    for (const [workflowId, workflow] of activeWorkflows) {
        const currentStep = workflow.steps[workflow.currentStepIndex];
        if (currentStep?.config?.toolName === toolName) {
            api.logger.debug(`[EO ContextWorkflow] Tool ${toolName} used by workflow ${workflowId}`);
        }
    }
}
/**
 * Get context manager for external access
 */
export function getContextManager() {
    return contextManager;
}
/**
 * Get active workflows
 */
export function getActiveWorkflows() {
    return activeWorkflows;
}
//# sourceMappingURL=context-workflow.js.map