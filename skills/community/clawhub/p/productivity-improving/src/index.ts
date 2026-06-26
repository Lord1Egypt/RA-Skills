/**
 * Productivity Improving - core activity tracking module.
 */

import * as fs from 'fs';
import * as path from 'path';

const DATA_DIR = path.join(__dirname, '..', 'data');
const ACTIVITIES_FILE = path.join(DATA_DIR, 'activities.json');
const LOGS_DIR = path.join(DATA_DIR, 'logs');

const CATEGORIES: Record<string, { color: string; keywords: string[]; name: string }> = {
  work: {
    color: '#4CAF50',
    keywords: ['code', 'coding', 'programming', 'meeting', 'email', 'planning', 'review', 'design', 'debug', 'deploy'],
    name: 'Deep Work',
  },
  learning: {
    color: '#2196F3',
    keywords: ['read', 'reading', 'study', 'course', 'learn', 'research', 'article', 'book'],
    name: 'Learning',
  },
  health: {
    color: '#FF9800',
    keywords: ['exercise', 'workout', 'gym', 'run', 'meditation', 'sleep', 'walk', 'yoga'],
    name: 'Health',
  },
  life: {
    color: '#9C27B0',
    keywords: ['cook', 'cooking', 'clean', 'shopping', 'family', 'child', 'home', 'meal'],
    name: 'Life',
  },
  rest: {
    color: '#607D8B',
    keywords: ['rest', 'break', 'entertainment', 'movie', 'game', 'social', 'relax'],
    name: 'Rest',
  },
};

interface Activity {
  id: string;
  name: string;
  category: string;
  startTime: string;
  endTime?: string;
  duration?: number;
  status: 'active' | 'completed' | 'paused';
}

function ensureDataDir(): void {
  if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
  }
  if (!fs.existsSync(LOGS_DIR)) {
    fs.mkdirSync(LOGS_DIR, { recursive: true });
  }
}

function loadActivities(): Activity[] {
  ensureDataDir();
  if (!fs.existsSync(ACTIVITIES_FILE)) {
    return [];
  }
  try {
    return JSON.parse(fs.readFileSync(ACTIVITIES_FILE, 'utf-8')) as Activity[];
  } catch {
    return [];
  }
}

function saveActivities(activities: Activity[]): void {
  ensureDataDir();
  fs.writeFileSync(ACTIVITIES_FILE, JSON.stringify(activities, null, 2));
}

function categorize(name: string): string {
  const lower = name.toLowerCase();
  for (const [category, config] of Object.entries(CATEGORIES)) {
    if (config.keywords.some((keyword) => lower.includes(keyword))) {
      return category;
    }
  }
  return 'life';
}

function genId(): string {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 11)}`;
}

function now(): string {
  return new Date().toISOString();
}

function calcDuration(start: string, end: string): number {
  return Math.round((new Date(end).getTime() - new Date(start).getTime()) / 60000);
}

export function startActivity(name: string): Activity {
  const activities = loadActivities();
  const activeIndex = activities.findIndex((activity) => activity.status === 'active');

  if (activeIndex >= 0) {
    activities[activeIndex].status = 'completed';
    activities[activeIndex].endTime = now();
    activities[activeIndex].duration = calcDuration(
      activities[activeIndex].startTime,
      activities[activeIndex].endTime!,
    );
  }

  const activity: Activity = {
    id: genId(),
    name,
    category: categorize(name),
    startTime: now(),
    status: 'active',
  };

  activities.push(activity);
  saveActivities(activities);
  return activity;
}

export function completeActivity(): Activity | null {
  const activities = loadActivities();
  const index = activities.findIndex((activity) => activity.status === 'active');

  if (index < 0) {
    return null;
  }

  const activity = activities[index];
  activity.status = 'completed';
  activity.endTime = now();
  activity.duration = calcDuration(activity.startTime, activity.endTime);
  saveActivities(activities);
  return activity;
}

export function getCurrentActivity(): Activity | null {
  return loadActivities().find((activity) => activity.status === 'active') || null;
}

export function logActivity(name: string, minutes: number): Activity {
  const activities = loadActivities();
  const end = new Date();
  const start = new Date(end.getTime() - minutes * 60000);

  const activity: Activity = {
    id: genId(),
    name,
    category: categorize(name),
    startTime: start.toISOString(),
    endTime: end.toISOString(),
    duration: minutes,
    status: 'completed',
  };

  activities.push(activity);
  saveActivities(activities);
  return activity;
}

export function getTodayActivities(): Activity[] {
  const today = new Date().toDateString();
  return loadActivities().filter((activity) => new Date(activity.startTime).toDateString() === today);
}

export function formatDuration(minutes: number): string {
  const hours = Math.floor(minutes / 60);
  const remainingMinutes = minutes % 60;
  return hours > 0 ? `${hours}h ${remainingMinutes}m` : `${remainingMinutes}m`;
}

export function generateReport(date?: string): string {
  const targetDate = date || new Date().toISOString().split('T')[0];
  const activities = loadActivities().filter((activity) => activity.startTime.startsWith(targetDate));

  const breakdown: Record<string, number> = {};
  let focusMinutes = 0;
  let otherMinutes = 0;

  for (const activity of activities) {
    if (!activity.duration) {
      continue;
    }

    breakdown[activity.category] = (breakdown[activity.category] || 0) + activity.duration;

    if (['work', 'learning'].includes(activity.category)) {
      focusMinutes += activity.duration;
    } else {
      otherMinutes += activity.duration;
    }
  }

  const totalMinutes = focusMinutes + otherMinutes;
  const focusRatio = totalMinutes > 0 ? Math.round((focusMinutes / totalMinutes) * 100) : 0;

  let report = `# ${targetDate} Work Log\n\n`;
  report += `## Overview\n- Total activities: ${activities.length}\n`;
  report += `- Focus time: ${formatDuration(focusMinutes)}\n`;
  report += `- Other time: ${formatDuration(otherMinutes)}\n`;
  report += `- Focus/Other ratio: ${focusRatio}%/${100 - focusRatio}%\n\n`;

  report += '## Time Distribution\n| Category | Duration | Percentage |\n|----------|----------|------------|\n';
  for (const [category, duration] of Object.entries(breakdown)) {
    const percentage = totalMinutes > 0 ? Math.round((duration / totalMinutes) * 100) : 0;
    report += `| ${CATEGORIES[category]?.name || category} | ${formatDuration(duration)} | ${percentage}% |\n`;
  }

  report += '\n## Key Activities\n';
  for (const activity of activities
    .filter((item) => (item.duration || 0) >= 30)
    .sort((left, right) => (right.duration || 0) - (left.duration || 0))) {
    report += `- ${activity.name} (${formatDuration(activity.duration || 0)})\n`;
  }

  fs.writeFileSync(path.join(LOGS_DIR, `${targetDate}.md`), report);
  return report;
}

export function getInsights(): string {
  const todayActivities = getTodayActivities();
  if (todayActivities.length === 0) {
    return 'No activities recorded yet today.';
  }

  const focusMinutes = todayActivities
    .filter((activity) => ['work', 'learning'].includes(activity.category))
    .reduce((sum, activity) => sum + (activity.duration || 0), 0);

  let insights = "Today's productivity insights\n\n";
  insights += `- Completed activities: ${todayActivities.length}\n`;
  insights += `- Focus time: ${formatDuration(focusMinutes)}\n`;

  if (focusMinutes > 240) {
    insights += '\nHigh focus day. Keep protecting your deep-work blocks.\n';
  } else if (focusMinutes < 120) {
    insights += '\nFocus time was limited. Consider grouping shallow tasks together.\n';
  }

  const longActivities = todayActivities.filter((activity) => (activity.duration || 0) >= 60);
  if (longActivities.length > 0) {
    insights += '\nLong sessions:\n';
    for (const activity of longActivities.slice(0, 3)) {
      insights += `- ${activity.name}: ${formatDuration(activity.duration || 0)}\n`;
    }
  }

  return insights;
}
