import { readDayLog, readGoals } from '../lib/storage.ts';
import { print, err, sumIngredients } from '../lib/format.ts';
import { GOAL_DIRECTION, NUTRIENT_KEYS } from '../lib/types.ts';
import type { Goals } from '../lib/types.ts';

type Args = Record<string, string | boolean | undefined>;

export function summaryCommand(args: Args): void {
  const date = args['date'] as string | undefined;
  if (!date) { err('--date YYYY-MM-DD is required'); process.exit(1); }

  const log   = readDayLog(date);
  const goals = readGoals();

  // Aggregate all ingredients across all meals
  const allIngredients = log.flatMap(m => m.ingredients);
  const totals = sumIngredients(allIngredients) as Goals;

  const summary: Record<string, unknown> = {};

  for (const key of NUTRIENT_KEYS) {
    const consumed = totals[key] ?? 0;
    const goal     = goals[key];
    const type     = GOAL_DIRECTION[key];
    const entry: Record<string, unknown> = { consumed, type };

    if (goal !== undefined) {
      const pct    = goal > 0 ? Math.round((consumed / goal) * 100) : 0;
      const status = type === 'max'
        ? (consumed > goal ? 'over' : 'ok')
        : (consumed < goal ? 'under' : 'ok');
      entry['goal']   = goal;
      entry['pct']    = pct;
      entry['status'] = status;
    }

    summary[key] = entry;
  }

  print({ date, summary });
}
