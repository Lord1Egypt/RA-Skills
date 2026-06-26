import type { ActionItem } from './types.js';

function isRecord(v: unknown): v is Record<string, unknown> {
  return typeof v === 'object' && v !== null && !Array.isArray(v);
}

function str(obj: Record<string, unknown>, key: string): string | undefined {
  const v = obj[key];
  return typeof v === 'string' ? v : undefined;
}

function extractDateTime(value: unknown): string | null {
  if (typeof value === 'string') return value;
  if (isRecord(value)) {
    return str(value, 'dateTime') ?? str(value, 'date') ?? null;
  }
  return null;
}

function extractOwner(item: Record<string, unknown>): string | null {
  if (Array.isArray(item.attendees)) {
    for (const att of item.attendees) {
      if (isRecord(att)) {
        const name = str(att, 'displayName') ?? str(att, 'email');
        if (name) return name;
      }
    }
  }
  if (isRecord(item.organizer)) {
    const org = item.organizer as Record<string, unknown>;
    return str(org, 'displayName') ?? str(org, 'email') ?? null;
  }
  if (isRecord(item.creator)) {
    const cre = item.creator as Record<string, unknown>;
    return str(cre, 'displayName') ?? str(cre, 'email') ?? null;
  }
  return null;
}

function collectParticipants(item: Record<string, unknown>): string[] {
  const parts: string[] = [];
  function add(name: string | undefined): void {
    if (name && !parts.includes(name)) parts.push(name);
  }
  if (isRecord(item.organizer)) {
    const o = item.organizer as Record<string, unknown>;
    add(str(o, 'displayName') ?? str(o, 'email'));
  }
  if (Array.isArray(item.attendees)) {
    for (const att of item.attendees) {
      if (isRecord(att)) add(str(att, 'displayName') ?? str(att, 'email'));
    }
  }
  return parts;
}

export function normalizeCalendar(raw: unknown): ActionItem[] {
  if (!Array.isArray(raw)) {
    if (raw !== undefined && raw !== null) {
      console.warn('normalizeCalendar: expected array, got ' + typeof raw);
    }
    return [];
  }

  const items: ActionItem[] = [];

  for (const entry of raw) {
    if (!isRecord(entry)) {
      console.warn('normalizeCalendar: skipping non-object entry');
      continue;
    }

    if (str(entry, 'status') === 'cancelled') {
      continue;
    }

    const eventId = str(entry, 'id');
    const title = str(entry, 'summary') ?? str(entry, 'title') ?? '';
    const htmlLink = str(entry, 'htmlLink') ?? str(entry, 'url') ?? '';

    const id = eventId ? `calendar:${eventId}` : `calendar:unknown-${items.length}`;

    const dueAt = str(entry, 'dueDate')
      ?? extractDateTime(entry.end)
      ?? extractDateTime(entry.start)
      ?? null;

    const owner = extractOwner(entry);
    const participants = collectParticipants(entry);

    const createdAt = str(entry, 'created') ?? new Date(0).toISOString();
    const updatedAt = str(entry, 'updated') ?? createdAt;
    const description = str(entry, 'description') ?? '';

    let confidence = 1.0;
    if (!owner) confidence -= 0.2;
    if (!title) confidence -= 0.1;
    confidence = Math.max(0.7, Math.round(confidence * 10) / 10);

    const dedupeKeys: string[] = [];
    if (eventId) dedupeKeys.push(eventId);
    if (htmlLink) dedupeKeys.push(htmlLink);

    items.push({
      id,
      source: 'calendar',
      sourceType: 'calendar',
      title: title || 'Untitled event',
      summary: description,
      owner: owner as string, // null when no owner — ticket requires no fabricated defaults
      participants,
      createdAt,
      updatedAt,
      dueAt,
      url: htmlLink,
      status: 'open',
      priorityScore: 0,
      blocker: null,
      replyDraft: null,
      followUpQuestion: null,
      suggestedNextAction: null,
      dedupeKeys,
      confidence,
    });
  }

  return items;
}
