export type Mood = 'great' | 'good' | 'normal' | 'tired' | 'terrible';
export type SleepQuality = 'good' | 'ok' | 'poor';

export const VALID_MOODS: Mood[] = ['great', 'good', 'normal', 'tired', 'terrible'];
export const VALID_SLEEP: SleepQuality[] = ['good', 'ok', 'poor'];

export interface DayState {
  date: string;
  mood?: Mood | string;
  energy?: number;
  soreness?: string[];
  sleep_quality?: SleepQuality | string;
  note?: string;
  updated_at?: string;
}
