// ============================================================================
// EO /architect Command Implementation
// ============================================================================
import { teamManager } from '../collaboration/team-manager.js';
import { sessionManager } from '../collaboration/session-manager.js';
import { buildExpertPrompt, aggregateExpertResults } from '../adapter/skill-adapter.js';
/**
 * Execute the /architect command
 *
 * Designs system architecture by assembling an architect + tech-lead + DBA team.
 */
export async function executeArchitect(options, ctx) {
    const startTime = Date.now();
    const { task, style, language, context = {} } = options;
    const logger = ctx.logger;
    logger.info(`[EO/architect] Starting architecture design for: ${task.slice(0, 50)}...`);
    try {
        // 1. Create session
        const session = sessionManager.createSession(`architect:${task}`, context);
        // 2. Assemble architecture team
        const expertTeam = teamManager.assembleTeam(task, ['architect', 'tech-lead', 'dba', 'devops']);
        sessionManager.addTeamToSession(session.id, expertTeam);
        logger.info(`[EO/architect] Team assembled: ${expertTeam.experts.map(e => e.name).join(', ')}`);
        // 3. Build architecture-specific prompts
        const archStyle = style ?? 'microservices';
        const archContext = {
            ...context,
            architectureStyle: archStyle,
            language: language ?? 'typescript',
        };
        const expertPrompts = {
            'architect': buildExpertPrompt('architect', 'Solutions Architect', `Design a comprehensive system architecture for:\n\n${task}\n\nStyle: ${archStyle}\nLanguage: ${language ?? 'TypeScript'}`, archContext),
            'tech-lead': buildExpertPrompt('tech-lead', 'Tech Lead', `Provide technical implementation guidance for:\n\n${task}\n\nArchitecture Style: ${archStyle}`, archContext),
            'dba': buildExpertPrompt('dba', 'Database Administrator', `Design database schema and data layer for:\n\n${task}\n\nArchitecture Style: ${archStyle}`, archContext),
            'devops': buildExpertPrompt('devops', 'DevOps Engineer', `Design deployment and infrastructure for:\n\n${task}\n\nArchitecture Style: ${archStyle}`, archContext),
        };
        // 4. Run expert analysis
        const results = await Promise.all(expertTeam.experts.map(async (expert) => {
            const prompt = expertPrompts[expert.id] ?? expertPrompts['architect'];
            const expertStart = Date.now();
            try {
                const runResult = await ctx.runtime.subagent.run({
                    sessionKey: ctx.sessionId ?? session.id,
                    message: prompt,
                    extraSystemPrompt: expert.prompt,
                });
                await ctx.runtime.subagent.waitForRun({ runId: runResult.runId, timeoutMs: 180000 });
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
        const output = aggregateExpertResults(results.map(r => ({ expertName: r.expertName, output: r.output, success: r.success })), 'architect');
        return {
            success: true,
            command: 'architect',
            output,
            expertResults: results,
            durationMs: Date.now() - startTime,
        };
    }
    catch (err) {
        logger.error(`[EO/architect] Error: ${err}`);
        return {
            success: false,
            command: 'architect',
            output: '',
            error: String(err),
            durationMs: Date.now() - startTime,
        };
    }
}
//# sourceMappingURL=architect.js.map