import type { ActionItem, Status } from './types.js';

function isRecord(v: unknown): v is Record<string, unknown> {
  return typeof v === 'object' && v !== null && !Array.isArray(v);
}

function str(obj: Record<string, unknown>, key: string): string | undefined {
  const v = obj[key];
  return typeof v === 'string' ? v : undefined;
}

function extractTitle(properties: Record<string, unknown>): string {
  for (const key of ['Name', 'name', 'Title', 'title']) {
    const prop = properties[key];
    if (!isRecord(prop)) continue;
    const titleArr = prop.title;
    if (!Array.isArray(titleArr)) continue;
    const texts: string[] = [];
    for (const block of titleArr) {
      if (isRecord(block)) {
        const text = str(block, 'plain_text');
        if (text) texts.push(text);
      }
    }
    if (texts.length > 0) return texts.join('');
  }
  return '';
}

function extractAssignee(properties: Record<string, unknown>): string | null {
  for (const key of ['Assignee', 'assignee', 'Assigned', 'assigned', 'Owner', 'owner']) {
    const prop = properties[key];
    if (!isRecord(prop)) continue;
    const people = prop.people;
    if (!Array.isArray(people) || people.length === 0) continue;
    const first = people[0];
    if (isRecord(first)) {
      return str(first, 'name') ?? str(first, 'id') ?? null;
    }
  }
  return null;
}

function extractDueDate(properties: Record<string, unknown>): string | null {
  for (const key of ['Due', 'due', 'Due Date', 'due_date', 'Date', 'date', 'Deadline', 'deadline']) {
    const prop = properties[key];
    if (!isRecord(prop)) continue;
    const dateObj = prop.date;
    if (!isRecord(dateObj)) continue;
    return str(dateObj, 'start') ?? str(dateObj, 'end') ?? null;
  }
  return null;
}

function extractStatus(properties: Record<string, unknown>): Status {
  for (const key of ['Status', 'status']) {
    const prop = properties[key];
    if (!isRecord(prop)) continue;
    for (const subKey of ['status', 'select']) {
      const val = prop[subKey];
      if (isRecord(val)) {
        const name = str(val, 'name')?.toLowerCase();
        if (name === 'done' || name === 'complete' || name === 'completed') return 'done';
        if (name === 'in progress' || name === 'in_progress') return 'in_progress';
        if (name === 'waiting' || name === 'blocked') return 'waiting';
      }
    }
  }
  return 'open';
}

function isCheckedComplete(properties: Record<string, unknown>): boolean {
  for (const key of ['Done', 'done', 'Complete', 'complete', 'Completed', 'completed']) {
    const prop = properties[key];
    if (!isRecord(prop)) continue;
    if (prop.checkbox === true) return true;
  }
  return false;
}

function collectParticipants(properties: Record<string, unknown>): string[] {
  const parts: string[] = [];
  for (const key of Object.keys(properties)) {
    const prop = properties[key];
    if (!isRecord(prop)) continue;
    const people = prop.people;
    if (!Array.isArray(people)) continue;
    for (const person of people) {
      if (isRecord(person)) {
        const name = str(person, 'name') ?? str(person, 'id');
        if (name && !parts.includes(name)) parts.push(name);
      }
    }
  }
  return parts;
}

export function normalizeNotion(raw: unknown): ActionItem[] {
  if (!Array.isArray(raw)) {
    if (raw !== undefined && raw !== null) {
      console.warn('normalizeNotion: expected array, got ' + typeof raw);
    }
    return [];
  }

  const items: ActionItem[] = [];

  for (const entry of raw) {
    if (!isRecord(entry)) {
      console.warn('normalizeNotion: skipping non-object entry');
      continue;
    }

    const pageId = str(entry, 'id') ?? '';
    const pageUrl = str(entry, 'url') ?? '';
    const properties = isRecord(entry.properties)
      ? (entry.properties as Record<string, unknown>)
      : {};

    const status = extractStatus(properties);

    if (status === 'done' || isCheckedComplete(properties)) {
      continue;
    }

    const title = extractTitle(properties);
    const owner = extractAssignee(properties);
    const dueAt = extractDueDate(properties);
    const participants = collectParticipants(properties);

    const id = pageId ? `notion:${pageId}` : `notion:unknown-${items.length}`;
    const createdAt = str(entry, 'created_time') ?? new Date(0).toISOString();
    const updatedAt = str(entry, 'last_edited_time') ?? createdAt;

    let confidence = 1.0;
    if (!owner) confidence -= 0.2;
    if (!title) confidence -= 0.1;
    confidence = Math.max(0.7, Math.round(confidence * 10) / 10);

    const dedupeKeys: string[] = [];
    if (pageId) dedupeKeys.push(pageId);
    if (pageUrl) dedupeKeys.push(pageUrl);

    items.push({
      id,
      source: 'notion',
      sourceType: 'notion',
      title: title || 'Untitled',
      summary: '',
      owner: owner as string, // null when no assignee — ticket requires no fabricated defaults
      participants,
      createdAt,
      updatedAt,
      dueAt,
      url: pageUrl,
      status,
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
