/**
 * G-03 — Off-Scope Response Filter
 * Layer: output | Severity: flag (audit only — content still passes through)
 *
 * Flags output containing political opinions, NSFW content, or competitor
 * disparagement. Does NOT block — passed: true in all cases.
 */

import type { GuardContext, GuardResult } from '../types.js';

interface FlagCategory {
  name: string;
  patterns: RegExp[];
}

const FLAG_CATEGORIES: FlagCategory[] = [
  {
    name: 'political opinion',
    patterns: [
      /vote\s+for/i,
      /political\s+party/i,
      /should\s+elect/i,
      /liberal\s+party/i,
      /labor\s+party/i,
      /\brepublican\b/i,
      /\bdemocrat\b/i,
    ],
  },
  {
    name: 'NSFW content',
    patterns: [
      /\bfuck/i,
      /\bshit/i,
      /\bass\b/i,
      /\bbitch\b/i,
      /\bdick\b/i,
      /\bcunt\b/i,
    ],
  },
  {
    name: 'competitor disparagement',
    patterns: [
      /openai\s+is\s+(bad|terrible|awful|worse|trash|garbage|useless)/i,
      /anthropic\s+is\s+(bad|terrible|awful|worse|trash|garbage|useless)/i,
      /google\s+(gemini|bard|ai)\s+is\s+(bad|terrible|awful|worse|trash|garbage|useless)/i,
      /microsoft\s+(copilot|azure\s+ai)\s+is\s+(bad|terrible|awful|worse|trash|garbage|useless)/i,
    ],
  },
];

export async function evaluate(ctx: GuardContext): Promise<GuardResult> {
  for (const category of FLAG_CATEGORIES) {
    for (const pattern of category.patterns) {
      if (pattern.test(ctx.content)) {
        return {
          passed: true,   // flag only — content still passes through
          rule: 'G-03',
          action: 'flag',
          detail: `Off-scope content detected: ${category.name} (matched: ${pattern.source})`,
        };
      }
    }
  }

  return { passed: true, action: 'pass' };
}
