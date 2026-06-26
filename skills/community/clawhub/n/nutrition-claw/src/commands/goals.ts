import { readGoals, writeGoals } from '../lib/storage.ts';
import { print, err } from '../lib/format.ts';
import type { Goals } from '../lib/types.ts';
import { NUTRIENT_KEYS } from '../lib/types.ts';

type Args = Record<string, string | boolean | undefined>;

export async function goalsCommand(sub: string, args: Args): Promise<void> {
  switch (sub) {
    case 'get': return goalsGet();
    case 'set': return goalsSet(args);
    case 'delete': return goalsDelete(args);
    default:
      err(`unknown goals subcommand: ${sub}. Use get | set | delete`);
      process.exit(1);
  }
}

function goalsGet(): void {
  const goals = readGoals();
  if (Object.keys(goals).length === 0) {
    print({ goals: 'not set — run: nutrition-claw configure' });
  } else {
    print({ goals });
  }
}

function goalsSet(args: Args): void {
  const goals = readGoals();
  let changed = false;
  for (const key of NUTRIENT_KEYS) {
    const flag = key.replace(/_/g, '-');
    const val = args[flag] ?? args[key];
    if (val !== undefined && val !== true) {
      const n = Number(val);
      if (isNaN(n)) { err(`invalid value for --${flag}: ${val}`); process.exit(1); }
      goals[key] = n;
      changed = true;
    }
  }
  if (!changed) { err('no nutrient flags provided'); process.exit(1); }
  writeGoals(goals);
  print({ goals });
}

function goalsDelete(args: Args): void {
  const nutrient = args['nutrient'] as string | undefined;
  if (nutrient) {
    const key = nutrient.replace(/-/g, '_') as keyof Goals;
    if (!NUTRIENT_KEYS.includes(key)) {
      err(`unknown nutrient: ${nutrient}`);
      process.exit(1);
    }
    const goals = readGoals();
    delete goals[key];
    writeGoals(goals);
    print({ deleted: nutrient, goals });
  } else {
    writeGoals({});
    print({ deleted: 'all goals' });
  }
}
