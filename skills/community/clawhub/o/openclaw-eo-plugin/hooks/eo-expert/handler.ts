// ============================================================================
// EO Expert Hook Handler
// Intercepts tool calls and routes them through the EO expert system
// ============================================================================

import type {
  PluginHookBeforeToolCallEvent,
  PluginHookBeforeToolCallResult,
  PluginHookAfterToolCallEvent,
  PluginHookToolContext,
} from '../../types/plugin.js';

// ---------------------------------------------------------------------------
// Expert Routing Configuration
// ---------------------------------------------------------------------------

const EO_TOOL_PATTERNS: Array<{
  pattern: RegExp;
  experts: string[];
  timeoutMs: number;
}> = [
  { pattern: /plan/i, experts: ['pm', 'engineer', 'qa'], timeoutMs: 120000 },
  { pattern: /architect/i, experts: ['architect', 'tech-lead', 'dba'], timeoutMs: 180000 },
  { pattern: /verify/i, experts: ['qa', 'code-reviewer', 'security-engineer'], timeoutMs: 120000 },
  { pattern: /code.?review/i, experts: ['code-reviewer', 'senior-dev'], timeoutMs: 180000 },
  { pattern: /deploy/i, experts: ['devops', 'sre', 'release-manager'], timeoutMs: 300000 },
  { pattern: /refactor/i, experts: ['senior-dev', 'code-reviewer'], timeoutMs: 180000 },
  { pattern: /security/i, experts: ['security-engineer', 'security-auditor'], timeoutMs: 120000 },
  { pattern: /performance/i, experts: ['performance-engineer', 'sre'], timeoutMs: 180000 },
];

// ---------------------------------------------------------------------------
// Hook Handlers
// ---------------------------------------------------------------------------

/**
 * before_tool_call hook
 *
 * Detects EO command patterns in tool calls and enriches them with expert context.
 */
export async function handleBeforeToolCall(
  event: PluginHookBeforeToolCallEvent,
  ctx: PluginHookToolContext
): Promise<PluginHookBeforeToolCallResult | void> {
  const { toolName, params } = event;

  // Check if tool matches EO pattern
  const routing = EO_TOOL_PATTERNS.find(r => r.pattern.test(toolName));
  if (!routing) return;

  // Enrich params with EO context
  const enrichedParams = {
    ...params,
    _eoExpertTeam: routing.experts,
    _eoTimeoutMs: routing.timeoutMs,
    _eoRoutingActive: true,
  };

  return {
    params: enrichedParams,
  };
}

/**
 * after_tool_call hook
 *
 * Logs expert results and updates collaboration state after EO tool execution.
 */
export async function handleAfterToolCall(
  event: PluginHookAfterToolCallEvent,
  ctx: PluginHookToolContext
): Promise<void> {
  const { toolName, result, durationMs, error } = event;

  // Only log EO-routed tools
  const routing = EO_TOOL_PATTERNS.find(r => r.pattern.test(toolName));
  if (!routing) return;

  const status = error ? '❌' : '✅';
  const duration = durationMs ? `(${(durationMs / 1000).toFixed(1)}s)` : '';

  // Log summary (actual logging is done by the calling tool)
  // This hook is primarily for state updates and side effects
  if (ctx.sessionKey) {
    // Could update session state here if needed
  }
}

// ---------------------------------------------------------------------------
// Registration
// ---------------------------------------------------------------------------

export const eoExpertHookHandlers = {
  'before_tool_call': handleBeforeToolCall,
  'after_tool_call': handleAfterToolCall,
};
