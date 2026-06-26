/**
 * Memoria — Real-time procedural capture hook (Layer 1b: after_tool_call)
 *
 * Extracted from index.ts Phase 2.2 — pure mechanical move, zero logic change.
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk/core";
import type { MemoriaConfig } from "./core/config.js";
import type { LLMProvider } from "./core/providers/types.js";
import type { ProceduralMemory, Procedure } from "./core/procedural.js";
import type { KnowledgeGraph } from "./core/graph.js";

/**
 * Register the after_tool_call hook for real-time procedural capture (Layer 1b).
 * Learns on-the-fly from successful tool call sequences.
 */
export function registerProceduralHook(
  api: OpenClawPluginApi,
  cfg: MemoriaConfig,
  extractLlm: LLMProvider,
  proceduralMem: ProceduralMemory,
  graph: KnowledgeGraph,
): void {
  // Session buffer: accumulates tool calls until a success pattern triggers assembly
  const toolCallBuffer: Array<{
    toolName: string;
    params: Record<string, unknown>;
    result?: unknown;
    error?: string;
    durationMs?: number;
    timestamp: number;
  }> = [];
  // Track which procedures were already assembled to avoid duplicates
  const assembledGoals = new Set<string>();
  // Cooldown to avoid assembling too frequently
  let lastAssemblyTime = 0;
  const ASSEMBLY_COOLDOWN_MS = 60_000; // 1 minute between assemblies

  api.on("after_tool_call", async (event: any, _ctx: any) => {
    try {
      const { toolName, params, result, error, durationMs } = event;

      // Buffer all tool calls (keep last 30 to avoid memory leak)
      toolCallBuffer.push({
        toolName,
        params: params || {},
        result: typeof result === 'string' ? result.slice(0, 2000) : result,
        error,
        durationMs,
        timestamp: Date.now(),
      });
      if (toolCallBuffer.length > 30) toolCallBuffer.shift();

      // Only trigger assembly on exec-type tools with a successful outcome
      if (toolName !== 'exec' && toolName !== 'Edit' && toolName !== 'Write') return;
      if (error) return; // failed step — don't assemble yet

      // Check result for success keywords (publish, deploy, commit, install, etc.)
      const resultStr = typeof result === 'string' ? result : JSON.stringify(result || '');
      const successPatterns = [
        /Published?\s/i, /✔|✅/, /success/i, /deployed/i, /created/i,
        /\[new tag\]/, /release.*created/i, /installed/i, /committed/i,
        /pushed/i, /merged/i, /completed/i, /OK\.\s/,
      ];

      const isSuccess = successPatterns.some(p => p.test(resultStr));
      if (!isSuccess) return;

      // Cooldown check
      const now = Date.now();
      if (now - lastAssemblyTime < ASSEMBLY_COOLDOWN_MS) return;

      // We have a success signal — assemble procedure from recent exec calls
      const recentExecs = toolCallBuffer
        .filter(tc => tc.toolName === 'exec' && !tc.error)
        .slice(-15); // last 15 exec calls

      if (recentExecs.length < 2) return;

      // Extract commands
      const commands = recentExecs
        .map(tc => (tc.params as any)?.command as string)
        .filter(Boolean)
        .filter(cmd => cmd.length > 5 && cmd.length < 1000);

      if (commands.length < 2) return;

      // Filter — only capture reusable procedures
      if (!proceduralMem.isReusableProcedure(commands)) {
        api.logger.debug?.(`memoria: procedural skipped — not reusable (${commands.length} cmds, no action pattern)`);
        return;
      }

      // Quick fingerprint to avoid duplicate assemblies
      const fingerprint = commands.slice(-3).join('|').slice(0, 200);
      if (assembledGoals.has(fingerprint)) return;

      // Assemble the procedure via LLM
      api.logger.info?.(`memoria: 🔧 real-time procedural capture — ${commands.length} commands, trigger: "${resultStr.slice(0, 80)}..."`);

      const prompt = `Analyze this successful command sequence and extract a reusable procedure.

Commands executed (in order):
${commands.map((c, i) => `${i + 1}. ${c}`).join('\n')}

Final result (success): ${resultStr.slice(0, 500)}

Output JSON only (no markdown, no explanation):
{
  "name": "Short name (e.g., 'Publish Memoria to ClawHub')",
  "goal": "What this accomplishes in one sentence",
  "trigger_patterns": ["keyword1", "keyword2"],
  "key_steps": ["step1 description", "step2 description"],
  "gotchas": ["pitfall or workaround learned"]
}`;

      try {
        const response = await extractLlm.generateWithMeta!(prompt, {
          maxTokens: 512,
          temperature: 0.1,
          format: "json",
          timeoutMs: 15000,
        });

        if (!response?.response) return;

        const cleaned = response.response.replace(/```json\n?|\n?```/g, '').trim();
        const meta = JSON.parse(cleaned);

        if (!meta.name || !meta.goal) return;

        // Re-check name for noise patterns
        if (!proceduralMem.isReusableProcedure(commands, meta.name)) {
          api.logger.debug?.(`memoria: procedural skipped — LLM named it noise: "${meta.name}"`);
          return;
        }

        // Smart duplicate detection
        const similar = proceduralMem.findSimilarProcedure(meta.name, meta.goal);

        if (similar) {
          // Reinforce existing procedure
          const totalDuration = recentExecs.reduce((sum, tc) => sum + (tc.durationMs || 0), 0);
          proceduralMem.recordExecution(similar.id, true, totalDuration);

          // Add improvement if steps changed
          const newSteps = commands.filter(c => !similar.steps.includes(c));
          if (newSteps.length > 0) {
            proceduralMem.addImprovement(
              similar.id,
              `Updated steps: ${newSteps.slice(0, 3).join('; ')}`,
              'Real-time learning from successful execution'
            );
          }

          // Reflect: was this the best approach?
          const reflectEvery = cfg.procedural?.reflectEvery ?? 3;
          if (reflectEvery > 0 && (similar.success_count + 1) % reflectEvery === 0) {
            try {
              const errors = recentExecs
                .filter(tc => tc.error)
                .map(tc => tc.error!);
              const reflection = await proceduralMem.reflect(similar.id, {
                durationMs: totalDuration,
                stepsTaken: commands,
                errorsEncountered: errors.length > 0 ? errors : undefined,
              });
              if (reflection?.should_improve) {
                api.logger.info?.(`memoria: procedural 🔍 reflected on "${similar.name}" — ${reflection.suggestions.slice(0, 2).join('; ')}`);
              }
            } catch (e) { api?.logger?.debug?.('memoria:procedural-reflection: ' + String(e)); }
          }

          api.logger.info?.(`memoria: procedural ✅ reinforced "${similar.name}" (v${similar.version}, ${similar.success_count + 1} successes, quality=${similar.quality.overall})`);
        } else {
          // Create new procedure with full type compliance
          const proc: Procedure = {
            id: `proc_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`,
            name: meta.name,
            goal: meta.goal,
            steps: commands,
            version: 1,
            success_count: 1,
            failure_count: 0,
            last_success_at: Date.now(),
            last_updated_at: Date.now(),
            improvements: [],
            quality: {
              speed: 0.5,
              reliability: 0.5,
              elegance: Math.max(0.2, 1 - commands.length * 0.1),
              safety: 0.8,
              overall: 0.5,
            },
            context: [...(meta.trigger_patterns || []), ...(meta.gotchas || [])].join(', '),
            gotchas: meta.gotchas?.join(' | '),
            degradation_score: 0,
            preferred: false,
          };

          proceduralMem.storeProcedure(proc);
          api.logger.info?.(`memoria: procedural ✅ NEW "${proc.name}" (${proc.steps.length} steps, real-time)`);

          // Cross-layer: enrich Knowledge Graph with procedure entities
          try {
            const procFact = `Procedure "${proc.name}": ${proc.goal}. Steps: ${commands.slice(0, 3).join('; ')}`;
            await graph.extractAndStore(`proc_${proc.id}`, procFact);
            api.logger.debug?.(`memoria: procedural → graph entities extracted for "${proc.name}"`);
          } catch (e) { api?.logger?.debug?.('memoria:procedural-graph: ' + String(e)); }
        }

        assembledGoals.add(fingerprint);
        lastAssemblyTime = now;

        // Clear old buffer entries (keep last 5 for context)
        toolCallBuffer.splice(0, Math.max(0, toolCallBuffer.length - 5));

      } catch (llmErr) {
        api.logger.debug?.(`memoria: procedural LLM failed: ${String(llmErr)}`);
      }

    } catch (err) {
      // Non-blocking — never crash the plugin
      api.logger.debug?.(`memoria: after_tool_call error: ${String(err)}`);
    }
  });
}
