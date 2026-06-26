import { describe, it, expect } from 'vitest';
import type { ActionItem } from './types.js';
import {
  URGENT_THRESHOLD,
  ACTIVE_THRESHOLD,
  groupByTier,
  renderMarkdown,
  renderItem,
  renderJSON,
  escapeMarkdown,
} from './render.js';

function makeItem(overrides: Partial<ActionItem> = {}): ActionItem {
  return {
    id: 'test-1',
    source: 'test-source',
    sourceType: 'email',
    title: 'Test item',
    summary: 'A test summary',
    owner: 'alice',
    participants: ['alice'],
    createdAt: '2026-03-20T00:00:00Z',
    updatedAt: '2026-03-25T00:00:00Z',
    dueAt: null,
    url: 'https://example.com/1',
    status: 'open',
    priorityScore: 0,
    blocker: null,
    replyDraft: null,
    followUpQuestion: null,
    suggestedNextAction: null,
    dedupeKeys: [],
    confidence: 1.0,
    ...overrides,
  };
}

describe('renderMarkdown', () => {
  it('renders mixed tiers correctly with items in each bucket', () => {
    const items = [
      makeItem({ id: 'u1', title: 'Urgent task', priorityScore: 80 }),
      makeItem({ id: 'a1', title: 'Active task', priorityScore: 50 }),
      makeItem({ id: 'l1', title: 'Low task', priorityScore: 10 }),
    ];
    const md = renderMarkdown(items);

    expect(md).toContain('## 🔴 Urgent');
    expect(md).toContain('## 🟡 Active');
    expect(md).toContain('## 🟢 Low Priority');
    expect(md).toContain('**Urgent task**');
    expect(md).toContain('**Active task**');
    expect(md).toContain('**Low task**');
  });

  it('omits empty tiers from output', () => {
    const items = [
      makeItem({ id: 'u1', title: 'Urgent only', priorityScore: 90 }),
    ];
    const md = renderMarkdown(items);

    expect(md).toContain('## 🔴 Urgent');
    expect(md).not.toContain('## 🟡 Active');
    expect(md).not.toContain('## 🟢 Low Priority');
  });

  it('renders all optional fields when present on an item', () => {
    const items = [
      makeItem({
        id: 'full',
        title: 'Full item',
        priorityScore: 80,
        blocker: 'Blocked on legal review',
        replyDraft: 'Thanks, will follow up.',
        followUpQuestion: 'When is the deadline?',
        suggestedNextAction: 'Schedule a meeting',
      }),
    ];
    const md = renderMarkdown(items);

    expect(md).toContain('⚠ Blocker: Blocked on legal review');
    expect(md).toContain('Reply draft: Thanks, will follow up.');
    expect(md).toContain('Follow-up: When is the deadline?');
    expect(md).toContain('Next action: Schedule a meeting');
    expect(md).toContain('Link: [https://example.com/1](https://example.com/1)');
  });

  it('renders minimal item with only required fields', () => {
    const items = [
      makeItem({
        id: 'min',
        title: 'Minimal',
        priorityScore: 50,
        owner: '',
        dueAt: null,
        status: 'open',
        blocker: null,
        replyDraft: null,
        followUpQuestion: null,
        suggestedNextAction: null,
        url: '',
      }),
    ];
    const md = renderMarkdown(items);

    expect(md).toContain('- [ ] **Minimal** (test-source) — A test summary');
    expect(md).not.toContain('Blocker');
    expect(md).not.toContain('Reply draft');
    expect(md).not.toContain('Follow-up');
    expect(md).not.toContain('Next action');
  });

  it('returns a meaningful no-items message for empty input', () => {
    const md = renderMarkdown([]);

    expect(md).toContain('Action Board');
    expect(md).toContain('No action items');
    expect(md.length).toBeGreaterThan(0);
  });

  it('escapes pipes and backticks in title and summary', () => {
    const items = [
      makeItem({
        id: 'esc',
        title: 'Fix | table `break`',
        summary: 'Pipes | and `backticks` in summary',
        priorityScore: 50,
      }),
    ];
    const md = renderMarkdown(items);

    expect(md).toContain('Fix \\| table \\`break\\`');
    expect(md).toContain('Pipes \\| and \\`backticks\\` in summary');
  });
});

describe('renderItem', () => {
  it('renders checkbox line with title, source, and summary', () => {
    const item = makeItem({ title: 'Review PR', source: 'github-repo', summary: 'Needs review' });
    const result = renderItem(item);

    expect(result).toContain('- [ ] **Review PR** (github-repo) — Needs review');
  });

  it('includes all metadata fields when present', () => {
    const item = makeItem({
      owner: 'bob',
      dueAt: '2026-03-28T00:00:00Z',
      status: 'in_progress',
      blocker: 'Waiting on design',
      replyDraft: 'Will address tomorrow',
      followUpQuestion: 'Any blockers?',
      suggestedNextAction: 'Ping designer',
      url: 'https://example.com/pr/42',
    });
    const result = renderItem(item);

    expect(result).toContain('  Owner: bob');
    expect(result).toContain('  Due: 2026-03-28T00:00:00Z');
    expect(result).toContain('  Status: in_progress');
    expect(result).toContain('  ⚠ Blocker: Waiting on design');
    expect(result).toContain('  Reply draft: Will address tomorrow');
    expect(result).toContain('  Follow-up: Any blockers?');
    expect(result).toContain('  Next action: Ping designer');
    expect(result).toContain('  Link: [https://example.com/pr/42](https://example.com/pr/42)');
  });

  it('omits metadata lines for null or empty fields', () => {
    const item = makeItem({
      owner: '',
      dueAt: null,
      blocker: null,
      replyDraft: null,
      followUpQuestion: null,
      suggestedNextAction: null,
      url: '',
    });
    const result = renderItem(item);

    expect(result).not.toContain('Owner:');
    expect(result).not.toContain('Due:');
    expect(result).not.toContain('Blocker:');
    expect(result).not.toContain('Reply draft:');
    expect(result).not.toContain('Follow-up:');
    expect(result).not.toContain('Next action:');
    expect(result).not.toContain('Link:');
  });

  it('shows warning indicator for blocker items', () => {
    const item = makeItem({ blocker: 'Blocked on API changes' });
    const result = renderItem(item);

    expect(result).toContain('⚠ Blocker: Blocked on API changes');
  });

  it('renders source URL as a markdown link on its own indented line', () => {
    const item = makeItem({ url: 'https://github.com/org/repo/issues/7' });
    const result = renderItem(item);
    const lines = result.split('\n');
    const linkLine = lines.find(l => l.includes('Link:'));

    expect(linkLine).toBe('  Link: [https://github.com/org/repo/issues/7](https://github.com/org/repo/issues/7)');
  });
});

describe('escapeMarkdown', () => {
  it('escapes pipe characters', () => {
    expect(escapeMarkdown('a | b')).toBe('a \\| b');
  });

  it('escapes backtick characters', () => {
    expect(escapeMarkdown('use `code` here')).toBe('use \\`code\\` here');
  });

  it('escapes both pipes and backticks in the same string', () => {
    expect(escapeMarkdown('col1 | `val`')).toBe('col1 \\| \\`val\\`');
  });

  it('returns plain text unchanged', () => {
    expect(escapeMarkdown('no special chars')).toBe('no special chars');
  });
});

describe('renderJSON', () => {
  it('produces valid JSON with items distributed across all three tiers', () => {
    const items = [
      makeItem({ id: 'u1', title: 'Urgent fix', priorityScore: 85 }),
      makeItem({ id: 'a1', title: 'Active task', priorityScore: 50 }),
      makeItem({ id: 'l1', title: 'Low item', priorityScore: 10, blocker: null, replyDraft: null }),
    ];
    const now = new Date('2026-03-25T10:00:00Z');
    const json = renderJSON(items, now);
    const parsed = JSON.parse(json);

    expect(parsed.totalItems).toBe(3);
    expect(parsed.tiers.urgent).toHaveLength(1);
    expect(parsed.tiers.active).toHaveLength(1);
    expect(parsed.tiers.low).toHaveLength(1);
    expect(parsed.tiers.urgent[0].id).toBe('u1');
    expect(parsed.tiers.active[0].id).toBe('a1');
    expect(parsed.tiers.low[0].id).toBe('l1');
    expect(parsed.metadata.tierThresholds.urgent).toBe(URGENT_THRESHOLD);
    expect(parsed.metadata.tierThresholds.active).toBe(ACTIVE_THRESHOLD);
    // Ensure no 'undefined' strings in output
    expect(json).not.toContain('"undefined"');
  });

  it('uses now parameter for deterministic generatedAt', () => {
    const fixedTime = new Date('2026-06-15T08:30:00Z');
    const json = renderJSON([], fixedTime);
    const parsed = JSON.parse(json);

    expect(parsed.generatedAt).toBe('2026-06-15T08:30:00.000Z');
  });

  it('produces valid JSON with zero counts and empty tier arrays for empty input', () => {
    const now = new Date('2026-03-25T12:00:00Z');
    const json = renderJSON([], now);
    const parsed = JSON.parse(json);

    expect(parsed.totalItems).toBe(0);
    expect(parsed.tiers.urgent).toEqual([]);
    expect(parsed.tiers.active).toEqual([]);
    expect(parsed.tiers.low).toEqual([]);
    expect(parsed.generatedAt).toBe('2026-03-25T12:00:00.000Z');
    expect(parsed.metadata.tierThresholds).toEqual({
      urgent: URGENT_THRESHOLD,
      active: ACTIVE_THRESHOLD,
    });
  });
});
