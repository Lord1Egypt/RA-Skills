import type { ActionItem } from './types.js';

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

export interface EmailMessage {
  messageId: string;
  subject?: string;
  date: string;
  lastMessageDate?: string;
  from: string;
  to: string[];
  webmailUrl?: string;
}

// context='awaiting-reply': owner is the sender (they're waiting on you).
// context='flagged-sent': owner is the recipient (you're waiting on them).
export function normalizeEmail(
  message: EmailMessage,
  context: 'awaiting-reply' | 'flagged-sent',
): ActionItem {
  if (!message.subject) {
    logSecurityEvent({
      event_type: 'input_validation',
      actor: 'normalizeEmail',
      outcome: 'degraded',
      detail: 'Email message has no subject',
      timestamp: new Date().toISOString(),
    });
  }

  const createdAt = message.date;
  const updatedAt = message.lastMessageDate ?? message.date;

  const owner =
    context === 'awaiting-reply'
      ? message.from
      : message.to[0] ?? '';

  const status = context === 'flagged-sent' ? 'waiting' : 'open';

  const url = message.webmailUrl ?? `mid:${message.messageId}`;

  const participants: string[] = [message.from];
  for (const recipient of message.to) {
    if (recipient && !participants.includes(recipient)) {
      participants.push(recipient);
    }
  }

  return {
    id: `email:${message.messageId}`,
    source: context === 'flagged-sent' ? 'email:sent' : 'email:inbox',
    sourceType: 'email',
    title: message.subject ?? 'No subject',
    summary: '',
    owner,
    participants,
    createdAt,
    updatedAt,
    dueAt: null,
    url,
    status,
    priorityScore: 0,
    blocker: null,
    replyDraft: null,
    followUpQuestion: null,
    suggestedNextAction: null,
    dedupeKeys: [`email:${message.messageId}`],
    confidence: message.subject ? 1.0 : 0.8,
  };
}
