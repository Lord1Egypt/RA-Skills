import { describe, it, expect } from 'vitest';
import { runPipeline, type RawSourceInput } from '../index.js';
import type { ActionItem } from '../types.js';

function makeItem(overrides: Partial<ActionItem> & { id: string; title: string }): ActionItem {
  return {
    source: 'test:src',
    sourceType: 'slack',
    summary: '',
    owner: 'alice',
    participants: ['alice'],
    createdAt: '2026-03-20T00:00:00Z',
    updatedAt: '2026-03-20T00:00:00Z',
    dueAt: null,
    url: 'https://example.com',
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

describe('runPipeline', () => {
  it('returns a valid empty result for zero sources', async () => {
    const result = await runPipeline([]);

    expect(result.markdown).toContain('No action items');
    expect(result.actionBoard.totalItems).toBe(0);
    expect(result.actionBoard.tiers.urgent).toHaveLength(0);
    expect(result.actionBoard.tiers.active).toHaveLength(0);
    expect(result.actionBoard.tiers.low).toHaveLength(0);
    expect(result.skippedSources).toHaveLength(0);
    expect(result.counts.total).toBe(0);
    expect(result.counts.afterDedupe).toBe(0);
  });

  it('returns a valid empty result when all sources fail', async () => {
    const sources: RawSourceInput[] = [
      {
        name: 'broken-slack',
        data: null,
        normalize: () => { throw new Error('connection refused'); },
      },
      {
        name: 'broken-github',
        data: null,
        normalize: () => { throw new Error('auth expired'); },
      },
    ];

    const result = await runPipeline(sources);

    expect(result.markdown).toContain('No action items');
    expect(result.actionBoard.totalItems).toBe(0);
    expect(result.skippedSources).toHaveLength(2);
    expect(result.skippedSources[0]).toEqual({
      sourceName: 'broken-slack',
      reason: 'connection refused',
    });
    expect(result.skippedSources[1]).toEqual({
      sourceName: 'broken-github',
      reason: 'auth expired',
    });
    expect(result.counts.total).toBe(0);
    expect(result.counts.afterDedupe).toBe(0);
  });

  it('skips a failing source and processes the rest', async () => {
    const item = makeItem({ id: 'ok-1', title: 'Valid task' });
    const sources: RawSourceInput[] = [
      {
        name: 'good-source',
        data: null,
        normalize: () => [item],
      },
      {
        name: 'bad-source',
        data: null,
        normalize: () => { throw new Error('timeout'); },
      },
    ];

    const result = await runPipeline(sources);

    expect(result.skippedSources).toHaveLength(1);
    expect(result.skippedSources[0].sourceName).toBe('bad-source');
    expect(result.actionBoard.totalItems).toBe(1);
    expect(result.counts.total).toBe(1);
    expect(result.counts.afterDedupe).toBe(1);
  });

  it('sorts output items by descending priorityScore', async () => {
    const lowPriority = makeItem({
      id: 'low-1',
      title: 'Low priority task with no urgency',
      url: 'https://example.com/low',
      dueAt: null,
      blocker: null,
    });
    const highPriority = makeItem({
      id: 'high-1',
      title: 'High priority task blocked on deploy',
      url: 'https://example.com/high',
      blocker: 'blocked on deploy',
      dueAt: '2026-03-20T00:00:00Z',
    });

    const sources: RawSourceInput[] = [
      {
        name: 'source-a',
        data: null,
        normalize: () => [lowPriority, highPriority],
      },
    ];

    const result = await runPipeline(sources);

    const allItems = [
      ...result.actionBoard.tiers.urgent,
      ...result.actionBoard.tiers.active,
      ...result.actionBoard.tiers.low,
    ];
    expect(allItems.length).toBe(2);

    for (let i = 1; i < allItems.length; i++) {
      expect(allItems[i - 1].priorityScore).toBeGreaterThanOrEqual(allItems[i].priorityScore);
    }
  });

  it('deduplicates items across sources', async () => {
    const itemA = makeItem({
      id: 'dup-1',
      title: 'Fix the login bug',
      url: 'https://github.com/org/repo/issues/42',
      sourceType: 'github',
      source: 'github:org/repo',
      createdAt: '2026-03-20T00:00:00Z',
      dedupeKeys: ['https://github.com/org/repo/issues/42'],
    });
    const itemB = makeItem({
      id: 'dup-2',
      title: 'Fix the login bug',
      url: 'https://github.com/org/repo/issues/42',
      sourceType: 'github',
      source: 'github:org/repo',
      createdAt: '2026-03-20T00:10:00Z',
      dedupeKeys: ['https://github.com/org/repo/issues/42'],
    });

    const sources: RawSourceInput[] = [
      { name: 'src-a', data: null, normalize: () => [itemA] },
      { name: 'src-b', data: null, normalize: () => [itemB] },
    ];

    const result = await runPipeline(sources);

    expect(result.counts.total).toBe(2);
    expect(result.counts.afterDedupe).toBe(1);
    expect(result.actionBoard.totalItems).toBe(1);
  });

  it('records non-Error throws as string reasons', async () => {
    const sources: RawSourceInput[] = [
      {
        name: 'string-thrower',
        data: null,
        normalize: () => { throw 'raw string error'; },
      },
    ];

    const result = await runPipeline(sources);

    expect(result.skippedSources).toHaveLength(1);
    expect(result.skippedSources[0].reason).toBe('raw string error');
  });

  it('populates byTier counts correctly', async () => {
    const items = [
      makeItem({ id: 'a', title: 'A', blocker: 'yes', dueAt: '2026-03-20T00:00:00Z' }),
      makeItem({ id: 'b', title: 'B' }),
    ];

    const sources: RawSourceInput[] = [
      { name: 'src', data: null, normalize: () => items },
    ];

    const result = await runPipeline(sources);

    const tierSum =
      result.counts.byTier['urgent'] +
      result.counts.byTier['active'] +
      result.counts.byTier['low'];
    expect(tierSum).toBe(result.counts.afterDedupe);
  });

  it('includes actionBoard metadata with tier thresholds', async () => {
    const result = await runPipeline([]);

    expect(result.actionBoard.metadata.tierThresholds.urgent).toBe(70);
    expect(result.actionBoard.metadata.tierThresholds.active).toBe(30);
  });

  it('includes generatedAt timestamp in actionBoard', async () => {
    const before = new Date().toISOString();
    const result = await runPipeline([]);
    const after = new Date().toISOString();

    expect(result.actionBoard.generatedAt >= before).toBe(true);
    expect(result.actionBoard.generatedAt <= after).toBe(true);
  });
});
