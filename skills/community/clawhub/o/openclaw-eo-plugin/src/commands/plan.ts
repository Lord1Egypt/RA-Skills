// ============================================================================
// EO /plan Command Implementation
// ============================================================================

import type { PlanOptions, EOCommandResult, ExpertResult } from '../types/index.js';
import { teamManager } from '../collaboration/team-manager.js';
import { sessionManager } from '../collaboration/session-manager.js';
import { buildExpertPrompt, aggregateExpertResults } from '../adapter/skill-adapter.js';

// ---------------------------------------------------------------------------
// Plan Command
// ---------------------------------------------------------------------------

export interface PlanCommandContext {
  runtime: {
    subagent: {
      run: (params: {
        sessionKey: string;
        message: string;
        extraSystemPrompt?: string;
        provider?: string;
        model?: string;
      }) => Promise<{ runId: string }>;
      waitForRun: (params: { runId: string; timeoutMs?: number }) => Promise<{ status: string; error?: string }>;
      getSessionMessages: (params: { sessionKey: string; limit?: number }) => Promise<{ messages: unknown[] }>;
    };
  };
  logger: { info: (msg: string) => void; warn: (msg: string) => void; error: (msg: string) => void };
  sessionId?: string;
}

/**
 * Execute the /plan command
 *
 * Creates a project plan by assembling a PM + Engineer + QA team,
 * then coordinating their analysis through subagent sessions.
 */
export async function executePlan(
  options: PlanOptions,
  ctx: PlanCommandContext
): Promise<EOCommandResult> {
  const startTime = Date.now();
  const { task, context = {}, team, constraints = [], priority = 'medium' } = options;
  const logger = ctx.logger;

  logger.info(`[EO/plan] Starting plan for: ${task.slice(0, 50)}...`);

  try {
    // 1. Create session
    const session = sessionManager.createSession(`plan:${task}`, context);

    // 2. Assemble team
    const expertIds = team ?? ['pm', 'engineer', 'qa'];
    const expertTeam = teamManager.createTeam(task, expertIds);
    sessionManager.addTeamToSession(session.id, expertTeam);

    logger.info(`[EO/plan] Team assembled: ${expertTeam.experts.map(e => e.name).join(', ')}`);

    // 3. Run expert analysis in parallel
    const expertPrompts: Record<string, string> = {
      'pm': buildExpertPrompt('pm', 'Project Manager', `Analyze this task and create a project plan:\n\n${task}\n\nPriority: ${priority}${constraints.length > 0 ? `\n\nConstraints: ${constraints.join(', ')}` : ''}`, context),
      'engineer': buildExpertPrompt('engineer', 'Software Engineer', `Technical analysis for this task:\n\n${task}${constraints.length > 0 ? `\n\nConstraints: ${constraints.join(', ')}` : ''}`, context),
      'qa': buildExpertPrompt('qa', 'QA Engineer', `Identify testing requirements and quality criteria for:\n\n${task}`, context),
    };

    const results: ExpertResult[] = await Promise.all(
      expertTeam.experts.map(async (expert) => {
        const prompt = expertPrompts[expert.id] ?? expertPrompts['engineer'];
        const expertStart = Date.now();

        try {
          // Spawn subagent for each expert
          const runResult = await ctx.runtime.subagent.run({
            sessionKey: ctx.sessionId ?? session.id,
            message: prompt,
            extraSystemPrompt: expert.prompt,
          });

          // Wait for completion
          await ctx.runtime.subagent.waitForRun({ runId: runResult.runId, timeoutMs: 120000 });

          // Get results
          const { messages } = await ctx.runtime.subagent.getSessionMessages({
            sessionKey: ctx.sessionId ?? session.id,
            limit: 5,
          });

          const lastMsg = messages[messages.length - 1] as { content?: string } | undefined;
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
        } catch (err) {
          return {
            expertId: expert.id,
            expertName: expert.name,
            output: '',
            durationMs: Date.now() - expertStart,
            success: false,
            error: String(err),
          };
        }
      })
    );

    // 4. Store results
    for (const r of results) {
      sessionManager.addExpertResult(session.id, r);
    }

    // 5. Complete session
    sessionManager.completeSession(session.id, 'completed');

    // 6. Format output
    const output = aggregateExpertResults(
      results.map(r => ({ expertName: r.expertName, output: r.output, success: r.success })),
      'plan'
    );

    return {
      success: true,
      command: 'plan',
      output,
      expertResults: results,
      durationMs: Date.now() - startTime,
    };
  } catch (err) {
    logger.error(`[EO/plan] Error: ${err}`);
    return {
      success: false,
      command: 'plan',
      output: '',
      error: String(err),
      durationMs: Date.now() - startTime,
    };
  }
}
