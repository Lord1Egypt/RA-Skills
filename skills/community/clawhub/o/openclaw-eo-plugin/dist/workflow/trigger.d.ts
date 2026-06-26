/**
 * Workflow Trigger
 * Detects when workflows should be invoked
 */
import type { Workflow, TriggerCondition, TriggerType } from './types.js';
export declare class WorkflowTrigger {
    /**
     * Check if a message matches trigger conditions
     */
    static matchesMessage(trigger: TriggerCondition, message: string): boolean;
    /**
     * Check if a tool call matches trigger conditions
     */
    static matchesToolCall(trigger: TriggerCondition, toolName: string): boolean;
    /**
     * Check if trigger type matches
     */
    static matchesType(trigger: TriggerCondition, type: TriggerType): boolean;
    /**
     * Find matching workflows for a given context
     */
    static findMatchingWorkflows(workflows: Workflow[], context: {
        message?: string;
        toolCall?: string;
        type?: TriggerType;
        contextLevel?: string;
    }): Workflow[];
    /**
     * Create a simple keyword trigger
     */
    static keywordTrigger(keywords: string[]): TriggerCondition;
    /**
     * Create a tool call trigger
     */
    static toolTrigger(toolName: string): TriggerCondition;
    /**
     * Create a context level trigger
     */
    static contextLevelTrigger(level: string): TriggerCondition;
}
//# sourceMappingURL=trigger.d.ts.map