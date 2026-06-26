import type { ActionItem, Status } from './types.js';

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

function isRecord(v: unknown): v is Record<string, unknown> {
  return typeof v === 'object' && v !== null && !Array.isArray(v);
}

function str(obj: Record<string, unknown>, key: string): string | undefined {
  const v = obj[key];
  return typeof v === 'string' ? v : undefined;
}

function num(obj: Record<string, unknown>, key: string): number | undefined {
  const v = obj[key];
  return typeof v === 'number' ? v : undefined;
}

function rec(obj: Record<string, unknown>, key: string): Record<string, unknown> | undefined {
  const v = obj[key];
  return isRecord(v) ? v : undefined;
}

function extractRepo(item: Record<string, unknown>): string {
  const repo = rec(item, 'repository');
  if (repo) {
    const fullName = str(repo, 'full_name');
    if (fullName) return fullName;
  }
  const url = str(item, 'html_url');
  if (url) {
    const match = url.match(/github\.com\/([^/]+\/[^/]+)/);
    if (match) return match[1];
  }
  return 'unknown/unknown';
}

function extractDueAt(item: Record<string, unknown>): string | null {
  const milestone = rec(item, 'milestone');
  if (milestone) {
    const dueOn = str(milestone, 'due_on');
    if (dueOn) return dueOn;
  }
  return null;
}

function buildDedupeKeys(htmlUrl: string, title: string): string[] {
  const keys: string[] = [];
  if (htmlUrl) keys.push(htmlUrl);
  const norm = title.toLowerCase().trim();
  if (norm) keys.push(norm);
  return keys;
}

function addParticipant(list: string[], login: string | undefined): void {
  if (login && login !== 'unknown' && login !== 'unassigned' && !list.includes(login)) {
    list.push(login);
  }
}

type ItemMapper = (item: Record<string, unknown>) => ActionItem | null;

function mapIssue(item: Record<string, unknown>): ActionItem | null {
  const itemNum = num(item, 'number');
  if (!itemNum) return null;

  const repo = extractRepo(item);
  const assignee = rec(item, 'assignee');
  const owner = assignee ? (str(assignee, 'login') ?? 'unassigned') : 'unassigned';
  const state = str(item, 'state');
  const status: Status = state === 'closed' ? 'done' : 'open';
  const htmlUrl = str(item, 'html_url') ?? '';
  const title = str(item, 'title') ?? '';
  const body = str(item, 'body') ?? '';
  const createdAt = str(item, 'created_at') ?? new Date(0).toISOString();
  const updatedAt = str(item, 'updated_at') ?? createdAt;

  let confidence = 1.0;
  if (!assignee) confidence -= 0.1;
  if (!str(item, 'body')) confidence -= 0.1;
  confidence = Math.max(0.7, Math.round(confidence * 10) / 10);

  const participants: string[] = [];
  addParticipant(participants, owner);
  const creator = rec(item, 'user');
  if (creator) addParticipant(participants, str(creator, 'login'));

  return {
    id: `github:${repo}#${itemNum}`,
    source: `github:${repo}`,
    sourceType: 'github',
    title: title || `GitHub issue #${itemNum}`,
    summary: body,
    owner,
    participants,
    createdAt,
    updatedAt,
    dueAt: extractDueAt(item),
    url: htmlUrl,
    status,
    priorityScore: 0,
    blocker: null,
    replyDraft: null,
    followUpQuestion: null,
    suggestedNextAction: null,
    dedupeKeys: buildDedupeKeys(htmlUrl, title),
    confidence,
  };
}

function mapPR(item: Record<string, unknown>): ActionItem | null {
  const itemNum = num(item, 'number');
  if (!itemNum) return null;

  const repo = extractRepo(item);
  const user = rec(item, 'user');
  const owner = user ? (str(user, 'login') ?? 'unknown') : 'unknown';
  const state = str(item, 'state');
  const merged = item.merged === true;
  const status: Status = merged || state === 'closed' ? 'done' : 'open';
  const htmlUrl = str(item, 'html_url') ?? '';
  const title = str(item, 'title') ?? '';
  const body = str(item, 'body') ?? '';
  const createdAt = str(item, 'created_at') ?? new Date(0).toISOString();
  const updatedAt = str(item, 'updated_at') ?? createdAt;

  let confidence = 1.0;
  if (!user) confidence -= 0.2;
  if (!str(item, 'title')) confidence -= 0.1;
  confidence = Math.max(0.7, Math.round(confidence * 10) / 10);

  const participants: string[] = [];
  addParticipant(participants, owner);
  if (Array.isArray(item.requested_reviewers)) {
    for (const r of item.requested_reviewers) {
      if (isRecord(r)) addParticipant(participants, str(r, 'login'));
    }
  }

  return {
    id: `github:${repo}#${itemNum}`,
    source: `github:${repo}`,
    sourceType: 'github',
    title: title || `GitHub PR #${itemNum}`,
    summary: body,
    owner,
    participants,
    createdAt,
    updatedAt,
    dueAt: extractDueAt(item),
    url: htmlUrl,
    status,
    priorityScore: 0,
    blocker: null,
    replyDraft: null,
    followUpQuestion: null,
    suggestedNextAction: null,
    dedupeKeys: buildDedupeKeys(htmlUrl, title),
    confidence,
  };
}

function mapReview(item: Record<string, unknown>): ActionItem | null {
  const itemNum = num(item, 'number');
  if (!itemNum) return null;

  const repo = extractRepo(item);
  const reviewer = rec(item, 'requested_reviewer');
  const owner = reviewer ? (str(reviewer, 'login') ?? 'unknown') : 'unknown';
  const htmlUrl = str(item, 'html_url') ?? '';
  const title = str(item, 'title') ?? '';
  const body = str(item, 'body') ?? '';
  const createdAt = str(item, 'created_at') ?? new Date(0).toISOString();
  const updatedAt = str(item, 'updated_at') ?? createdAt;

  let confidence = 1.0;
  if (!reviewer) confidence -= 0.2;
  if (!str(item, 'title')) confidence -= 0.1;
  confidence = Math.max(0.7, Math.round(confidence * 10) / 10);

  const participants: string[] = [];
  addParticipant(participants, owner);
  const prAuthor = rec(item, 'user');
  if (prAuthor) addParticipant(participants, str(prAuthor, 'login'));

  return {
    id: `github:${repo}#${itemNum}`,
    source: `github:${repo}`,
    sourceType: 'github',
    title: title || `GitHub review #${itemNum}`,
    summary: body,
    owner,
    participants,
    createdAt,
    updatedAt,
    dueAt: extractDueAt(item),
    url: htmlUrl,
    status: 'open',
    priorityScore: 0,
    blocker: null,
    replyDraft: null,
    followUpQuestion: null,
    suggestedNextAction: null,
    dedupeKeys: buildDedupeKeys(htmlUrl, title),
    confidence,
  };
}

const dispatchMap: Record<string, ItemMapper> = {
  issue: mapIssue,
  pull_request: mapPR,
  review_requested: mapReview,
};

function inferType(item: Record<string, unknown>): string {
  const explicit = str(item, 'type');
  if (explicit && explicit in dispatchMap) return explicit;
  if (item.pull_request !== undefined || str(item, 'merge_commit_sha') !== undefined) {
    return 'pull_request';
  }
  if (rec(item, 'requested_reviewer')) return 'review_requested';
  return 'issue';
}

export function normalizeGithub(raw: unknown): ActionItem[] {
  if (!Array.isArray(raw)) {
    if (raw !== undefined && raw !== null) {
      logSecurityEvent({
        event_type: 'input_validation',
        actor: 'normalizeGithub',
        outcome: 'rejected',
        detail: `Expected array, received ${typeof raw}`,
        timestamp: new Date().toISOString(),
      });
    }
    return [];
  }

  const items: ActionItem[] = [];

  for (const entry of raw) {
    if (!isRecord(entry)) {
      logSecurityEvent({
        event_type: 'input_validation',
        actor: 'normalizeGithub',
        outcome: 'skipped',
        detail: 'Non-object entry in input array',
        timestamp: new Date().toISOString(),
      });
      continue;
    }

    const itemType = inferType(entry);
    const mapper = dispatchMap[itemType];
    if (!mapper) {
      logSecurityEvent({
        event_type: 'input_validation',
        actor: 'normalizeGithub',
        outcome: 'skipped',
        detail: `Unsupported item type: ${String(itemType)}`,
        timestamp: new Date().toISOString(),
      });
      continue;
    }

    const result = mapper(entry);
    if (result) {
      items.push(result);
    } else {
      logSecurityEvent({
        event_type: 'input_validation',
        actor: 'normalizeGithub',
        outcome: 'degraded',
        detail: `Failed to map ${itemType} entry — missing required fields`,
        timestamp: new Date().toISOString(),
      });
    }
  }

  return items;
}
