import { describe, it, expect } from 'vitest';
import { matchByUrl, matchByTitle, matchByTimestamp, deduplicateItems, normalizeUrl } from '../src/dedupe.js';
import type { DedupedItem } from '../src/dedupe.js';
import type { ActionItem } from '../src/types.js';

function makeItem(overrides: Partial<ActionItem> = {}): ActionItem {
  return {
    id: 'test-1',
    source: 'test',
    sourceType: 'slack',
    title: 'Test item',
    summary: 'A test action item',
    owner: 'user@example.com',
    participants: [],
    createdAt: '2026-03-01T00:00:00Z',
    updatedAt: '2026-03-01T00:00:00Z',
    dueAt: null,
    url: '',
    status: 'open',
    priorityScore: 0,
    blocker: null,
    replyDraft: null,
    followUpQuestion: null,
    suggestedNextAction: null,
    dedupeKeys: [],
    confidence: 1,
    ...overrides,
  };
}

describe('matchByUrl', () => {
  it('returns 1.0 for URLs differing only in protocol and trailing slash', () => {
    const a = makeItem({ url: 'http://example.com/page/' });
    const b = makeItem({ url: 'https://example.com/page' });
    expect(matchByUrl(a, b)).toBe(1.0);
  });

  it('returns 1.0 for URLs differing only in utm_* tracking params', () => {
    const a = makeItem({ url: 'https://example.com/page?utm_source=twitter&utm_medium=social' });
    const b = makeItem({ url: 'https://example.com/page' });
    expect(matchByUrl(a, b)).toBe(1.0);
  });

  it('returns 0.7 for same domain+path but different non-tracking query params', () => {
    const a = makeItem({ url: 'https://example.com/page?tab=overview' });
    const b = makeItem({ url: 'https://example.com/page?tab=details' });
    expect(matchByUrl(a, b)).toBe(0.7);
  });

  it('returns 0.0 when either item has no URL', () => {
    const a = makeItem({ url: 'https://example.com/page' });
    const b = makeItem({ url: '' });
    expect(matchByUrl(a, b)).toBe(0.0);
    expect(matchByUrl(b, a)).toBe(0.0);
  });

  it('returns 0.0 for completely different domains', () => {
    const a = makeItem({ url: 'https://example.com/page' });
    const b = makeItem({ url: 'https://other.com/page' });
    expect(matchByUrl(a, b)).toBe(0.0);
  });
});

describe('matchByTitle', () => {
  it('returns 1.0 for exact title match after normalization', () => {
    const a = makeItem({ title: 'Fix the login bug' });
    const b = makeItem({ title: 'fix the login bug' });
    expect(matchByTitle(a, b)).toBe(1.0);
  });

  it('returns 1.0 for case-insensitive match with extra whitespace', () => {
    const a = makeItem({ title: '  Review  PR  #42  ' });
    const b = makeItem({ title: 'review pr #42' });
    expect(matchByTitle(a, b)).toBe(1.0);
  });

  it('returns high similarity for overlapping titles', () => {
    const a = makeItem({ title: 'Update user authentication flow' });
    const b = makeItem({ title: 'Update user authentication logic' });
    const score = matchByTitle(a, b);
    expect(score).toBeGreaterThan(0.5);
    expect(score).toBeLessThan(1.0);
  });

  it('returns low similarity for barely overlapping titles', () => {
    const a = makeItem({ title: 'Fix database connection pooling' });
    const b = makeItem({ title: 'Design new landing page layout' });
    const score = matchByTitle(a, b);
    expect(score).toBeLessThan(0.3);
  });

  it('returns 0.0 when either title is empty', () => {
    const a = makeItem({ title: 'Some title' });
    const b = makeItem({ title: '' });
    expect(matchByTitle(a, b)).toBe(0.0);
    expect(matchByTitle(b, a)).toBe(0.0);
  });

  it('returns 0.0 when either title is null', () => {
    const a = makeItem({ title: 'Some title' });
    const b = makeItem({ title: null as unknown as string });
    expect(matchByTitle(a, b)).toBe(0.0);
    expect(matchByTitle(b, a)).toBe(0.0);
  });

  it('returns 1.0 for short title exact match', () => {
    const a = makeItem({ title: 'ab' });
    const b = makeItem({ title: 'AB' });
    expect(matchByTitle(a, b)).toBe(1.0);
  });

  it('caps score at 0.0 for non-exact short titles (<=2 chars)', () => {
    const a = makeItem({ title: 'ab' });
    const b = makeItem({ title: 'ac' });
    expect(matchByTitle(a, b)).toBe(0.0);
  });

  it('produces reasonable score for word-reorder similarity', () => {
    const a = makeItem({ title: 'deploy backend service' });
    const b = makeItem({ title: 'backend service deploy' });
    const score = matchByTitle(a, b);
    expect(score).toBeGreaterThan(0.5);
    expect(score).toBeLessThan(1.0);
  });

  it('handles unicode titles correctly', () => {
    const a = makeItem({ title: 'Revue des tâches prioritaires' });
    const b = makeItem({ title: 'Revue des tâches prioritaires' });
    expect(matchByTitle(a, b)).toBe(1.0);
  });
});

describe('matchByTimestamp', () => {
  it('returns 1.0 for items created within 1 hour of each other', () => {
    const a = makeItem({ createdAt: '2026-03-01T00:00:00Z' });
    const b = makeItem({ createdAt: '2026-03-01T00:30:00Z' });
    expect(matchByTimestamp(a, b)).toBe(1.0);
  });

  it('returns ~0.5 for items created ~36 hours apart', () => {
    const a = makeItem({ createdAt: '2026-03-01T00:00:00Z' });
    const b = makeItem({ createdAt: '2026-03-02T12:00:00Z' });
    const score = matchByTimestamp(a, b);
    expect(score).toBeCloseTo(0.5, 1);
  });

  it('returns 0.0 for items created more than 72 hours apart', () => {
    const a = makeItem({ createdAt: '2026-03-01T00:00:00Z' });
    const b = makeItem({ createdAt: '2026-03-05T00:00:00Z' });
    expect(matchByTimestamp(a, b)).toBe(0.0);
  });
});

describe('deduplicateItems', () => {
  it('merges same-source items with matching URLs and similar titles', () => {
    const a = makeItem({
      id: 'a',
      sourceType: 'slack',
      url: 'https://example.com/issue/1',
      title: 'Fix authentication flow in login service',
      createdAt: '2026-03-01T00:00:00Z',
    });
    const b = makeItem({
      id: 'b',
      sourceType: 'slack',
      url: 'https://example.com/issue/1',
      title: 'Fix authentication flow in login module',
      createdAt: '2026-03-01T00:30:00Z',
    });
    const result = deduplicateItems([a, b]);
    expect(result).toHaveLength(1);
    expect(result[0].createdAt).toBe('2026-03-01T00:00:00Z');
  });

  it('merges cross-source items with high confidence (>=0.85)', () => {
    const a = makeItem({
      id: 'a',
      sourceType: 'slack',
      url: 'https://example.com/issue/1',
      title: 'Fix authentication flow in login service',
      createdAt: '2026-03-01T00:00:00Z',
    });
    const b = makeItem({
      id: 'b',
      sourceType: 'github',
      url: 'https://example.com/issue/1',
      title: 'Fix authentication flow in login service',
      createdAt: '2026-03-01T00:00:00Z',
    });
    const result = deduplicateItems([a, b]);
    expect(result).toHaveLength(1);
  });

  it('does not merge cross-source items with confidence below 0.85', () => {
    const a = makeItem({
      id: 'a',
      sourceType: 'slack',
      url: 'https://example.com/issue/1',
      title: 'Fix authentication flow in login service',
      createdAt: '2026-03-01T00:00:00Z',
    });
    const b = makeItem({
      id: 'b',
      sourceType: 'github',
      url: 'https://example.com/issue/1',
      title: 'Deploy new monitoring dashboard update',
      createdAt: '2026-03-01T00:00:00Z',
    });
    const result = deduplicateItems([a, b]);
    expect(result).toHaveLength(2);
  });

  it('preserves non-null fields from secondary where primary field is null', () => {
    const a = makeItem({
      id: 'a',
      sourceType: 'slack',
      url: 'https://example.com/issue/1',
      title: 'Fix authentication flow in login service',
      createdAt: '2026-03-01T00:00:00Z',
      dueAt: null,
      blocker: null,
    });
    const b = makeItem({
      id: 'b',
      sourceType: 'slack',
      url: 'https://example.com/issue/1',
      title: 'Fix authentication flow in login service',
      createdAt: '2026-03-01T00:30:00Z',
      dueAt: '2026-03-10T00:00:00Z',
      blocker: 'Waiting on API key',
    });
    const result = deduplicateItems([a, b]);
    expect(result).toHaveLength(1);
    expect(result[0].dueAt).toBe('2026-03-10T00:00:00Z');
    expect(result[0].blocker).toBe('Waiting on API key');
  });

  it('unions dedupeKeys from both source items', () => {
    const a = makeItem({
      id: 'a',
      sourceType: 'slack',
      url: 'https://example.com/issue/1',
      title: 'Fix authentication flow in login service',
      createdAt: '2026-03-01T00:00:00Z',
      dedupeKeys: ['key-1', 'key-2'],
    });
    const b = makeItem({
      id: 'b',
      sourceType: 'slack',
      url: 'https://example.com/issue/1',
      title: 'Fix authentication flow in login service',
      createdAt: '2026-03-01T00:30:00Z',
      dedupeKeys: ['key-2', 'key-3'],
    });
    const result = deduplicateItems([a, b]);
    expect(result).toHaveLength(1);
    expect(result[0].dedupeKeys).toEqual(expect.arrayContaining(['key-1', 'key-2', 'key-3']));
    expect(result[0].dedupeKeys).toHaveLength(3);
  });

  it('populates mergedFrom with secondary item source and id', () => {
    const a = makeItem({
      id: 'a',
      source: 'slack-workspace',
      sourceType: 'slack',
      url: 'https://example.com/issue/1',
      title: 'Fix authentication flow in login service',
      createdAt: '2026-03-01T00:00:00Z',
    });
    const b = makeItem({
      id: 'b',
      source: 'slack-channel',
      sourceType: 'slack',
      url: 'https://example.com/issue/1',
      title: 'Fix authentication flow in login service',
      createdAt: '2026-03-01T00:30:00Z',
    });
    const result = deduplicateItems([a, b]) as DedupedItem[];
    expect(result).toHaveLength(1);
    expect(result[0].mergedFrom).toEqual([{ source: 'slack-channel', id: 'b' }]);
  });

  it('does not mutate the input array or items', () => {
    const a = makeItem({
      id: 'a',
      sourceType: 'slack',
      url: 'https://example.com/issue/1',
      title: 'Fix authentication flow in login service',
      createdAt: '2026-03-01T00:00:00Z',
      dedupeKeys: ['key-1'],
    });
    const b = makeItem({
      id: 'b',
      sourceType: 'slack',
      url: 'https://example.com/issue/1',
      title: 'Fix authentication flow in login service',
      createdAt: '2026-03-01T00:30:00Z',
      dedupeKeys: ['key-2'],
    });
    const input = [a, b];
    const aCopy = JSON.parse(JSON.stringify(a));
    const bCopy = JSON.parse(JSON.stringify(b));
    deduplicateItems(input);
    expect(input).toHaveLength(2);
    expect(input[0]).toEqual(aCopy);
    expect(input[1]).toEqual(bCopy);
  });

  it('produces identical results regardless of input order', () => {
    const a = makeItem({
      id: 'a',
      sourceType: 'slack',
      url: 'https://example.com/issue/1',
      title: 'Fix authentication flow in login service',
      createdAt: '2026-03-01T00:00:00Z',
    });
    const b = makeItem({
      id: 'b',
      sourceType: 'slack',
      url: 'https://example.com/issue/1',
      title: 'Fix authentication flow in login service',
      createdAt: '2026-03-01T00:30:00Z',
    });
    const c = makeItem({
      id: 'c',
      sourceType: 'slack',
      url: 'https://other.com/different',
      title: 'Unrelated task about deployment',
      createdAt: '2026-03-10T00:00:00Z',
    });
    const result1 = deduplicateItems([a, b, c]);
    const result2 = deduplicateItems([c, b, a]);
    const result3 = deduplicateItems([b, c, a]);
    expect(result1).toEqual(result2);
    expect(result1).toEqual(result3);
  });

  it('merges A and B while C stays when only A-B match', () => {
    const a = makeItem({
      id: 'a',
      sourceType: 'slack',
      url: 'https://example.com/issue/1',
      title: 'Fix authentication flow in login service',
      createdAt: '2026-03-01T00:00:00Z',
    });
    const b = makeItem({
      id: 'b',
      sourceType: 'slack',
      url: 'https://example.com/issue/1',
      title: 'Fix authentication flow in login service',
      createdAt: '2026-03-01T00:30:00Z',
    });
    const c = makeItem({
      id: 'c',
      sourceType: 'slack',
      url: 'https://other.com/page',
      title: 'Completely different task about infrastructure',
      createdAt: '2026-03-10T00:00:00Z',
    });
    const result = deduplicateItems([a, b, c]);
    expect(result).toHaveLength(2);
    const merged = result.find((r) => (r as DedupedItem).mergedFrom !== undefined) as DedupedItem;
    expect(merged).toBeDefined();
    expect(merged.id).toBe('a');
    expect(merged.mergedFrom).toEqual([{ source: 'test', id: 'b' }]);
    const kept = result.find((r) => r.id === 'c');
    expect(kept).toBeDefined();
  });

  it('returns all items when none match', () => {
    const items = [
      makeItem({ id: 'a', url: 'https://a.com', title: 'Alpha task', createdAt: '2026-01-01T00:00:00Z' }),
      makeItem({ id: 'b', url: 'https://b.com', title: 'Beta task', createdAt: '2026-02-01T00:00:00Z' }),
      makeItem({ id: 'c', url: 'https://c.com', title: 'Gamma task', createdAt: '2026-03-01T00:00:00Z' }),
    ];
    const result = deduplicateItems(items);
    expect(result).toHaveLength(3);
  });

  it('returns empty array for empty input', () => {
    expect(deduplicateItems([])).toEqual([]);
  });

  it('returns a copy of the single item for single-element input', () => {
    const item = makeItem({ id: 'only' });
    const result = deduplicateItems([item]);
    expect(result).toHaveLength(1);
    expect(result[0]).toEqual(item);
    expect(result[0]).not.toBe(item);
  });

  it('breaks confidence ties by earliest createdAt', () => {
    // A can merge with both B and C (same confidence).
    // B has earlier createdAt than C, so A-B pair has earlier earliest => merges first.
    // C remains unmerged.
    const a = makeItem({
      id: 'a',
      sourceType: 'slack',
      url: 'https://example.com/issue/1',
      title: 'Fix authentication flow in login service',
      createdAt: '2026-03-01T00:00:00Z',
    });
    const b = makeItem({
      id: 'b',
      sourceType: 'slack',
      url: 'https://example.com/issue/1',
      title: 'Fix authentication flow in login service',
      createdAt: '2026-03-01T00:10:00Z',
    });
    const c = makeItem({
      id: 'c',
      sourceType: 'slack',
      url: 'https://example.com/issue/1',
      title: 'Fix authentication flow in login service',
      createdAt: '2026-03-01T00:20:00Z',
    });
    const result = deduplicateItems([a, b, c]);
    expect(result).toHaveLength(2);
    const merged = result.find((r) => (r as DedupedItem).mergedFrom !== undefined) as DedupedItem;
    expect(merged).toBeDefined();
    // A merges with B (earlier pair), C stays
    expect(merged.id).toBe('a');
    const unmerged = result.find((r) => (r as DedupedItem).mergedFrom === undefined);
    expect(unmerged).toBeDefined();
    expect(unmerged!.id).toBe('c');
  });

  it('does not merge items with no URL even with matching title and timestamp', () => {
    const a = makeItem({
      id: 'a',
      sourceType: 'slack',
      url: '',
      title: 'Fix authentication flow in login service',
      createdAt: '2026-03-01T00:00:00Z',
    });
    const b = makeItem({
      id: 'b',
      sourceType: 'slack',
      url: '',
      title: 'Fix authentication flow in login service',
      createdAt: '2026-03-01T00:30:00Z',
    });
    // Fixed weights: 0.45*0 + 0.35*1.0 + 0.20*1.0 = 0.55 < 0.75 threshold
    const result = deduplicateItems([a, b]);
    expect(result).toHaveLength(2);
  });

  it('does not merge items with no title even with matching URL and timestamp', () => {
    const a = makeItem({
      id: 'a',
      sourceType: 'slack',
      url: 'https://example.com/issue/1',
      title: '',
      createdAt: '2026-03-01T00:00:00Z',
    });
    const b = makeItem({
      id: 'b',
      sourceType: 'slack',
      url: 'https://example.com/issue/1',
      title: '',
      createdAt: '2026-03-01T00:30:00Z',
    });
    // Fixed weights: 0.45*1.0 + 0.35*0 + 0.20*1.0 = 0.65 < 0.75 threshold
    const result = deduplicateItems([a, b]);
    expect(result).toHaveLength(2);
  });
});

describe('dedupe — URL exact match', () => {
  it('merges two items with identical URLs into one with both source IDs in dedupeKeys', () => {
    const a = makeItem({
      id: 'url-a',
      sourceType: 'slack',
      url: 'https://github.com/org/repo/issues/42',
      title: 'Fix login timeout on mobile devices',
      createdAt: '2026-03-10T10:00:00Z',
      dedupeKeys: ['slack-msg-100'],
    });
    const b = makeItem({
      id: 'url-b',
      sourceType: 'slack',
      url: 'https://github.com/org/repo/issues/42',
      title: 'Fix login timeout on mobile devices',
      createdAt: '2026-03-10T10:05:00Z',
      dedupeKeys: ['slack-msg-200'],
    });
    const result = deduplicateItems([a, b]);
    expect(result).toHaveLength(1);
    expect(result[0].dedupeKeys).toEqual(expect.arrayContaining(['slack-msg-100', 'slack-msg-200']));
    expect(result[0].dedupeKeys).toHaveLength(2);
    expect(result[0].confidence).toBeGreaterThanOrEqual(0.75);
  });

  it('does NOT merge two items with different URLs even when titles match', () => {
    const a = makeItem({
      id: 'url-c',
      sourceType: 'slack',
      url: 'https://github.com/org/repo/issues/42',
      title: 'Fix login timeout on mobile devices',
      createdAt: '2026-03-10T10:00:00Z',
    });
    const b = makeItem({
      id: 'url-d',
      sourceType: 'slack',
      url: 'https://jira.company.com/browse/PROJ-99',
      title: 'Fix login timeout on mobile devices',
      createdAt: '2026-03-10T10:00:00Z',
    });
    // url=0.0, title=1.0, timestamp=1.0 → composite=0.55 < 0.75 threshold
    const result = deduplicateItems([a, b]);
    expect(result).toHaveLength(2);
  });
});

describe('dedupe — title similarity', () => {
  it('merges items with identical titles regardless of case', () => {
    const a = makeItem({
      id: 'title-a',
      sourceType: 'github',
      url: 'https://github.com/org/repo/pull/10',
      title: 'Review Backend API Authentication Changes',
      createdAt: '2026-03-15T08:00:00Z',
      dedupeKeys: ['gh-pr-10'],
    });
    const b = makeItem({
      id: 'title-b',
      sourceType: 'github',
      url: 'https://github.com/org/repo/pull/10',
      title: 'review backend api authentication changes',
      createdAt: '2026-03-15T08:02:00Z',
      dedupeKeys: ['gh-issue-10'],
    });
    const result = deduplicateItems([a, b]);
    expect(result).toHaveLength(1);
    expect(result[0].dedupeKeys).toEqual(expect.arrayContaining(['gh-pr-10', 'gh-issue-10']));
    expect(result[0].confidence).toBeGreaterThanOrEqual(0.75);
  });

  it('merges items whose titles differ only by whitespace or punctuation', () => {
    const a = makeItem({
      id: 'title-c',
      sourceType: 'slack',
      url: 'https://example.com/task/5',
      title: 'Update user onboarding flow',
      createdAt: '2026-03-15T09:00:00Z',
    });
    const b = makeItem({
      id: 'title-d',
      sourceType: 'slack',
      url: 'https://example.com/task/5',
      title: 'Update  user  onboarding  flow.',
      createdAt: '2026-03-15T09:01:00Z',
    });
    // Normalized: "update user onboarding flow" vs "update user onboarding flow."
    // High dice coefficient (~0.98) plus same URL → merges
    const result = deduplicateItems([a, b]);
    expect(result).toHaveLength(1);
  });

  it('does NOT merge items with less than 70% title similarity', () => {
    const a = makeItem({
      id: 'title-e',
      sourceType: 'trello',
      url: '',
      title: 'Fix database connection pooling',
      createdAt: '2026-03-15T10:00:00Z',
    });
    const b = makeItem({
      id: 'title-f',
      sourceType: 'trello',
      url: '',
      title: 'Deploy monitoring dashboard',
      createdAt: '2026-03-15T10:00:00Z',
    });
    // url=0, title<0.20, timestamp=1.0 → composite well below 0.75
    const result = deduplicateItems([a, b]);
    expect(result).toHaveLength(2);
  });

  it('does NOT auto-merge when one title is a substring of the other unless similarity exceeds threshold', () => {
    const a = makeItem({
      id: 'title-g',
      sourceType: 'notion',
      url: '',
      title: 'Update API endpoint',
      createdAt: '2026-03-15T11:00:00Z',
    });
    const b = makeItem({
      id: 'title-h',
      sourceType: 'notion',
      url: '',
      title: 'Update API endpoint documentation and add comprehensive integration tests',
      createdAt: '2026-03-15T11:00:00Z',
    });
    // url=0, title≈0.47 (substring but large length difference), timestamp=1.0
    // composite ≈ 0 + 0.35*0.47 + 0.20 ≈ 0.365 < 0.75 → no merge
    const result = deduplicateItems([a, b]);
    expect(result).toHaveLength(2);
  });

  it('merges items with unicode titles that have equivalent normalised forms', () => {
    const a = makeItem({
      id: 'title-i',
      sourceType: 'email',
      url: 'https://mail.example.com/thread/abc',
      title: 'Réviser les tâches urgentes du projet',
      createdAt: '2026-03-15T12:00:00Z',
      dedupeKeys: ['email-abc'],
    });
    const b = makeItem({
      id: 'title-j',
      sourceType: 'email',
      url: 'https://mail.example.com/thread/abc',
      title: 'RÉVISER LES TÂCHES URGENTES DU PROJET',
      createdAt: '2026-03-15T12:01:00Z',
      dedupeKeys: ['email-def'],
    });
    // Both normalize to "réviser les tâches urgentes du projet", same URL → merges
    const result = deduplicateItems([a, b]);
    expect(result).toHaveLength(1);
    expect(result[0].dedupeKeys).toEqual(expect.arrayContaining(['email-abc', 'email-def']));
  });
});

describe('dedupe — timestamp proximity', () => {
  it('merges items created within 5 minutes with similar titles', () => {
    const a = makeItem({
      id: 'ts-a',
      sourceType: 'slack',
      url: 'https://example.com/item/1',
      title: 'Investigate production latency spike in payments',
      createdAt: '2026-03-20T14:00:00Z',
    });
    const b = makeItem({
      id: 'ts-b',
      sourceType: 'slack',
      url: 'https://example.com/item/1',
      title: 'Investigate production latency spike in payment service',
      createdAt: '2026-03-20T14:05:00Z',
    });
    // url=1.0, title high (~0.90), timestamp=1.0 (5 min < 1 hour)
    // composite ≈ 0.45 + 0.315 + 0.20 ≈ 0.965 ≥ 0.75 → merges
    const result = deduplicateItems([a, b]);
    expect(result).toHaveLength(1);
    expect(result[0].confidence).toBeGreaterThanOrEqual(0.75);
  });

  it('does NOT merge items created more than 24 hours apart with similar titles', () => {
    const a = makeItem({
      id: 'ts-c',
      sourceType: 'github',
      url: '',
      title: 'Refactor authentication middleware',
      createdAt: '2026-03-20T10:00:00Z',
    });
    const b = makeItem({
      id: 'ts-d',
      sourceType: 'github',
      url: '',
      title: 'Refactor authentication middleware',
      createdAt: '2026-03-21T11:00:00Z',
    });
    // url=0, title=1.0, timestamp≈0.66 (25 hours apart)
    // composite = 0 + 0.35 + 0.20*0.66 ≈ 0.482 < 0.75 → no merge
    const result = deduplicateItems([a, b]);
    expect(result).toHaveLength(2);
  });

  it('keeps items separate at exactly the 72-hour proximity boundary', () => {
    const a = makeItem({
      id: 'ts-e',
      sourceType: 'calendar',
      url: '',
      title: 'Quarterly planning review session',
      createdAt: '2026-03-20T00:00:00Z',
    });
    const b = makeItem({
      id: 'ts-f',
      sourceType: 'calendar',
      url: '',
      title: 'Quarterly planning review session',
      createdAt: '2026-03-23T00:00:00Z',
    });
    // url=0, title=1.0, timestamp=0.0 (exactly 72h → boundary is exclusive)
    // composite = 0 + 0.35 + 0 = 0.35 < 0.75 → no merge
    const result = deduplicateItems([a, b]);
    expect(result).toHaveLength(2);
  });
});

describe('dedupe — cross-source merge', () => {
  it('merges a GitHub issue and Slack thread sharing the same URL into one item with confidence >= 0.85', () => {
    const githubItem = makeItem({
      id: 'cs-gh-1',
      source: 'github-org',
      sourceType: 'github',
      url: 'https://github.com/acme/payments/issues/55',
      title: 'Upgrade Redis client to v5 for cluster support',
      createdAt: '2026-03-18T09:00:00Z',
      owner: 'alice@acme.com',
      dedupeKeys: ['gh-issue-55'],
    });
    const slackItem = makeItem({
      id: 'cs-sl-1',
      source: 'slack-eng',
      sourceType: 'slack',
      url: 'https://github.com/acme/payments/issues/55',
      title: 'Upgrade Redis client to v5 for cluster support',
      createdAt: '2026-03-18T09:15:00Z',
      owner: 'bob@acme.com',
      dedupeKeys: ['slack-thread-8821'],
    });
    // url=1.0, title=1.0, timestamp=1.0 (15 min apart)
    // composite = 0.45 + 0.35 + 0.20 = 1.0 >= 0.85 cross-source threshold
    const result = deduplicateItems([githubItem, slackItem]);
    expect(result).toHaveLength(1);
    expect(result[0].confidence).toBeGreaterThanOrEqual(0.85);
    expect(result[0].dedupeKeys).toEqual(expect.arrayContaining(['gh-issue-55', 'slack-thread-8821']));
  });

  it('retains the most complete fields from each source after cross-source merge', () => {
    const githubItem = makeItem({
      id: 'cs-gh-2',
      source: 'github-org',
      sourceType: 'github',
      url: 'https://github.com/acme/platform/issues/77',
      title: 'Migrate user service to new auth provider',
      createdAt: '2026-03-18T08:00:00Z',
      owner: 'alice@acme.com',
      dueAt: null,
      blocker: null,
      followUpQuestion: null,
      replyDraft: null,
      suggestedNextAction: null,
      dedupeKeys: ['gh-issue-77'],
    });
    const calendarItem = makeItem({
      id: 'cs-cal-2',
      source: 'google-calendar',
      sourceType: 'calendar',
      url: 'https://github.com/acme/platform/issues/77',
      title: 'Migrate user service to new auth provider',
      createdAt: '2026-03-18T08:30:00Z',
      owner: 'carol@acme.com',
      dueAt: '2026-04-01T17:00:00Z',
      blocker: 'Needs security review sign-off',
      followUpQuestion: 'Confirm migration timeline with SRE team',
      replyDraft: null,
      suggestedNextAction: null,
      dedupeKeys: ['cal-event-auth-migration'],
    });
    // GitHub is primary (earlier createdAt). Calendar's non-null fields fill primary's nulls.
    const result = deduplicateItems([githubItem, calendarItem]);
    expect(result).toHaveLength(1);
    const merged = result[0] as DedupedItem;
    // Owner retained from primary (GitHub)
    expect(merged.owner).toBe('alice@acme.com');
    // Nullable fields filled from secondary (Calendar)
    expect(merged.dueAt).toBe('2026-04-01T17:00:00Z');
    expect(merged.blocker).toBe('Needs security review sign-off');
    expect(merged.followUpQuestion).toBe('Confirm migration timeline with SRE team');
    // mergedFrom tracks the secondary
    expect(merged.mergedFrom).toEqual([{ source: 'google-calendar', id: 'cs-cal-2' }]);
  });

  it('merges partial overlap batch: 4 items with 1 duplicate pair and 2 unique produce 3 results', () => {
    const items: ActionItem[] = [
      {
        id: 'po-sl-1',
        source: 'slack-eng',
        sourceType: 'slack',
        title: 'Investigate flaky CI pipeline for payments service',
        summary: 'CI failures in payments',
        owner: 'alice@acme.com',
        participants: [],
        createdAt: '2026-03-20T09:00:00Z',
        updatedAt: '2026-03-20T09:00:00Z',
        dueAt: null,
        url: 'https://github.com/acme/payments/issues/101',
        status: 'open',
        priorityScore: 0,
        blocker: null,
        replyDraft: null,
        followUpQuestion: null,
        suggestedNextAction: null,
        dedupeKeys: ['slack-msg-5001'],
        confidence: 1,
      },
      {
        id: 'po-gh-1',
        source: 'github-org',
        sourceType: 'github',
        title: 'Investigate flaky CI pipeline for payments service',
        summary: 'CI failures in payments',
        owner: 'bob@acme.com',
        participants: [],
        createdAt: '2026-03-20T09:10:00Z',
        updatedAt: '2026-03-20T09:10:00Z',
        dueAt: null,
        url: 'https://github.com/acme/payments/issues/101',
        status: 'open',
        priorityScore: 0,
        blocker: null,
        replyDraft: null,
        followUpQuestion: null,
        suggestedNextAction: null,
        dedupeKeys: ['gh-issue-101'],
        confidence: 1,
      },
      {
        id: 'po-tr-1',
        source: 'trello-board',
        sourceType: 'trello',
        title: 'Design new onboarding flow wireframes',
        summary: 'Onboarding redesign',
        owner: 'carol@acme.com',
        participants: [],
        createdAt: '2026-03-20T10:00:00Z',
        updatedAt: '2026-03-20T10:00:00Z',
        dueAt: null,
        url: 'https://trello.com/c/abc123/onboarding-wireframes',
        status: 'open',
        priorityScore: 0,
        blocker: null,
        replyDraft: null,
        followUpQuestion: null,
        suggestedNextAction: null,
        dedupeKeys: ['trello-abc123'],
        confidence: 1,
      },
      {
        id: 'po-cal-1',
        source: 'google-calendar',
        sourceType: 'calendar',
        title: 'Quarterly budget review with finance',
        summary: 'Budget review',
        owner: 'dave@acme.com',
        participants: [],
        createdAt: '2026-03-21T14:00:00Z',
        updatedAt: '2026-03-21T14:00:00Z',
        dueAt: null,
        url: 'https://calendar.google.com/event/xyz789',
        status: 'open',
        priorityScore: 0,
        blocker: null,
        replyDraft: null,
        followUpQuestion: null,
        suggestedNextAction: null,
        dedupeKeys: ['cal-xyz789'],
        confidence: 1,
      },
    ];
    const result = deduplicateItems(items);
    expect(result).toHaveLength(3);
  });

  it('merges multi-source batch: 6 items from 6 sources with 3 URL-matching pairs produce 3 merged items with combined dedupeKeys', () => {
    const items: ActionItem[] = [
      {
        id: 'ms-slack-1',
        source: 'slack-eng',
        sourceType: 'slack',
        title: 'Upgrade Redis client to v5 for cluster support',
        summary: 'Redis upgrade',
        owner: 'alice@acme.com',
        participants: [],
        createdAt: '2026-03-20T09:00:00Z',
        updatedAt: '2026-03-20T09:00:00Z',
        dueAt: null,
        url: 'https://github.com/acme/infra/issues/200',
        status: 'open',
        priorityScore: 0,
        blocker: null,
        replyDraft: null,
        followUpQuestion: null,
        suggestedNextAction: null,
        dedupeKeys: ['slack-thread-200'],
        confidence: 1,
      },
      {
        id: 'ms-github-1',
        source: 'github-org',
        sourceType: 'github',
        title: 'Upgrade Redis client to v5 for cluster support',
        summary: 'Redis upgrade',
        owner: 'bob@acme.com',
        participants: [],
        createdAt: '2026-03-20T09:05:00Z',
        updatedAt: '2026-03-20T09:05:00Z',
        dueAt: null,
        url: 'https://github.com/acme/infra/issues/200',
        status: 'open',
        priorityScore: 0,
        blocker: null,
        replyDraft: null,
        followUpQuestion: null,
        suggestedNextAction: null,
        dedupeKeys: ['gh-issue-200'],
        confidence: 1,
      },
      {
        id: 'ms-calendar-1',
        source: 'google-calendar',
        sourceType: 'calendar',
        title: 'Finalize Q2 roadmap with product team',
        summary: 'Roadmap planning',
        owner: 'carol@acme.com',
        participants: [],
        createdAt: '2026-03-20T10:00:00Z',
        updatedAt: '2026-03-20T10:00:00Z',
        dueAt: null,
        url: 'https://notion.so/acme/q2-roadmap-abc',
        status: 'open',
        priorityScore: 0,
        blocker: null,
        replyDraft: null,
        followUpQuestion: null,
        suggestedNextAction: null,
        dedupeKeys: ['cal-roadmap-q2'],
        confidence: 1,
      },
      {
        id: 'ms-notion-1',
        source: 'notion-workspace',
        sourceType: 'notion',
        title: 'Finalize Q2 roadmap with product team',
        summary: 'Roadmap planning',
        owner: 'dave@acme.com',
        participants: [],
        createdAt: '2026-03-20T10:15:00Z',
        updatedAt: '2026-03-20T10:15:00Z',
        dueAt: null,
        url: 'https://notion.so/acme/q2-roadmap-abc',
        status: 'open',
        priorityScore: 0,
        blocker: null,
        replyDraft: null,
        followUpQuestion: null,
        suggestedNextAction: null,
        dedupeKeys: ['notion-page-q2'],
        confidence: 1,
      },
      {
        id: 'ms-trello-1',
        source: 'trello-board',
        sourceType: 'trello',
        title: 'Migrate legacy auth to OAuth2 provider',
        summary: 'Auth migration',
        owner: 'eve@acme.com',
        participants: [],
        createdAt: '2026-03-20T11:00:00Z',
        updatedAt: '2026-03-20T11:00:00Z',
        dueAt: null,
        url: 'https://jira.acme.com/browse/AUTH-42',
        status: 'open',
        priorityScore: 0,
        blocker: null,
        replyDraft: null,
        followUpQuestion: null,
        suggestedNextAction: null,
        dedupeKeys: ['trello-card-auth42'],
        confidence: 1,
      },
      {
        id: 'ms-email-1',
        source: 'gmail-inbox',
        sourceType: 'email',
        title: 'Migrate legacy auth to OAuth2 provider',
        summary: 'Auth migration',
        owner: 'frank@acme.com',
        participants: [],
        createdAt: '2026-03-20T11:20:00Z',
        updatedAt: '2026-03-20T11:20:00Z',
        dueAt: null,
        url: 'https://jira.acme.com/browse/AUTH-42',
        status: 'open',
        priorityScore: 0,
        blocker: null,
        replyDraft: null,
        followUpQuestion: null,
        suggestedNextAction: null,
        dedupeKeys: ['email-thread-auth42'],
        confidence: 1,
      },
    ];

    const result = deduplicateItems(items);
    expect(result).toHaveLength(3);

    // Each merged item must carry dedupeKeys from both contributing sources
    const allDedupeKeys = result.flatMap((r) => r.dedupeKeys);

    // Pair 1: slack + github
    expect(allDedupeKeys).toContain('slack-thread-200');
    expect(allDedupeKeys).toContain('gh-issue-200');
    const redisMerged = result.find((r) =>
      r.dedupeKeys.includes('slack-thread-200') || r.dedupeKeys.includes('gh-issue-200'),
    )!;
    expect(redisMerged.dedupeKeys).toContain('slack-thread-200');
    expect(redisMerged.dedupeKeys).toContain('gh-issue-200');

    // Pair 2: calendar + notion
    const roadmapMerged = result.find((r) =>
      r.dedupeKeys.includes('cal-roadmap-q2') || r.dedupeKeys.includes('notion-page-q2'),
    )!;
    expect(roadmapMerged.dedupeKeys).toContain('cal-roadmap-q2');
    expect(roadmapMerged.dedupeKeys).toContain('notion-page-q2');

    // Pair 3: trello + email
    const authMerged = result.find((r) =>
      r.dedupeKeys.includes('trello-card-auth42') || r.dedupeKeys.includes('email-thread-auth42'),
    )!;
    expect(authMerged.dedupeKeys).toContain('trello-card-auth42');
    expect(authMerged.dedupeKeys).toContain('email-thread-auth42');
  });

  it('returns empty array for empty input without throwing', () => {
    const result = deduplicateItems([]);
    expect(result).toEqual([]);
    expect(result).toHaveLength(0);
  });

  it('does NOT merge two cross-source items with similar titles but different URLs and timestamps >24h apart', () => {
    const trelloItem = makeItem({
      id: 'cs-tr-3',
      source: 'trello-eng',
      sourceType: 'trello',
      url: 'https://trello.com/c/Xk9mQ2/review-quarterly-okr-progress-engineering',
      title: 'Review quarterly OKR progress for engineering team',
      createdAt: '2026-03-15T10:00:00Z',
      owner: 'dave@acme.com',
      dedupeKeys: ['trello-card-Xk9mQ2'],
    });
    const notionItem = makeItem({
      id: 'cs-no-3',
      source: 'notion-workspace',
      sourceType: 'notion',
      url: 'https://notion.so/acme/review-quarterly-okr-progress-product-abc123',
      title: 'Review quarterly OKR progress for product team',
      createdAt: '2026-03-16T14:00:00Z',
      owner: 'eve@acme.com',
      dedupeKeys: ['notion-page-abc123'],
    });
    // url=0.0 (completely different domains), title ~0.83 (high but not identical —
    // "engineering team" vs "product team"), timestamp ~0.60 (28h apart)
    // composite = 0.45*0 + 0.35*~0.83 + 0.20*~0.60 ≈ 0.41 < 0.85 cross-source threshold
    const result = deduplicateItems([trelloItem, notionItem]);
    expect(result).toHaveLength(2);
    // Verify both items preserved with their original IDs
    const ids = result.map((r) => r.id).sort();
    expect(ids).toEqual(['cs-no-3', 'cs-tr-3']);
  });
});

describe('dedupe — confidence threshold boundaries', () => {
  it('rejects merge for items with only vague title similarity, no URL match, and distant timestamps', () => {
    // Two items sharing common words ("Update" and "docs") but distinct in intent.
    // No URL match, timestamps >24h apart — confidence should be well below threshold.
    // url=0.0 (no URLs), title=Dice on "update docs" vs "update documentation page"
    // (moderate overlap but not high), timestamp=0.0 (>72h apart)
    // composite = 0.45*0 + 0.35*~0.5 + 0.20*0 ≈ 0.17 — far below 0.75
    const itemA = makeItem({
      id: 'low-conf-1',
      source: 'slack-workspace',
      sourceType: 'slack',
      title: 'Update docs',
      url: '',
      createdAt: '2026-03-01T10:00:00Z',
      updatedAt: '2026-03-01T10:00:00Z',
      dedupeKeys: ['slack-msg-100'],
    });

    const itemB = makeItem({
      id: 'low-conf-2',
      source: 'slack-workspace',
      sourceType: 'slack',
      title: 'Update documentation page',
      url: '',
      createdAt: '2026-03-05T18:00:00Z',
      updatedAt: '2026-03-05T18:00:00Z',
      dedupeKeys: ['slack-msg-200'],
    });

    const result = deduplicateItems([itemA, itemB]);
    expect(result).toHaveLength(2);
    const ids = result.map((r) => r.id).sort();
    expect(ids).toEqual(['low-conf-1', 'low-conf-2']);
    // Neither item should have mergedFrom since no merge occurred
    for (const item of result) {
      expect(item.mergedFrom).toBeUndefined();
    }
  });

  it('merges items with identical URL, near-identical title, and timestamps within 1 hour', () => {
    // Identical URL -> urlScore=1.0, near-identical title -> titleScore≈1.0,
    // timestamps 30 min apart -> timestampScore=1.0
    // composite ≈ 0.45*1.0 + 0.35*1.0 + 0.20*1.0 = 1.0 — well above 0.75
    const itemA = makeItem({
      id: 'high-conf-1',
      source: 'github-repo',
      sourceType: 'github',
      title: 'Fix authentication timeout in login service',
      url: 'https://github.com/org/repo/issues/42',
      createdAt: '2026-03-10T14:00:00Z',
      updatedAt: '2026-03-10T14:00:00Z',
      dedupeKeys: ['gh-issue-42'],
    });

    const itemB = makeItem({
      id: 'high-conf-2',
      source: 'github-repo',
      sourceType: 'github',
      title: 'Fix authentication timeout in login service',
      url: 'https://github.com/org/repo/issues/42',
      createdAt: '2026-03-10T14:30:00Z',
      updatedAt: '2026-03-10T14:30:00Z',
      dedupeKeys: ['gh-issue-42-dup'],
    });

    const result = deduplicateItems([itemA, itemB]);
    expect(result).toHaveLength(1);

    const merged = result[0];
    // Primary should be the item with earlier createdAt
    expect(merged.id).toBe('high-conf-1');
    // Confidence must be present and above the same-source threshold (0.75)
    expect(merged.confidence).toBeGreaterThan(0.75);
    // mergedFrom should reference the secondary item
    expect(merged.mergedFrom).toBeDefined();
    expect(merged.mergedFrom).toHaveLength(1);
    expect(merged.mergedFrom![0].id).toBe('high-conf-2');
  });

  it('produces correct count in mixed batch: 1 high-conf pair merges, 1 low-conf pair stays, 1 unique passes through', () => {
    // High-confidence pair: identical URL + title + close timestamps -> will merge
    const highA = makeItem({
      id: 'mix-high-1',
      source: 'trello-board',
      sourceType: 'trello',
      title: 'Deploy monitoring dashboard to staging',
      url: 'https://trello.com/c/abc123',
      createdAt: '2026-03-12T09:00:00Z',
      updatedAt: '2026-03-12T09:00:00Z',
      dedupeKeys: ['trello-abc123'],
    });

    const highB = makeItem({
      id: 'mix-high-2',
      source: 'trello-board',
      sourceType: 'trello',
      title: 'Deploy monitoring dashboard to staging',
      url: 'https://trello.com/c/abc123',
      createdAt: '2026-03-12T09:45:00Z',
      updatedAt: '2026-03-12T09:45:00Z',
      dedupeKeys: ['trello-abc123-dup'],
    });

    // Low-confidence pair: vague title overlap, no URL, distant timestamps -> won't merge
    const lowA = makeItem({
      id: 'mix-low-1',
      source: 'email-inbox',
      sourceType: 'email',
      title: 'Review quarterly budget',
      url: '',
      createdAt: '2026-03-01T08:00:00Z',
      updatedAt: '2026-03-01T08:00:00Z',
      dedupeKeys: ['email-msg-500'],
    });

    const lowB = makeItem({
      id: 'mix-low-2',
      source: 'email-inbox',
      sourceType: 'email',
      title: 'Review annual budget proposal',
      url: '',
      createdAt: '2026-03-08T16:00:00Z',
      updatedAt: '2026-03-08T16:00:00Z',
      dedupeKeys: ['email-msg-600'],
    });

    // Unique item: no match with anything
    const unique = makeItem({
      id: 'mix-unique-1',
      source: 'notion-workspace',
      sourceType: 'notion',
      title: 'Prepare onboarding checklist for new hires',
      url: 'https://notion.so/onboarding-checklist',
      createdAt: '2026-03-15T11:00:00Z',
      updatedAt: '2026-03-15T11:00:00Z',
      dedupeKeys: ['notion-onboarding'],
    });

    const result = deduplicateItems([highA, highB, lowA, lowB, unique]);
    // 5 items -> 1 merge (high pair) + 2 kept separate (low pair) + 1 unique = 4
    expect(result).toHaveLength(4);

    const ids = result.map((r) => r.id).sort();
    // high pair merged into mix-high-1, low pair kept as both, unique kept
    expect(ids).toEqual(['mix-high-1', 'mix-low-1', 'mix-low-2', 'mix-unique-1']);
  });
});
