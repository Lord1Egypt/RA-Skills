import { describe, it, expect } from 'vitest';
import { normalizeCalendar } from './normalize-calendar.js';

function makeCalendarEvent(overrides: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    id: 'evt_abc123',
    summary: 'Sprint retrospective',
    description: 'Review action items from last sprint',
    status: 'confirmed',
    htmlLink: 'https://calendar.google.com/event?eid=evt_abc123',
    start: { dateTime: '2024-02-01T14:00:00Z' },
    end: { dateTime: '2024-02-01T15:00:00Z' },
    created: '2024-01-20T09:00:00Z',
    updated: '2024-01-25T10:00:00Z',
    organizer: { email: 'alice@example.com', displayName: 'Alice' },
    attendees: [
      { email: 'alice@example.com', displayName: 'Alice', organizer: true },
      { email: 'bob@example.com', displayName: 'Bob' },
    ],
    ...overrides,
  };
}

describe('normalizeCalendar', () => {
  // ---- 1. Happy path: well-formed calendar event ----
  it('maps a well-formed calendar event to a valid ActionItem', () => {
    const result = normalizeCalendar([makeCalendarEvent()]);

    expect(result).toHaveLength(1);
    const item = result[0];
    expect(item.id).toBe('calendar:evt_abc123');
    expect(item.sourceType).toBe('calendar');
    expect(item.source).toBe('calendar');
    expect(item.title).toBe('Sprint retrospective');
    expect(item.summary).toBe('Review action items from last sprint');
    expect(item.owner).toBe('Alice');
    expect(item.url).toBe('https://calendar.google.com/event?eid=evt_abc123');
    expect(item.status).toBe('open');
    expect(item.dueAt).toBe('2024-02-01T15:00:00Z');
    expect(item.dedupeKeys).toContain('evt_abc123');
    expect(item.dedupeKeys).toContain('https://calendar.google.com/event?eid=evt_abc123');
    expect(item.participants).toContain('Alice');
    expect(item.participants).toContain('Bob');
    expect(item.confidence).toBe(1.0);
  });

  // ---- 2. Missing fields: no attendees, no organizer ----
  it('handles missing attendees and organizer with owner=null and no fabricated defaults', () => {
    const result = normalizeCalendar([makeCalendarEvent({
      attendees: undefined,
      organizer: undefined,
      start: undefined,
      end: undefined,
    })]);

    expect(result).toHaveLength(1);
    const item = result[0];
    expect(item.owner).toBeNull();
    expect(item.dueAt).toBeNull();
    expect(item.participants).toEqual([]);
    expect(item.confidence).toBeLessThan(1.0);
    expect(item.confidence).toBeGreaterThanOrEqual(0.7);
    // Still has valid structure
    expect(item.sourceType).toBe('calendar');
    expect(item.id).toBe('calendar:evt_abc123');
  });

  // ---- 3. Cancelled event yields empty result ----
  it('skips cancelled calendar events', () => {
    const result = normalizeCalendar([makeCalendarEvent({ status: 'cancelled' })]);

    expect(result).toHaveLength(0);
  });
});
