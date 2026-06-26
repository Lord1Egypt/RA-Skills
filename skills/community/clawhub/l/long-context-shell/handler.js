const fs = require("node:fs");
const path = require("node:path");
const os = require("node:os");
const crypto = require("node:crypto");
const { spawn, execSync } = require("node:child_process");

const BASE_DIR = path.join(os.tmpdir(), "trae-long-context-shell");
const LOG_DIR = path.join(BASE_DIR, "logs");
const SESSION_DIR = path.join(BASE_DIR, "sessions");
const EXIT_MARKER = "__LONG_CONTEXT_SHELL_EXIT_CODE__=";
const DEFAULT_HEAD_LINES = 12;
const DEFAULT_TAIL_LINES = 24;
const DEFAULT_WAIT_MS = 1200;
const DEFAULT_BACKGROUND_WAIT_MS = 400;
const DEFAULT_SCAN_PATTERNS = [
  "fatal",
  "panic",
  "exception",
  "traceback",
  "segmentation fault",
  "permission denied",
  "enoent",
  "error",
  "failed",
  "timeout",
  "killed",
  "warn"
];

function ensureRuntimeDirs() {
  fs.mkdirSync(LOG_DIR, { recursive: true });
  fs.mkdirSync(SESSION_DIR, { recursive: true });
}

function clampNumber(value, fallback, min, max) {
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) {
    return fallback;
  }
  return Math.min(max, Math.max(min, Math.floor(parsed)));
}

function nowIso() {
  return new Date().toISOString();
}

function makeSessionId() {
  return typeof crypto.randomUUID === "function"
    ? crypto.randomUUID()
    : crypto.randomBytes(16).toString("hex");
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function stripAnsi(text) {
  return String(text).replace(/\u001b\[[0-9;?]*[ -/]*[@-~]/g, "");
}

function sanitizeSegment(text) {
  return String(text)
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 48) || "command";
}

function getSessionFilePath(sessionId) {
  return path.join(SESSION_DIR, `${sessionId}.json`);
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function writeJson(filePath, value) {
  fs.writeFileSync(filePath, JSON.stringify(value, null, 2));
}

function readSession(sessionId) {
  const filePath = getSessionFilePath(sessionId);
  if (!fs.existsSync(filePath)) {
    throw new Error(`Unknown sessionId: ${sessionId}`);
  }
  return readJson(filePath);
}

function saveSession(session) {
  writeJson(getSessionFilePath(session.sessionId), session);
}

function appendLogLine(logPath, streamName, line) {
  const clean = stripAnsi(line).replace(/\r/g, "");
  fs.appendFileSync(logPath, `[${nowIso()}] [${streamName}] ${clean}\n`);
}

function createLineCollector(logPath, streamName) {
  let buffer = "";
  return {
    push(chunk) {
      buffer += chunk.toString("utf8");
      const parts = buffer.split(/\r?\n/);
      buffer = parts.pop();
      for (const line of parts) {
        appendLogLine(logPath, streamName, line);
      }
    },
    flush() {
      if (buffer.length > 0) {
        appendLogLine(logPath, streamName, buffer);
        buffer = "";
      }
    }
  };
}

function looksContinuousCommand(command) {
  return /\b(watch|top|tail\s+-f|ping\b|docker\s+logs\s+-f|Get-Content\b.*-Wait)\b/i.test(command);
}

function resolveBackgroundMode(command, input) {
  if (typeof input.background === "boolean") {
    return input.background;
  }
  return looksContinuousCommand(command);
}

function resolveWaitMs(input, background) {
  const fallback = background ? DEFAULT_BACKGROUND_WAIT_MS : DEFAULT_WAIT_MS;
  return clampNumber(input.waitMs, fallback, 0, 15000);
}

function isDangerousCommand(command) {
  const patterns = [
    /\bsudo\b/i,
    /\brm\s+-rf\b/i,
    /\bdel\s+\/[a-z]*\s*\*\b/i,
    /\bformat\b/i,
    /\bmkfs\b/i,
    /\bdd\b/i,
    /\breboot\b/i,
    /\bshutdown\b/i,
    /\bhalt\b/i,
    /\bpoweroff\b/i
  ];
  return patterns.some(pattern => pattern.test(command));
}

function chooseShell(command) {
  if (process.platform === "win32") {
    return {
      file: "powershell.exe",
      args: ["-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command]
    };
  }
  return {
    file: "/bin/sh",
    args: ["-lc", command]
  };
}

function isProcessRunning(pid) {
  if (!pid || typeof pid !== "number") {
    return false;
  }
  try {
    if (process.platform === "win32") {
      execSync(`powershell.exe -NoProfile -Command "Get-Process -Id ${pid} | Out-Null"`, {
        stdio: "ignore"
      });
      return true;
    }
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
}

function terminateProcessTree(pid) {
  if (!pid || typeof pid !== "number") {
    return false;
  }
  try {
    if (process.platform === "win32") {
      execSync(`taskkill /PID ${pid} /T /F`, { stdio: "ignore" });
    } else {
      try {
        process.kill(-pid, "SIGTERM");
      } catch {
        process.kill(pid, "SIGTERM");
      }
    }
    return true;
  } catch {
    return false;
  }
}

function readLines(logPath) {
  if (!logPath || !fs.existsSync(logPath)) {
    return [];
  }
  const text = stripAnsi(fs.readFileSync(logPath, "utf8"));
  const lines = text.split(/\r?\n/);
  if (lines.length > 0 && lines[lines.length - 1] === "") {
    lines.pop();
  }
  return lines;
}

function extractExitCode(lines) {
  for (let index = lines.length - 1; index >= 0; index -= 1) {
    const match = lines[index].match(/__LONG_CONTEXT_SHELL_EXIT_CODE__=(\d+)/);
    if (match) {
      return Number(match[1]);
    }
  }
  return null;
}

function visibleLines(lines) {
  return lines.filter(line => !line.includes(EXIT_MARKER));
}

function getLogStreamName(line) {
  const match = String(line).match(/^\[[^\]]+\]\s+\[([^\]]+)\]/);
  return match ? match[1] : null;
}

function buildPreview(lines, headLines, tailLines) {
  if (lines.length === 0) {
    return {
      truncated: false,
      head: [],
      tail: [],
      text: ""
    };
  }

  if (lines.length <= headLines + tailLines) {
    return {
      truncated: false,
      head: lines,
      tail: [],
      text: lines.join("\n")
    };
  }

  const head = lines.slice(0, headLines);
  const tail = lines.slice(-tailLines);
  const omitted = lines.length - head.length - tail.length;

  return {
    truncated: true,
    head,
    tail,
    text: `${head.join("\n")}\n... [omitted ${omitted} lines, inspect the log file for details] ...\n${tail.join("\n")}`
  };
}

function getLogStats(logPath, options = {}) {
  const headLines = clampNumber(options.headLines, DEFAULT_HEAD_LINES, 1, 80);
  const tailLines = clampNumber(options.tailLines, DEFAULT_TAIL_LINES, 1, 120);
  const lines = readLines(logPath);
  const visible = visibleLines(lines);
  const exitCode = extractExitCode(lines);
  const stat = fs.existsSync(logPath) ? fs.statSync(logPath) : null;
  const preview = buildPreview(visible, headLines, tailLines);
  const timeQuery = typeof options.timeQuery === "string" && options.timeQuery.trim() ? options.timeQuery.trim() : "";
  const timeMatches = timeQuery ? visible.filter(line => line.includes(timeQuery)).slice(-tailLines) : [];

  return {
    bytes: stat ? stat.size : 0,
    lineCount: visible.length,
    updatedAt: stat ? stat.mtime.toISOString() : null,
    exitCode,
    preview,
    timeQuery,
    timeMatches
  };
}

function resolveSessionLike(input) {
  if (input && typeof input.sessionId === "string" && input.sessionId.trim()) {
    return readSession(input.sessionId.trim());
  }
  if (input && typeof input.logPath === "string" && input.logPath.trim()) {
    return {
      sessionId: null,
      command: null,
      commandPid: null,
      workerPid: null,
      status: "unknown",
      startedAt: null,
      endedAt: null,
      logPath: input.logPath.trim()
    };
  }
  throw new Error("sessionId or logPath is required");
}

function deriveStatus(session, stats) {
  if (session.status === "stopped") {
    return "stopped";
  }
  if (typeof stats.exitCode === "number") {
    return stats.exitCode === 0 ? "success" : "failed";
  }
  if (isProcessRunning(session.commandPid) || isProcessRunning(session.workerPid)) {
    return "running";
  }
  return session.status === "running" ? "finished" : session.status || "unknown";
}

function buildRecommendation(status, stats) {
  if (status === "running") {
    return "Use long_context_shell_peek with the same sessionId to monitor the latest state. Stop the session when observation is no longer needed.";
  }
  if (status === "failed") {
    return "Use long_context_shell_scan with the same sessionId to locate likely failure lines.";
  }
  if (status === "stopped") {
    return "The session was stopped. Re-run the command if you need a fresh capture.";
  }
  if (stats.preview.truncated) {
    return "The preview is truncated. Inspect the log file or run long_context_shell_scan for targeted analysis.";
  }
  return "No further action is required unless you need deeper inspection.";
}

function buildStatusCard(session, options = {}) {
  const stats = getLogStats(session.logPath, options);
  const status = deriveStatus(session, stats);

  return {
    sessionId: session.sessionId,
    command: session.command,
    background: Boolean(session.background),
    status,
    exitCode: stats.exitCode,
    startedAt: session.startedAt,
    endedAt: session.endedAt || null,
    logPath: session.logPath,
    bytes: stats.bytes,
    lineCount: stats.lineCount,
    updatedAt: stats.updatedAt,
    truncated: stats.preview.truncated,
    preview: stats.preview.text,
    timeQuery: stats.timeQuery || null,
    timeMatches: stats.timeMatches,
    recommendation: buildRecommendation(status, stats)
  };
}

function toRegex(pattern) {
  if (pattern instanceof RegExp) {
    return pattern;
  }
  if (typeof pattern !== "string" || !pattern.trim()) {
    return null;
  }
  try {
    return new RegExp(pattern, "i");
  } catch {
    return new RegExp(pattern.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"), "i");
  }
}

function scorePattern(pattern) {
  const text = pattern.toLowerCase();
  if (text.includes("fatal")) {
    return 100;
  }
  if (text.includes("exception")) {
    return 90;
  }
  if (text.includes("error")) {
    return 80;
  }
  if (text.includes("failed")) {
    return 70;
  }
  if (text.includes("timeout")) {
    return 60;
  }
  if (text.includes("killed")) {
    return 55;
  }
  if (text.includes("warn")) {
    return 40;
  }
  return 20;
}

function scoreToSeverity(score) {
  if (score >= 90) {
    return "critical";
  }
  if (score >= 70) {
    return "high";
  }
  if (score >= 50) {
    return "medium";
  }
  return "low";
}

async function long_context_shell_run(input = {}) {
  ensureRuntimeDirs();

  const command = typeof input.command === "string" ? input.command.trim() : "";
  if (!command) {
    return { error: "command is required" };
  }

  if (isDangerousCommand(command)) {
    return {
      error: "dangerous_command",
      message: `Command looks dangerous. Ask the user for explicit approval before running: ${command}`
    };
  }

  const sessionId = makeSessionId();
  const startedAt = nowIso();
  const background = resolveBackgroundMode(command, input);
  const waitMs = resolveWaitMs(input, background);
  const commandSlug = sanitizeSegment(command.split(/\s+/).slice(0, 3).join("-"));
  const logPath = path.join(LOG_DIR, `${startedAt.replace(/[:.]/g, "-")}-${commandSlug}-${sessionId.slice(0, 8)}.log`);

  const session = {
    sessionId,
    command,
    startedAt,
    endedAt: null,
    status: "running",
    logPath,
    background,
    workerPid: null,
    commandPid: null
  };

  saveSession(session);

  const worker = spawn(process.execPath, [__filename, "__worker__", getSessionFilePath(sessionId)], {
    detached: true,
    windowsHide: true,
    stdio: "ignore"
  });

  session.workerPid = worker.pid;
  saveSession(session);
  worker.unref();

  if (waitMs > 0) {
    await sleep(waitMs);
  }

  return buildStatusCard(readSession(sessionId), input);
}

async function long_context_shell_peek(input = {}) {
  const session = resolveSessionLike(input);
  return buildStatusCard(session, input);
}

async function long_context_shell_scan(input = {}) {
  const session = resolveSessionLike(input);
  const contextLines = clampNumber(input.contextLines, 2, 0, 8);
  const limit = clampNumber(input.limit, 8, 1, 20);
  const patterns = Array.isArray(input.patterns) && input.patterns.length > 0
    ? input.patterns
    : DEFAULT_SCAN_PATTERNS;
  const regexes = patterns.map(toRegex).filter(Boolean);
  const lines = visibleLines(readLines(session.logPath));
  const matches = [];

  for (let index = 0; index < lines.length; index += 1) {
    const line = lines[index];
    const streamName = getLogStreamName(line);
    if (streamName && !["stdout", "stderr"].includes(streamName)) {
      continue;
    }
    let matchedPattern = null;
    let matchedScore = -1;

    for (let regexIndex = 0; regexIndex < regexes.length; regexIndex += 1) {
      if (!regexes[regexIndex].test(line)) {
        continue;
      }
      const score = scorePattern(patterns[regexIndex]);
      if (score > matchedScore) {
        matchedPattern = patterns[regexIndex];
        matchedScore = score;
      }
    }

    if (!matchedPattern) {
      continue;
    }

    if (matches.length > 0 && index + 1 - matches[matches.length - 1].lineNumber <= contextLines) {
      if (matches[matches.length - 1].score >= matchedScore) {
        continue;
      }
      matches.pop();
    }

    matches.push({
      lineNumber: index + 1,
      pattern: matchedPattern,
      score: matchedScore,
      severity: scoreToSeverity(matchedScore),
      line,
      context: lines.slice(Math.max(0, index - contextLines), Math.min(lines.length, index + contextLines + 1))
    });

    if (matches.length >= limit) {
      break;
    }
  }

  matches.sort((left, right) => right.score - left.score || left.lineNumber - right.lineNumber);
  const severityCounts = matches.reduce((result, match) => {
    result[match.severity] = (result[match.severity] || 0) + 1;
    return result;
  }, {});

  const statusCard = buildStatusCard(session, input);

  return {
    sessionId: session.sessionId,
    logPath: session.logPath,
    status: statusCard.status,
    exitCode: statusCard.exitCode,
    matchedCount: matches.length,
    severityCounts,
    patterns,
    matches: matches.map(({ score, ...rest }) => rest),
    recommendation: matches.length > 0
      ? "Review the highest-severity matches first."
      : "No configured patterns matched. Use long_context_shell_peek or inspect the log file directly if needed."
  };
}

async function long_context_shell_stop(input = {}) {
  if (!input || typeof input.sessionId !== "string" || !input.sessionId.trim()) {
    return { error: "sessionId is required" };
  }

  const session = readSession(input.sessionId.trim());
  const stopped = terminateProcessTree(session.commandPid)
    || (!session.commandPid && terminateProcessTree(session.workerPid));

  if (!stopped) {
    session.status = "stopped";
    session.endedAt = session.endedAt || nowIso();
    saveSession(session);
    return buildStatusCard(session, input);
  }

  session.status = "stopped";
  session.endedAt = session.endedAt || nowIso();
  saveSession(session);
  appendLogLine(session.logPath, "meta", "session stopped by user request");

  return buildStatusCard(session, input);
}

async function runWorker(sessionFilePath) {
  ensureRuntimeDirs();
  const session = readJson(sessionFilePath);
  const shell = chooseShell(session.command);
  const child = spawn(shell.file, shell.args, {
    detached: process.platform !== "win32",
    windowsHide: true,
    stdio: ["ignore", "pipe", "pipe"]
  });

  session.workerPid = process.pid;
  session.commandPid = child.pid;
  session.status = "running";
  saveSession(session);

  appendLogLine(session.logPath, "meta", `session_id=${session.sessionId}`);
  appendLogLine(session.logPath, "meta", `command=${session.command}`);
  appendLogLine(session.logPath, "meta", `worker_pid=${process.pid}`);
  appendLogLine(session.logPath, "meta", `command_pid=${child.pid}`);

  const stdoutCollector = createLineCollector(session.logPath, "stdout");
  const stderrCollector = createLineCollector(session.logPath, "stderr");

  child.stdout.on("data", chunk => stdoutCollector.push(chunk));
  child.stderr.on("data", chunk => stderrCollector.push(chunk));

  child.on("error", error => {
    appendLogLine(session.logPath, "stderr", error.message);
  });

  child.on("close", code => {
    stdoutCollector.flush();
    stderrCollector.flush();
    appendLogLine(session.logPath, "meta", `${EXIT_MARKER}${typeof code === "number" ? code : 1}`);
    const latest = readJson(sessionFilePath);
    latest.commandPid = null;
    latest.workerPid = null;
    latest.exitCode = typeof code === "number" ? code : 1;
    latest.endedAt = latest.endedAt || nowIso();
    if (latest.status !== "stopped") {
      latest.status = code === 0 ? "success" : "failed";
    }
    saveSession(latest);
    process.exit(0);
  });
}

if (require.main === module && process.argv[2] === "__worker__" && process.argv[3]) {
  runWorker(process.argv[3]).catch(error => {
    try {
      const session = readJson(process.argv[3]);
      appendLogLine(session.logPath, "stderr", error.stack || error.message);
      session.status = "failed";
      session.endedAt = nowIso();
      session.exitCode = 1;
      session.commandPid = null;
      session.workerPid = null;
      saveSession(session);
    } catch {}
    process.exit(1);
  });
}

module.exports = {
  long_context_shell_run,
  long_context_shell_peek,
  long_context_shell_scan,
  long_context_shell_stop
};
