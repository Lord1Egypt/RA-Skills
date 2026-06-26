// ============================================================================
// EO Skill Executor - Unified skill invocation interface
// ============================================================================
import { skills } from './index.js';
import { EXPERTS } from '../experts/data.js';
import { executeWithProgressReporting } from '../workflow/progress-executor.js';
import { logger } from '../utils/logger.js';
// ---------------------------------------------------------------------------
// Default Logger
// ---------------------------------------------------------------------------
function createDefaultLogger() {
    return {
        info: (msg) => logger.info(`[skill-executor] INFO: ${msg}`),
        warn: (msg) => console.warn(`[skill-executor] WARN: ${msg}`),
        error: (msg) => console.error(`[skill-executor] ERROR: ${msg}`),
    };
}
// ---------------------------------------------------------------------------
// Core Executor Function
// ---------------------------------------------------------------------------
/**
 * Execute a skill by name with the given arguments and context.
 *
 * Core logic:
 * 1. Validate skill exists in registry
 * 2. Resolve expert from skill definition
 * 3. For long tasks (timeout >= 180000ms): use progress reporting
 * 4. For short tasks: use simple Promise.race timeout
 * 5. Return structured result with timing and expert info
 */
export async function executeSkill(options) {
    const { skillName, args, context, timeoutMs = 300000, useProgressReporting, progressIntervalMs = 30000, onProgress } = options;
    const logger = context.logger ?? createDefaultLogger();
    const startTime = Date.now();
    // Auto-enable progress reporting for long tasks
    const shouldUseProgress = useProgressReporting ?? (timeoutMs >= 180000);
    // 1. Validate skill
    const skill = skills[skillName];
    if (!skill) {
        return {
            success: false,
            output: '',
            skillName,
            durationMs: Date.now() - startTime,
            expertUsed: [],
            error: `Skill not found: ${skillName}. Available: ${Object.keys(skills).join(', ')}`,
        };
    }
    logger.info(`[execute-skill] Running skill="${skillName}" args="${args.slice(0, 50)}..." timeoutMs=${timeoutMs} progressReporting=${shouldUseProgress}`);
    try {
        // 2. Build execution context
        const execContext = {
            runtime: context.runtime,
            logger,
            sessionId: context.sessionId,
        };
        let result;
        if (shouldUseProgress) {
            // 3a. Execute with progress reporting for long tasks
            const progressResult = await executeWithProgressReporting({
                skillName,
                args,
                context: execContext,
                timeoutMs,
                progressIntervalMs,
                maxTimeoutMs: timeoutMs * 2, // Allow up to 2x for adaptive extensions
                onProgress: onProgress ?? ((update) => {
                    logger.info(`[execute-skill] Progress: ${update.stage} - ${update.message}`);
                }),
            });
            return {
                success: progressResult.success,
                output: progressResult.output,
                skillName: progressResult.skillName,
                durationMs: progressResult.durationMs,
                expertUsed: progressResult.expertUsed,
                error: progressResult.error,
            };
        }
        else {
            // 3b. Execute with simple timeout for short tasks
            result = await Promise.race([
                skill.execute(args, execContext),
                new Promise((_, reject) => setTimeout(() => reject(new Error(`Skill "${skillName}" timed out after ${timeoutMs}ms`)), timeoutMs)),
            ]);
        }
        // 4. Resolve expert used
        const expertUsed = resolveExpert(skill.expert);
        const output = typeof result === 'string' ? result : result.output ?? '';
        const success = typeof result === 'string' ? true : result.success !== false;
        logger.info(`[execute-skill] Completed skill="${skillName}" success=${success} durationMs=${Date.now() - startTime}`);
        return {
            success,
            output,
            skillName,
            durationMs: Date.now() - startTime,
            expertUsed,
        };
    }
    catch (err) {
        const errorMsg = err instanceof Error ? err.message : String(err);
        logger.error(`[execute-skill] Failed skill="${skillName}" error="${errorMsg}"`);
        return {
            success: false,
            output: '',
            skillName,
            durationMs: Date.now() - startTime,
            expertUsed: [skill.expert],
            error: errorMsg,
        };
    }
}
// ---------------------------------------------------------------------------
// Batch Executor
// ---------------------------------------------------------------------------
/**
 * Execute multiple skills in parallel and aggregate results.
 */
export async function executeSkillsBatch(requests, context) {
    return Promise.all(requests.map(req => executeSkill({
        ...req,
        context,
    })));
}
// ---------------------------------------------------------------------------
// Skill Router - Direct command-like invocation
// ---------------------------------------------------------------------------
/**
 * Simple command router that executes a skill by name with string args.
 * Convenience wrapper for command-style invocations.
 */
export async function routeSkillCommand(command, args, context) {
    const skillName = command.toLowerCase();
    if (!hasSkill(skillName)) {
        const available = Object.keys(skills);
        return `Unknown command: ${command}\n\nAvailable skills:\n${available
            .map(name => {
            const s = skills[name];
            return `- /${name}: ${s.description}`;
        })
            .join('\n')}`;
    }
    const result = await executeSkill({ skillName, args, context });
    if (!result.success) {
        return `❌ Skill "${skillName}" failed: ${result.error}\n\nOutput:\n${result.output}`;
    }
    return result.output;
}
// ---------------------------------------------------------------------------
// Helper Functions
// ---------------------------------------------------------------------------
function resolveExpert(expertId) {
    // Check if it's a role key in EXPERTS
    const expert = EXPERTS[expertId];
    if (expert)
        return [expert.name];
    // Check if it's a role category (architect, planner, etc.)
    const roleKey = expertId.toLowerCase();
    const matchingExperts = Object.values(EXPERTS).filter(e => e.role === roleKey);
    if (matchingExperts.length > 0) {
        return matchingExperts.map(e => e.name);
    }
    return [expertId];
}
function hasSkill(name) {
    return name in skills;
}
//# sourceMappingURL=executor.js.map