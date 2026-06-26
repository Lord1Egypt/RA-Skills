import { getNumber, getString, type ParsedArgs } from '../lib/args.js';
import { err, print, todayISO, nowISO } from '../lib/format.js';
import { mergeState } from '../lib/storage.js';
import { VALID_MOODS, VALID_SLEEP, type DayState } from '../lib/types.js';

export function setCommand(flags: ParsedArgs['flags']): void {
  const date = getString(flags, 'date') ?? todayISO();
  const patch: Partial<DayState> = { updated_at: nowISO() };

  const mood = getString(flags, 'mood');
  if (mood !== undefined) patch.mood = mood.toLowerCase();

  const energy = getNumber(flags, 'energy');
  if (energy !== undefined) {
    if (energy < 1 || energy > 10) {
      err(`energy must be between 1 and 10 (got ${energy})`);
      process.exit(1);
    }
    patch.energy = energy;
  }

  const sleep = getString(flags, 'sleep');
  if (sleep !== undefined) patch.sleep_quality = sleep.toLowerCase();

  const sore = getString(flags, 'sore');
  if (sore !== undefined) {
    patch.soreness = sore.split(',').map(s => s.trim().toLowerCase()).filter(Boolean);
  }

  const note = getString(flags, 'note');
  if (note !== undefined) patch.note = note;

  const fieldsTouched = Object.keys(patch).filter(k => k !== 'updated_at');
  if (fieldsTouched.length === 0) {
    err('set requires at least one of: --mood, --energy, --sore, --sleep, --note');
    process.exit(1);
  }

  const merged = mergeState(date, patch);
  print({
    set: { date, fields_updated: fieldsTouched },
    state: merged,
    hints: {
      mood: `recommended: ${VALID_MOODS.join(' | ')} (freeform accepted)`,
      sleep_quality: `recommended: ${VALID_SLEEP.join(' | ')} (freeform accepted)`,
    },
  });
}
