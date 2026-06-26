/**
 * G-01 — Prompt Injection Detection
 * Layer: input | Severity: block
 *
 * Detects common prompt injection patterns and blocks dispatch.
 */

import type { GuardContext, GuardResult } from '../types.js';

// Base64 pattern: sequences of valid base64 chars longer than 100 chars
const BASE64_PATTERN = /[A-Za-z0-9+/]{100,}={0,2}/;

const INJECTION_PATTERNS: Array<{ pattern: RegExp; label: string }> = [
  {
    pattern: /ignore\s+all\s+previous\s+instructions/i,
    label: 'ignore all previous instructions',
  },
  {
    pattern: /ignore\s+previous\s+instructions/i,
    label: 'ignore previous instructions',
  },
  {
    // "you are now" followed by something other than common benign continuations
    pattern: /you\s+are\s+now\s+(?!sure|correct|ready|done|able|welcome|free|set)/i,
    label: 'persona override: "you are now ..."',
  },
  {
    pattern: /jailbreak/i,
    label: 'jailbreak keyword',
  },
  {
    pattern: /DAN\s+mode/i,
    label: 'DAN mode keyword',
  },
  {
    pattern: /do\s+anything\s+now/i,
    label: 'do anything now',
  },
  {
    pattern: /\[SYSTEM\]/,
    label: '[SYSTEM] tag in user message',
  },
  {
    pattern: /<<SYS>>/,
    label: '<<SYS>> tag in user message',
  },
  {
    pattern: BASE64_PATTERN,
    label: 'long Base64 string (potential encoded injection)',
  },
];

export async function evaluate(ctx: GuardContext): Promise<GuardResult> {
  for (const { pattern, label } of INJECTION_PATTERNS) {
    if (pattern.test(ctx.content)) {
      return {
        passed: false,
        rule: 'G-01',
        action: 'block',
        detail: `Matched pattern: "${label}"`,
      };
    }
  }

  return { passed: true, action: 'pass' };
}
