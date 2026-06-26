import { DatabaseSync } from "node:sqlite";
import { toLines, unique } from "../utils/text.js";

function buildWindow(date) {
  const start = `${date} 00:00:00`;
  const endDate = new Date(`${date}T00:00:00Z`);
  endDate.setUTCDate(endDate.getUTCDate() + 1);
  const end = `${endDate.toISOString().slice(0, 10)} 00:00:00`;
  return { start, end };
}

function placeholders(count) {
  return Array.from({ length: count }, () => "?").join(", ");
}

function pickSummaryConversationIds(database, { start, end, sessionKey, conversationLimit }) {
  const query = `
    SELECT
      s.conversation_id,
      MAX(COALESCE(s.latest_at, s.created_at)) AS last_summary_at
    FROM summaries s
    JOIN conversations c ON c.conversation_id = s.conversation_id
    WHERE COALESCE(s.latest_at, s.created_at) >= ?
      AND COALESCE(s.earliest_at, s.created_at) < ?
      AND (${sessionKey ? "c.session_key = ? AND" : ""} 1 = 1)
    GROUP BY s.conversation_id
    ORDER BY last_summary_at DESC
    LIMIT ?
  `;

  const statement = database.prepare(query);
  const rows = sessionKey
    ? statement.all(start, end, sessionKey, conversationLimit)
    : statement.all(start, end, conversationLimit);

  return rows.map((row) => Number(row.conversation_id));
}

function pickRecentMessageConversationIds(database, { start, end, sessionKey, includeTools, conversationLimit }) {
  const query = `
    SELECT
      c.conversation_id,
      MAX(m.created_at) AS last_message_at,
      COUNT(*) AS message_count
    FROM messages m
    JOIN conversations c ON c.conversation_id = m.conversation_id
    WHERE m.created_at >= ?
      AND m.created_at < ?
      AND (${sessionKey ? "c.session_key = ? AND" : ""} 1 = 1)
      AND (${includeTools ? "1 = 1" : "m.role != 'tool'"})
    GROUP BY c.conversation_id
    ORDER BY last_message_at DESC
    LIMIT ?
  `;

  const statement = database.prepare(query);
  const rows = sessionKey
    ? statement.all(start, end, sessionKey, conversationLimit)
    : statement.all(start, end, conversationLimit);

  return rows.map((row) => Number(row.conversation_id));
}

function readRecentMessages(database, { start, end, includeTools, conversationIds, messageTail }) {
  if (conversationIds.length === 0) {
    return [];
  }

  const query = `
    SELECT
      m.conversation_id,
      m.message_id,
      m.role,
      m.content,
      m.created_at
    FROM messages m
    WHERE m.created_at >= ?
      AND m.created_at < ?
      AND m.conversation_id IN (${placeholders(conversationIds.length)})
      AND (${includeTools ? "1 = 1" : "m.role != 'tool'"})
    ORDER BY m.created_at DESC, m.message_id DESC
  `;

  const rows = database.prepare(query).all(start, end, ...conversationIds);
  const perConversation = new Map();

  for (const row of rows) {
    const list = perConversation.get(row.conversation_id) ?? [];
    if (list.length < messageTail) {
      list.push(row);
      perConversation.set(row.conversation_id, list);
    }
  }

  return [...perConversation.values()]
    .flatMap((items) => items.reverse())
    .map((row) => String(row.content ?? ""));
}

function readRelevantSummaries(database, { start, end, conversationIds, summaryLimit, includeSummaries }) {
  if (!includeSummaries || conversationIds.length === 0) {
    return [];
  }

  const query = `
    SELECT
      s.conversation_id,
      s.summary_id,
      s.depth,
      s.kind,
      s.content,
      COALESCE(s.latest_at, s.created_at) AS sort_time
    FROM summaries s
    WHERE s.conversation_id IN (${placeholders(conversationIds.length)})
      AND COALESCE(s.latest_at, s.created_at) >= ?
      AND COALESCE(s.earliest_at, s.created_at) < ?
    ORDER BY sort_time DESC, s.depth ASC
  `;

  const rows = database.prepare(query).all(...conversationIds, start, end);
  const perConversation = new Map();

  for (const row of rows) {
    const list = perConversation.get(row.conversation_id) ?? [];
    if (list.length < summaryLimit) {
      list.push(row);
      perConversation.set(row.conversation_id, list);
    }
  }

  return [...perConversation.values()]
    .flatMap((items) => items)
    .map((row) => String(row.content ?? ""));
}

export async function readLcmDayContext({
  date,
  dbPath,
  sessionKey = null,
  includeTools = false,
  limit = 500,
  conversationLimit = 3,
  rawConversationLimit = 1,
  messageTail = 30,
  summaryLimit = 2,
  includeSummaries = true,
} = {}) {
  if (!date) {
    throw new Error("LCM day context requires a date.");
  }

  if (!dbPath) {
    throw new Error("LCM day context requires a dbPath.");
  }

  const { start, end } = buildWindow(date);
  const database = new DatabaseSync(dbPath, { open: true, readOnly: true });

  try {
    const summaryConversationIds = pickSummaryConversationIds(database, {
      start,
      end,
      sessionKey,
      conversationLimit,
    });

    const recentMessageConversationIds = pickRecentMessageConversationIds(database, {
      start,
      end,
      sessionKey,
      includeTools,
      conversationLimit: rawConversationLimit,
    });

    const conversationIds = unique([...summaryConversationIds, ...recentMessageConversationIds]);

    const summaryTexts = readRelevantSummaries(database, {
      start,
      end,
      conversationIds,
      summaryLimit,
      includeSummaries,
    });

    const messageTexts = readRecentMessages(database, {
      start,
      end,
      includeTools,
      conversationIds,
      messageTail,
    });

    const lines = unique(
      [...summaryTexts, ...messageTexts]
        .flatMap((text) => toLines(text))
        .filter(Boolean),
    ).slice(0, limit);

    return {
      source: "lcm",
      dbPath,
      sessionKey,
      conversationIds,
      count: lines.length,
      content: lines.join("\n"),
      lines,
    };
  } finally {
    database.close();
  }
}
