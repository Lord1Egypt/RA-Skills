#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

const DEFAULT_SESSIONS_DIR = path.join(os.homedir(), '.openclaw', 'agents', 'main', 'sessions');
const DEFAULT_HOURS = 6;
const DEFAULT_MAX_FILES = 120;
const DEFAULT_TASKS_PATH = process.env.BLOCKER_TASKS_PATH
  || path.join(os.homedir(), 'Tasks.md');
const DEFAULT_JOURNAL_DIR = process.env.BLOCKER_JOURNAL_DIR
  || path.join(os.homedir(), 'Journal');

const BLOCKER_SIGNAL_RE = /\b(blocker|blocked|needs\s+andrew|needs-?you|need\s+andrew|awaiting\s+andrew|PILOT_BLOCKED_MISSING|requires\s+andrew)\b/i;
const EXPLICIT_NONE_RE = /\b(blocked|blocker|needs\s+you|needs\s+andrew)\b[^\n]{0,24}\bnone\b/i;
const BLOCKER_ID_RE = /BLOCKER_ID\s*:\s*([A-Za-z0-9._:-]+)/gi;
const ABS_MD_PATH_RE = /\/Users\/[^\n`)]*?\.md/g;

function printHelp() {
  console.log(`check-subagent-blocker-routing.js

Usage:
  node scripts/check-subagent-blocker-routing.js [options]

Options:
  --json                  Print JSON output
  --sessions-dir <path>   Sessions directory (default: ${DEFAULT_SESSIONS_DIR})
  --hours <n>             Lookback window in hours (default: ${DEFAULT_HOURS})
  --max-files <n>         Max session files to scan (default: ${DEFAULT_MAX_FILES})
  --all-files             Ignore lookback and scan all session files
  --tasks-path <path>     Tasks.md path (default: ${DEFAULT_TASKS_PATH})
  --journal-dir <path>    Journal directory (default: ${DEFAULT_JOURNAL_DIR})
  -h, --help              Show help

Exit codes:
  0 = compliant (or no blocker-bearing subagent completion messages found)
  1 = one or more blocker-bearing completion messages missing/verifying routing evidence
`);
}

function parseArgs(argv) {
  const args = {
    sessionsDir: DEFAULT_SESSIONS_DIR,
    hours: DEFAULT_HOURS,
    maxFiles: DEFAULT_MAX_FILES,
    allFiles: false,
    json: false,
    tasksPath: DEFAULT_TASKS_PATH,
    journalDir: DEFAULT_JOURNAL_DIR,
  };

  for (let i = 2; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === '--json') {
      args.json = true;
    } else if (token === '--all-files') {
      args.allFiles = true;
    } else if (token === '--sessions-dir') {
      args.sessionsDir = String(argv[i + 1] || '').trim();
      i += 1;
    } else if (token === '--hours') {
      const n = Number(argv[i + 1]);
      if (!Number.isFinite(n) || n <= 0) throw new Error('--hours must be a positive number');
      args.hours = n;
      i += 1;
    } else if (token === '--max-files') {
      const n = Number(argv[i + 1]);
      if (!Number.isFinite(n) || n <= 0) throw new Error('--max-files must be a positive number');
      args.maxFiles = Math.floor(n);
      i += 1;
    } else if (token === '--tasks-path') {
      args.tasksPath = String(argv[i + 1] || '').trim();
      i += 1;
    } else if (token === '--journal-dir') {
      args.journalDir = String(argv[i + 1] || '').trim();
      i += 1;
    } else if (token === '-h' || token === '--help') {
      printHelp();
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${token}`);
    }
  }

  return args;
}

function isJsonlSessionFile(name) {
  if (!name.endsWith('.jsonl')) return false;
  if (name === 'sessions.jsonl') return false;
  if (name.endsWith('.lock')) return false;
  return true;
}

function listSessionFiles({ sessionsDir, hours, maxFiles, allFiles }) {
  if (!sessionsDir || !fs.existsSync(sessionsDir)) return [];
  const cutoffMs = Date.now() - hours * 60 * 60 * 1000;

  return fs
    .readdirSync(sessionsDir, { withFileTypes: true })
    .filter((entry) => entry.isFile() && isJsonlSessionFile(entry.name))
    .map((entry) => {
      const filePath = path.join(sessionsDir, entry.name);
      const stats = fs.statSync(filePath);
      return { filePath, mtimeMs: stats.mtimeMs };
    })
    .filter((item) => allFiles || item.mtimeMs >= cutoffMs)
    .sort((a, b) => b.mtimeMs - a.mtimeMs)
    .slice(0, maxFiles)
    .map((item) => item.filePath);
}

function extractTextFromContent(contentArr) {
  if (!Array.isArray(contentArr)) return '';
  const parts = [];
  for (const part of contentArr) {
    if (part && part.type === 'text' && typeof part.text === 'string') {
      parts.push(part.text);
    }
  }
  return parts.join('\n').trim();
}

function todayEtDateString() {
  const parts = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'America/New_York',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).formatToParts(new Date());

  const map = Object.fromEntries(parts.map((p) => [p.type, p.value]));
  return `${map.year}-${map.month}-${map.day}`;
}

function basenameLooksLikeProjectBoard(filePath) {
  const base = path.basename(String(filePath || '')).toLowerCase();
  return base.includes('project board');
}

function basenameLooksLikeLivePlan(filePath) {
  const base = path.basename(String(filePath || '')).toLowerCase();
  return base.includes('live plan');
}

function normalizePathCandidates(rawText) {
  const raw = String(rawText || '');
  const matches = raw.match(ABS_MD_PATH_RE) || [];
  const unique = [...new Set(matches.map((v) => v.trim()))];
  return unique;
}

function extractBlockerIds(text) {
  const out = [];
  let m;
  while ((m = BLOCKER_ID_RE.exec(text)) !== null) {
    out.push(String(m[1] || '').trim());
  }
  return [...new Set(out.filter(Boolean))];
}

function hasBlockerSignal(text) {
  const t = String(text || '');
  if (!BLOCKER_SIGNAL_RE.test(t)) return false;
  if (EXPLICIT_NONE_RE.test(t)) return false;
  return true;
}

function readFileSafe(filePath) {
  try {
    return fs.readFileSync(filePath, 'utf8');
  } catch {
    return '';
  }
}

function classifyArtifactPaths(text, opts = {}) {
  const paths = normalizePathCandidates(text);
  const tasksPath = opts.tasksPath || DEFAULT_TASKS_PATH;
  const journalTodayPath = path.join(opts.journalDir || DEFAULT_JOURNAL_DIR, `${todayEtDateString()}.md`);

  const boardPaths = paths.filter((p) => basenameLooksLikeProjectBoard(p));
  const planPaths = paths.filter((p) => basenameLooksLikeLivePlan(p));
  const explicitTasks = paths.filter((p) => path.basename(p).toLowerCase() === 'tasks.md');
  const explicitJournal = paths.filter((p) => p.includes('/Journal/') || /\/Journal\/.+\.md$/i.test(p));

  const result = {
    boardPaths,
    planPaths,
    tasksPath: explicitTasks[0] || (text.includes('Tasks.md') ? tasksPath : ''),
    journalPath: explicitJournal[0] || (text.includes('Journal/') || text.includes('journal') ? journalTodayPath : ''),
  };

  return result;
}

function recordViolation(violations, payload) {
  violations.push({
    filePath: payload.filePath,
    line: payload.line,
    timestamp: payload.timestamp || null,
    reason: payload.reason,
    details: payload.details || '',
    snippet: String(payload.snippet || '').replace(/\s+/g, ' ').slice(0, 220),
  });
}

function scanSessionFile(filePath, state, options) {
  const text = readFileSafe(filePath);
  const lines = text.split('\n');
  const cutoffMs = options.allFiles ? null : Date.now() - options.hours * 60 * 60 * 1000;

  for (let idx = 0; idx < lines.length; idx += 1) {
    const line = lines[idx];
    if (!line || !line.trim()) continue;

    let record;
    try {
      record = JSON.parse(line);
    } catch {
      state.parseErrors += 1;
      continue;
    }

    if (record.type !== 'message') continue;
    if (record.message?.role !== 'assistant') continue;

    const tsMs = Date.parse(record.timestamp || '');
    if (cutoffMs !== null && Number.isFinite(tsMs) && tsMs < cutoffMs) continue;

    const assistantText = extractTextFromContent(record.message?.content || []);
    if (!assistantText) continue;
    if (!assistantText.includes('✅ Subagent main finished')) continue;

    state.completionMessages += 1;

    if (!hasBlockerSignal(assistantText)) continue;
    state.blockerCompletionMessages += 1;

    const ids = extractBlockerIds(assistantText);
    const artifacts = classifyArtifactPaths(assistantText, options);

    if (ids.length === 0) {
      recordViolation(state.violations, {
        filePath,
        line: idx + 1,
        timestamp: record.timestamp,
        reason: 'missing-blocker-id',
        details: 'Blocker signal found but no BLOCKER_ID token in completion output.',
        snippet: assistantText,
      });
      continue;
    }

    if (artifacts.boardPaths.length === 0) {
      recordViolation(state.violations, {
        filePath,
        line: idx + 1,
        timestamp: record.timestamp,
        reason: 'missing-board-path',
        details: 'Blocker signal found but no Project Board path in completion output.',
        snippet: assistantText,
      });
      continue;
    }

    // Plan path is optional since plans can be chat-only (CR-002 chat-first policy)
    // Only warn, don't fail, if no plan path found
    if (artifacts.planPaths.length === 0) {
      // Log warning but don't record as violation - plans may be chat-only
      if (process.env.VERBOSE) {
        console.warn(`[WARN] No plan path found for blocker at ${filePath}:${idx + 1} - may be chat-only plan`);
      }
      // Continue checking other artifacts instead of skipping
    }

    if (!artifacts.tasksPath) {
      recordViolation(state.violations, {
        filePath,
        line: idx + 1,
        timestamp: record.timestamp,
        reason: 'missing-tasks-path',
        details: 'Blocker signal found but no Tasks path evidence in completion output.',
        snippet: assistantText,
      });
      continue;
    }

    if (!artifacts.journalPath) {
      recordViolation(state.violations, {
        filePath,
        line: idx + 1,
        timestamp: record.timestamp,
        reason: 'missing-journal-path',
        details: 'Blocker signal found but no Journal path evidence in completion output.',
        snippet: assistantText,
      });
      continue;
    }

    const filesToCheck = [
      ...artifacts.boardPaths,
      ...artifacts.planPaths,
      artifacts.tasksPath,
      artifacts.journalPath,
    ];

    for (const artifactPath of filesToCheck) {
      if (!artifactPath || !fs.existsSync(artifactPath)) {
        recordViolation(state.violations, {
          filePath,
          line: idx + 1,
          timestamp: record.timestamp,
          reason: 'missing-artifact-file',
          details: `Referenced artifact not found: ${artifactPath || '(empty path)'}`,
          snippet: assistantText,
        });
        continue;
      }

      const artifactText = readFileSafe(artifactPath);
      for (const blockerId of ids) {
        if (!artifactText.includes(blockerId)) {
          recordViolation(state.violations, {
            filePath,
            line: idx + 1,
            timestamp: record.timestamp,
            reason: 'blocker-id-not-found-in-artifact',
            details: `BLOCKER_ID ${blockerId} not found in ${artifactPath}`,
            snippet: assistantText,
          });
        }
      }
    }
  }
}

function buildTextMessage(report) {
  if (report.ok) {
    if (report.blockerCompletionMessages === 0) {
      return `BLOCKER ROUTING LINT OK — no blocker-bearing subagent completion messages found (scanned ${report.scannedFiles} file(s)).`;
    }

    return `BLOCKER ROUTING LINT OK — ${report.blockerCompletionMessages} blocker-bearing completion message(s) passed routing evidence checks (scanned ${report.scannedFiles} file(s)).`;
  }

  const lines = [];
  lines.push(
    `BLOCKER ROUTING LINT FAIL — ${report.violationsCount} issue(s) across ${report.blockerCompletionMessages} blocker-bearing completion message(s) (scanned ${report.scannedFiles} file(s)).`
  );
  lines.push('Runbook: node scripts/check-subagent-blocker-routing.js --hours 6 --json');

  const max = 10;
  for (const v of report.violations.slice(0, max)) {
    const file = path.basename(String(v.filePath || 'unknown'));
    lines.push(`- ${file}:${v.line} ${v.reason} ${v.details || ''}`.trim());
  }

  if (report.violations.length > max) {
    lines.push(`- … ${report.violations.length - max} more violation(s)`);
  }

  return lines.join('\n');
}

function run(options = {}) {
  const args = {
    sessionsDir: String(options.sessionsDir || DEFAULT_SESSIONS_DIR),
    hours: Number.isFinite(options.hours) && options.hours > 0 ? Number(options.hours) : DEFAULT_HOURS,
    maxFiles: Number.isFinite(options.maxFiles) && options.maxFiles > 0 ? Math.floor(options.maxFiles) : DEFAULT_MAX_FILES,
    allFiles: Boolean(options.allFiles),
    tasksPath: String(options.tasksPath || DEFAULT_TASKS_PATH),
    journalDir: String(options.journalDir || DEFAULT_JOURNAL_DIR),
  };

  const files = listSessionFiles(args);
  const state = {
    completionMessages: 0,
    blockerCompletionMessages: 0,
    parseErrors: 0,
    violations: [],
  };

  for (const filePath of files) {
    scanSessionFile(filePath, state, args);
  }

  const report = {
    ok: state.violations.length === 0,
    sessionsDir: args.sessionsDir,
    lookbackHours: args.allFiles ? null : args.hours,
    scannedFiles: files.length,
    maxFiles: args.maxFiles,
    completionMessages: state.completionMessages,
    blockerCompletionMessages: state.blockerCompletionMessages,
    violationsCount: state.violations.length,
    parseErrors: state.parseErrors,
    violations: state.violations,
    generatedAt: new Date().toISOString(),
  };

  report.message = buildTextMessage(report);
  return report;
}

function main() {
  const args = parseArgs(process.argv);
  const report = run(args);

  if (args.json) {
    console.log(JSON.stringify(report, null, 2));
  } else {
    console.log(report.message);
  }

  process.exit(report.ok ? 0 : 1);
}

if (require.main === module) {
  try {
    main();
  } catch (error) {
    console.error(`check-subagent-blocker-routing.js error: ${error.message}`);
    process.exit(1);
  }
}

module.exports = {
  run,
  parseArgs,
};
