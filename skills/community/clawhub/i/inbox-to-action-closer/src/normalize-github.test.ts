import { describe, it, expect, vi, afterEach } from 'vitest';
import { normalizeGithub } from './normalize-github.js';
import { normalizeSlack } from './normalize-slack.js';
import type { ActionItem } from './types.js';

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

// ---- Test fixtures ----

function makeGithubIssue(overrides: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    type: 'issue',
    number: 42,
    title: 'Fix login timeout',
    body: 'Users report 30s timeouts on /login',
    state: 'open',
    html_url: 'https://github.com/acme/app/issues/42',
    created_at: '2024-01-15T10:00:00Z',
    updated_at: '2024-01-16T12:00:00Z',
    user: { login: 'alice' },
    assignee: { login: 'bob' },
    milestone: { due_on: '2024-02-01T00:00:00Z' },
    repository: { full_name: 'acme/app' },
    ...overrides,
  };
}

function makeGithubPR(overrides: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    number: 101,
    title: 'Add retry logic',
    body: 'Implements exponential backoff',
    state: 'open',
    html_url: 'https://github.com/acme/app/pull/101',
    created_at: '2024-01-15T10:00:00Z',
    updated_at: '2024-01-16T12:00:00Z',
    user: { login: 'charlie' },
    pull_request: { url: 'https://api.github.com/repos/acme/app/pulls/101' },
    requested_reviewers: [{ login: 'dave' }],
    repository: { full_name: 'acme/app' },
    ...overrides,
  };
}

function makeGithubReview(overrides: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    type: 'review_requested',
    number: 101,
    title: 'Add retry logic',
    body: 'Please review',
    html_url: 'https://github.com/acme/app/pull/101',
    created_at: '2024-01-15T10:00:00Z',
    updated_at: '2024-01-16T12:00:00Z',
    user: { login: 'charlie' },
    requested_reviewer: { login: 'eve' },
    repository: { full_name: 'acme/app' },
    ...overrides,
  };
}

// ---- Tests ----

describe('normalizeGithub', () => {
  // ---- 1. valid GitHub issue ----
  it('maps a complete GitHub issue to a valid ActionItem', () => {
    const spy = vi.spyOn(console, 'warn').mockImplementation(() => {});
    const result = normalizeGithub([makeGithubIssue()]);
    spy.mockRestore();

    expect(result).toHaveLength(1);
    const item = result[0];
    expect(item.id).toBe('github:acme/app#42');
    expect(item.sourceType).toBe('github');
    expect(item.source).toBe('github:acme/app');
    expect(item.title).toBe('Fix login timeout');
    expect(item.summary).toBe('Users report 30s timeouts on /login');
    expect(item.owner).toBe('bob');
    expect(item.participants).toContain('bob');
    expect(item.participants).toContain('alice');
    expect(item.url).toBe('https://github.com/acme/app/issues/42');
    expect(item.status).toBe('open');
    expect(item.dueAt).toBe('2024-02-01T00:00:00Z');
    expect(item.confidence).toBe(1.0);
    expect(item.dedupeKeys).toContain(item.url);
    expect(item.dedupeKeys).toContain('fix login timeout');
  });

  // ---- 2. valid GitHub PR ----
  it('maps a complete GitHub PR to a valid ActionItem', () => {
    const spy = vi.spyOn(console, 'warn').mockImplementation(() => {});
    const result = normalizeGithub([makeGithubPR()]);
    spy.mockRestore();

    expect(result).toHaveLength(1);
    const item = result[0];
    expect(item.id).toBe('github:acme/app#101');
    expect(item.sourceType).toBe('github');
    expect(item.owner).toBe('charlie');
    expect(item.participants).toContain('charlie');
    expect(item.participants).toContain('dave');
    expect(item.status).toBe('open');
    expect(item.confidence).toBe(1.0);
    expect(item.dedupeKeys).toContain('https://github.com/acme/app/pull/101');
  });

  // ---- 3. valid GitHub review request ----
  it('maps a review request with requested_reviewer as owner', () => {
    const spy = vi.spyOn(console, 'warn').mockImplementation(() => {});
    const result = normalizeGithub([makeGithubReview()]);
    spy.mockRestore();

    expect(result).toHaveLength(1);
    const item = result[0];
    expect(item.id).toBe('github:acme/app#101');
    expect(item.owner).toBe('eve');
    expect(item.participants).toContain('eve');
    expect(item.participants).toContain('charlie');
    expect(item.status).toBe('open');
    expect(item.confidence).toBe(1.0);
  });

  // ---- 4a. GitHub missing assignee fallback ----
  it('degrades confidence when issue has no assignee', () => {
    const spy = vi.spyOn(console, 'warn').mockImplementation(() => {});
    const result = normalizeGithub([makeGithubIssue({ assignee: null })]);
    spy.mockRestore();

    expect(result).toHaveLength(1);
    expect(result[0].owner).toBe('unassigned');
    expect(result[0].confidence).toBeLessThan(1.0);
    expect(result[0].confidence).toBeGreaterThanOrEqual(0.7);
  });

  // ---- 4b. GitHub missing user fallback on PR ----
  it('degrades confidence when PR has no user', () => {
    const spy = vi.spyOn(console, 'warn').mockImplementation(() => {});
    const result = normalizeGithub([makeGithubPR({ user: null })]);
    spy.mockRestore();

    expect(result).toHaveLength(1);
    expect(result[0].owner).toBe('unknown');
    expect(result[0].confidence).toBeLessThan(1.0);
    expect(result[0].confidence).toBeGreaterThanOrEqual(0.7);
  });

  // ---- 5. GitHub empty/malformed input ----
  it('returns empty array for non-array and malformed inputs without throwing', () => {
    const logs = captureSecurityLogs(() => {
      expect(normalizeGithub(null)).toEqual([]);
      expect(normalizeGithub(undefined)).toEqual([]);
      expect(normalizeGithub('string')).toEqual([]);
      expect(normalizeGithub(42)).toEqual([]);
      expect(normalizeGithub({})).toEqual([]);
      expect(normalizeGithub([])).toEqual([]);
      expect(normalizeGithub([null, 123, 'str'])).toEqual([]);
    });

    // Verify structured security events were logged for invalid inputs
    expect(logs.length).toBeGreaterThan(0);
    for (const event of logs) {
      assertStructuredEvent(event);
    }
  });

  // ---- 6. consistent ID format across both adapters ----
  it('produces deterministic IDs with correct prefix for both adapters', () => {
    const spy = vi.spyOn(console, 'warn').mockImplementation(() => {});

    const ghResult = normalizeGithub([
      makeGithubIssue({ number: 1 }),
      makeGithubPR({ number: 2 }),
    ]);
    expect(ghResult[0].id).toBe('github:acme/app#1');
    expect(ghResult[1].id).toBe('github:acme/app#2');
    for (const item of ghResult) {
      expect(item.id).toMatch(/^github:[^#]+#\d+$/);
    }

    spy.mockRestore();

    const slackResult = normalizeSlack([
      { ts: '1700000000.000100', channel: 'C01', text: 'hi', user: 'U1' },
    ]);
    expect(slackResult[0].id).toMatch(/^slack:/);
  });

  // ---- 7. null timestamp handling across both adapters ----
  it('handles missing timestamps gracefully in both adapters', () => {
    const spy = vi.spyOn(console, 'warn').mockImplementation(() => {});

    const ghResult = normalizeGithub([makeGithubIssue({
      created_at: undefined,
      updated_at: undefined,
    })]);
    expect(ghResult).toHaveLength(1);
    expect(ghResult[0].createdAt).toBe(new Date(0).toISOString());
    expect(ghResult[0].updatedAt).toBe(new Date(0).toISOString());

    spy.mockRestore();

    const slackResult = normalizeSlack([{
      ts: 'not-a-number',
      channel: 'C01',
      text: 'test',
      user: 'U1',
    }]);
    expect(slackResult).toHaveLength(1);
    expect(slackResult[0].createdAt).toBe(new Date(0).toISOString());
  });

  // ---- 8. structured security logging on malformed input ----
  it('emits structured security events with required fields on invalid input', () => {
    const logs = captureSecurityLogs(() => {
      normalizeGithub('not-an-array');
    });

    expect(logs).toHaveLength(1);
    const event = logs[0] as Record<string, unknown>;
    expect(event.event_type).toBe('input_validation');
    expect(event.actor).toBe('normalizeGithub');
    expect(event.outcome).toBe('rejected');
    expect(typeof event.timestamp).toBe('string');
  });
});
