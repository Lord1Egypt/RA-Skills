import type { ExpertResult } from '../types/index.js';
export interface PlanSkillInput {
    task: string;
    team?: string[];
    constraints?: string[];
    priority?: 'low' | 'medium' | 'high';
    template?: string;
}
export interface PlanSkillContext {
    runtime: {
        subagent: {
            run: (params: {
                sessionKey: string;
                message: string;
                extraSystemPrompt?: string;
                provider?: string;
                model?: string;
            }) => Promise<{
                runId: string;
            }>;
            waitForRun: (params: {
                runId: string;
                timeoutMs?: number;
            }) => Promise<{
                status: string;
                error?: string;
            }>;
            getSessionMessages: (params: {
                sessionKey: string;
                limit?: number;
            }) => Promise<{
                messages: unknown[];
            }>;
        };
    };
    logger: {
        info: (msg: string) => void;
        warn: (msg: string) => void;
        error: (msg: string) => void;
    };
    sessionId?: string;
}
export interface PlanSkillResult {
    success: boolean;
    output: string;
    expertResults: ExpertResult[];
    durationMs: number;
    wbs?: WBSMilestone[];
    error?: string;
}
export interface WBSMilestone {
    id: string;
    name: string;
    tasks: WBSTask[];
    status: 'pending' | 'in_progress' | 'completed' | 'failed';
    completion: number;
}
export interface WBSTask {
    id: string;
    name: string;
    estimatedHours?: number;
    assignee?: string;
    dependencies?: string[];
    priority?: 'low' | 'medium' | 'high';
}
export declare const planSkill: {
    name: string;
    description: string;
    expert: string;
    role: string;
    /**
     * Execute the plan skill
     * 1. Parse input arguments
     * 2. Generate WBS structure
     * 3. Invoke planner + engineer + qa experts via subagent
     * 4. Return structured plan result
     */
    execute(args: string, context: PlanSkillContext): Promise<PlanSkillResult>;
};
//# sourceMappingURL=plan-skill.d.ts.map