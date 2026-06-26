/**
 * G-04 — Budget Guard
 * Layer: input | Severity: block
 *
 * Reads the agent's BUDGET.json and blocks dispatch if status is "red".
 */

import * as fs from 'fs';
import * as path from 'path';
import type { GuardContext, GuardResult } from '../types.js';

interface BudgetFile {
  status: 'green' | 'yellow' | 'red';
  daily_tokens_used?: number;
  daily_limit?: number;
}

export async function evaluate(ctx: GuardContext): Promise<GuardResult> {
  const budgetPath = path.join(
    ctx.workspaceRoot,
    'agents',
    ctx.agentId,
    'BUDGET.json',
  );

  // If the budget file doesn't exist, allow through
  if (!fs.existsSync(budgetPath)) {
    return { passed: true, action: 'pass' };
  }

  let budget: BudgetFile;
  try {
    const raw = fs.readFileSync(budgetPath, 'utf8');
    budget = JSON.parse(raw) as BudgetFile;
  } catch {
    // Malformed budget file — fail open (don't block on parse error)
    return { passed: true, action: 'pass' };
  }

  if (budget.status === 'red') {
    const used = budget.daily_tokens_used ?? 'unknown';
    const limit = budget.daily_limit ?? 'unknown';
    return {
      passed: false,
      rule: 'G-04',
      action: 'block',
      detail: `Agent ${ctx.agentId} is over daily budget (used: ${used} / limit: ${limit})`,
    };
  }

  return { passed: true, action: 'pass' };
}
