import { describe, it, expect, vi, afterEach } from 'vitest';
import { normalizeTrello, DEFAULT_CLOSED_LIST_NAMES } from './normalizeTrello.js';
import type { TrelloCard } from './normalizeTrello.js';

// ---- Structured security-event log helpers (SEC-OPS-001) ----

/** Capture structured security events emitted via console.warn during `fn`. */
function captureSecurityLogs(fn: () => void): unknown[] {
  const spy = vi.spyOn(console, 'warn').mockImplementation(() => {});
  fn();
  const parsed: unknown[] = [];
  for (const call of spy.mock.calls) {
    try { parsed.push(JSON.parse(String(call[0]))); } catch { /* non-JSON warn */ }
  }
  spy.mockRestore();
  return parsed;
}

function assertStructuredEvent(event: unknown): void {
  expect(event).toHaveProperty('event_type');
  expect(event).toHaveProperty('actor');
  expect(event).toHaveProperty('outcome');
  expect(event).toHaveProperty('timestamp');
}

afterEach(() => { vi.restoreAllMocks(); });

// ---- Fixtures ----

function makeTrelloCard(overrides: Partial<TrelloCard> = {}): TrelloCard {
  return {
    id: 'card-001',
    name: 'Implement login page',
    idMembers: ['member-1'],
    due: '2024-03-01T00:00:00Z',
    shortUrl: 'https://trello.com/c/abc123',
    list: { name: 'In Progress' },
    labels: [],
    ...overrides,
  };
}

// ---- Trello tests ----

describe('normalizeTrello', () => {
  // 1. Happy path
  it('maps a Trello card to a valid ActionItem with correct fields', () => {
    const spy = vi.spyOn(console, 'warn').mockImplementation(() => {});
    const item = normalizeTrello(makeTrelloCard());
    spy.mockRestore();

    expect(item.id).toBe('trello:card-001');
    expect(item.sourceType).toBe('trello');
    expect(item.title).toBe('Implement login page');
    expect(item.owner).toBe('member-1');
    expect(item.dueAt).toBe('2024-03-01T00:00:00Z');
    expect(item.url).toBe('https://trello.com/c/abc123');
    expect(item.status).toBe('open');
    expect(item.blocker).toBeNull();
    expect(item.dedupeKeys).toEqual(['trello:card-001']);
    expect(item.confidence).toBe(1.0);
  });

  // 2. Status mapping across list names including unknown lists
  it('maps status based on list name against closedListNames', () => {
    const spy = vi.spyOn(console, 'warn').mockImplementation(() => {});

    expect(DEFAULT_CLOSED_LIST_NAMES).toEqual(['Done', 'Closed', 'Archived']);

    const doneCard = normalizeTrello(makeTrelloCard({ list: { name: 'Done' } }));
    expect(doneCard.status).toBe('done');

    const closedCard = normalizeTrello(makeTrelloCard({ list: { name: 'Closed' } }));
    expect(closedCard.status).toBe('done');

    const archivedCard = normalizeTrello(makeTrelloCard({ list: { name: 'Archived' } }));
    expect(archivedCard.status).toBe('done');

    // Case-insensitive matching
    const doneLower = normalizeTrello(makeTrelloCard({ list: { name: 'done' } }));
    expect(doneLower.status).toBe('done');

    // Unknown list names map to open
    const backlog = normalizeTrello(makeTrelloCard({ list: { name: 'Backlog' } }));
    expect(backlog.status).toBe('open');

    const inProgress = normalizeTrello(makeTrelloCard({ list: { name: 'In Progress' } }));
    expect(inProgress.status).toBe('open');

    // Blocked label sets blocker field
    const blocked = normalizeTrello(makeTrelloCard({
      labels: [{ name: 'Blocked' }, { name: 'Bug' }],
    }));
    expect(blocked.blocker).toBe('blocked');

    // Case-insensitive blocked label
    const blockedLower = normalizeTrello(makeTrelloCard({
      labels: [{ name: 'blocked' }],
    }));
    expect(blockedLower.blocker).toBe('blocked');

    spy.mockRestore();
  });

  // 3. Missing due date and no members — emits structured security event
  it('handles a card with missing due date and no members', () => {
    const logs = captureSecurityLogs(() => {
      const item = normalizeTrello(makeTrelloCard({
        idMembers: undefined,
        members: undefined,
        due: null,
      }));

      expect(item.dueAt).toBeNull();
      expect(item.owner).toBe('');
      expect(item.participants).toEqual([]);
      expect(item.confidence).toBeLessThan(1.0);
      expect(item.title).toBe('Implement login page');
      expect(item.dedupeKeys).toEqual(['trello:card-001']);
    });

    // SEC-OPS-001: verify structured security event for missing owner
    expect(logs.length).toBeGreaterThan(0);
    for (const event of logs) {
      assertStructuredEvent(event);
    }
  });
});

