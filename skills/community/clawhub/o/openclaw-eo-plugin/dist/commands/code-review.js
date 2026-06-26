// ============================================================================
// EO /code-review Command Implementation
// ============================================================================
import { teamManager } from '../collaboration/team-manager.js';
import { sessionManager } from '../collaboration/session-manager.js';
import { buildExpertPrompt, aggregateExpertResults } from '../adapter/skill-adapter.js';
/**
 * Code review focus areas
 */
const REVIEW_FOCUS_EXPERTS = {
    'quick': ['code-reviewer'],
    'standard': ['code-reviewer', 'senior-dev'],
    'deep': ['code-reviewer', 'senior-dev', 'security-engineer'],
};
/**
 * Execute the /code-review command
 *
 * Performs code review using code-reviewer + senior-dev experts.
 */
export async function executeCodeReview(options, ctx) {
    const startTime = Date.now();
    const { files = [], prUrl, focus = [], depth = 'standard' } = options;
    const logger = ctx.logger;
    const targetDesc = prUrl ? `PR: ${prUrl}` : files.length > 0 ? `Files: ${files.join(', ')}` : 'No specific files';
    logger.info(`[EO/code-review] Starting ${depth} code review - ${targetDesc}`);
    try {
        // 1. Create session
        const session = sessionManager.createSession(`code-review:${targetDesc}`, { files, prUrl, depth });
        // 2. Assemble review team
        const expertIds = REVIEW_FOCUS_EXPERTS[depth] ?? REVIEW_FOCUS_EXPERTS['standard'];
        const expertTeam = teamManager.assembleTeam('code-review', expertIds);
        sessionManager.addTeamToSession(session.id, expertTeam);
        logger.info(`[EO/code-review] Team assembled: ${expertTeam.experts.map(e => e.name).join(', ')}`);
        // 3. Build review prompts
        const filesStr = files.length > 0 ? `\n\n## Files to Review\n${files.map(f => `- ${f}`).join('\n')}` : '';
        const prStr = prUrl ? `\n\n## Pull Request\n${prUrl}` : '';
        const focusStr = focus.length > 0 ? `\n\n## Focus Areas\n${focus.map(f => `- ${f}`).join('\n')}` : '';
        const reviewContext = {
            files,
            prUrl,
            depth,
            focusAreas: focus,
        };
        const expertPrompts = {
            'code-reviewer': buildExpertPrompt('code-reviewer', 'Code Reviewer', `Review the following code:\n\n${targetDesc}${filesStr}${prStr}${focusStr}\n\nDepth: ${depth}`, reviewContext),
            'senior-dev': buildExpertPrompt('senior-dev', 'Senior Developer', `Provide senior-level code review for:\n\n${targetDesc}${filesStr}${prStr}${focusStr}\n\nDepth: ${depth}`, reviewContext),
            'security-engineer': buildExpertPrompt('security-engineer', 'Security Engineer', `Perform security-focused code review for:\n\n${targetDesc}${filesStr}${prStr}${focusStr}\n\nDepth: ${depth}`, reviewContext),
        };
        // 4. Run review in parallel
        const results = await Promise.all(expertTeam.experts.map(async (expert) => {
            const prompt = expertPrompts[expert.id] ?? expertPrompts['code-reviewer'];
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
        const output = aggregateExpertResults(results.map(r => ({ expertName: r.expertName, output: r.output, success: r.success })), 'code-review');
        return {
            success: true,
            command: 'code-review',
            output,
            expertResults: results,
            durationMs: Date.now() - startTime,
        };
    }
    catch (err) {
        logger.error(`[EO/code-review] Error: ${err}`);
        return {
            success: false,
            command: 'code-review',
            output: '',
            error: String(err),
            durationMs: Date.now() - startTime,
        };
    }
}
//# sourceMappingURL=code-review.js.map