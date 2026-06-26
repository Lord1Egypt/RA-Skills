import { readDayLog, listLogDates } from '../lib/storage.ts';
import { print, err, sumIngredients } from '../lib/format.ts';
import type { Goals } from '../lib/types.ts';

type Args = Record<string, string | boolean | undefined>;

function addDays(date: string, n: number): string {
  const d = new Date(date + 'T00:00:00');
  d.setDate(d.getDate() + n);
  return d.toISOString().slice(0, 10);
}

function dateRange(from: string, to: string): string[] {
  const dates: string[] = [];
  let cur = from;
  while (cur <= to) {
    dates.push(cur);
    cur = addDays(cur, 1);
  }
  return dates;
}

export function historyCommand(args: Args): void {
  const from = args['from'] as string | undefined;
  if (!from) { err('--from YYYY-MM-DD is required'); process.exit(1); }

  let to = args['to'] as string | undefined;
  const days = args['days'] !== undefined ? Number(args['days']) : undefined;

  if (!to && days !== undefined) {
    to = addDays(from, days - 1);
  }
  if (!to) { err('--to YYYY-MM-DD or --days N is required'); process.exit(1); }

  const allDates = new Set(listLogDates());
  const history = dateRange(from, to)
    .filter(d => allDates.has(d))
    .map(date => {
      const log  = readDayLog(date);
      const all  = log.flatMap(m => m.ingredients);
      const tots = sumIngredients(all) as Goals;
      return { date, ...tots };
    });

  print({ history });
}
