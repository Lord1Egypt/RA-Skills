/**
 * Preset Workflow Templates
 * Pre-defined workflows for common scenarios
 */
import type { PresetWorkflowTemplate, Workflow } from './types.js';
/**
 * Preset Workflow Templates
 */
export declare const PRESET_WORKFLOWS: PresetWorkflowTemplate[];
/**
 * Create a workflow instance from a preset template
 */
export declare function createWorkflowFromPreset(presetId: string, context?: Record<string, any>): Workflow | null;
/**
 * Get all preset workflow IDs
 */
export declare function getPresetIds(): string[];
/**
 * Get preset by ID
 */
export declare function getPresetById(id: string): PresetWorkflowTemplate | undefined;
//# sourceMappingURL=presets.d.ts.map