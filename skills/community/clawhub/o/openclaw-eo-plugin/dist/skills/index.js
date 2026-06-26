// ============================================================================
// EO Skills Registry - Central registration for all .ts Skills
// ============================================================================
import { planSkill } from './plan-skill.js';
import { architectSkill } from './architect-skill.js';
import { verifySkill } from './verify-skill.js';
import { codeReviewSkill } from './code-review-skill.js';
// Task decomposition and multi-expert trigger
import { TaskDecomposer, taskDecomposer } from './task-decomposer.js';
import { MultiExpertTriggerEngine, multiExpertTrigger } from './multi-expert-trigger.js';
// ---------------------------------------------------------------------------
// Registered Skills
// ---------------------------------------------------------------------------
export const skills = {
    plan: planSkill,
    architect: architectSkill,
    verify: verifySkill,
    'code-review': codeReviewSkill,
};
export const SKILL_NAMES = ['plan', 'architect', 'verify', 'code-review'];
// ---------------------------------------------------------------------------
// Skill Metadata
// ---------------------------------------------------------------------------
export const SKILL_META = {
    plan: {
        description: 'Create a structured project plan with WBS, milestones, and expert team analysis',
        expert: 'planner',
        icon: '📋',
    },
    architect: {
        description: 'Design system architecture with technology stack, modules, and risk assessment',
        expert: 'architect',
        icon: '🏗️',
    },
    verify: {
        description: 'Verify implementation against specifications using checkpoint-based validation',
        expert: 'qa',
        icon: '✅',
    },
    'code-review': {
        description: 'Review code for quality, security, and best practices using multiple expert perspectives',
        expert: 'reviewer',
        icon: '🔍',
    },
};
export { TaskDecomposer, taskDecomposer };
export { MultiExpertTriggerEngine, multiExpertTrigger };
// ---------------------------------------------------------------------------
// Phase 5: Trinity Orchestrator - EO + Hermes + Claude Code
// ----------------------------------------------------------------------------
// Skill Generator (Hermes-style auto-skill generation)
export { SkillGenerator, skillGenerator } from './skill-generator.js';
// Trinity Orchestrator (Three-layer fusion)
export { TrinityOrchestrator, trinityOrchestrator } from './trinity-orchestrator.js';
// ---------------------------------------------------------------------------
// Utility Functions
// ---------------------------------------------------------------------------
/**
 * Get a skill by name
 */
export function getSkill(name) {
    return skills[name];
}
/**
 * List all registered skill names
 */
export function listSkillNames() {
    return [...SKILL_NAMES];
}
/**
 * Get skill metadata
 */
export function getSkillMeta(name) {
    return SKILL_META[name];
}
/**
 * Check if a skill name is registered
 */
export function hasSkill(name) {
    return name in skills;
}
//# sourceMappingURL=index.js.map