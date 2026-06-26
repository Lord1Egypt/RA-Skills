// ============================================================================
// EO /verify Command Implementation
// ============================================================================
import { teamManager } from '../collaboration/team-manager.js';
import { sessionManager } from '../collaboration/session-manager.js';
import { buildExpertPrompt, aggregateExpertResults } from '../adapter/skill-adapter.js';
/**
 * Expert mapping by verification type
 */
const VERIFY_TYPE_EXPERTS = {
    'code': ['qa', 'code-reviewer'],
    'architecture': ['architect', 'tech-lead'],
    'test': ['qa', 'sdet'],
    'security': ['security-engineer', 'security-auditor'],
    'performance': ['performance-engineer', 'sre'],
};
/**
 * Execute the /verify command
 *
 * Verifies implementation against specifications using appropriate experts.
 */
export async function executeVerify(options, ctx) {
    const startTime = Date.now();
    const { target, type, criteria = [], context = {} } = options;
    const logger = ctx.logger;
    logger.info(`[EO/verify] Starting ${type} verification for: ${target.slice(0, 50)}...`);
    try {
        // 1. Create session
        const session = sessionManager.createSession(`verify:${type}:${target}`, context);
        // 2. Get verification experts
        const expertIds = VERIFY_TYPE_EXPERTS[type] ?? VERIFY_TYPE_EXPERTS['code'];
        const expertTeam = teamManager.assembleTeam(target, expertIds);
        sessionManager.addTeamToSession(session.id, expertTeam);
        logger.info(`[EO/verify] Team assembled: ${expertTeam.experts.map(e => e.name).join(', ')}`);
        // 3. Build verification prompts
        const criteriaStr = criteria.length > 0 ? `\n\nVerification Criteria:\n${criteria.map(c => `- ${c}`).join('\n')}` : '';
        const expertPrompts = {
            'qa': buildExpertPrompt('qa', 'QA Engineer', `Verify the following ${type} implementation:\n\nTarget: ${target}${criteriaStr}`, context),
            'code-reviewer': buildExpertPrompt('code-reviewer', 'Code Reviewer', `Review code quality and correctness for:\n\n${target}${criteriaStr}`, context),
            'security-engineer': buildExpertPrompt('security-engineer', 'Security Engineer', `Perform security verification for:\n\n${target}${criteriaStr}`, context),
            'performance-engineer': buildExpertPrompt('performance-engineer', 'Performance Engineer', `Verify performance characteristics for:\n\n${target}${criteriaStr}`, context),
        };
        // 4. Run verification in parallel
        const results = await Promise.all(expertTeam.experts.map(async (expert) => {
            const prompt = expertPrompts[expert.id] ?? expertPrompts['qa'];
            const expertStart = Date.now();
            try {
                const runResult = await ctx.runtime.subagent.run({
                    sessionKey: ctx.sessionId ?? session.id,
                    message: prompt,
                    extraSystemPrompt: expert.prompt,
                });
                await ctx.runtime.subagent.waitForRun({ runId: runResult.runId, timeoutMs: 120000 });
                const { messages } = await ctx.runtime.subagent.getSessionMessages({
                    sessionKey: ctx.sessionId ?? session.id,
                    limit: 5,
                });
                const lastMsg = messages[messages.length - 1];
                const output = typeof lastMsg?.content === 'string'
                    ? lastMsg.content.slice(0, 2000)
                    : 'No output';
                return {
                    expertId: expert.id,
                    expertName: expert.name,
                    output,
                    durationMs: Date.now() - expertStart,
                    success: true,
                };
            }
            catch (err) {
                return {
                    expertId: expert.id,
                    expertName: expert.name,
                    output: '',
                    durationMs: Date.now() - expertStart,
                    success: false,
                    error: String(err),
                };
            }
        }));
        // 5. Store and complete
        for (const r of results) {
            sessionManager.addExpertResult(session.id, r);
        }
        sessionManager.completeSession(session.id, 'completed');
        // 6. Format output
        const output = aggregateExpertResults(results.map(r => ({ expertName: r.expertName, output: r.output, success: r.success })), `verify:${type}`);
        return {
            success: true,
            command: `verify:${type}`,
            output,
            expertResults: results,
            durationMs: Date.now() - startTime,
        };
    }
    catch (err) {
        logger.error(`[EO/verify] Error: ${err}`);
        return {
            success: false,
            command: `verify:${type}`,
            output: '',
            error: String(err),
            durationMs: Date.now() - startTime,
        };
    }
}
//# sourceMappingURL=verify.js.map