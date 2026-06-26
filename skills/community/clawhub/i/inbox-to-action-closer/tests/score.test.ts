import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import {
  scoreItems,
  OVERDUE_BOOST,
  DUE_SOON_BOOST,
  DUE_WEEK_WINDOW,
  BLOCKER_BOOST,
  ASSIGNMENT_BOOST,
  FOLLOW_UP_BOOST,
} from '../src/score.js';
import type { ActionItem } from '../src/types.js';

function makeItem(overrides: Partial<ActionItem> = {}): ActionItem {
  return {
    id: 'test-1',
    source: 'test',
    sourceType: 'github',
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

const NOW = new Date('2026-03-25T12:00:00Z');

describe('scoreItems', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    vi.setSystemTime(NOW);
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  // --- overdue-by-hours vs overdue-by-months (2) ---

  it('scores an item overdue by hours with OVERDUE_BOOST', () => {
    const items = [makeItem({ dueAt: '2026-03-24T23:00:00Z' })];
    const [scored] = scoreItems(items);
    expect(scored.priorityScore).toBe(OVERDUE_BOOST);
    expect(scored.priorityScore).toBeGreaterThan(DUE_SOON_BOOST);
  });

  it('scores an item overdue by months the same as overdue by hours (flat boost)', () => {
    const overdueHours = makeItem({ id: 'hours', dueAt: '2026-03-24T23:00:00Z' });
    const overdueMonths = makeItem({ id: 'months', dueAt: '2026-01-01T00:00:00Z' });
    const [hoursScored, monthsScored] = scoreItems([overdueHours, overdueMonths]);
    expect(hoursScored.priorityScore).toBe(OVERDUE_BOOST);
    expect(monthsScored.priorityScore).toBe(OVERDUE_BOOST);
    expect(hoursScored.priorityScore).toBe(monthsScored.priorityScore);
  });

  // --- due-today boundary (2) ---

  it('scores an item due at start of today as DUE_SOON_BOOST', () => {
    const items = [makeItem({ dueAt: '2026-03-25T00:00:00Z' })];
    const [scored] = scoreItems(items);
    expect(scored.priorityScore).toBe(DUE_SOON_BOOST);
  });

  it('scores an item due at end of today as DUE_SOON_BOOST', () => {
    const items = [makeItem({ dueAt: '2026-03-25T23:59:59Z' })];
    const [scored] = scoreItems(items);
    expect(scored.priorityScore).toBe(DUE_SOON_BOOST);
  });

  // --- due-within-week taper (2) ---

  it('scores an item due in 3 days with tapering value between 0 and DUE_SOON_BOOST', () => {
    const items = [makeItem({ dueAt: '2026-03-28T10:00:00Z' })];
    const [scored] = scoreItems(items);
    const expected = DUE_SOON_BOOST * (1 - 3 / DUE_WEEK_WINDOW);
    expect(scored.priorityScore).toBeCloseTo(expected, 5);
    expect(scored.priorityScore).toBeGreaterThan(0);
    expect(scored.priorityScore).toBeLessThan(DUE_SOON_BOOST);
  });

  it('scores an item due in 6 days lower than one due in 3 days', () => {
    const due3 = makeItem({ id: '3d', dueAt: '2026-03-28T10:00:00Z' });
    const due6 = makeItem({ id: '6d', dueAt: '2026-03-31T10:00:00Z' });
    const [scored3, scored6] = scoreItems([due3, due6]);
    expect(scored3.priorityScore).toBeGreaterThan(scored6.priorityScore);
    expect(scored6.priorityScore).toBeGreaterThan(0);
  });

  // --- no-due-date (1) ---

  it('gives 0 due-date contribution when dueAt is absent', () => {
    const items = [makeItem({ dueAt: null, blocker: null })];
    const [scored] = scoreItems(items);
    expect(scored.priorityScore).toBe(0);
  });

  // --- blocker-flag boost (2) ---

  it('scores a blocker item strictly higher than an identical non-blocker', () => {
    const withBlocker = makeItem({ id: 'b', dueAt: '2026-03-26T10:00:00Z', blocker: 'Waiting on deploy' });
    const noBlocker = makeItem({ id: 'nb', dueAt: '2026-03-26T10:00:00Z', blocker: null });
    const [scoredB, scoredNB] = scoreItems([withBlocker, noBlocker]);
    expect(scoredB.priorityScore).toBe(scoredNB.priorityScore + BLOCKER_BOOST);
  });

  it('gives blocker score even when there is no due date', () => {
    const items = [makeItem({ dueAt: null, blocker: 'Blocked on review' })];
    const [scored] = scoreItems(items);
    expect(scored.priorityScore).toBe(BLOCKER_BOOST);
  });

  // --- combined overdue+blocker (1) ---

  it('combines overdue and blocker for the highest score', () => {
    const combined = makeItem({ dueAt: '2026-03-24T23:00:00Z', blocker: 'Critical' });
    const overdueOnly = makeItem({ dueAt: '2026-03-24T23:00:00Z', blocker: null });
    const blockerOnly = makeItem({ dueAt: null, blocker: 'Critical' });
    const neitherItem = makeItem({ dueAt: null, blocker: null });
    const [c, o, b, n] = scoreItems([combined, overdueOnly, blockerOnly, neitherItem]);
    expect(c.priorityScore).toBe(OVERDUE_BOOST + BLOCKER_BOOST);
    expect(c.priorityScore).toBeGreaterThan(o.priorityScore);
    expect(c.priorityScore).toBeGreaterThan(b.priorityScore);
    expect(o.priorityScore).toBeGreaterThan(n.priorityScore);
    expect(b.priorityScore).toBeGreaterThan(n.priorityScore);
  });

  // --- empty array (1) ---

  it('returns an empty array for empty input', () => {
    expect(scoreItems([])).toEqual([]);
  });

  // --- null dueAt field (1) ---

  it('produces no NaN or error when dueAt is null', () => {
    const items = [makeItem({ dueAt: null })];
    const [scored] = scoreItems(items);
    expect(Number.isNaN(scored.priorityScore)).toBe(false);
    expect(typeof scored.priorityScore).toBe('number');
  });

  // --- T020: overdue/due-today/far-future ordering (3) ---

  it('overdue+blocker scores strictly higher than overdue-only, and both beat due-today and far-future', () => {
    const overdueBlocker = makeItem({
      id: 'overdue-blocker',
      dueAt: '2026-03-22T12:00:00Z',
      blocker: 'Critical dependency',
    });
    const overdueOnly = makeItem({
      id: 'overdue-only',
      dueAt: '2026-03-22T12:00:00Z',
      blocker: null,
    });
    const dueToday = makeItem({
      id: 'due-today',
      dueAt: '2026-03-25T12:00:00Z',
      blocker: null,
    });
    const farFuture = makeItem({
      id: 'far-future',
      dueAt: '2026-04-24T12:00:00Z',
      blocker: null,
    });

    const [ob, oo, dt, ff] = scoreItems([overdueBlocker, overdueOnly, dueToday, farFuture]);

    // Blocker weight actually contributes: overdue+blocker > overdue-only
    expect(ob.priorityScore).toBeGreaterThan(oo.priorityScore);
    // Both overdue variants beat due-today
    expect(ob.priorityScore).toBeGreaterThan(dt.priorityScore);
    expect(oo.priorityScore).toBeGreaterThan(dt.priorityScore);
    // Both overdue variants beat far-future
    expect(ob.priorityScore).toBeGreaterThan(ff.priorityScore);
    expect(oo.priorityScore).toBeGreaterThan(ff.priorityScore);
  });

  it('due-today with direct assignment scores strictly higher than far-future unassigned', () => {
    const currentUser = 'active-user@example.com';
    const dueTodayAssigned = makeItem({
      id: 'today-assigned',
      dueAt: '2026-03-25T12:00:00Z',
      owner: currentUser,
      blocker: null,
    });
    const farFutureUnassigned = makeItem({
      id: 'far-unassigned',
      dueAt: '2026-04-24T12:00:00Z',
      owner: 'someone-else@example.com',
      blocker: null,
    });

    const [today, future] = scoreItems([dueTodayAssigned, farFutureUnassigned], currentUser);

    expect(today.priorityScore).toBeGreaterThan(future.priorityScore);
  });

  it('far-future non-blocker unassigned scores strictly lower than both overdue and due-today items', () => {
    const overdue = makeItem({
      id: 'overdue',
      dueAt: '2026-03-22T12:00:00Z',
      blocker: null,
    });
    const dueToday = makeItem({
      id: 'today',
      dueAt: '2026-03-25T12:00:00Z',
      blocker: null,
    });
    const farFuture = makeItem({
      id: 'far-future',
      dueAt: '2026-04-24T12:00:00Z',
      blocker: null,
      owner: '',
    });

    const [od, dt, ff] = scoreItems([overdue, dueToday, farFuture]);

    expect(ff.priorityScore).toBeLessThan(od.priorityScore);
    expect(ff.priorityScore).toBeLessThan(dt.priorityScore);
  });

  // --- T021: blocker boost, direct-assignment boost, unanswered follow-up boost (3+1) ---

  it('blocker boost: item with blocker scores strictly higher than identical item without', () => {
    const withBlocker = makeItem({ id: 'blocker-on', blocker: 'Waiting on deploy' });
    const noBlocker = makeItem({ id: 'blocker-off', blocker: null });
    const [scored, control] = scoreItems([withBlocker, noBlocker]);
    expect(scored.priorityScore).toBeGreaterThan(control.priorityScore);
  });

  it('direct-assignment boost: item owned by currentUser scores strictly higher than unowned', () => {
    const currentUser = 'me@example.com';
    const assigned = makeItem({ id: 'assigned', owner: currentUser });
    const unassigned = makeItem({ id: 'unassigned', owner: 'other@example.com' });
    const [scored, control] = scoreItems([assigned, unassigned], currentUser);
    expect(scored.priorityScore).toBeGreaterThan(control.priorityScore);
  });

  it('unanswered follow-up boost: item with followUpQuestion scores strictly higher than without', () => {
    const withFollowUp = makeItem({ id: 'followup-on', followUpQuestion: 'Any update on the deploy?' });
    const noFollowUp = makeItem({ id: 'followup-off', followUpQuestion: null });
    const [scored, control] = scoreItems([withFollowUp, noFollowUp]);
    expect(scored.priorityScore).toBeGreaterThan(control.priorityScore);
  });

  it('additivity: blocker + direct-assignment scores higher than blocker alone', () => {
    const currentUser = 'me@example.com';
    const both = makeItem({ id: 'both', blocker: 'Blocked', owner: currentUser });
    const blockerOnly = makeItem({ id: 'blocker-only', blocker: 'Blocked', owner: 'other@example.com' });
    const [scoredBoth, scoredBlocker] = scoreItems([both, blockerOnly], currentUser);
    expect(scoredBoth.priorityScore).toBeGreaterThan(scoredBlocker.priorityScore);
  });

  // --- T022: recency weighting, type weights, combined factor ordering (3) ---

  it('recency ordering: items at 1 hour, 3 days, and 30 days ago rank in strictly descending score order', () => {
    const oneHourAgo = makeItem({
      id: 'recent-1h',
      updatedAt: '2026-03-25T11:00:00Z',
      dueAt: null,
      blocker: null,
      followUpQuestion: null,
      owner: '',
    });
    const threeDaysAgo = makeItem({
      id: 'recent-3d',
      updatedAt: '2026-03-22T12:00:00Z',
      dueAt: null,
      blocker: null,
      followUpQuestion: null,
      owner: '',
    });
    const thirtyDaysAgo = makeItem({
      id: 'old-30d',
      updatedAt: '2026-02-23T12:00:00Z',
      dueAt: null,
      blocker: null,
      followUpQuestion: null,
      owner: '',
    });

    const [scored1h, scored3d, scored30d] = scoreItems([oneHourAgo, threeDaysAgo, thirtyDaysAgo]);

    expect(scored1h.priorityScore).toBeGreaterThan(scored3d.priorityScore);
    expect(scored3d.priorityScore).toBeGreaterThan(scored30d.priorityScore);
    expect(scored30d.priorityScore).toBe(0);
  });

  it('type-weight ordering: higher-weight sourceType scores above lower-weight with identical timestamps', () => {
    const githubItem = makeItem({
      id: 'github-type',
      sourceType: 'github',
      updatedAt: '2026-03-25T10:00:00Z',
      dueAt: null,
      blocker: null,
      followUpQuestion: null,
      owner: '',
    });
    const calendarItem = makeItem({
      id: 'calendar-type',
      sourceType: 'calendar',
      updatedAt: '2026-03-25T10:00:00Z',
      dueAt: null,
      blocker: null,
      followUpQuestion: null,
      owner: '',
    });

    const [scoredGithub, scoredCalendar] = scoreItems([githubItem, calendarItem]);

    expect(scoredGithub.priorityScore).toBeGreaterThan(scoredCalendar.priorityScore);
  });

  it('combined: recent low-weight type beats old high-weight type when recency gap is large', () => {
    const recentCalendar = makeItem({
      id: 'recent-calendar',
      sourceType: 'calendar',
      updatedAt: '2026-03-25T11:00:00Z',
      dueAt: null,
      blocker: null,
      followUpQuestion: null,
      owner: '',
    });
    const oldGithub = makeItem({
      id: 'old-github',
      sourceType: 'github',
      updatedAt: '2026-03-13T12:00:00Z',
      dueAt: null,
      blocker: null,
      followUpQuestion: null,
      owner: '',
    });

    const [scoredCalendar, scoredGithub] = scoreItems([recentCalendar, oldGithub]);

    // Recency dominates type weight when the gap is large
    expect(scoredCalendar.priorityScore).toBeGreaterThan(scoredGithub.priorityScore);
    // Both should have non-zero scores (github is still within 14-day recency window)
    expect(scoredGithub.priorityScore).toBeGreaterThan(0);
  });

  // --- T023: zero-field edge case, all-factors item, mixed-batch ordering (3) ---

  it('zero-field edge case: item with all optional scoring fields absent returns a finite non-negative score', () => {
    const bare = makeItem({
      id: 'bare-minimum',
      dueAt: null,
      blocker: null,
      owner: '',
      followUpQuestion: null,
      createdAt: '',
      updatedAt: '',
    });
    const [scored] = scoreItems([bare]);
    expect(Number.isFinite(scored.priorityScore)).toBe(true);
    expect(scored.priorityScore).toBeGreaterThanOrEqual(0);
  });

  it('all-factors item scores strictly higher than a minimal baseline item', () => {
    const currentUser = 'poweruser@example.com';
    const fullyLoaded = makeItem({
      id: 'all-factors',
      sourceType: 'github',
      dueAt: '2026-03-24T10:00:00Z',        // overdue → OVERDUE_BOOST
      blocker: 'Deployment blocked',          // → BLOCKER_BOOST
      owner: currentUser,                     // → ASSIGNMENT_BOOST
      followUpQuestion: 'Any update?',        // → FOLLOW_UP_BOOST
      updatedAt: '2026-03-25T11:00:00Z',     // very recent → RECENCY_MAX_BOOST
      status: 'open',
    });
    const minimal = makeItem({
      id: 'minimal',
      dueAt: null,
      blocker: null,
      owner: '',
      followUpQuestion: null,
      createdAt: '',
      updatedAt: '',
    });
    const [scoredFull, scoredMinimal] = scoreItems([fullyLoaded, minimal], currentUser);
    expect(scoredFull.priorityScore).toBeGreaterThan(scoredMinimal.priorityScore);
    // Verify every boost contributed (full score > any single boost)
    expect(scoredFull.priorityScore).toBeGreaterThan(OVERDUE_BOOST);
    expect(scoredFull.priorityScore).toBeGreaterThan(BLOCKER_BOOST);
    expect(scoredFull.priorityScore).toBeGreaterThan(ASSIGNMENT_BOOST);
    expect(scoredFull.priorityScore).toBeGreaterThan(FOLLOW_UP_BOOST);
  });

  it('mixed-batch: 6 heterogeneous items are scored in correct descending priority order', () => {
    const currentUser = 'batch-user@example.com';

    // Profile A: every factor active (overdue + blocker + assigned + follow-up + recent + github)
    const allFactors = makeItem({
      id: 'A-all-factors',
      sourceType: 'github',
      dueAt: '2026-03-24T10:00:00Z',
      blocker: 'Deploy blocked',
      owner: currentUser,
      followUpQuestion: 'Status?',
      updatedAt: '2026-03-25T11:00:00Z',
      status: 'open',
    });

    // Profile B: overdue + blocker only (old update, unassigned, no follow-up)
    const overdueBlocker = makeItem({
      id: 'B-overdue-blocker',
      sourceType: 'github',
      dueAt: '2026-03-20T10:00:00Z',
      blocker: 'Waiting on API',
      owner: 'someone-else@example.com',
      followUpQuestion: null,
      updatedAt: '2026-02-20T12:00:00Z',
      status: 'open',
    });

    // Profile C: due today + assigned + follow-up + recent (no blocker, slack weight 0.8)
    const dueTodayAssigned = makeItem({
      id: 'C-today-assigned',
      sourceType: 'slack',
      dueAt: '2026-03-25T18:00:00Z',
      blocker: null,
      owner: currentUser,
      followUpQuestion: 'Need confirmation',
      updatedAt: '2026-03-25T08:00:00Z',
      status: 'in_progress',
    });

    // Profile D: blocker + recent only (no due date, unassigned, no follow-up)
    const blockerRecent = makeItem({
      id: 'D-blocker-recent',
      sourceType: 'github',
      dueAt: null,
      blocker: 'CI pipeline broken',
      owner: 'other@example.com',
      followUpQuestion: null,
      updatedAt: '2026-03-25T09:00:00Z',
      status: 'open',
    });

    // Profile E: recency only (no due date, no blocker, unassigned, calendar weight 0.7)
    const recentOnly = makeItem({
      id: 'E-recent-only',
      sourceType: 'calendar',
      dueAt: null,
      blocker: null,
      owner: 'other@example.com',
      followUpQuestion: null,
      updatedAt: '2026-03-25T10:00:00Z',
      status: 'open',
    });

    // Profile F: no scoring factors at all (stale, no due date, no blocker)
    const noFactors = makeItem({
      id: 'F-no-factors',
      sourceType: 'github',
      dueAt: null,
      blocker: null,
      owner: 'other@example.com',
      followUpQuestion: null,
      createdAt: '',
      updatedAt: '',
      status: 'open',
    });

    const scored = scoreItems(
      [noFactors, recentOnly, allFactors, blockerRecent, dueTodayAssigned, overdueBlocker],
      currentUser,
    );

    // Sort by priorityScore descending
    const sorted = [...scored].sort((a, b) => b.priorityScore - a.priorityScore);

    // Verify descending order holds
    for (let i = 0; i < sorted.length - 1; i++) {
      expect(sorted[i].priorityScore).toBeGreaterThanOrEqual(sorted[i + 1].priorityScore);
    }

    // Verify expected factor-dominance ranking
    const scoreMap = new Map(scored.map(item => [item.id, item.priorityScore]));
    const scoreA = scoreMap.get('A-all-factors')!;
    const scoreB = scoreMap.get('B-overdue-blocker')!;
    const scoreC = scoreMap.get('C-today-assigned')!;
    const scoreD = scoreMap.get('D-blocker-recent')!;
    const scoreE = scoreMap.get('E-recent-only')!;
    const scoreF = scoreMap.get('F-no-factors')!;

    // All-factors dominates everything
    expect(scoreA).toBeGreaterThan(scoreB);
    // Overdue+blocker beats due-today combo despite slack's lower weight
    expect(scoreB).toBeGreaterThan(scoreC);
    // Due-today+assigned+follow-up+recent beats blocker+recent alone
    expect(scoreC).toBeGreaterThan(scoreD);
    // Blocker+recent beats recency-only (especially with calendar's lower weight)
    expect(scoreD).toBeGreaterThan(scoreE);
    // Any active factor beats zero
    expect(scoreE).toBeGreaterThan(scoreF);
    expect(scoreF).toBe(0);
  });
});
