// parser.js — Parse JSONL entries into display-ready objects

// ── Utilities ──

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

/** Truncate to n chars, append ... if truncated */
function trunc(s, n) {
  s = String(s);
  return s.length > n ? s.slice(0, n) + '...' : s;
}

/** Truncate filename: first 4 + ... + last 23 if over 30 chars */
function truncPath(p) {
  const name = p.split('/').pop() || p;
  if (name.length <= 30) return name;
  return name.slice(0, 4) + '...' + name.slice(-23);
}

/** Strip metadata noise from user messages */
function stripMeta(t) {
  return t
    .replace(/Conversation info \(untrusted[^]*?\n```\n/g, '')
    .replace(/Sender \(untrusted[^]*?\n```\n/g, '')
    .replace(/Replied message \(untrusted[^]*?\n```\n/g, '')
    .replace(/```json\n[^]*?\n```/g, '')
    .replace(/\[Queued messages while agent was busy\]/g, '')
    .replace(/---\s*Queued #\d+/g, '')
    .replace(/System: \[.*?\].*?\n?/g, '')
    .replace(/<<<BEGIN_OPENCLAW_INTERNAL_CONTEXT>>>/g, '')
    .replace(/<<<END_OPENCLAW_INTERNAL_CONTEXT>>>/g, '')
    .replace(/<<<EXTERNAL_UNTRUSTED_CONTENT[^>]*>>>/g, '')
    .replace(/<<<END_EXTERNAL_UNTRUSTED_CONTENT[^>]*>>>/g, '')
    .replace(/\[Inter-session message\][^\n]*/g, '')
    .replace(/\[(Mon|Tue|Wed|Thu|Fri|Sat|Sun) \d{4}-\d{2}-\d{2} \d{2}:\d{2} GMT[+-]\d+\]\s*/g, '')
    .replace(/\n/g, ' ').replace(/\s+/g, ' ').trim();
}

/** Get file path arg from tool arguments */
function getFilePath(args) {
  return args.path || args.file || args.filePath || args.file_path || '';
}

/** Extract model name, strip provider prefix */
function shortModel(m) {
  if (!m) return null;
  m = m.replace(/^.*\//, '');  // strip provider prefix (e.g. github-copilot/)
  if (/delivery-mirror/i.test(m)) return null; // internal, skip
  return m;
}

const MAX = 300;

// ── Tool Call Formatting (assistant → tool) ──
// Format: <b>name</b> <b>target</b> <i>args</i>

function summarizeTool(c) {
  const args = c.arguments || {};

  if (c.name === 'exec') {
    const cmd = (args.command || '').replace(/\n/g, ' ').trim();
    if (!cmd) return '<b>exec</b>';
    const parts = cmd.split(/\s+/);
    const prog = parts[0];
    const rest = trunc(parts.slice(1).join(' '), 50);
    return rest
      ? `<b>exec</b> <b>${esc(prog)}</b> <i>${esc(rest)}</i>`
      : `<b>exec</b> <b>${esc(prog)}</b>`;
  }

  if (c.name === 'read' || c.name === 'write' || c.name === 'edit') {
    const p = getFilePath(args);
    return p
      ? `<b>${c.name}</b> <b>${esc(truncPath(p))}</b>`
      : `<b>${c.name}</b>`;
  }

  if (c.name === 'sessions_spawn') {
    const task = trunc((args.task || '').replace(/\n/g, ' ').trim(), 40);
    return task ? `<b>spawn</b>🚀 <i>${esc(task)}</i>` : '<b>spawn</b>🚀';
  }

  if (c.name === 'web_search') {
    return `<b>search</b> <i>${esc(trunc(args.query || '', 40))}</i>`;
  }

  if (c.name === 'web_fetch') {
    return `<b>fetch</b> <b>${esc(trunc(args.url || '', 40))}</b>`;
  }

  if (c.name === 'process') {
    const a = args.action || '';
    const sid = args.sessionId || '';
    return sid
      ? `<b>poll</b> <i>${a}:${esc(sid.slice(0, 10))}</i>`
      : `<b>poll</b> <i>${a}</i>`;
  }

  return `<b>${esc(c.name)}</b>`;
}

// ── Tool Result Formatting (tool → assistant) ──
// Format: ◀ 「content」

function summarizeResult(msg) {
  const name = msg.toolName || '';
  const details = msg.details || {};
  const content = Array.isArray(msg.content) ? msg.content : [];
  const raw = content
    .filter(c => c.type === 'text' && c.text)
    .map(c => c.text).join(' ').trim()
    .replace(/\n/g, ' ').replace(/\s+/g, ' ');

  if (name === 'exec') {
    if (/Command still running/.test(raw)) return '「⏳」';
    const code = details.exitCode;
    if (!raw || raw === '(no output)') return `「${code === 0 ? '✅' : '✗ exit=' + code}」`;
    return `「${esc(trunc(raw, 80))}」`;
  }

  if (name === 'process') {
    if (/Command still running/.test(raw) || /no new output/.test(raw)) return '「⏳」';
    if (/Process exited/.test(raw)) {
      const m = raw.match(/code (\d+)/);
      return `「exit=${m ? m[1] : '?'}」`;
    }
    if (!raw) return '「✅」';
    return `「${esc(trunc(raw, 80))}」`;
  }

  if (name === 'read' || name === 'write' || name === 'edit') {
    const m = raw.match(/Successfully (wrote|replaced).*?([\w./-]+\.\w+)/);
    if (m) return `「✅ ${esc(truncPath(m[2]))}」`;
    if (!raw) return '「✅」';
    return `「${esc(trunc(raw, raw.length > 100 ? 60 : 80))}」`;
  }

  if (name === 'sessions_spawn') {
    const m = raw.match(/"mode":\s*"(\w+)"/);
    return `「${m ? m[1] : '✅'}」`;
  }

  if (!raw) return '「✅」';
  return `「${esc(trunc(raw, 80))}」`;
}

// ── User Message Patterns ──
// Principle: strip known boilerplate, show 「tag …」+ remaining useful content
// ORDER MATTERS: inbound_meta/Conversation info must be first (most common wrapper)
const USER_PATTERNS = [
  {
    // Real user input — strip metadata envelope, show clean text
    test: t => t.includes('openclaw.inbound_meta') || t.includes('Conversation info (untrusted'),
    render: t => {
      const clean = stripMeta(t);
      return clean ? { sender: '👤', text: esc(trunc(clean, MAX)) } : null;
    },
  },
  {
    test: t => t.includes('Read HEARTBEAT.md'),
    render: t => {
      const clean = t
        .replace(/Read HEARTBEAT\.md[^]*?(?:HEARTBEAT_OK|reply HEARTBEAT_OK)[.\s]*/i, '')
        .replace(/When reading HEARTBEAT\.md[^]*/i, '')
        .replace(/\n/g, ' ').replace(/\s+/g, ' ').trim();
      return { sender: '⚡', text: clean ? '「heartbeat …」' + esc(trunc(clean, 80)) : '「heartbeat …」' };
    },
  },
  {
    test: t => t.includes('Post-compaction context refresh') || t.includes('Session was just compacted'),
    render: t => {
      const clean = t
        .replace(/\[Post-compaction context refresh\]/g, '')
        .replace(/Session was just compacted\.[^]*?startup sequence[^.]*\./i, '')
        .replace(/Critical rules from AGENTS\.md:[^]*/i, '')
        .replace(/Execute your Session Startup[^]*/i, '')
        .replace(/Current time:[^\n]*/i, '')
        .replace(/\n/g, ' ').replace(/\s+/g, ' ').trim();
      return { sender: '⚡', text: clean ? '「compacted …」' + esc(trunc(clean, 80)) : '「compacted …」' };
    },
  },
  {
    test: t => t.includes('[Subagent Context]') || t.includes('You are running as a subagent'),
    render: t => {
      const clean = t
        .replace(/\[Subagent Context\]\s*/g, '')
        .replace(/You are running as a subagent[^.]*\.\s*/i, '')
        .replace(/Results auto-announce[^.]*\.\s*/i, '')
        .replace(/\n/g, ' ').replace(/\s+/g, ' ').trim();
      return { sender: '⚡', text: clean ? '「subagent-init …」' + esc(trunc(clean, 80)) : '「subagent-init …」' };
    },
  },
  {
    test: t => t.includes('BEGIN_UNTRUSTED_CHILD_RESULT') || t.includes('END_UNTRUSTED_CHILD_RESULT'),
    render: t => {
      const clean = t.replace(/<<<[A-Z_]+>>>/g, '').replace(/\n/g, ' ').replace(/\s+/g, ' ').trim();
      return { sender: '⚡', text: clean ? '「child-result …」' + esc(trunc(clean, 80)) : '「child-result …」' };
    },
  },
  {
    test: t => t.includes('[media attached:'),
    render: t => {
      const files = [...t.matchAll(/\/([^/\s|]+\.\w+)/g)].map(m => m[1]);
      const names = files.length ? files.map(f => f.length > 20 ? f.slice(-20) : f).join(', ') : 'file';
      return { sender: '⚡', text: '「media …」' + esc(names) };
    },
  },
  {
    test: t => /^System: \[/.test(t),
    render: t => {
      const detail = t.replace(/^System: \[[^\]]*\]\s*/, '').replace(/\n/g, ' ').trim();
      return { sender: '⚡', text: '「system …」' + esc(trunc(detail, 80)) };
    },
  },
  {
    test: t => t.includes('OPENCLAW_INTERNAL_CONTEXT') || t.includes('openclaw.inbound'),
    render: t => {
      const clean = stripMeta(t);
      return { sender: '⚡', text: clean ? '「internal …」' + esc(trunc(clean, 100)) : '「internal …」' };
    },
  },
  {
    test: t => t.includes('Inter-session message'),
    render: t => {
      const clean = stripMeta(t);
      return clean ? { sender: '⚡', text: '「cross-session …」' + esc(trunc(clean, 100)) } : null;
    },
  },
  {
    test: t => t.length > 1000,
    render: t => {
      const preview = trunc(t.replace(/\n/g, ' ').replace(/\s+/g, ' ').trim(), 80);
      return { sender: '⚡', text: '「long …」' + esc(preview) };
    },
  },
];

function parse(entry) {
  const msg = entry.message;
  if (!msg) return null;

  // ── assistant ──
  if (msg.role === 'assistant') {
    const content = Array.isArray(msg.content) ? msg.content : [];
    const tools = content.filter(c => c.type === 'toolCall').map(summarizeTool);
    const model = shortModel(msg.model);
    const text = content
      .filter(c => c.type === 'text' && c.text)
      .map(c => c.text).join(' ').trim()
      .replace(/\n/g, ' ').replace(/\s+/g, ' ')
      .replace(/\[\[reply_to_current\]\]/g, '\x00REPLY\x00')
      .replace(/\[\[reply_to:[^\]]*\]\]/g, '\x00REPLY\x00');

    if (/^NO_REPLY\s*$/.test(text)) return { sender: '🤖', text: '〔〕', model };
    if (/HEARTBEAT_OK/.test(text)) return { sender: '🤖', text: esc(trunc(text, MAX)).replace(/\x00REPLY\x00/g, '<i>↪reply</i>') + ' 💤', model };
    if (/ANNOUNCE_SKIP/.test(text)) return { sender: '🤖', text: '💤', model };

    const parts = [];
    if (tools.length) parts.push(tools.join(' '));
    if (text) parts.push(esc(trunc(text, MAX)).replace(/\x00REPLY\x00/g, '<i>↪reply</i>'));
    if (!parts.length) return { sender: '🤖', text: '…', model };
    return { sender: '🤖', text: parts.join(' | '), model };
  }

  // ── user ──
  if (msg.role === 'user') {
    const content = Array.isArray(msg.content)
      ? msg.content
      : [{ type: 'text', text: msg.content }];

    for (const c of content) {
      if (c.type !== 'text' || !c.text) continue;
      const t = c.text;

      for (const p of USER_PATTERNS) {
        if (p.test(t)) return p.render(t);
      }

      // fallback: strip metadata and show
      const clean = stripMeta(t);
      return clean ? { sender: '⚡', text: esc(trunc(clean, MAX)) } : null;
    }
  }

  // ── toolResult ──
  if (msg.role === 'toolResult') {
    return { sender: '↩️', text: summarizeResult(msg) };
  }

  // ── system (not used in OpenClaw JSONL transcripts, kept for compatibility) ──
  if (msg.role === 'system') {
    return { sender: '⚡', text: '「system-prompt …」' };
  }

  return null;
}

module.exports = { parse };
