import type { ActionItem } from './types.js';

export function normalizeSlack(raw: unknown): ActionItem[] {
  if (!Array.isArray(raw)) {
    if (raw !== undefined && raw !== null) {
      console.warn('normalizeSlack: expected array, got ' + typeof raw);
    }
    return [];
  }

  const items: ActionItem[] = [];

  for (const entry of raw) {
    if (typeof entry !== 'object' || entry === null) {
      console.warn('normalizeSlack: skipping non-object entry');
      continue;
    }

    const msg = entry as Record<string, unknown>;

    if (typeof msg.ts !== 'string' || typeof msg.channel !== 'string') {
      console.warn('normalizeSlack: skipping entry missing ts or channel');
      continue;
    }

    const ts = msg.ts;
    const channel = msg.channel as string;
    const text = typeof msg.text === 'string' ? msg.text : '';
    const user = typeof msg.user === 'string' ? msg.user : '';
    const threadTs = typeof msg.thread_ts === 'string' ? msg.thread_ts : null;
    const isReply = threadTs !== null && threadTs !== ts;

    const id = `slack:${channel}-${ts}`;

    let url: string;
    if (typeof msg.permalink === 'string' && msg.permalink) {
      url = msg.permalink;
    } else if (isReply) {
      url = `https://slack.com/archives/${channel}/p${threadTs!.replace('.', '')}`;
    } else {
      url = `https://slack.com/archives/${channel}/p${ts.replace('.', '')}`;
    }

    const title = text || `Message in ${channel}`;
    const summary = text;
    const owner = user || 'unknown';

    const participants: string[] = [];
    if (user) participants.push(user);
    if (Array.isArray(msg.reply_users)) {
      for (const u of msg.reply_users) {
        if (typeof u === 'string' && !participants.includes(u)) {
          participants.push(u);
        }
      }
    }

    const tsFloat = parseFloat(ts);
    const createdAt = isFinite(tsFloat)
      ? new Date(tsFloat * 1000).toISOString()
      : new Date(0).toISOString();

    let updatedAt = createdAt;
    if (typeof msg.latest_reply === 'string') {
      const latestFloat = parseFloat(msg.latest_reply as string);
      if (isFinite(latestFloat)) {
        updatedAt = new Date(latestFloat * 1000).toISOString();
      }
    }

    let confidence = 1.0;
    if (!user) confidence -= 0.2;
    if (!text) confidence -= 0.1;
    confidence = Math.max(0.7, Math.round(confidence * 10) / 10);

    const dedupeKeys: string[] = [url];
    const normalizedTitle = title.toLowerCase().trim();
    if (normalizedTitle) {
      dedupeKeys.push(normalizedTitle);
    }

    items.push({
      id,
      source: `slack:${channel}`,
      sourceType: 'slack',
      title,
      summary,
      owner,
      participants,
      createdAt,
      updatedAt,
      dueAt: null,
      url,
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
