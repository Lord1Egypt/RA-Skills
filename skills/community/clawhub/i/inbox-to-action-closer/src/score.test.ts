import { describe, it, expect, vi, afterEach } from 'vitest';
import type { ActionItem } from './types.js';
import {
  assignmentBoost,
  recencyBoost,
  followUpBoost,
  typeWeight,
  scoreItems,
  ASSIGNMENT_BOOST,
  RECENCY_MAX_BOOST,
  FOLLOW_UP_BOOST,
  DEFAULT_TYPE_WEIGHT,
  TYPE_WEIGHT_MAP,
} from './score.js';

function makeItem(overrides: Partial<ActionItem> = {}): ActionItem {
  return {
    id: 'test-1',
    source: 'test',
    sourceType: 'email',
    title: 'Test item',
    summary: 'A test item',
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

// --- Assignment boost (3 tests) ---

describe('assignmentBoost', () => {
  it('returns ASSIGNMENT_BOOST when owner matches currentUser', () => {
    expect(assignmentBoost(makeItem({ owner: 'alice' }), 'alice')).toBe(ASSIGNMENT_BOOST);
  });

  it('returns 0 when owner does not match currentUser', () => {
    expect(assignmentBoost(makeItem({ owner: 'alice' }), 'bob')).toBe(0);
  });

  it('returns 0 when currentUser is undefined', () => {
    expect(assignmentBoost(makeItem({ owner: 'alice' }))).toBe(0);
  });
});

// --- Recency boost (3 tests) ---

describe('recencyBoost', () => {
  const now = new Date('2026-03-25T12:00:00Z');

  it('returns max boost for items updated today (0 days)', () => {
    const item = makeItem({ updatedAt: '2026-03-25T00:00:00Z' });
    expect(recencyBoost(now, item)).toBe(RECENCY_MAX_BOOST);
  });

  it('returns ~7.5 for items updated 7 days ago (midpoint)', () => {
    const item = makeItem({ updatedAt: '2026-03-18T00:00:00Z' });
    expect(recencyBoost(now, item)).toBeCloseTo(7.5, 5);
  });

  it('returns 0 for items updated 14 days ago (boundary)', () => {
    const item = makeItem({ updatedAt: '2026-03-11T00:00:00Z' });
    expect(recencyBoost(now, item)).toBe(0);
  });

  it('returns 0 for items updated beyond 14 days (15 days)', () => {
    const item = makeItem({ updatedAt: '2026-03-10T00:00:00Z' });
    expect(recencyBoost(now, item)).toBe(0);
  });

  it('falls back to createdAt when updatedAt is empty', () => {
    const item = makeItem({ updatedAt: '', createdAt: '2026-03-25T00:00:00Z' });
    expect(recencyBoost(now, item)).toBe(RECENCY_MAX_BOOST);
  });

  it('returns 0 when both updatedAt and createdAt are missing', () => {
    const item = makeItem({ updatedAt: '', createdAt: '' });
    expect(recencyBoost(now, item)).toBe(0);
  });
});

// --- Follow-up boost (1 test) ---

describe('followUpBoost', () => {
  it('returns FOLLOW_UP_BOOST when followUpQuestion is truthy and status is open', () => {
    const item = makeItem({ followUpQuestion: 'Need more info?', status: 'open' });
    expect(followUpBoost(item)).toBe(FOLLOW_UP_BOOST);
  });

  it('returns 0 when status is done even with a followUpQuestion', () => {
    const item = makeItem({ followUpQuestion: 'Need more info?', status: 'done' });
    expect(followUpBoost(item)).toBe(0);
  });

  it('returns 0 when followUpQuestion is null', () => {
    const item = makeItem({ followUpQuestion: null, status: 'open' });
    expect(followUpBoost(item)).toBe(0);
  });
});

// --- Type weight ---

describe('typeWeight', () => {
  it('returns correct multiplier for each known source type', () => {
    for (const [source, weight] of Object.entries(TYPE_WEIGHT_MAP)) {
      const item = makeItem({ sourceType: source as ActionItem['sourceType'] });
      expect(typeWeight(item)).toBe(weight);
    }
  });

  it('returns DEFAULT_TYPE_WEIGHT for unknown sourceType', () => {
    const item = makeItem({ sourceType: 'unknown' as ActionItem['sourceType'] });
    expect(typeWeight(item)).toBe(DEFAULT_TYPE_WEIGHT);
  });

  it('returns DEFAULT_TYPE_WEIGHT for missing/undefined sourceType', () => {
    const item = makeItem({ sourceType: undefined as unknown as ActionItem['sourceType'] });
    expect(typeWeight(item)).toBe(DEFAULT_TYPE_WEIGHT);
  });
});

// --- Composite integration (1 test) ---

describe('scoreItems (composite)', () => {
  afterEach(() => {
    vi.useRealTimers();
  });

  it('integrates all six signals with type-weight multiplier', () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date('2026-03-25T12:00:00Z'));

    const item = makeItem({
      dueAt: '2026-03-24T00:00:00Z',       // overdue → 30
      blocker: 'blocked on review',          // → 25
      owner: 'alice',                        // → 10 (currentUser = 'alice')
      updatedAt: '2026-03-25T00:00:00Z',    // 0 days → 15
      followUpQuestion: 'What is the ETA?',  // → 12
      status: 'open',
      sourceType: 'github',                  // weight 1.0
    });

    const [scored] = scoreItems([item], 'alice');
    // raw = 30 + 25 + 10 + 15 + 12 = 92, × 1.0 = 92
    expect(scored.priorityScore).toBe(92);
  });

  it('typeWeight multiplicatively scales the sum', () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date('2026-03-25T12:00:00Z'));

    const item = makeItem({
      dueAt: '2026-03-24T00:00:00Z',       // overdue → 30
      blocker: 'blocked on review',          // → 25
      owner: 'alice',                        // → 10
      updatedAt: '2026-03-25T00:00:00Z',    // 0 days → 15
      followUpQuestion: 'What is the ETA?',  // → 12
      status: 'open',
      sourceType: 'slack',                   // weight 0.8
    });

    const [scored] = scoreItems([item], 'alice');
    // raw = 30 + 25 + 10 + 15 + 12 = 92, × 0.8 = 73.6
    expect(scored.priorityScore).toBeCloseTo(73.6, 5);
  });

  it('default typeWeight (1.0) leaves sum unchanged for unknown sourceType', () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date('2026-03-25T12:00:00Z'));

    const item = makeItem({
      dueAt: '2026-03-24T00:00:00Z',       // overdue → 30
      blocker: 'blocked on review',          // → 25
      owner: 'alice',                        // → 10
      updatedAt: '2026-03-25T00:00:00Z',    // 0 days → 15
      followUpQuestion: 'What is the ETA?',  // → 12
      status: 'open',
      sourceType: 'unknown' as ActionItem['sourceType'], // default weight 1.0
    });

    const [scored] = scoreItems([item], 'alice');
    // raw = 92, × 1.0 = 92 (unchanged)
    expect(scored.priorityScore).toBe(92);
  });
});
