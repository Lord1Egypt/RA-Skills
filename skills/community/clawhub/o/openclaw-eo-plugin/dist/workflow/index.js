/**
 * Workflow Module - Workflow Orchestration Engine
 *
 * Features:
 * - Workflow definition and management
 * - Step-by-step execution with parallel support
 * - Trigger-based workflow invocation
 * - Preset workflow templates
 * - Conditional branching and loops
 */
export * from './types.js';
export { WorkflowTrigger } from './trigger.js';
export { WorkflowExecutor } from './executor.js';
export { PRESET_WORKFLOWS, createWorkflowFromPreset, getPresetIds, getPresetById, } from './presets.js';
//# sourceMappingURL=index.js.map