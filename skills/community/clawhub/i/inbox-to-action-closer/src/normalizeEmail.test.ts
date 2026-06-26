import { describe, it, expect, vi, afterEach } from 'vitest';
import { normalizeEmail } from './normalizeEmail.js';
import type { EmailMessage } from './normalizeEmail.js';

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

function makeEmailMessage(overrides: Partial<EmailMessage> = {}): EmailMessage {
  return {
    messageId: 'msg-001',
    subject: 'Project status update',
    date: '2024-01-10T09:00:00Z',
    lastMessageDate: '2024-01-11T14:00:00Z',
    from: 'alice@example.com',
    to: ['bob@example.com'],
    webmailUrl: 'https://mail.example.com/thread/001',
    ...overrides,
  };
}

// ---- Email tests ----

describe('normalizeEmail', () => {
  // 1. Awaiting-reply mapping
  it('maps an awaiting-reply message with owner as sender and status open', () => {
    const spy = vi.spyOn(console, 'warn').mockImplementation(() => {});
    const item = normalizeEmail(makeEmailMessage(), 'awaiting-reply');
    spy.mockRestore();

    expect(item.id).toBe('email:msg-001');
    expect(item.sourceType).toBe('email');
    expect(item.source).toBe('email:inbox');
    expect(item.title).toBe('Project status update');
    expect(item.owner).toBe('alice@example.com');
    expect(item.status).toBe('open');
    expect(item.createdAt).toBe('2024-01-10T09:00:00Z');
    expect(item.updatedAt).toBe('2024-01-11T14:00:00Z');
    expect(item.url).toBe('https://mail.example.com/thread/001');
    expect(item.dedupeKeys).toEqual(['email:msg-001']);
    expect(item.confidence).toBe(1.0);
    expect(item.participants).toEqual(['alice@example.com', 'bob@example.com']);
  });

  // 2. Flagged-sent mapping
  it('maps a flagged-sent message with owner as recipient and status waiting', () => {
    const spy = vi.spyOn(console, 'warn').mockImplementation(() => {});
    const item = normalizeEmail(
      makeEmailMessage({
        messageId: 'msg-002',
        from: 'me@example.com',
        to: ['client@example.com'],
        webmailUrl: undefined,
      }),
      'flagged-sent',
    );
    spy.mockRestore();

    expect(item.owner).toBe('client@example.com');
    expect(item.source).toBe('email:sent');
    expect(item.status).toBe('waiting');
    expect(item.url).toBe('mid:msg-002');
    expect(item.dedupeKeys).toEqual(['email:msg-002']);
    expect(item.createdAt).toBe('2024-01-10T09:00:00Z');
    expect(item.updatedAt).toBe('2024-01-11T14:00:00Z');
    expect(item.participants).toEqual(['me@example.com', 'client@example.com']);
  });

  // 3. Missing subject line — emits structured security event
  it('handles a message with missing subject line', () => {
    const logs = captureSecurityLogs(() => {
      const item = normalizeEmail(
        makeEmailMessage({ subject: undefined }),
        'awaiting-reply',
      );

      expect(item.title).toBe('No subject');
      expect(item.confidence).toBeLessThan(1.0);
      expect(item.sourceType).toBe('email');
      expect(item.dedupeKeys).toEqual(['email:msg-001']);
    });

    // SEC-OPS-001: verify structured security event for missing subject
    expect(logs.length).toBeGreaterThan(0);
    for (const event of logs) {
      assertStructuredEvent(event);
    }
  });
});
