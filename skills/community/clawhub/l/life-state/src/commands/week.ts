import { getNumber, type ParsedArgs } from '../lib/args.js';
import { print } from '../lib/format.js';
import { listStateDates, readState } from '../lib/storage.js';
import type { DayState } from '../lib/types.js';

export function weekCommand(flags: ParsedArgs['flags']): void {
  const days = getNumber(flags, 'days') ?? 7;
  const cutoff = new Date();
  cutoff.setDate(cutoff.getDate() - days);
  const cutoffISO = cutoff.toISOString().slice(0, 10);

  const states: DayState[] = [];
  for (const date of listStateDates()) {
    if (date < cutoffISO) continue;
    const s = readState(date);
    if (s) states.push(s);
  }

  // Average energy if any captured
  const energyValues = states.map(s => s.energy).filter((e): e is number => typeof e === 'number');
  const avgEnergy = energyValues.length > 0
    ? Math.round((energyValues.reduce((a, b) => a + b, 0) / energyValues.length) * 10) / 10
    : null;

  // Mood histogram
  const moodCounts: Record<string, number> = {};
  for (const s of states) {
    if (s.mood) moodCounts[s.mood] = (moodCounts[s.mood] ?? 0) + 1;
  }

  // Most common soreness areas
  const soreCounts: Record<string, number> = {};
  for (const s of states) {
    for (const area of s.soreness ?? []) {
      soreCounts[area] = (soreCounts[area] ?? 0) + 1;
    }
  }

  print({
    window: { days, since: cutoffISO, captured: states.length },
    avg_energy: avgEnergy,
    mood_counts: Object.keys(moodCounts).length ? moodCounts : undefined,
    soreness_areas: Object.keys(soreCounts).length ? soreCounts : undefined,
    days: states.reverse().map(s => ({
      date: s.date,
      mood: s.mood,
      energy: s.energy,
      sleep_quality: s.sleep_quality,
      soreness: s.soreness,
      note: s.note,
    })),
  });
}
