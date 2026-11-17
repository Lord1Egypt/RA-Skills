import fs from 'fs';
import path from 'path';
import zlib from 'zlib';
import { execFileSync } from 'child_process';
import { DEFAULT_SOURCES, HOME_DIR, LENS_DIR, checkAccess, preflight } from './bootstrap.js';

const TWENTY_FOUR_HOURS = 24 * 60 * 60 * 1000;

const SYSTEM_PATTERNS = [
  '<<<BEGIN_UNTRUSTED_CHILD_RESULT>>>',
  'SECURITY NOTICE',
  'OpenClaw runtime context',
  '[Subagent Context]',
  'The previous agent run was aborted',
  'An async command the user already approved',
  'An async command you ran earlier has completed.',
  'A scheduled reminder has been triggered',
  'Pre-compaction memory flush',
  'The following is an ephemeral message',
  'You are the autonomous agent assigned to this task',
  'Do NOT ask for human confirmation',
  'reply with ONLY: NO_REPLY',
  'EXISTING BOARD TASKS',
  '=== EMAIL #',
  'DISTILLATION_READY',
  'INTERVIEW_READY',
  'BOOTSTRAP_LENS',
  'TRACE_EMPTY',
  'oauth2/callback',
  'oauth/callback',
  'auth/callback',
  'login/callback',
  'oauth2callback'
];

const CANONICAL_LENS_FILES = [
  'AXIOM.yaml',
  'ETHOS.yaml',
  'MODUS.yaml',
  'SCOPE.json',
  'README.md',
  '.gitignore'
];

const SECURITY_PATTERNS = [
  { name: 'URL', regex: /https?:\/\/(?:localhost|(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{2,63})\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)/gi },
  { name: 'PRIVATE_KEY', regex: /-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED |PGP )?PRIVATE KEY(?: BLOCK)?-----[\s\S]*?-----END (?:RSA |EC |DSA |OPENSSH |ENCRYPTED |PGP )?PRIVATE KEY(?: BLOCK)?-----/g },
  { name: 'PASSWORD', regex: /\b(?:(?:password|passwd|secret|token)(?:\s+(?:is|was)\s+|\s*[:=]\s*)|bearer\s+)["']?[^\s,;"']+["']?/gi },
  { name: 'API_ID_KEYS', regex: /\b(?:(?:sk|pk|ghp|gho|ghu|ghs|ghr|github_pat|xoxb|xoxp|xoxa|glpat|AIza|AKIA|ya29)[a-zA-Z0-9._-]{12,}|(?=[a-zA-Z0-9_]*[a-zA-Z])(?=[a-zA-Z0-9_]*\d)[a-zA-Z0-9_]{20,})\b/g },
  { name: 'SSN', regex: /\b\d{3}-\d{2}-\d{4}\b/g },
  { name: 'BANK', regex: /\b(?:\d{9}|\d{10,12})\b/g },
  { name: 'IP', regex: /\b(?:\d{1,3}\.){3}\d{1,3}\b|::1\b|\b(?:[a-fA-F0-9]{1,4}:){1,7}:?[a-fA-F0-9]{0,4}(?::[a-fA-F0-9]{1,4}){1,7}\b|\b(?:[a-fA-F0-9]{1,4}:){7,8}[a-fA-F0-9]{1,4}\b/g }
];

const PRIVATE_PATTERNS = [
  { name: 'EMAIL', regex: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/g },
  { name: 'PHONE', regex: /(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b|\b\d{3}[-.\s]\d{4}\b|\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b/g },
  { name: 'ADDRESS', regex: /\b\d{1,5}\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Circle|Cir|Way|Pkwy|Parkway)\b/g },
  { name: 'DOB', regex: /\b(?:\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4})\b/g },
  { name: 'USER_HANDLE', regex: /\B@[\w.-]+\b/g }
];

const STRIPPED_XML_TAG_REGEX = /<(ADDITIONAL_METADATA|USER_SETTINGS_CHANGE|SYSTEM_MESSAGE|ide_opened_file|ide_selection|system-reminder|local-command-stdout|local-command-caveat|task-notification|user-prompt-submit-hook|bash-input|bash-stdout|bash-stderr|ultraplan|skill|subagent_notification|turn_aborted|system_instruction)>[\s\S]*?<\/\1>/g;

const PASTE_LEAD_IN_REGEX = /(?:got|received|sent me|asked me|saw|pasted|shared|forwarded)\s+this(?:\s+now)?(?:\.{2,}|:)\s*$/i;

function parseTimestamp(rawTs, fallbackTs = 0) {
  if (typeof rawTs === 'number' && Number.isFinite(rawTs)) {
    return rawTs > 0 && rawTs < 1e11 ? rawTs * 1000 : rawTs;
  }
  if (typeof rawTs === 'string' && rawTs.trim()) {
    const trimmed = rawTs.trim();
    if (/^\d+(?:\.\d+)?$/.test(trimmed)) {
      const num = Number(trimmed);
      return num > 0 && num < 1e11 ? num * 1000 : num;
    }
    const parsed = Date.parse(trimmed);
    if (!Number.isNaN(parsed)) return parsed;
  }
  return fallbackTs;
}

function redact(text, anonymized = false) {
  let cleaned = text;

  SECURITY_PATTERNS.forEach(p => {
    cleaned = cleaned.replace(p.regex, `[REDACTED_${p.name}]`);
  });

  if (anonymized) {
    PRIVATE_PATTERNS.forEach(p => {
      cleaned = cleaned.replace(p.regex, `[REDACTED_${p.name}]`);
    });
  }

  return cleaned;
}

function getSubjectNameTokens() {
  const tokens = new Set();
  const axiomPath = path.join(LENS_DIR, 'AXIOM.yaml');
  if (!fs.existsSync(axiomPath)) return tokens;
  try {
    const content = fs.readFileSync(axiomPath, 'utf8');
    const bioMatch = content.match(/^biometrics_and_chronological_timeline:\r?\n(?:[ \t]+.*\r?\n)*?[ \t]+name:\s*["']?([^"'\r\n]+)["']?/m);
    const topMatch = bioMatch || content.match(/^name:\s*["']?([^"'\r\n]+)["']?/m);
    if (topMatch && topMatch[1]) {
      const rawName = topMatch[1].trim();
      if (rawName && rawName.toLowerCase() !== 'unknown' && !rawName.includes('Pending Input')) {
        for (const part of rawName.split(/\s+/)) {
          const clean = part.replace(/[^a-zA-Z]/g, '').toLowerCase();
          if (clean.length >= 2) {
            tokens.add(clean);
            if (clean.length >= 5) {
              tokens.add(clean.slice(0, 4));
            }
          }
        }
      }
    }
  } catch (e) {}
  return tokens;
}

function stripUnfencedJsonBlocks(text) {
  const lines = text.split('\n');
  const kept = [];
  let i = 0;

  while (i < lines.length) {
    const trimmed = lines[i].trim();
    if (/^[\[{]\s*$/.test(trimmed)) {
      let depth = 0;
      let inString = false;
      let escaped = false;
      let j = i;
      let hasJsonKey = false;

      while (j < lines.length) {
        const line = lines[j];
        if (!hasJsonKey && /"[^"\n]+"\s*:/.test(line)) hasJsonKey = true;
        for (let c = 0; c < line.length; c++) {
          const ch = line[c];
          if (escaped) {
            escaped = false;
            continue;
          }
          if (ch === '\\' && inString) {
            escaped = true;
            continue;
          }
          if (ch === '"') {
            inString = !inString;
            continue;
          }
          if (!inString) {
            if (ch === '{' || ch === '[') depth++;
            else if (ch === '}' || ch === ']') depth--;
          }
        }
        j++;
        if (depth <= 0) break;
      }

      if (depth <= 0 && j - i >= 3 && hasJsonKey) {
        i = j;
        continue;
      }
      if (depth > 0) {
        while (i < lines.length) {
          if (!/^\s*(?:[\[{}\],]+|"[^"\n]+"\s*:\s*(?:["\d\[{]|true\b|false\b|null\b).*)\s*$/.test(lines[i])) {
            kept.push(lines[i]);
          }
          i++;
        }
        break;
      }
    }

    if (/^\s*(?:[\[{}\],]+|"[^"\n]+"\s*:\s*(?:["\d\[{]|true\b|false\b|null\b).*)\s*$/.test(lines[i])) {
      i++;
      continue;
    }

    kept.push(lines[i]);
    i++;
  }

  return kept.join('\n');
}

function stripPasteLeadInBlocks(text) {
  const paragraphs = text.split(/\r?\n\s*\r?\n/);
  if (paragraphs.length <= 1) return text;

  const kept = [];
  let i = 0;

  while (i < paragraphs.length) {
    const para = paragraphs[i].trim();
    if (PASTE_LEAD_IN_REGEX.test(para) && i + 1 < paragraphs.length) {
      kept.push(paragraphs[i]);
      i++;
      while (i < paragraphs.length) {
        if (/^---+$/.test(paragraphs[i].trim())) {
          i++;
          break;
        }
        i++;
      }
      continue;
    }
    kept.push(paragraphs[i]);
    i++;
  }

  return kept.join('\n\n');
}

function isContaminatedParagraph(para, subjectNames) {
  const trimmed = para.trim();
  if (!trimmed) return true;
  if (/^---+$/.test(trimmed)) return true;
  if (trimmed.length > 2000) return true;

  if (/^[A-Z][A-Za-z .'-]{1,40}\s+\[?\d{1,2}:\d{2}\s*(?:AM|PM)\]?\s*(?:\r?\n|$)/.test(trimmed)) {
    return true;
  }

  const mentionStart = trimmed.match(/^(?:\[@([A-Za-z0-9_.\s-]+)\]|@([A-Za-z0-9_.-]+))(?:\([^)]*\))?[,:]?\s+/);
  const mentionTarget = mentionStart ? (mentionStart[1] || mentionStart[2] || '') : '';
  if (mentionTarget && subjectNames.size > 0) {
    const mentionedParts = mentionTarget.toLowerCase().split(/\s+/);
    if (mentionedParts.some(p => subjectNames.has(p))) {
      return true;
    }
  }

  if (/^\s*\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}/m.test(trimmed)) return true;
  if (/##\[(?:group|endgroup|error|warning|command)\]/.test(trimmed)) return true;
  if (/^\s+at\s+\S+\s+\(.*:\d+:\d+\)/m.test(trimmed)) return true;
  if (/^(?:diff --git |@@\s+-\d+,\d+\s+\+\d+,\d+\s+@@)/m.test(trimmed)) return true;

  const headerMatches = trimmed.match(/^(?:Credentials|Degrees?|Education|Experience|Certifications|Licensure|Qualifications|Specialties|From|To|Subject|Sent|Date):\s*/gm);
  if (headerMatches && headerMatches.length >= 2) return true;

  if (/^(?:Meet|About)\s+[A-Z][a-z]+(?:\s+[–—-]\s+.*)?$/m.test(trimmed)) return true;

  const selfIntro = trimmed.match(/\bMy name is ([A-Z][a-z]+)\b/);
  if (selfIntro && subjectNames.size > 0 && !subjectNames.has(selfIntro[1].toLowerCase())) {
    return true;
  }

  return false;
}

function cleanUserText(rawText, subjectNames = new Set(), automatedPrompts = new Set(), anonymized = false) {
  if (!rawText || typeof rawText !== 'string') return '';
  if (rawText.includes('HEARTBEAT_OK') || rawText.startsWith('[cron:') || rawText.includes('A new session was started via')) {
    return '';
  }

  let text = rawText;
  if (text.includes('<')) {
    text = text.replace(STRIPPED_XML_TAG_REGEX, '');

    const cmdNameMatch = text.match(/<command-name>\s*([\s\S]*?)\s*<\/command-name>/);
    if (cmdNameMatch) {
      const cmdArgsMatch = text.match(/<command-args>\s*([\s\S]*?)\s*<\/command-args>/);
      const cmdName = cmdNameMatch[1].trim();
      const cmdArgs = cmdArgsMatch ? cmdArgsMatch[1].trim() : '';
      if (/^\/?(?:clear|compact|login|logout|model|resume|mcp|init|config|doctor|cost|status|permissions|terminal-setup|vim|memory|help|quit|exit)$/i.test(cmdName)) {
        return '';
      }
      if (cmdArgs) {
        text = cmdArgs;
      } else {
        text = text.replace(/<command-(?:name|message|args)>[\s\S]*?<\/command-(?:name|message|args)>/g, '');
      }
    } else {
      text = text.replace(/<command-(?:message|args)>[\s\S]*?<\/command-(?:message|args)>/g, '');
    }

    const userRequestMatch = text.match(/<USER_REQUEST>\s*([\s\S]*?)\s*<\/USER_REQUEST>/);
    if (userRequestMatch) {
      text = userRequestMatch[1];
    }
  }

  const trimmedInitial = text.trim();
  if (!trimmedInitial) return '';
  if (automatedPrompts.has(trimmedInitial)) return '';

  if (
    trimmedInitial.startsWith('Base directory for this skill:') ||
    trimmedInitial.startsWith('This session is being continued from a previous conversation') ||
    trimmedInitial.startsWith('[Request interrupted by user')
  ) {
    return '';
  }

  if (trimmedInitial.includes('#private') || SYSTEM_PATTERNS.some(pattern => trimmedInitial.includes(pattern))) {
    return '';
  }

  if (/^[A-Z][A-Za-z .'-]{1,40}\s+\[?\d{1,2}:\d{2}\s*(?:AM|PM)\]?\s*\r?\n/.test(trimmedInitial)) {
    return '';
  }

  const salutationMatch = trimmedInitial.match(/^(?:Hi|Hello|Hey|Dear)\s+([A-Z][a-z]+)[,!:\r\n]/);
  if (salutationMatch) {
    const greeted = salutationMatch[1].toLowerCase();
    if (
      (subjectNames.size > 0 && subjectNames.has(greeted)) ||
      /(?:Thank you!?|Thanks[,!]?|Best(?: regards)?[,!]?|Sincerely[,!]?|Regards[,!]?)\s*$/i.test(trimmedInitial)
    ) {
      return '';
    }
  }

  if (/^(?:Meet|About)\s+[A-Z][a-z]+(?:\s+[–—-]\s+.*)?\s*\r?\n/.test(trimmedInitial)) {
    return '';
  }

  const selfIntroMatch = trimmedInitial.match(/\bMy name is ([A-Z][a-z]+)\b/);
  if (selfIntroMatch && subjectNames.size > 0 && !subjectNames.has(selfIntroMatch[1].toLowerCase())) {
    return '';
  }

  const totalHeaders = trimmedInitial.match(/^(?:Credentials|Degrees?|Education|Experience|Certifications|Licensure|Qualifications|Specialties|From|To|Subject|Sent|Date):\s*/gm);
  if (totalHeaders && totalHeaders.length >= 2) {
    return '';
  }

  text = text.replace(/^System(?: \([^)]+\))?: \[.*?\][\s\S]*?(?=\r?\n\s*\r?\n|$)/gm, '');
  text = text.replace(/^Action:\s.*$/gm, '');
  text = text.replace(/Sender \(untrusted metadata\):[^\r\n]*\r?\n```[\s\S]*?```\n*/g, '');
  text = text.replace(/^\[[^\r\n\]]*\]\s*/gm, '');
  text = text.replace(/^Current time:.*$/gm, '');
  text = text.replace(/```[\s\S]*?```/g, '');
  text = text.replace(/^>.*$/gm, '');
  text = text.replace(/<<<EXTERNAL_UNTRUSTED_CONTENT[\s\S]*?END_EXTERNAL_UNTRUSTED_CONTENT.*>>>/g, '');
  text = stripUnfencedJsonBlocks(text);
  text = stripPasteLeadInBlocks(text);
  text = text.replace(/"\[@[^\]]+\]\([^)]+\)[^"]*"/g, '');
  text = text.replace(/[ \t]{2,}/g, ' ');

  const paragraphs = text
    .split(/\r?\n\s*\r?\n/)
    .map(p => p.trim())
    .filter(p => !isContaminatedParagraph(p, subjectNames));

  text = paragraphs.join('\n\n').trim();
  if (!text || automatedPrompts.has(text)) return '';

  const redacted = redact(text, anonymized);
  const substantive = redacted.replace(/\[REDACTED_[A-Z_]+\]/g, '').trim();
  return substantive.length > 10 ? redacted : '';
}

function readVarint(buf, offset) {
  let value = 0;
  let shift = 0;
  let pos = offset;
  while (pos < buf.length) {
    const byte = buf[pos++];
    value += (byte & 0x7f) * (2 ** shift);
    if ((byte & 0x80) === 0) return { value, nextOffset: pos };
    shift += 7;
    if (shift > 49) break;
  }
  return null;
}

function isSidecarRawSummary(rawSummary, convId, sidecarIds) {
  if (!rawSummary) return false;
  const buf = Buffer.isBuffer(rawSummary)
    ? rawSummary
    : ArrayBuffer.isView(rawSummary)
      ? Buffer.from(rawSummary.buffer, rawSummary.byteOffset, rawSummary.byteLength)
      : Buffer.from(rawSummary);
  const str = buf.toString('utf8');

  if (
    str.includes('agentapi') ||
    str.includes('new-conversation') ||
    str.includes('command(') ||
    str.includes('read_file(') ||
    str.includes('write_file(') ||
    str.includes('read_url(')
  ) {
    return true;
  }

  for (const id of sidecarIds) {
    if (id && str.includes(id)) return true;
  }

  if (convId && convId.length === 36) {
    const marker = Buffer.from(`\x32\x24${convId}`, 'utf8');
    const idx = buf.indexOf(marker);
    if (idx !== -1) {
      let pos = idx + marker.length;
      while (pos < buf.length && buf[pos] === 0x3a) {
        const lenInfo = readVarint(buf, pos + 1);
        if (!lenInfo) break;
        pos = lenInfo.nextOffset + lenInfo.value;
      }
      if (pos < buf.length && buf[pos] === 0x62) {
        return true;
      }
    }
  }

  return false;
}

function collectAutomationMetadata(homeDir) {
  const automatedPrompts = new Set();
  const sidecarIds = new Set();
  const sidecarConvIds = new Set();

  const registerPrompt = prompt => {
    if (typeof prompt === 'string' && prompt.trim()) {
      automatedPrompts.add(prompt.trim());
    }
  };

  const sidecarsConfigDir = path.join(homeDir, '.gemini/config/sidecars');
  if (fs.existsSync(sidecarsConfigDir)) {
    try {
      const entries = fs.readdirSync(sidecarsConfigDir, { withFileTypes: true });
      for (const entry of entries) {
        if (!entry.isDirectory()) continue;
        sidecarIds.add(entry.name);
        const cfgPath = path.join(sidecarsConfigDir, entry.name, 'sidecar.json');
        if (fs.existsSync(cfgPath)) {
          try {
            const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
            if (Array.isArray(cfg.args)) {
              const sepIdx = cfg.args.indexOf('--');
              if (sepIdx !== -1 && cfg.args[sepIdx + 1]) {
                registerPrompt(cfg.args[sepIdx + 1]);
              } else if (cfg.args.includes('new-conversation') || cfg.args.includes('send-message')) {
                registerPrompt(cfg.args[cfg.args.length - 1]);
              }
            }
          } catch (e) {}
        }
      }
    } catch (e) {}
  }

  const openclawCronStores = new Set([path.join(homeDir, '.openclaw/cron/jobs.json')]);
  const openclawConfigPath = path.join(homeDir, '.openclaw/openclaw.json');
  if (fs.existsSync(openclawConfigPath)) {
    try {
      const cfg = JSON.parse(fs.readFileSync(openclawConfigPath, 'utf8'));
      const jobs = Array.isArray(cfg.cron?.jobs) ? cfg.cron.jobs : (Array.isArray(cfg.jobs) ? cfg.jobs : []);
      for (const job of jobs) {
        registerPrompt(job?.payload?.message || job?.payload?.text);
      }
      if (typeof cfg.cron?.store === 'string' && cfg.cron.store.trim()) {
        const storePath = cfg.cron.store.startsWith('~/')
          ? path.join(homeDir, cfg.cron.store.slice(2))
          : cfg.cron.store;
        openclawCronStores.add(storePath);
      }
      if (typeof cfg.agents?.defaults?.heartbeat?.prompt === 'string') {
        registerPrompt(cfg.agents.defaults.heartbeat.prompt);
      }
    } catch (e) {}
  }

  for (const cronStorePath of openclawCronStores) {
    if (fs.existsSync(cronStorePath)) {
      try {
        const parsed = JSON.parse(fs.readFileSync(cronStorePath, 'utf8'));
        const jobs = Array.isArray(parsed) ? parsed : (Array.isArray(parsed?.jobs) ? parsed.jobs : []);
        for (const job of jobs) {
          registerPrompt(job?.payload?.message || job?.payload?.text);
        }
      } catch (e) {}
    }
  }

  if (process.env.OPENCLAW_CRON_LIST) {
    try {
      const parsed = JSON.parse(process.env.OPENCLAW_CRON_LIST);
      const jobs = Array.isArray(parsed) ? parsed : (Array.isArray(parsed?.jobs) ? parsed.jobs : []);
      for (const job of jobs) {
        registerPrompt(job?.payload?.message || job?.payload?.text);
      }
    } catch (e) {}
  }

  return { automatedPrompts, sidecarIds, sidecarConvIds, registerPrompt };
}

function statTranscript(logsDir) {
  const fullPath = path.join(logsDir, 'transcript_full.jsonl');
  try {
    return { targetPath: fullPath, stats: fs.statSync(fullPath) };
  } catch (e) {}

  const compactPath = path.join(logsDir, 'transcript.jsonl');
  try {
    return { targetPath: compactPath, stats: fs.statSync(compactPath) };
  } catch (e) {}

  return null;
}

async function collectAntigravityMessages(homeDir, now, subjectNames, automationMeta, anonymized) {
  const messages = [];
  const geminiDir = path.join(homeDir, '.gemini');
  const agyDirs = [];

  if (fs.existsSync(geminiDir)) {
    try {
      const dirs = fs.readdirSync(geminiDir, { withFileTypes: true })
        .filter(dirent => dirent.isDirectory() && dirent.name.startsWith('antigravity'))
        .map(dirent => path.join(geminiDir, dirent.name));
      agyDirs.push(...dirs);
    } catch (e) {
      checkAccess(e);
    }
  }

  const { automatedPrompts, sidecarIds, sidecarConvIds, registerPrompt } = automationMeta;
  const subagentConvIds = new Set();

  for (const agyDir of agyDirs) {
    const brainDir = path.join(agyDir, 'brain');
    if (!fs.existsSync(brainDir)) continue;

    let conversations = [];
    try {
      conversations = fs.readdirSync(brainDir, { withFileTypes: true })
        .filter(dirent => dirent.isDirectory())
        .map(dirent => dirent.name);
    } catch (e) {
      checkAccess(e);
      continue;
    }

    const recentConversations = [];
    const recentConvIdSet = new Set();

    for (const convId of conversations) {
      const logsDir = path.join(brainDir, convId, '.system_generated/logs');
      const found = statTranscript(logsDir);
      if (!found) continue;
      if (now - found.stats.mtimeMs <= TWENTY_FOUR_HOURS) {
        recentConversations.push({
          convId,
          targetPath: found.targetPath,
          mtimeMs: found.stats.mtimeMs
        });
        recentConvIdSet.add(convId);
      }
    }

    if (recentConversations.length === 0) continue;

    const sidecarDataDir = path.join(agyDir, 'sidecar_data');
    if (fs.existsSync(sidecarDataDir)) {
      try {
        const scDirs = fs.readdirSync(sidecarDataDir, { withFileTypes: true }).filter(d => d.isDirectory());
        for (const scDir of scDirs) {
          sidecarIds.add(scDir.name);
          const eventsDir = path.join(sidecarDataDir, scDir.name, 'events');
          if (!fs.existsSync(eventsDir)) continue;
          const eventFiles = fs.readdirSync(eventsDir).filter(f => f.endsWith('.json'));
          for (const ef of eventFiles) {
            try {
              const ev = JSON.parse(fs.readFileSync(path.join(eventsDir, ef), 'utf8'));
              const newConv = ev?.payload?.newConversation;
              const sendMsg = ev?.payload?.sendMessage;
              if (newConv?.conversationId) sidecarConvIds.add(newConv.conversationId);
              if (newConv?.prompt) registerPrompt(newConv.prompt);
              if (sendMsg?.conversationId) sidecarConvIds.add(sendMsg.conversationId);
              if (sendMsg?.prompt) registerPrompt(sendMsg.prompt);
              if (sendMsg?.message) registerPrompt(sendMsg.message);
            } catch (e) {}
          }
        }
      } catch (e) {}
    }

    const dbPath = path.join(agyDir, 'conversation_summaries.db');
    if (fs.existsSync(dbPath)) {
      try {
        const sqlite = await import('node:sqlite');
        const db = new sqlite.DatabaseSync(dbPath, { readOnly: true });
        try {
          const rows = db.prepare('SELECT conversation_id, nesting_depth, parent_conversation_id, agent_name, raw_summary FROM conversation_summaries').all();
          for (const row of rows) {
            const cid = row.conversation_id;
            if (!cid || !recentConvIdSet.has(cid)) continue;
            if ((row.nesting_depth && row.nesting_depth > 0) || row.parent_conversation_id || row.agent_name) {
              subagentConvIds.add(cid);
              continue;
            }
            if (isSidecarRawSummary(row.raw_summary, cid, sidecarIds)) {
              sidecarConvIds.add(cid);
            }
          }
        } finally {
          db.close();
        }
      } catch (e) {}
    }

    for (const { convId, targetPath, mtimeMs } of recentConversations) {
      if (subagentConvIds.has(convId)) continue;

      let lines = [];
      try {
        lines = fs.readFileSync(targetPath, 'utf8').split('\n');
      } catch (e) {
        continue;
      }

      const isSidecarConv = sidecarConvIds.has(convId);
      let seenFirstUserInput = false;

      for (const line of lines) {
        if (!line.trim()) continue;
        try {
          const entry = JSON.parse(line);
          if (entry.source === 'USER_EXPLICIT' && entry.type === 'USER_INPUT' && typeof entry.content === 'string') {
            const isInitialStep = entry.step_index === 0 || !seenFirstUserInput;
            seenFirstUserInput = true;
            if (isSidecarConv && isInitialStep) {
              continue;
            }
            const ts = parseTimestamp(entry.created_at, mtimeMs);
            if (now - ts <= TWENTY_FOUR_HOURS) {
              const cleaned = cleanUserText(entry.content, subjectNames, automatedPrompts, anonymized);
              if (cleaned) {
                messages.push({ timestamp: ts, text: cleaned });
              }
            }
          }
        } catch (e) {}
      }
    }
  }

  return messages;
}

function isNonHumanOpenClawValue(val) {
  if (!val || typeof val !== 'string') return false;
  return /\b(?:subagent|cron|system|automation|daemon|webhook|inter_session|hook|heartbeat)\b/i.test(val);
}

function parseOpenClawEntry(entry, fallbackTs, now, messages, subjectNames, automatedPrompts, nonHumanSessionIds = new Set(), anonymized = false) {
  if (!entry || entry.type !== 'message' || entry.message?.role !== 'user') return;

  const entrySessionId = entry.sessionId || entry.session_id || entry.sessionKey || entry.session_key || '';
  if (entrySessionId && (nonHumanSessionIds.has(entrySessionId) || isNonHumanOpenClawValue(entrySessionId))) {
    return;
  }

  const candidateFields = [
    entry.message?.sender?.label,
    entry.message?.sender?.id,
    entry.message?.sender?.kind,
    entry.message?.provenance?.kind,
    entry.provenance?.kind,
    entry.source
  ];
  if (candidateFields.some(isNonHumanOpenClawValue)) {
    return;
  }

  const messageContent = Array.isArray(entry.message.content)
    ? entry.message.content
      .filter(c => c.type === 'text' && typeof c.text === 'string')
      .map(c => c.text)
      .join('\n')
    : typeof entry.message.content === 'string' ? entry.message.content : '';

  const rawTs = entry.message.timestamp || entry.timestamp;
  const ts = parseTimestamp(rawTs, fallbackTs);

  if (ts > 0 && now - ts <= TWENTY_FOUR_HOURS) {
    const cleaned = cleanUserText(messageContent, subjectNames, automatedPrompts, anonymized);
    if (cleaned) {
      messages.push({ timestamp: ts, text: cleaned });
    }
  }
}

async function collectOpenClawMessages(homeDir, now, subjectNames, automatedPrompts, anonymized) {
  const messages = [];
  const nonHumanSessionIds = new Set();
  const sessionsDir = path.join(homeDir, '.openclaw/agents/main/sessions');
  const sessionsIndexPath = path.join(sessionsDir, 'sessions.json');

  if (fs.existsSync(sessionsIndexPath)) {
    try {
      const idx = JSON.parse(fs.readFileSync(sessionsIndexPath, 'utf8'));
      if (idx && typeof idx === 'object') {
        for (const [k, v] of Object.entries(idx)) {
          if (
            isNonHumanOpenClawValue(k) ||
            isNonHumanOpenClawValue(v?.key) ||
            isNonHumanOpenClawValue(v?.sessionKey) ||
            isNonHumanOpenClawValue(v?.subagentRole) ||
            isNonHumanOpenClawValue(v?.origin?.surface) ||
            isNonHumanOpenClawValue(v?.origin?.provider) ||
            Boolean(v?.spawnedBy)
          ) {
            nonHumanSessionIds.add(k);
            if (v?.sessionId) nonHumanSessionIds.add(v.sessionId);
            if (v?.id) nonHumanSessionIds.add(v.id);
          }
        }
      }
    } catch (e) {}
  }

  const sqlitePath = path.join(homeDir, '.openclaw/agents/main/agent/openclaw-agent.sqlite');

  if (fs.existsSync(sqlitePath)) {
    try {
      const stats = fs.statSync(sqlitePath);
      const walPath = `${sqlitePath}-wal`;
      const walMtime = fs.existsSync(walPath) ? fs.statSync(walPath).mtimeMs : 0;
      const latestMtime = Math.max(stats.mtimeMs, walMtime);
      if (now - latestMtime <= TWENTY_FOUR_HOURS) {
        const sqlite = await import('node:sqlite');
        const db = new sqlite.DatabaseSync(sqlitePath, { readOnly: true });
        try {
          const rows = db.prepare('SELECT event_json, event_zstd FROM transcript_events').all();
          const parsedEvents = [];
          for (const row of rows) {
            let rawJson = row.event_json;
            if (!rawJson && row.event_zstd && typeof zlib.zstdDecompressSync === 'function') {
              rawJson = zlib.zstdDecompressSync(row.event_zstd).toString('utf8');
            }
            if (!rawJson) continue;
            if (!rawJson.includes('"session"') && !(rawJson.includes('"message"') && rawJson.includes('"user"'))) {
              continue;
            }
            try {
              const entry = JSON.parse(rawJson);
              if (entry?.type === 'session') {
                const sid = entry.id || entry.sessionId || entry.session_id;
                const skey = entry.key || entry.sessionKey || entry.session_key;
                if (
                  isNonHumanOpenClawValue(sid) ||
                  isNonHumanOpenClawValue(skey) ||
                  isNonHumanOpenClawValue(entry.subagentRole) ||
                  Boolean(entry.spawnedBy)
                ) {
                  if (sid) nonHumanSessionIds.add(sid);
                  if (skey) nonHumanSessionIds.add(skey);
                }
              } else if (entry?.type === 'message' && entry.message?.role === 'user') {
                parsedEvents.push(entry);
              }
            } catch (e) {}
          }
          for (const entry of parsedEvents) {
            parseOpenClawEntry(entry, 0, now, messages, subjectNames, automatedPrompts, nonHumanSessionIds, anonymized);
          }
        } finally {
          db.close();
        }
      }
    } catch (e) {
      checkAccess(e);
    }
  }

  if (!fs.existsSync(sessionsDir)) return messages;

  let files = [];
  try {
    files = fs.readdirSync(sessionsDir).filter(f => f.endsWith('.jsonl'));
  } catch (e) {
    checkAccess(e);
    return messages;
  }

  for (const file of files) {
    const baseId = file.replace(/\.jsonl$/, '');
    if (nonHumanSessionIds.has(baseId) || isNonHumanOpenClawValue(baseId)) continue;

    const filePath = path.join(sessionsDir, file);
    let stats;
    try {
      stats = fs.statSync(filePath);
    } catch (e) {
      continue;
    }

    if (now - stats.mtimeMs > TWENTY_FOUR_HOURS) continue;

    let lines = [];
    try {
      lines = fs.readFileSync(filePath, 'utf8').split('\n');
    } catch (e) {
      continue;
    }

    for (const line of lines) {
      if (!line.trim()) continue;
      try {
        const entry = JSON.parse(line);
        if (entry?.type === 'session') {
          const sid = entry.id || entry.sessionId || entry.session_id;
          const skey = entry.key || entry.sessionKey || entry.session_key;
          if (
            (sid && nonHumanSessionIds.has(sid)) ||
            (skey && nonHumanSessionIds.has(skey)) ||
            isNonHumanOpenClawValue(sid) ||
            isNonHumanOpenClawValue(skey) ||
            isNonHumanOpenClawValue(entry.subagentRole) ||
            Boolean(entry.spawnedBy)
          ) {
            break;
          }
          continue;
        }
        parseOpenClawEntry(entry, stats.mtimeMs, now, messages, subjectNames, automatedPrompts, nonHumanSessionIds, anonymized);
      } catch (e) {}
    }
  }

  return messages;
}

function collectClaudeCodeMessages(homeDir, now, subjectNames, automatedPrompts, anonymized) {
  const messages = [];
  const projectsDir = path.join(homeDir, '.claude/projects');
  if (!fs.existsSync(projectsDir)) return messages;

  let projects = [];
  try {
    projects = fs.readdirSync(projectsDir, { withFileTypes: true })
      .filter(dirent => dirent.isDirectory())
      .map(dirent => path.join(projectsDir, dirent.name));
  } catch (e) {
    checkAccess(e);
    return messages;
  }

  for (const projectPath of projects) {
    let files = [];
    try {
      files = fs.readdirSync(projectPath).filter(f => f.endsWith('.jsonl'));
    } catch (e) {
      continue;
    }

    for (const file of files) {
      const filePath = path.join(projectPath, file);
      let stats;
      try {
        stats = fs.statSync(filePath);
      } catch (e) {
        continue;
      }

      if (now - stats.mtimeMs > TWENTY_FOUR_HOURS) continue;

      let lines = [];
      try {
        lines = fs.readFileSync(filePath, 'utf8').split('\n');
      } catch (e) {
        continue;
      }

      for (const line of lines) {
        if (!line.trim()) continue;
        try {
          const entry = JSON.parse(line);
          if (entry.isMeta || entry.isSidechain || entry.isCompactSummary || entry.isVisibleInTranscriptOnly || Boolean(entry.agentId)) {
            continue;
          }
          if (entry.userType && entry.userType !== 'external') continue;
          if (typeof entry.entrypoint === 'string' && /^sdk/i.test(entry.entrypoint)) continue;
          if (entry.type === 'user' && entry.message?.role === 'user') {
            if (Array.isArray(entry.message.content) && entry.message.content.some(c => c.type === 'tool_result')) {
              continue;
            }

            const messageContent = Array.isArray(entry.message.content)
              ? entry.message.content
                .filter(c => c.type === 'text' && typeof c.text === 'string')
                .map(c => c.text)
                .filter(t => !t.trim().startsWith('Base directory for this skill:') && !t.trim().startsWith('This session is being continued from a previous conversation') && !t.trim().startsWith('[Request interrupted by user'))
                .join('\n')
              : typeof entry.message.content === 'string' ? entry.message.content : '';

            const ts = parseTimestamp(entry.timestamp, stats.mtimeMs);

            if (now - ts <= TWENTY_FOUR_HOURS) {
              const cleaned = cleanUserText(messageContent, subjectNames, automatedPrompts, anonymized);
              if (cleaned) {
                messages.push({ timestamp: ts, text: cleaned });
              }
            }
          }
        } catch (e) {}
      }
    }
  }

  return messages;
}

function collectCodexMessages(homeDir, now, subjectNames, automatedPrompts, anonymized) {
  const messages = [];
  const codexDir = process.env.CODEX_HOME || path.join(homeDir, '.codex');
  const sessionsDir = path.join(codexDir, 'sessions');
  if (!fs.existsSync(sessionsDir)) return messages;

  let files = [];
  try {
    files = fs.readdirSync(sessionsDir, { recursive: true })
      .filter(f => typeof f === 'string' && f.endsWith('.jsonl'))
      .map(f => path.join(sessionsDir, f));
  } catch (e) {
    checkAccess(e);
    return messages;
  }

  for (const filePath of files) {
    let stats;
    try {
      stats = fs.statSync(filePath);
    } catch (e) {
      continue;
    }

    if (now - stats.mtimeMs > TWENTY_FOUR_HOURS) continue;

    let lines = [];
    try {
      lines = fs.readFileSync(filePath, 'utf8').split('\n');
    } catch (e) {
      continue;
    }

    for (const line of lines) {
      if (!line.trim()) continue;
      try {
        const entry = JSON.parse(line);
        if (entry.type === 'session_meta') {
          const src = entry.payload?.source;
          const orig = entry.payload?.originator;
          if (
            (src && typeof src === 'object') ||
            (typeof src === 'string' && /^(?:subagent|exec|mcp)$/i.test(src)) ||
            orig === 'codex_exec' ||
            Boolean(entry.payload?.parent_thread_id) ||
            Boolean(entry.payload?.agent_role)
          ) {
            break;
          }
          continue;
        }
        if (entry.type === 'response_item' && entry.payload?.type === 'message' && entry.payload?.role === 'user' && Array.isArray(entry.payload.content)) {
          const textBlocks = entry.payload.content
            .filter(c => c.type === 'input_text' && typeof c.text === 'string')
            .map(c => c.text)
            .filter(t => (
              !t.includes('<environment_context>') &&
              !t.includes('<permissions instructions>') &&
              !t.includes('<user_instructions>') &&
              !t.includes('<skill>') &&
              !t.includes('<subagent_notification>') &&
              !t.includes('<turn_aborted>') &&
              !t.includes('<system_instruction>') &&
              !t.startsWith('# AGENTS.md instructions')
            ));

          const messageContent = textBlocks.join('\n');
          const ts = parseTimestamp(entry.timestamp, stats.mtimeMs);

          if (now - ts <= TWENTY_FOUR_HOURS) {
            const cleaned = cleanUserText(messageContent, subjectNames, automatedPrompts, anonymized);
            if (cleaned) {
              messages.push({ timestamp: ts, text: cleaned });
            }
          }
        }
      } catch (e) {}
    }
  }

  return messages;
}

function commitLensRepo() {
  const gitDir = path.join(LENS_DIR, '.git');
  if (!fs.existsSync(gitDir)) {
    return;
  }

  try {
    const gitignorePath = path.join(LENS_DIR, '.gitignore');
    const gitignoreContent = fs.existsSync(gitignorePath) ? fs.readFileSync(gitignorePath, 'utf8') : '';
    const gitignoreLines = gitignoreContent.split(/\r?\n/).map(l => l.trim());
    if (!gitignoreLines.includes('TRACE.txt')) {
      const prefix = gitignoreContent && !gitignoreContent.endsWith('\n') ? '\n' : '';
      fs.writeFileSync(gitignorePath, `${gitignoreContent}${prefix}TRACE.txt\n`, 'utf8');
    }

    const trackedTrace = execFileSync('git', ['ls-files', '--', 'TRACE.txt'], {
      cwd: LENS_DIR,
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore']
    }).trim();

    if (trackedTrace) {
      execFileSync('git', ['rm', '--cached', '--ignore-unmatch', '--', 'TRACE.txt'], {
        cwd: LENS_DIR,
        stdio: 'ignore'
      });
    }

    const existingFiles = CANONICAL_LENS_FILES.filter(f => fs.existsSync(path.join(LENS_DIR, f)));
    const commitTargets = [...(trackedTrace ? ['TRACE.txt'] : []), ...existingFiles];
    if (commitTargets.length === 0) {
      return;
    }

    const status = execFileSync('git', ['status', '--porcelain', '--', ...commitTargets], {
      cwd: LENS_DIR,
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore']
    }).trim();

    if (!status) {
      return;
    }

    const modifiedNodes = [];
    if (/AXIOM\.ya?ml/i.test(status)) modifiedNodes.push('AXIOM');
    if (/ETHOS\.ya?ml/i.test(status)) modifiedNodes.push('ETHOS');
    if (/MODUS\.ya?ml/i.test(status)) modifiedNodes.push('MODUS');

    let commitMsg = 'Distill LENS identity.';
    if (modifiedNodes.length > 0) {
      commitMsg = `Distill ${modifiedNodes.join(', ')}.`;
    }

    if (existingFiles.length > 0) {
      execFileSync('git', ['add', '--', ...existingFiles], { cwd: LENS_DIR, stdio: 'ignore' });
    }
    execFileSync('git', ['commit', '-m', commitMsg], { cwd: LENS_DIR, stdio: 'ignore' });

    let shouldPush = false;
    try {
      const scopePath = path.join(LENS_DIR, 'SCOPE.json');
      if (fs.existsSync(scopePath)) {
        const scope = JSON.parse(fs.readFileSync(scopePath, 'utf8'));
        shouldPush = scope?.meta?.push === true;
      }
    } catch (scopeErr) {}

    if (shouldPush) {
      try {
        execFileSync('git', ['push'], { cwd: LENS_DIR, stdio: 'ignore' });
      } catch (pushErr) {}
    }
  } catch (err) {
    checkAccess(err);
  }
}

async function distillation() {
  const { scope } = preflight('distillation');

  const outputFile = path.join(LENS_DIR, 'TRACE.txt');
  const anonymized = scope?.meta?.anonymize === true;
  const enabledSources = Array.isArray(scope?.distillation?.sources)
    ? new Set(
      scope.distillation.sources
        .filter(s => typeof s === 'string')
        .map(s => s.trim().toLowerCase())
    )
    : new Set(DEFAULT_SOURCES);

  const homeDir = HOME_DIR || '';
  const now = Date.now();
  const subjectNames = getSubjectNameTokens();
  const automationMeta = collectAutomationMetadata(homeDir);

  const rawMessages = [
    ...(enabledSources.has('antigravity') ? await collectAntigravityMessages(homeDir, now, subjectNames, automationMeta, anonymized) : []),
    ...(enabledSources.has('openclaw') ? await collectOpenClawMessages(homeDir, now, subjectNames, automationMeta.automatedPrompts, anonymized) : []),
    ...(enabledSources.has('claude') ? collectClaudeCodeMessages(homeDir, now, subjectNames, automationMeta.automatedPrompts, anonymized) : []),
    ...(enabledSources.has('codex') ? collectCodexMessages(homeDir, now, subjectNames, automationMeta.automatedPrompts, anonymized) : [])
  ];

  rawMessages.sort((a, b) => a.timestamp - b.timestamp);

  const seen = new Set();
  const userMessages = rawMessages.filter(m => {
    if (seen.has(m.text)) return false;
    seen.add(m.text);
    return true;
  });

  if (userMessages.length === 0) {
    try {
      fs.writeFileSync(outputFile, '', 'utf8');
    } catch (e) {
      checkAccess(e);
      throw e;
    }
    console.log('TRACE_EMPTY');
    return;
  }

  const formattedOutput = userMessages.map(m => m.text).join('\n---\n');
  try {
    fs.writeFileSync(outputFile, formattedOutput + '\n', 'utf8');
  } catch (e) {
    checkAccess(e);
    throw e;
  }
  console.log('DISTILLATION_READY');
}

if (process.argv.includes('--commit')) {
  commitLensRepo();
} else {
  distillation();
}
