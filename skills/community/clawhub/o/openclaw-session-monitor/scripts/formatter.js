// formatter.js — Merge consecutive same-sender messages, build HTML output

/**
 * Merge consecutive same-sender entries into blocks.
 * Returns array of "ICON text\ntext..." strings.
 */
function mergeMessages(entries) {
  if (!entries.length) return [];
  const blocks = [];
  let cur = { sender: entries[0].sender, lines: [entries[0].text] };
  for (let i = 1; i < entries.length; i++) {
    if (entries[i].sender === cur.sender) {
      cur.lines.push(entries[i].text);
    } else {
      blocks.push(cur);
      cur = { sender: entries[i].sender, lines: [entries[i].text] };
    }
  }
  blocks.push(cur);
  return blocks.map(b => `${b.sender} │ ${b.lines.join('\n  │ ')}`);
}

/**
 * Sort priority: other(0) → 👶 subagent(1) → external groups(2) → external direct(3)
 */
function tagOrder(tag) {
  if (/↔/.test(tag)) return 3;         // direct chats (Agent↔Alice)
  if (/👶/.test(tag)) return 1;           // subagents
  if (/^main/.test(tag)) return 0;        // main, heartbeat
  return 2;                                 // everything else (groups, etc.)
}

/**
 * Build the final Telegram HTML message from grouped session entries.
 * @param {Map<string, Array<{sender,text,model?}>>} groups  tag → entries (full accumulated)
 * @returns {string} HTML text
 */
function buildMessage(groups) {
  // sort by priority
  const sorted = [...groups.entries()].sort((a, b) => tagOrder(a[0]) - tagOrder(b[0]));

  const parts = [];
  for (const [tag, entries] of sorted) {
    // find last model used in this session
    let model = null;
    for (let i = entries.length - 1; i >= 0; i--) {
      if (entries[i].model) { model = entries[i].model; break; }
    }
    const merged = mergeMessages(entries);
    const body = merged.join('\n');
    const header = model ? `<b>${tag}</b> <i>${model}</i>` : `<b>${tag}</b>`;
    parts.push(`<blockquote expandable>${header}\n${body}</blockquote>`);
  }
  let msg = parts.join('\n');
  if (msg.length > 4000) msg = msg.slice(0, 3950) + '\n…';
  return msg;
}

module.exports = { mergeMessages, buildMessage };
