import { describe, it, expect } from 'vitest';
import { normalizeEmail } from '../src/normalizeEmail.js';
import type { EmailMessage } from '../src/normalizeEmail.js';
import { normalizeNotion } from '../src/normalize-notion.js';
import { normalizeTrello } from '../src/normalizeTrello.js';
import type { TrelloCard } from '../src/normalizeTrello.js';

describe('normalizeEmail', () => {
  it('flagged email maps sender as owner and subject as title', () => {
    const message: EmailMessage = {
      messageId: 'em-001',
      subject: 'Q1 budget review needed',
      date: '2026-03-20T09:00:00Z',
      from: 'boss@acme.com',
      to: ['me@acme.com'],
      webmailUrl: 'https://mail.acme.com/msg/em-001',
    };

    const item = normalizeEmail(message, 'awaiting-reply');

    expect(item.id).toBe('email:em-001');
    expect(item.source).toBe('email:inbox');
    expect(item.sourceType).toBe('email');
    expect(item.title).toBe('Q1 budget review needed');
    expect(item.owner).toBe('boss@acme.com');
    expect(item.url).toBe('https://mail.acme.com/msg/em-001');
    expect(item.status).toBe('open');
    expect(item.confidence).toBe(1.0);
  });

  it('thread awaiting reply preserves timing and marks open for follow-up', () => {
    const message: EmailMessage = {
      messageId: 'em-002',
      subject: 'Re: Deployment schedule',
      date: '2026-03-18T14:00:00Z',
      lastMessageDate: '2026-03-22T10:30:00Z',
      from: 'colleague@acme.com',
      to: ['me@acme.com'],
      webmailUrl: 'https://mail.acme.com/msg/em-002',
    };

    const item = normalizeEmail(message, 'awaiting-reply');

    expect(item.id).toBe('email:em-002');
    expect(item.source).toBe('email:inbox');
    expect(item.sourceType).toBe('email');
    expect(item.title).toBe('Re: Deployment schedule');
    expect(item.owner).toBe('colleague@acme.com');
    expect(item.status).toBe('open');
    expect(item.createdAt).toBe('2026-03-18T14:00:00Z');
    expect(item.updatedAt).toBe('2026-03-22T10:30:00Z');
    expect(item.replyDraft).toBeNull();
    expect(item.followUpQuestion).toBeNull();
    expect(item.url).toBe('https://mail.acme.com/msg/em-002');
  });

  it('flagged-sent email sets owner to recipient not sender and does not mark as blocker', () => {
    const message: EmailMessage = {
      messageId: 'em-003',
      subject: 'Follow up: design review',
      date: '2026-03-19T11:00:00Z',
      from: 'me@acme.com',
      to: ['designer@acme.com'],
      webmailUrl: 'https://mail.acme.com/msg/em-003',
    };

    const item = normalizeEmail(message, 'flagged-sent');

    expect(item.id).toBe('email:em-003');
    expect(item.source).toBe('email:sent');
    expect(item.sourceType).toBe('email');
    expect(item.title).toBe('Follow up: design review');
    expect(item.owner).toBe('designer@acme.com');
    expect(item.status).toBe('waiting');
    expect(item.blocker).toBeNull();
    expect(item.url).toBe('https://mail.acme.com/msg/em-003');
  });

  it('email without subject produces valid ActionItem with degraded confidence', () => {
    const message: EmailMessage = {
      messageId: 'em-004',
      date: '2026-03-21T08:00:00Z',
      from: 'noreply@service.com',
      to: ['me@acme.com'],
      webmailUrl: 'https://mail.acme.com/msg/em-004',
    };

    const item = normalizeEmail(message, 'awaiting-reply');

    expect(item.id).toBe('email:em-004');
    expect(item.source).toBe('email:inbox');
    expect(item.sourceType).toBe('email');
    expect(item.title).toBe('No subject');
    expect(item.summary).toBe('');
    expect(item.confidence).toBe(0.8);
    expect(item.url).toBe('https://mail.acme.com/msg/em-004');
  });

  it('email with multiple recipients populates participants array correctly', () => {
    const message: EmailMessage = {
      messageId: 'em-005',
      subject: 'Team sync notes',
      date: '2026-03-22T15:00:00Z',
      from: 'lead@acme.com',
      to: ['dev1@acme.com', 'dev2@acme.com', 'dev3@acme.com'],
      webmailUrl: 'https://mail.acme.com/msg/em-005',
    };

    const item = normalizeEmail(message, 'awaiting-reply');

    expect(item.id).toBe('email:em-005');
    expect(item.source).toBe('email:inbox');
    expect(item.sourceType).toBe('email');
    expect(item.title).toBe('Team sync notes');
    expect(item.url).toBe('https://mail.acme.com/msg/em-005');
    expect(item.participants).toHaveLength(4);
    expect(item.participants[0]).toBe('lead@acme.com');
    expect(item.participants).toContain('dev1@acme.com');
    expect(item.participants).toContain('dev2@acme.com');
    expect(item.participants).toContain('dev3@acme.com');
  });
});

describe('normalizeNotion', () => {
  it('pages with unchecked TODO checkboxes produce one ActionItem per page with page URL', () => {
    const raw = [
      {
        id: 'page-001',
        url: 'https://notion.so/page-001',
        created_time: '2026-03-15T10:00:00Z',
        last_edited_time: '2026-03-20T14:00:00Z',
        properties: {
          Name: { title: [{ plain_text: 'Fix homepage layout' }] },
          Done: { checkbox: false },
          Assignee: { people: [{ name: 'Alice', id: 'user-alice' }] },
        },
      },
      {
        id: 'page-002',
        url: 'https://notion.so/page-002',
        created_time: '2026-03-16T11:00:00Z',
        last_edited_time: '2026-03-21T09:00:00Z',
        properties: {
          Name: { title: [{ plain_text: 'Update footer links' }] },
          Done: { checkbox: false },
          Assignee: { people: [{ name: 'Alice', id: 'user-alice' }] },
        },
      },
    ];

    const result = normalizeNotion(raw);
    expect(result).toHaveLength(2);

    for (const item of result) {
      expect(item.id).toBeDefined();
      expect(item.id).not.toBe('');
      expect(item.source).toBe('notion');
      expect(item.sourceType).toBe('notion');
      expect(item.title).toBeDefined();
      expect(item.title).not.toBe('');
      expect(item.url).toBeDefined();
      expect(item.url).not.toBe('');
    }

    expect(result[0].id).toBe('notion:page-001');
    expect(result[0].title).toBe('Fix homepage layout');
    expect(result[0].url).toBe('https://notion.so/page-001');
    expect(result[1].id).toBe('notion:page-002');
    expect(result[1].title).toBe('Update footer links');
    expect(result[1].url).toBe('https://notion.so/page-002');
  });

  it('page with all checkboxes checked produces zero ActionItems', () => {
    const raw = [
      {
        id: 'page-003',
        url: 'https://notion.so/page-003',
        created_time: '2026-03-10T08:00:00Z',
        last_edited_time: '2026-03-18T12:00:00Z',
        properties: {
          Name: { title: [{ plain_text: 'Setup CI pipeline' }] },
          Done: { checkbox: true },
        },
      },
    ];

    const result = normalizeNotion(raw);
    expect(result).toHaveLength(0);
  });

  it('page with assignee property extracts the assigned user as owner', () => {
    const raw = [
      {
        id: 'page-004',
        url: 'https://notion.so/page-004',
        created_time: '2026-03-12T09:00:00Z',
        last_edited_time: '2026-03-21T11:00:00Z',
        properties: {
          Name: { title: [{ plain_text: 'Review API documentation' }] },
          Owner: { people: [{ name: 'Bob', id: 'user-bob' }] },
        },
      },
    ];

    const result = normalizeNotion(raw);
    expect(result).toHaveLength(1);

    const item = result[0];
    expect(item.id).toBe('notion:page-004');
    expect(item.source).toBe('notion');
    expect(item.sourceType).toBe('notion');
    expect(item.title).toBe('Review API documentation');
    expect(item.owner).toBe('Bob');
    expect(item.url).toBe('https://notion.so/page-004');
    expect(item.participants).toContain('Bob');
    expect(item.confidence).toBe(1.0);
  });
});

describe('normalizeTrello', () => {
  it('assigned card maps list name into status and due date into dueAt', () => {
    const card: TrelloCard = {
      id: 'card-001',
      name: 'Implement search feature',
      idMembers: ['member-alice'],
      due: '2026-04-01T17:00:00Z',
      shortUrl: 'https://trello.com/c/abc123',
      list: { name: 'In Progress' },
    };

    const item = normalizeTrello(card);

    expect(item.id).toBe('trello:card-001');
    expect(item.source).toBe('trello');
    expect(item.sourceType).toBe('trello');
    expect(item.title).toBe('Implement search feature');
    expect(item.owner).toBe('member-alice');
    expect(item.dueAt).toBe('2026-04-01T17:00:00Z');
    expect(item.url).toBe('https://trello.com/c/abc123');
    expect(item.status).toBe('open');
  });

  it('overdue card with blocked label sets blocker flag and confidence >= 0.8', () => {
    const card: TrelloCard = {
      id: 'card-002',
      name: 'Deploy to production',
      idMembers: ['member-bob'],
      due: '2026-03-20T12:00:00Z',
      shortUrl: 'https://trello.com/c/def456',
      list: { name: 'Backlog' },
      labels: [{ name: 'blocked' }],
    };

    const item = normalizeTrello(card);

    expect(item.id).toBe('trello:card-002');
    expect(item.source).toBe('trello');
    expect(item.sourceType).toBe('trello');
    expect(item.title).toBe('Deploy to production');
    expect(item.blocker).toBe('blocked');
    expect(item.confidence).toBeGreaterThanOrEqual(0.8);
    expect(item.dueAt).toBe('2026-03-20T12:00:00Z');
    expect(item.url).toBe('https://trello.com/c/def456');
  });
});
