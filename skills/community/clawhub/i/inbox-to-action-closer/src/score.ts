import type { ActionItem } from './types.js';

export const OVERDUE_BOOST = 30;
export const DUE_SOON_BOOST = 20;
export const DUE_WEEK_WINDOW = 7;
export const BLOCKER_BOOST = 25;
export const ASSIGNMENT_BOOST = 10;
export const RECENCY_MAX_BOOST = 15;
export const RECENCY_WINDOW_DAYS = 14;
export const FOLLOW_UP_BOOST = 12;
export const DEFAULT_TYPE_WEIGHT = 1.0;

// Weights reflect signal-to-noise of each source: task trackers (github, notion,
// trello) carry full weight; email/slack are noisier; calendar events are often
// informational rather than actionable.
export const TYPE_WEIGHT_MAP: Record<string, number> = {
  github: 1.0,
  slack: 0.8,
  email: 0.9,
  calendar: 0.7,
  notion: 1.0,
  trello: 1.0,
};

export function startOfDayUTC(date: Date): Date {
  const d = new Date(date);
  d.setUTCHours(0, 0, 0, 0);
  return d;
}

/**
 * Returns the integer number of days from now to dueAt using UTC day
 * boundaries. Negative means overdue.
 */
export function daysUntilDue(now: Date, dueAt: Date): number {
  const nowDay = startOfDayUTC(now);
  const dueDay = startOfDayUTC(dueAt);
  const MS_PER_DAY = 24 * 60 * 60 * 1000;
  return Math.round((dueDay.getTime() - nowDay.getTime()) / MS_PER_DAY);
}

export function computeDueDateScore(now: Date, dueAt: Date | null | undefined): number {
  if (dueAt == null) return 0;
  const days = daysUntilDue(now, dueAt);
  if (days < 0) return OVERDUE_BOOST;
  if (days <= 1) return DUE_SOON_BOOST;
  if (days <= DUE_WEEK_WINDOW) {
    return DUE_SOON_BOOST * (1 - days / DUE_WEEK_WINDOW);
  }
  return 0;
}

export function computeBlockerScore(isBlocker: boolean): number {
  return isBlocker ? BLOCKER_BOOST : 0;
}

export function assignmentBoost(item: ActionItem, currentUser?: string): number {
  if (!currentUser || !item.owner) return 0;
  return item.owner === currentUser ? ASSIGNMENT_BOOST : 0;
}

export function recencyBoost(now: Date, item: ActionItem): number {
  const dateStr = item.updatedAt || item.createdAt;
  if (!dateStr) return 0;
  const MS_PER_DAY = 24 * 60 * 60 * 1000;
  const daysSince = Math.round(
    (startOfDayUTC(now).getTime() - startOfDayUTC(new Date(dateStr)).getTime()) / MS_PER_DAY,
  );
  if (daysSince >= RECENCY_WINDOW_DAYS) return 0;
  if (daysSince <= 0) return RECENCY_MAX_BOOST;
  return RECENCY_MAX_BOOST * (1 - daysSince / RECENCY_WINDOW_DAYS);
}

export function followUpBoost(item: ActionItem): number {
  if (item.followUpQuestion && item.status !== 'done') return FOLLOW_UP_BOOST;
  return 0;
}

export function typeWeight(item: ActionItem): number {
  if (!item.sourceType) return DEFAULT_TYPE_WEIGHT;
  return TYPE_WEIGHT_MAP[item.sourceType] ?? DEFAULT_TYPE_WEIGHT;
}

function computeScore(item: ActionItem, now: Date, currentUser?: string): number {
  const dueDateScore = computeDueDateScore(now, item.dueAt ? new Date(item.dueAt) : null);
  const blockerScore = computeBlockerScore(item.blocker !== null);
  const assignment = assignmentBoost(item, currentUser);
  const recency = recencyBoost(now, item);
  const followUp = followUpBoost(item);
  const raw = dueDateScore + blockerScore + assignment + recency + followUp;
  return raw * typeWeight(item);
}

export function scoreItems(items: ActionItem[], currentUser?: string): ActionItem[] {
  const now = new Date();
  return items.map(item => ({
    ...item,
    priorityScore: computeScore(item, now, currentUser),
  }));
}
