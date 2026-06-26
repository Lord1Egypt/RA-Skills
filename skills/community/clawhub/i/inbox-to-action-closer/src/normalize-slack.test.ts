import { describe, it, expect } from 'vitest';
import { normalizeSlack } from './normalize-slack.js';
import type { ActionItem } from './types.js';

function makeSlackMsg(overrides: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    ts: '1700000000.000100',
    channel: 'C01ABC',
    text: 'Ship the fix today',
    user: 'U_ALICE',
    permalink: 'https://myteam.slack.com/archives/C01ABC/p1700000000000100',
    ...overrides,
  };
}

describe('normalizeSlack', () => {
  // ---- 1. valid Slack message ----
  it('maps a complete Slack message to a valid ActionItem', () => {
    const raw = [makeSlackMsg()];
    const result = normalizeSlack(raw);

    expect(result).toHaveLength(1);
    const item = result[0];
    expect(item.id).toBe('slack:C01ABC-1700000000.000100');
    expect(item.sourceType).toBe('slack');
    expect(item.source).toBe('slack:C01ABC');
    expect(item.title).toBe('Ship the fix today');
    expect(item.summary).toBe('Ship the fix today');
    expect(item.owner).toBe('U_ALICE');
    expect(item.participants).toContain('U_ALICE');
    expect(item.url).toBe('https://myteam.slack.com/archives/C01ABC/p1700000000000100');
    expect(item.dueAt).toBeNull();
    expect(item.status).toBe('open');
    expect(item.confidence).toBe(1.0);
    expect(item.dedupeKeys).toContain(item.url);
    expect(item.dedupeKeys).toContain('ship the fix today');
  });

  // ---- 2. Slack thread with participants ----
  it('captures thread participants from reply_users', () => {
    const raw = [makeSlackMsg({
      reply_users: ['U_BOB', 'U_CAROL'],
      thread_ts: '1700000000.000100',
      latest_reply: '1700000900.000200',
    })];
    const result = normalizeSlack(raw);

    expect(result).toHaveLength(1);
    const item = result[0];
    // sender + reply users, no duplicates
    expect(item.participants).toEqual(['U_ALICE', 'U_BOB', 'U_CAROL']);
    // updatedAt reflects latest_reply
    expect(new Date(item.updatedAt).getTime()).toBeGreaterThan(new Date(item.createdAt).getTime());
  });

  // ---- 3. Slack DM awaiting reply ----
  it('handles a DM channel message awaiting reply', () => {
    const raw = [makeSlackMsg({
      channel: 'D01PRIVATE',
      text: 'Can you review my PR?',
      permalink: '',
    })];
    const result = normalizeSlack(raw);

    expect(result).toHaveLength(1);
    const item = result[0];
    expect(item.id).toBe('slack:D01PRIVATE-1700000000.000100');
    expect(item.source).toBe('slack:D01PRIVATE');
    expect(item.title).toBe('Can you review my PR?');
    // Without permalink, URL is constructed
    expect(item.url).toContain('D01PRIVATE');
    expect(item.confidence).toBe(1.0);
  });

  // ---- 4a. Slack missing user field fallback ----
  it('degrades confidence and sets owner to unknown when user is missing', () => {
    const raw = [makeSlackMsg({ user: undefined })];
    const result = normalizeSlack(raw);

    expect(result).toHaveLength(1);
    const item = result[0];
    expect(item.owner).toBe('unknown');
    expect(item.confidence).toBeLessThan(1.0);
    expect(item.confidence).toBeGreaterThanOrEqual(0.7);
    expect(item.participants).toEqual([]);
  });

  // ---- 4b. Slack missing text field fallback ----
  it('degrades confidence and uses fallback title when text is missing', () => {
    const raw = [makeSlackMsg({ text: undefined })];
    const result = normalizeSlack(raw);

    expect(result).toHaveLength(1);
    const item = result[0];
    expect(item.title).toBe('Message in C01ABC');
    expect(item.summary).toBe('');
    expect(item.confidence).toBeLessThan(1.0);
    expect(item.confidence).toBeGreaterThanOrEqual(0.7);
  });

  // ---- 5. Slack empty/malformed input ----
  it('returns empty array for non-array and malformed inputs without throwing', () => {
    expect(normalizeSlack(null)).toEqual([]);
    expect(normalizeSlack(undefined)).toEqual([]);
    expect(normalizeSlack('not-an-array')).toEqual([]);
    expect(normalizeSlack(42)).toEqual([]);
    expect(normalizeSlack({})).toEqual([]);
    expect(normalizeSlack([])).toEqual([]);
    // Array with non-objects
    expect(normalizeSlack([null, 123, 'str'])).toEqual([]);
    // Object missing required ts/channel
    expect(normalizeSlack([{ text: 'hello' }])).toEqual([]);
  });

  // ---- 6. Thread reply references parent URL ----
  it('constructs parent-thread URL for thread replies', () => {
    const raw = [makeSlackMsg({
      ts: '1700000500.000300',
      thread_ts: '1700000000.000100',
      permalink: undefined,
    })];
    const result = normalizeSlack(raw);

    expect(result).toHaveLength(1);
    const item = result[0];
    // Reply should reference the parent thread
    expect(item.url).toBe('https://slack.com/archives/C01ABC/p1700000000000100');
    expect(item.id).toBe('slack:C01ABC-1700000500.000300');
  });

  // ---- 7. Consistent ID format ----
  it('produces deterministic slack:{channel}-{ts} IDs', () => {
    const raw = [
      makeSlackMsg({ ts: '1700000000.000100', channel: 'C01' }),
      makeSlackMsg({ ts: '1700000000.000200', channel: 'C02' }),
    ];
    const result = normalizeSlack(raw);

    expect(result[0].id).toBe('slack:C01-1700000000.000100');
    expect(result[1].id).toBe('slack:C02-1700000000.000200');
    // All IDs match the pattern
    for (const item of result) {
      expect(item.id).toMatch(/^slack:[A-Z0-9]+-\d+\.\d+$/);
    }
  });

  // ---- 8. dedupeKeys always includes source URL ----
  it('always includes source URL in dedupeKeys', () => {
    const raw = [makeSlackMsg(), makeSlackMsg({ text: '', permalink: '' })];
    const result = normalizeSlack(raw);

    for (const item of result) {
      expect(item.dedupeKeys.length).toBeGreaterThanOrEqual(1);
      expect(item.dedupeKeys[0]).toContain('slack.com/archives');
    }
  });

  // ---- 9. All returned items satisfy ActionItem interface ----
  it('returns items with all required ActionItem fields', () => {
    const result = normalizeSlack([makeSlackMsg()]);
    const item = result[0];

    const requiredStringFields: (keyof ActionItem)[] = [
      'id', 'source', 'title', 'summary', 'owner', 'createdAt', 'updatedAt', 'url',
    ];
    for (const field of requiredStringFields) {
      expect(typeof item[field]).toBe('string');
    }
    expect(Array.isArray(item.participants)).toBe(true);
    expect(Array.isArray(item.dedupeKeys)).toBe(true);
    expect(typeof item.priorityScore).toBe('number');
    expect(typeof item.confidence).toBe('number');
    expect(item.sourceType).toBe('slack');
    // Nullable fields are null by default
    expect(item.blocker).toBeNull();
    expect(item.replyDraft).toBeNull();
    expect(item.followUpQuestion).toBeNull();
    expect(item.suggestedNextAction).toBeNull();
  });

  // ---- 10. Skips invalid entries but processes valid ones ----
  it('skips invalid entries and processes valid ones in the same array', () => {
    const raw = [
      null,
      { text: 'no ts or channel' },
      makeSlackMsg({ ts: '1700000000.000100' }),
      42,
    ];
    const result = normalizeSlack(raw);
    expect(result).toHaveLength(1);
    expect(result[0].title).toBe('Ship the fix today');
  });

  // ---- 11. Multiple missing fields compound confidence degradation ----
  it('degrades confidence further when both user and text are missing', () => {
    const raw = [makeSlackMsg({ user: undefined, text: undefined })];
    const result = normalizeSlack(raw);

    expect(result).toHaveLength(1);
    expect(result[0].confidence).toBe(0.7);
  });

  // ---- 12. Duplicate reply_users are not duplicated in participants ----
  it('deduplicates reply_users against the sender', () => {
    const raw = [makeSlackMsg({
      user: 'U_ALICE',
      reply_users: ['U_ALICE', 'U_BOB', 'U_BOB'],
    })];
    const result = normalizeSlack(raw);

    expect(result[0].participants).toEqual(['U_ALICE', 'U_BOB']);
  });

  // ---- 13. Thread root (thread_ts === ts) is not treated as a reply ----
  it('treats thread root messages as top-level, not replies', () => {
    const raw = [makeSlackMsg({
      thread_ts: '1700000000.000100',
      ts: '1700000000.000100',
      permalink: '',
    })];
    const result = normalizeSlack(raw);

    // URL should point to the message itself, not a parent
    expect(result[0].url).toBe('https://slack.com/archives/C01ABC/p1700000000000100');
  });

  // ---- 14. createdAt falls back to epoch for unparseable timestamp ----
  it('falls back to epoch for non-numeric timestamp', () => {
    const raw = [makeSlackMsg({ ts: 'not-a-number' })];
    const result = normalizeSlack(raw);

    expect(result).toHaveLength(1);
    expect(result[0].createdAt).toBe(new Date(0).toISOString());
  });
});
