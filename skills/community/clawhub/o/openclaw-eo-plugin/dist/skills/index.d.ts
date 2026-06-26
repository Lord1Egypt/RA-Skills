import { type PlanSkillContext, type PlanSkillResult } from './plan-skill.js';
import { type ArchitectSkillContext, type ArchitectSkillResult } from './architect-skill.js';
import { type VerifySkillContext, type VerifySkillResult } from './verify-skill.js';
import { type CodeReviewSkillContext, type CodeReviewSkillResult } from './code-review-skill.js';
import { TaskDecomposer, taskDecomposer, type DecomposedTask, type TaskDecomposition } from './task-decomposer.js';
import { MultiExpertTriggerEngine, multiExpertTrigger, type TriggerRule, type TriggerContext, type TriggerResult, type ExpertType } from './multi-expert-trigger.js';
export interface EOSkill {
    name: string;
    description: string;
    expert: string;
    role: string;
    execute(args: string, context: SkillContext): Promise<SkillResult>;
}
export interface SkillContext {
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
export interface SkillResult {
    success: boolean;
    output: string;
    durationMs: number;
    error?: string;
}
export declare const skills: Record<string, EOSkill>;
export type SkillName = keyof typeof skills;
export declare const SKILL_NAMES: readonly SkillName[];
export declare const SKILL_META: Record<SkillName, {
    description: string;
    expert: string;
    icon: string;
}>;
export type { PlanSkillContext, PlanSkillResult };
export type { ArchitectSkillContext, ArchitectSkillResult };
export type { VerifySkillContext, VerifySkillResult };
export type { CodeReviewSkillContext, CodeReviewSkillResult };
export type { DecomposedTask, TaskDecomposition };
export { TaskDecomposer, taskDecomposer };
export type { TriggerRule, TriggerContext, TriggerResult, ExpertType };
export { MultiExpertTriggerEngine, multiExpertTrigger };
export { SkillGenerator, skillGenerator, type SkillTemplate, type SkillStep, type GeneratedSkill, type SkillGenerationRequest, type SkillFusionResult } from './skill-generator.js';
export { TrinityOrchestrator, trinityOrchestrator, type TrinityLayer, type TrinityConfig, type TrinityTask, type TrinityResult, type LayerResult, type RoutingDecision } from './trinity-orchestrator.js';
/**
 * Get a skill by name
 */
export declare function getSkill(name: SkillName): EOSkill | undefined;
/**
 * List all registered skill names
 */
export declare function listSkillNames(): SkillName[];
/**
 * Get skill metadata
 */
export declare function getSkillMeta(name: SkillName): {
    description: string;
    expert: string;
    icon: string;
};
/**
 * Check if a skill name is registered
 */
export declare function hasSkill(name: string): name is SkillName;
//# sourceMappingURL=index.d.ts.map