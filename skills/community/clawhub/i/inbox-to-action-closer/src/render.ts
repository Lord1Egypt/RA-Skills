import type { ActionItem } from './types.js';

const TIER_THRESHOLDS = { urgent: 70, active: 30 } as const;

export const URGENT_THRESHOLD = TIER_THRESHOLDS.urgent;
export const ACTIVE_THRESHOLD = TIER_THRESHOLDS.active;

export interface TieredItems {
  urgent: ActionItem[];
  active: ActionItem[];
  low: ActionItem[];
}

/** Preserves input order within each tier. */
export function groupByTier(items: ActionItem[]): TieredItems {
  const urgent: ActionItem[] = [];
  const active: ActionItem[] = [];
  const low: ActionItem[] = [];

  for (const item of items) {
    if (item.priorityScore >= URGENT_THRESHOLD) {
      urgent.push(item);
    } else if (item.priorityScore >= ACTIVE_THRESHOLD) {
      active.push(item);
    } else {
      low.push(item);
    }
  }

  return { urgent, active, low };
}

export function escapeMarkdown(text: string): string {
  return text.replace(/\|/g, '\\|').replace(/`/g, '\\`');
}

const TIER_LABELS: { key: keyof TieredItems; heading: string }[] = [
  { key: 'urgent', heading: '🔴 Urgent' },
  { key: 'active', heading: '🟡 Active' },
  { key: 'low', heading: '🟢 Low Priority' },
];

export function renderItem(item: ActionItem): string {
  const lines: string[] = [];

  const title = escapeMarkdown(item.title);
  const summary = escapeMarkdown(item.summary);
  lines.push(`- [ ] **${title}** (${item.source}) — ${summary}`);

  if (item.owner) {
    lines.push(`  Owner: ${item.owner}`);
  }
  if (item.dueAt) {
    lines.push(`  Due: ${item.dueAt}`);
  }
  if (item.status) {
    lines.push(`  Status: ${item.status}`);
  }
  if (item.blocker) {
    lines.push(`  ⚠ Blocker: ${item.blocker}`);
  }
  if (item.replyDraft) {
    lines.push(`  Reply draft: ${item.replyDraft}`);
  }
  if (item.followUpQuestion) {
    lines.push(`  Follow-up: ${item.followUpQuestion}`);
  }
  if (item.suggestedNextAction) {
    lines.push(`  Next action: ${item.suggestedNextAction}`);
  }
  if (item.url) {
    lines.push(`  Link: [${item.url}](${item.url})`);
  }

  return lines.join('\n');
}

export function renderMarkdown(items: ActionItem[]): string {
  if (items.length === 0) {
    return '# Action Board\n\nNo action items found. All clear!';
  }

  const tiers = groupByTier(items);
  const sections: string[] = ['# Action Board'];

  for (const { key, heading } of TIER_LABELS) {
    const tierItems = tiers[key];
    if (tierItems.length === 0) continue;

    sections.push(`\n## ${heading}\n`);
    sections.push(tierItems.map(renderItem).join('\n\n'));
  }

  return sections.join('\n');
}

// Prevent 'undefined' strings in JSON.stringify output
function cleanItem(item: ActionItem): Record<string, unknown> {
  const result: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(item)) {
    if (value !== undefined) {
      result[key] = value;
    }
  }
  return result;
}

export function renderJSON(items: ActionItem[], now?: Date): string {
  const tiers = groupByTier(items);

  const output = {
    generatedAt: (now ?? new Date()).toISOString(),
    totalItems: items.length,
    tiers: {
      urgent: tiers.urgent.map(cleanItem),
      active: tiers.active.map(cleanItem),
      low: tiers.low.map(cleanItem),
    },
    metadata: {
      tierThresholds: {
        urgent: TIER_THRESHOLDS.urgent,
        active: TIER_THRESHOLDS.active,
      },
    },
  };

  return JSON.stringify(output, null, 2);
}
