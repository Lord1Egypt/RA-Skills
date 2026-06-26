const REPLY_PATTERNS = {
  cancel: [
    /\b(stop|cancel|leave me alone|shut up|dont remind|don't remind|no more reminders)\b/i,
    /(取消|别提醒了|不用提醒|别再提醒|不要再提醒|停掉|停了|闭嘴|别催了)/
  ],
  confirm: [
    /\b(done|did it|handled|finished|completed|got it done|wrapped up|taken care of|took care of)\b/i,
    /(好了|完成了|做完了|搞定了|处理好了|已经处理|已完成|弄完了)/
  ],
  snooze: [
    /\b(snooze|snooze\s+\d+|later\s+\d+|remind me in|give me \d+|push it|delay|postpone|snooze for|稍后\s*\d*|等\s*\d+|推迟|延后)\b/i,
    /\b(\d+\s*(?:min|minute|minutes|hour|hours|hr|hrs|m|h)\s*(?:later|from now)?)/i
  ],
  followup: [
    /\b(later|give me a minute|give me a sec|i saw it|saw it|in a bit|working on it|on it|will do|got it|okay|ok|kk)\b/i,
    /(等会儿|等会|稍后|一会儿|待会|等下|待一下|我知道了|知道了|看到了|收到|在弄|马上|回头弄|晚点)/
  ]
};

function parseSnoozeDuration(text) {
  const m = text.match(/(\d+)\s*(min|minute|minutes|m|hour|hours|hr|hrs|h)/i);
  if (!m) return 15 * 60; // default 15 minutes
  const n = parseInt(m[1], 10);
  const unit = m[2].toLowerCase();
  if (unit.startsWith('h')) return n * 3600;
  return n * 60;
}

export function classifyReplyIntent(replyText) {
  const text = String(replyText || "").trim();
  if (!text) return "ignore";
  for (const pattern of REPLY_PATTERNS.cancel) {
    if (pattern.test(text)) return "cancel";
  }
  for (const pattern of REPLY_PATTERNS.confirm) {
    if (pattern.test(text)) return "confirm";
  }
  for (const pattern of REPLY_PATTERNS.snooze) {
    if (pattern.test(text)) return "snooze";
  }
  for (const pattern of REPLY_PATTERNS.followup) {
    if (pattern.test(text)) return "followup";
  }
  return "ignore";
}

export { parseSnoozeDuration };

export function buildReplyClassifierPrompt(candidates, replyText) {
  return [
    "Classify a user's chat reply against pending reminders.",
    "Return JSON only. No markdown.",
    'Schema: {"match_id":"id-or-none","action":"confirm|cancel|snooze|followup|ignore","reason":"short"}',
    "- confirm: the user clearly says the reminder or task is completed",
    "- cancel: the user wants these reminders to stop",
    "- snooze: the user wants to delay/postpone the reminder (e.g. 'snooze 15m', 'give me 30 min', 'later 1h')",
    "- followup: the user is replying to the reminder but not marking it done or snoozing",
    '- ignore: unrelated message or no clear match. Use match_id="none".',
    '',
    `Pending reminders: ${JSON.stringify(candidates, null, 2)}`,
    '',
    `User reply: ${replyText}`
  ].join("\n");
}
