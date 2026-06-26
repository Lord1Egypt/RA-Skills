/**
 * Multi-Expert Trigger Rules - 强制多专家协作触发引擎
 *
 * 核心原则：满足以下条件的任务必须强制触发多专家协作
 *
 * 触发条件：
 * 1. 任务涉及多个专业领域（frontend + backend + db等）
 * 2. 任务预估时间超过15分钟
 * 3. 任务包含"复杂"关键词
 * 4. 任务涉及安全/架构/性能关键决策
 * 5. 用户明确要求"多专家"或"团队协作"
 */
export type ExpertType = 'architect' | 'planner' | 'frontend' | 'backend' | 'qa' | 'security' | 'devops' | 'codeReviewer';
export interface TriggerRule {
    id: string;
    name: string;
    description: string;
    condition: (task: string, context?: TriggerContext) => boolean;
    requiredExperts: ExpertType[];
    minTaskDurationMinutes?: number;
    priority: 'required' | 'recommended' | 'optional';
}
export interface TriggerContext {
    taskDescription: string;
    language?: string;
    framework?: string;
    codebasePath?: string;
    estimatedMinutes?: number;
    domains?: string[];
}
export interface TriggerResult {
    shouldTrigger: boolean;
    reason: string;
    priority: 'required' | 'recommended' | 'optional';
    suggestedExperts: ExpertType[];
    alternativeTrigger?: string;
}
/**
 * Multi-Expert Trigger Engine
 */
export declare class MultiExpertTriggerEngine {
    private rules;
    constructor();
    /**
     * Initialize default trigger rules
     */
    private initializeRules;
    /**
     * Check if task should trigger multi-expert collaboration
     */
    check(task: string, context?: TriggerContext): TriggerResult;
    /**
     * Get the trigger command based on required experts
     */
    private getTriggerCommand;
    /**
     * Add custom rule
     */
    addRule(rule: Omit<TriggerRule, 'id'>): void;
    /**
     * Get all rules
     */
    getRules(): TriggerRule[];
    /**
     * Detect domains from task description
     */
    static detectDomains(task: string): string[];
}
export declare const multiExpertTrigger: MultiExpertTriggerEngine;
//# sourceMappingURL=multi-expert-trigger.d.ts.map