// Micro Memory - Spaced Repetition Review System

import { ReviewSchedule, ReviewData, Memory } from './types';
import { readJson, writeJson, REVIEWS_FILE, formatTimestamp, printColored } from './utils';

const INTERVALS = [1, 3, 7, 14, 30, 60, 90]; // Days between reviews

export class ReviewManager {
  private data: ReviewData;

  constructor() {
    this.data = readJson<ReviewData>(REVIEWS_FILE, { schedules: [] });
  }

  private save(): void {
    writeJson(REVIEWS_FILE, this.data);
  }

  getSchedule(memoryId: number): ReviewSchedule | undefined {
    return this.data.schedules.find(s => s.id === memoryId);
  }

  createSchedule(memoryId: number): ReviewSchedule {
    const now = new Date();
    const nextReview = new Date(now.getTime() + 24 * 60 * 60 * 1000); // Tomorrow
    
    const schedule: ReviewSchedule = {
      id: memoryId,
      nextReview: formatTimestamp(nextReview),
      interval: 1,
      level: 0,
    };
    
    this.data.schedules.push(schedule);
    this.save();
    return schedule;
  }

  updateSchedule(memoryId: number, success: boolean): void {
    const schedule = this.getSchedule(memoryId);
    if (!schedule) return;

    if (success) {
      schedule.level = Math.min(schedule.level + 1, INTERVALS.length - 1);
    } else {
      schedule.level = Math.max(schedule.level - 1, 0);
    }

    schedule.interval = INTERVALS[schedule.level];
    
    const nextDate = new Date();
    nextDate.setDate(nextDate.getDate() + schedule.interval);
    schedule.nextReview = formatTimestamp(nextDate);
    
    this.save();
  }

  getDueReviews(today: boolean = false): ReviewSchedule[] {
    const now = formatTimestamp();
    return this.data.schedules.filter(s => {
      if (today) {
        return s.nextReview.startsWith(now.substring(0, 10));
      }
      return s.nextReview <= now;
    });
  }

  removeSchedule(memoryId: number): void {
    this.data.schedules = this.data.schedules.filter(s => s.id !== memoryId);
    this.save();
  }
}

export function reviewCommand(args: Record<string, string | boolean>, memories: Memory[]): void {
  const reviewManager = new ReviewManager();
  const today = args.today === true;
  const dueReviews = reviewManager.getDueReviews(today);

  if (dueReviews.length === 0) {
    if (today) {
      printColored('✓ No reviews due today!', 'green');
    } else {
      printColored('✓ No reviews due!', 'green');
    }
    return;
  }

  const header = today ? '\n📅 Reviews Due Today:\n' : '\n📅 Due Reviews:\n';
  console.log(header);

  for (const schedule of dueReviews) {
    const memory = memories.find(m => m.id === schedule.id);
    if (!memory) continue;

    const emoji = schedule.level >= 4 ? '🔥' : schedule.level >= 2 ? '⭐' : '📝';
    console.log(`${emoji} #${memory.id} [Level ${schedule.level}] [Interval ${schedule.interval}d]`);
    console.log(`   ${memory.content.substring(0, 80)}`);
    if (memory.tag) console.log(`   Tag: #${memory.tag}`);
    console.log(`   Next review: ${schedule.nextReview}`);
    console.log();
  }

  console.log(`Total due: ${dueReviews.length}`);
}

export function calculateNextReview(memory: Memory): string {
  const reviewManager = new ReviewManager();
  const schedule = reviewManager.getSchedule(memory.id);
  
  if (schedule) {
    return schedule.nextReview;
  }
  
  // Create new schedule if none exists
  const newSchedule = reviewManager.createSchedule(memory.id);
  return newSchedule.nextReview;
}
