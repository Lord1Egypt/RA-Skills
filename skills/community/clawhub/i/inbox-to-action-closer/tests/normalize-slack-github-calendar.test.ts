import { describe, it, expect } from 'vitest';
import { normalizeSlack } from '../src/normalize-slack.js';
import { normalizeGithub } from '../src/normalize-github.js';
import { normalizeCalendar } from '../src/normalize-calendar.js';

describe('normalizeSlack', () => {
  it('maps standard channel message with all fields correctly', () => {
    const raw = [
      {
        ts: '1711300000.000100',
        channel: 'C01GENERAL',
        text: 'Deploy the hotfix to staging',
        user: 'U001ALICE',
        permalink: 'https://myteam.slack.com/archives/C01GENERAL/p1711300000000100',
      },
    ];

    const result = normalizeSlack(raw);
    expect(result).toHaveLength(1);

    const item = result[0];
    expect(item.id).toBe('slack:C01GENERAL-1711300000.000100');
    expect(item.source).toBe('slack:C01GENERAL');
    expect(item.sourceType).toBe('slack');
    expect(item.title).toBe('Deploy the hotfix to staging');
    expect(item.summary).toBe('Deploy the hotfix to staging');
    expect(item.owner).toBe('U001ALICE');
    expect(item.participants).toEqual(['U001ALICE']);
    expect(item.url).toBe(
      'https://myteam.slack.com/archives/C01GENERAL/p1711300000000100',
    );
    expect(item.status).toBe('open');
    expect(item.dueAt).toBeNull();
    expect(item.confidence).toBe(1.0);
    expect(item.dedupeKeys).toContain(item.url);
  });

  it('threaded reply preserves parent URL and sets participants', () => {
    const raw = [
      {
        ts: '1711300500.000200',
        channel: 'C02DEV',
        text: 'I will handle this',
        user: 'U002BOB',
        thread_ts: '1711300000.000100',
        reply_users: ['U001ALICE', 'U003CAROL'],
      },
    ];

    const result = normalizeSlack(raw);
    expect(result).toHaveLength(1);

    const item = result[0];
    expect(item.id).toBe('slack:C02DEV-1711300500.000200');
    expect(item.source).toBe('slack:C02DEV');
    expect(item.sourceType).toBe('slack');
    expect(item.title).toBe('I will handle this');
    // isReply: thread_ts !== ts → URL uses parent thread_ts
    expect(item.url).toBe(
      'https://slack.com/archives/C02DEV/p1711300000000100',
    );
    expect(item.participants).toEqual(['U002BOB', 'U001ALICE', 'U003CAROL']);
  });

  it('DM sets sourceType and owner correctly', () => {
    const raw = [
      {
        ts: '1711301000.000300',
        channel: 'D04DM',
        text: 'Hey can you review my PR?',
        user: 'U004DAVE',
      },
    ];

    const result = normalizeSlack(raw);
    expect(result).toHaveLength(1);

    const item = result[0];
    expect(item.id).toBe('slack:D04DM-1711301000.000300');
    expect(item.sourceType).toBe('slack');
    expect(item.source).toBe('slack:D04DM');
    expect(item.owner).toBe('U004DAVE');
    expect(item.title).toBe('Hey can you review my PR?');
    expect(item.url).toBe(
      'https://slack.com/archives/D04DM/p1711301000000300',
    );
  });

  it('message with missing text produces valid ActionItem with empty summary', () => {
    const raw = [
      {
        ts: '1711301500.000400',
        channel: 'C05RANDOM',
        user: 'U005EVE',
        // text intentionally omitted
      },
    ];

    const result = normalizeSlack(raw);
    expect(result).toHaveLength(1);

    const item = result[0];
    expect(item.id).toBe('slack:C05RANDOM-1711301500.000400');
    expect(item.source).toBe('slack:C05RANDOM');
    expect(item.sourceType).toBe('slack');
    expect(item.summary).toBe('');
    expect(item.title).toBe('Message in C05RANDOM');
    expect(item.url).toBeDefined();
    expect(item.confidence).toBe(0.9); // -0.1 for missing text
  });

  it('unresolved thread with no reply sets followUpQuestion and blocker to null', () => {
    const raw = [
      {
        ts: '1711302000.000500',
        channel: 'C06SUPPORT',
        text: 'Is the deploy pipeline broken?',
        user: 'U006FRANK',
        thread_ts: '1711302000.000500', // thread_ts === ts → this is the parent
        // no reply_users, no latest_reply
      },
    ];

    const result = normalizeSlack(raw);
    expect(result).toHaveLength(1);

    const item = result[0];
    expect(item.id).toBe('slack:C06SUPPORT-1711302000.000500');
    expect(item.sourceType).toBe('slack');
    expect(item.title).toBe('Is the deploy pipeline broken?');
    expect(item.url).toBeDefined();
    expect(item.followUpQuestion).toBeNull();
    expect(item.blocker).toBeNull();
    expect(item.participants).toEqual(['U006FRANK']);
    expect(item.status).toBe('open');
  });
});

describe('normalizeGithub', () => {
  it('open PR maps title/url/owner/status correctly', () => {
    const raw = [
      {
        number: 42,
        title: 'Add caching layer for API responses',
        body: 'This PR adds Redis caching to reduce API latency.',
        html_url: 'https://github.com/acme/app/pull/42',
        state: 'open',
        user: { login: 'alice' },
        created_at: '2026-03-20T10:00:00Z',
        updated_at: '2026-03-21T15:30:00Z',
        pull_request: {},
        repository: { full_name: 'acme/app' },
      },
    ];

    const result = normalizeGithub(raw);
    expect(result).toHaveLength(1);

    const item = result[0];
    expect(item.id).toBe('github:acme/app#42');
    expect(item.source).toBe('github:acme/app');
    expect(item.sourceType).toBe('github');
    expect(item.title).toBe('Add caching layer for API responses');
    expect(item.url).toBe('https://github.com/acme/app/pull/42');
    expect(item.owner).toBe('alice');
    expect(item.status).toBe('open');
    expect(item.confidence).toBe(1.0);
  });

  it('review request sets owner to reviewer', () => {
    const raw = [
      {
        number: 55,
        title: 'Refactor auth middleware',
        body: 'Needs security review.',
        html_url: 'https://github.com/acme/app/pull/55',
        state: 'open',
        created_at: '2026-03-19T08:00:00Z',
        updated_at: '2026-03-20T09:00:00Z',
        requested_reviewer: { login: 'bob-reviewer' },
        user: { login: 'alice' },
        repository: { full_name: 'acme/app' },
      },
    ];

    const result = normalizeGithub(raw);
    expect(result).toHaveLength(1);

    const item = result[0];
    expect(item.id).toBe('github:acme/app#55');
    expect(item.sourceType).toBe('github');
    expect(item.title).toBe('Refactor auth middleware');
    expect(item.url).toBe('https://github.com/acme/app/pull/55');
    expect(item.owner).toBe('bob-reviewer');
    expect(item.blocker).toBeNull();
    expect(item.participants).toContain('bob-reviewer');
    expect(item.participants).toContain('alice');
    expect(item.status).toBe('open');
  });

  it('assigned issue maps body into summary and sets dueAt from milestone', () => {
    const raw = [
      {
        number: 100,
        title: 'Fix login timeout on mobile',
        body: 'Users report 30s timeout on iOS Safari.',
        html_url: 'https://github.com/acme/app/issues/100',
        state: 'open',
        assignee: { login: 'carol' },
        user: { login: 'dave' },
        created_at: '2026-03-15T12:00:00Z',
        updated_at: '2026-03-22T16:00:00Z',
        milestone: { due_on: '2026-04-01T00:00:00Z' },
        repository: { full_name: 'acme/app' },
      },
    ];

    const result = normalizeGithub(raw);
    expect(result).toHaveLength(1);

    const item = result[0];
    expect(item.id).toBe('github:acme/app#100');
    expect(item.sourceType).toBe('github');
    expect(item.title).toBe('Fix login timeout on mobile');
    expect(item.url).toBe('https://github.com/acme/app/issues/100');
    expect(item.summary).toBe('Users report 30s timeout on iOS Safari.');
    expect(item.dueAt).toBe('2026-04-01T00:00:00Z');
    expect(item.owner).toBe('carol');
    expect(item.participants).toContain('carol');
    expect(item.participants).toContain('dave');
  });

  it('draft PR is normalised with open status', () => {
    const raw = [
      {
        number: 77,
        title: 'WIP: Database migration v2',
        body: 'Draft — do not merge yet.',
        html_url: 'https://github.com/acme/app/pull/77',
        state: 'open',
        draft: true,
        user: { login: 'eve' },
        created_at: '2026-03-18T14:00:00Z',
        updated_at: '2026-03-18T14:30:00Z',
        pull_request: {},
        repository: { full_name: 'acme/app' },
      },
    ];

    const result = normalizeGithub(raw);
    expect(result).toHaveLength(1);

    const item = result[0];
    expect(item.id).toBe('github:acme/app#77');
    expect(item.sourceType).toBe('github');
    expect(item.title).toBe('WIP: Database migration v2');
    expect(item.url).toBe('https://github.com/acme/app/pull/77');
    // Adapter does not distinguish draft PRs — status based on state/merged
    expect(item.status).toBe('open');
    expect(item.owner).toBe('eve');
    expect(item.confidence).toBe(1.0);
  });
});

describe('normalizeCalendar', () => {
  it('upcoming event extracts correct dueAt and participants', () => {
    const raw = [
      {
        id: 'cal-evt-001',
        summary: 'Sprint planning',
        description: 'Review backlog and assign stories for next sprint.',
        htmlLink: 'https://calendar.google.com/event?eid=cal-evt-001',
        start: { dateTime: '2026-03-26T09:00:00Z' },
        end: { dateTime: '2026-03-26T10:00:00Z' },
        created: '2026-03-20T08:00:00Z',
        updated: '2026-03-24T12:00:00Z',
        organizer: { displayName: 'Team Lead', email: 'lead@example.com' },
        attendees: [
          { displayName: 'Alice', email: 'alice@example.com' },
          { displayName: 'Bob', email: 'bob@example.com' },
        ],
      },
    ];

    const result = normalizeCalendar(raw);
    expect(result).toHaveLength(1);

    const item = result[0];
    expect(item.id).toBe('calendar:cal-evt-001');
    expect(item.source).toBe('calendar');
    expect(item.sourceType).toBe('calendar');
    expect(item.title).toBe('Sprint planning');
    expect(item.url).toBe(
      'https://calendar.google.com/event?eid=cal-evt-001',
    );
    // dueAt from end.dateTime
    expect(item.dueAt).toBe('2026-03-26T10:00:00Z');
    expect(item.participants).toContain('Team Lead');
    expect(item.participants).toContain('Alice');
    expect(item.participants).toContain('Bob');
    // owner is first attendee (extractOwner checks attendees first)
    expect(item.owner).toBe('Alice');
    expect(item.confidence).toBe(1.0);
  });

  it('cancelled event produces zero ActionItems', () => {
    const raw = [
      {
        id: 'cal-evt-002',
        summary: 'Cancelled standup',
        status: 'cancelled',
        start: { dateTime: '2026-03-10T09:00:00Z' },
        end: { dateTime: '2026-03-10T09:15:00Z' },
        created: '2026-03-01T08:00:00Z',
        updated: '2026-03-09T17:00:00Z',
      },
    ];

    const result = normalizeCalendar(raw);
    expect(result).toHaveLength(0);
  });
});
