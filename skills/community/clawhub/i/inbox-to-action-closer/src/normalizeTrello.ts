import type { ActionItem } from './types.js';

export const DEFAULT_CLOSED_LIST_NAMES = ['Done', 'Closed', 'Archived'];

// ---- Structured security event logger (SEC-OPS-001) ----

interface SecurityEvent {
  event_type: string;
  actor: string;
  outcome: 'success' | 'rejected' | 'skipped' | 'degraded';
  detail?: string;
  timestamp: string;
}

function logSecurityEvent(event: SecurityEvent): void {
  console.warn(JSON.stringify(event));
}

export interface TrelloCard {
  id: string;
  name: string;
  idMembers?: string[];
  members?: Array<{ id?: string; fullName?: string; username?: string }>;
  due?: string | null;
  shortUrl: string;
  list?: { name: string };
  labels?: Array<{ name: string }>;
}

export function normalizeTrello(
  card: TrelloCard,
  closedListNames: string[] = DEFAULT_CLOSED_LIST_NAMES,
): ActionItem {
  let owner: string | null = null;
  if (card.idMembers && card.idMembers.length > 0) {
    owner = card.idMembers[0];
  } else if (card.members && card.members.length > 0) {
    const m = card.members[0];
    owner = m.fullName ?? m.username ?? m.id ?? null;
  }

  if (!owner) {
    logSecurityEvent({
      event_type: 'input_validation',
      actor: 'normalizeTrello',
      outcome: 'degraded',
      detail: 'Card has no assignable owner',
      timestamp: new Date().toISOString(),
    });
  }

  const listName = card.list?.name ?? '';
  const isClosed = closedListNames.some(
    (name) => name.toLowerCase() === listName.toLowerCase(),
  );

  const hasBlockedLabel = card.labels?.some(
    (label) => label.name.toLowerCase() === 'blocked',
  ) ?? false;

  const now = new Date().toISOString();

  return {
    id: `trello:${card.id}`,
    source: 'trello',
    sourceType: 'trello',
    title: card.name || 'Untitled',
    summary: '',
    owner: owner ?? '',
    participants: owner ? [owner] : [],
    createdAt: now,
    updatedAt: now,
    dueAt: card.due ?? null,
    url: card.shortUrl,
    status: isClosed ? 'done' : 'open',
    priorityScore: 0,
    blocker: hasBlockedLabel ? 'blocked' : null,
    replyDraft: null,
    followUpQuestion: null,
    suggestedNextAction: null,
    dedupeKeys: [`trello:${card.id}`],
    confidence: owner ? 1.0 : 0.8,
  };
}
