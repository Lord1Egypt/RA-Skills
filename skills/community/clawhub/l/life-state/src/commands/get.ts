import { getString, type ParsedArgs } from '../lib/args.js';
import { print, todayISO } from '../lib/format.js';
import { readState } from '../lib/storage.js';

export function getCommand(flags: ParsedArgs['flags']): void {
  const date = getString(flags, 'date') ?? todayISO();
  const state = readState(date);

  if (!state) {
    print({ date, state: null, message: 'no state captured for this date' });
    return;
  }
  print(state);
}
