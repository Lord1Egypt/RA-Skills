/**
 * G-05 — Context Length Guard
 * Layer: input | Severity: warn / block
 *
 * Estimates token count (length/4 heuristic) and warns or blocks
 * if the message is approaching or exceeding the context limit.
 */

import type { GuardContext, GuardResult } from '../types.js';

const WARN_THRESHOLD = 6000;   // tokens — warn
const BLOCK_THRESHOLD = 12000; // tokens — hard block

export async function evaluate(ctx: GuardContext): Promise<GuardResult> {
  const estimatedTokens = Math.ceil(ctx.content.length / 4);

  if (estimatedTokens > BLOCK_THRESHOLD) {
    return {
      passed: false,
      rule: 'G-05',
      action: 'block',
      detail: `Message too long: estimated ${estimatedTokens} tokens exceeds limit (${BLOCK_THRESHOLD})`,
    };
  }

  if (estimatedTokens > WARN_THRESHOLD) {
    return {
      passed: true,
      rule: 'G-05',
      action: 'warn',
      detail: `Estimated ${estimatedTokens} tokens — approaching context limit (${WARN_THRESHOLD})`,
    };
  }

  return { passed: true, action: 'pass' };
}
