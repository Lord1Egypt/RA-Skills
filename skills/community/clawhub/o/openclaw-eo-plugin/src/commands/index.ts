// ============================================================================
// EO Collaboration Commands - Registration
// ============================================================================

import type { PluginCommandContext, PluginCommandResult } from '../types/index.js';
import { executePlan } from './plan.js';
import { executeArchitect } from './architect.js';
import { executeVerify } from './verify.js';
import { executeCodeReview } from './code-review.js';

// ---------------------------------------------------------------------------
// Command Definitions
// ---------------------------------------------------------------------------

export const EO_COMMANDS = [
  {
    name: 'plan',
    description: 'Create a structured project plan with PM + Engineer + QA expert team',
    acceptsArgs: true,
    handler: async (ctx: PluginCommandContext): Promise<PluginCommandResult> => {
      // Parse args from ctx.args
      const args = ctx.args ?? '';
      const { parsePlanArgs } = await import('./index.js');
      const options = parsePlanArgs(args);

      // The actual execution is done in the tool handler where runtime is available
      // Command handlers here are for slash-command routing
      return {
        text: `🗺 **EO/plan**\n\nTask: ${options.task}\n\n_Initializing expert team..._`,
      };
    },
  },
  {
    name: 'architect',
    description: 'Design system architecture with architect + tech-lead + DBA expert team',
    acceptsArgs: true,
    handler: async (ctx: PluginCommandContext): Promise<PluginCommandResult> => {
      const args = ctx.args ?? '';
      const { parseArchitectArgs } = await import('./index.js');
      const options = parseArchitectArgs(args);

      return {
        text: `🏗 **EO/architect**\n\nTask: ${options.task}\n\n_Initializing architecture team..._`,
      };
    },
  },
  {
    name: 'verify',
    description: 'Verify implementation against specifications (code, architecture, test, security, performance)',
    acceptsArgs: true,
    handler: async (ctx: PluginCommandContext): Promise<PluginCommandResult> => {
      const args = ctx.args ?? '';
      const { parseVerifyArgs } = await import('./index.js');
      const options = parseVerifyArgs(args);

      return {
        text: `✅ **EO/verify**\n\nType: ${options.type}\n\n_Initializing verification team..._`,
      };
    },
  },
  {
    name: 'code-review',
    description: 'Perform code review with code-reviewer + senior-dev experts',
    acceptsArgs: true,
    handler: async (ctx: PluginCommandContext): Promise<PluginCommandResult> => {
      const args = ctx.args ?? '';
      const { parseCodeReviewArgs } = await import('./index.js');
      const options = parseCodeReviewArgs(args);

      const target = options.prUrl ?? (options.files?.length ? `Files: ${options.files.join(', ')}` : 'All recent changes');

      return {
        text: `🔍 **EO/code-review**\n\nTarget: ${target}\n\n_Initializing review team..._`,
      };
    },
  },
] as const;

// ---------------------------------------------------------------------------
// Argument Parsers (used by both commands and tools)
// ---------------------------------------------------------------------------

export function parsePlanArgs(args: string): {
  task: string;
  team?: string[];
  constraints?: string[];
  priority?: string;
} {
  // Simple key=value parser
  const params: Record<string, string> = {};
  const remaining: string[] = [];

  for (const part of args.split(/\s+/)) {
    const eqIdx = part.indexOf('=');
    if (eqIdx > 0) {
      const key = part.slice(0, eqIdx);
      const val = part.slice(eqIdx + 1);
      params[key] = val;
    } else {
      remaining.push(part);
    }
  }

  return {
    task: params.task ?? remaining.join(' ') ?? 'Unspecified task',
    team: params.team ? params.team.split(',').map(s => s.trim()) : undefined,
    constraints: params.constraints ? params.constraints.split(',').map(s => s.trim()) : [],
    priority: params.priority ?? 'medium',
  };
}

export function parseArchitectArgs(args: string): {
  task: string;
  style?: string;
  language?: string;
} {
  const params: Record<string, string> = {};
  const remaining: string[] = [];

  for (const part of args.split(/\s+/)) {
    const eqIdx = part.indexOf('=');
    if (eqIdx > 0) {
      params[part.slice(0, eqIdx)] = part.slice(eqIdx + 1);
    } else {
      remaining.push(part);
    }
  }

  return {
    task: params.task ?? remaining.join(' ') ?? 'Unspecified task',
    style: params.style,
    language: params.language,
  };
}

export function parseVerifyArgs(args: string): {
  target: string;
  type: string;
  criteria?: string[];
} {
  const params: Record<string, string> = {};
  const remaining: string[] = [];

  for (const part of args.split(/\s+/)) {
    const eqIdx = part.indexOf('=');
    if (eqIdx > 0) {
      params[part.slice(0, eqIdx)] = part.slice(eqIdx + 1);
    } else {
      remaining.push(part);
    }
  }

  return {
    target: params.target ?? remaining.join(' ') ?? 'Unspecified target',
    type: params.type ?? 'code',
    criteria: params.criteria ? params.criteria.split(',').map(s => s.trim()) : [],
  };
}

export function parseCodeReviewArgs(args: string): {
  files?: string[];
  prUrl?: string;
  focus?: string[];
  depth?: string;
} {
  const params: Record<string, string> = {};
  const remaining: string[] = [];

  for (const part of args.split(/\s+/)) {
    const eqIdx = part.indexOf('=');
    if (eqIdx > 0) {
      params[part.slice(0, eqIdx)] = part.slice(eqIdx + 1);
    } else {
      remaining.push(part);
    }
  }

  return {
    files: params.files ? params.files.split(',').map(s => s.trim()) : undefined,
    prUrl: params.prUrl,
    focus: params.focus ? params.focus.split(',').map(s => s.trim()) : [],
    depth: params.depth ?? 'standard',
  };
}

export { executePlan, executeArchitect, executeVerify, executeCodeReview };
