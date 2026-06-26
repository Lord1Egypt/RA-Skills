import os from "node:os";
import path from "node:path";

const ALLOWED_FORMATS = new Set(["text", "html"]);
const ALLOWED_EMAIL_MODES = new Set(["file", "sendmail", "nexlink"]);
const ALLOWED_BRIEF_MODES = new Set(["hybrid", "lossless-only"]);

function defaultLcmPath() {
  return path.join(os.homedir(), ".openclaw", "lcm.db");
}

function defaultTitleForMode(briefMode) {
  if (briefMode === "lossless-only") {
    return "Mindkeeper Lossless-Only Brief";
  }

  return "Mindkeeper Hybrid Brief";
}

export function resolveConfig(argv = process.argv.slice(2)) {
  const args = new Map();

  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) continue;
    const key = token.slice(2);
    const value = argv[i + 1] && !argv[i + 1].startsWith("--") ? argv[++i] : true;
    args.set(key, value);
  }

  const format = String(args.get("format") ?? "text");
  if (!ALLOWED_FORMATS.has(format)) {
    throw new Error(`Unsupported --format value: ${format}. Use one of: text, html.`);
  }

  const useLcm = Boolean(args.get("use-lcm"));
  const focusTerms = args.get("focus")
    ? String(args.get("focus")).split(",").map((term) => term.trim()).filter(Boolean)
    : [];
  const emailMode = String(args.get("email-mode") ?? "file");
  const briefMode = String(args.get("brief-mode") ?? "hybrid");

  if (!ALLOWED_EMAIL_MODES.has(emailMode)) {
    throw new Error(`Unsupported --email-mode value: ${emailMode}. Use one of: file, sendmail, nexlink.`);
  }

  if (!ALLOWED_BRIEF_MODES.has(briefMode)) {
    throw new Error(`Unsupported --brief-mode value: ${briefMode}. Use one of: hybrid, lossless-only.`);
  }

  const titleExplicit = args.has("title");
  const title = String(args.get("title") ?? defaultTitleForMode(briefMode));

  return {
    date: String(args.get("date") ?? new Date().toISOString().slice(0, 10)),
    briefMode,
    comparePair: Boolean(args.get("compare-pair")),
    memoryFile: args.get("memory-file") ? String(args.get("memory-file")) : null,
    format,
    out: args.get("out") ? String(args.get("out")) : null,
    title,
    titleExplicit,
    focusTitle: titleExplicit ? title : "",
    prompt: args.get("prompt") ? String(args.get("prompt")) : "",
    focusTerms,
    email: {
      enabled: Boolean(args.get("email-to")),
      to: args.get("email-to") ? String(args.get("email-to")) : null,
      from: args.get("email-from") ? String(args.get("email-from")) : null,
      subject: args.get("email-subject") ? String(args.get("email-subject")) : null,
      mode: emailMode,
      out: args.get("email-out") ? String(args.get("email-out")) : null,
      sendmailPath: args.get("sendmail-path") ? String(args.get("sendmail-path")) : "sendmail",
      nexlinkCliPath: args.get("nexlink-cli") ? String(args.get("nexlink-cli")) : path.join(os.homedir(), ".openclaw", "skills", "nexlink", "scripts", "nexlink.py"),
      pythonBin: args.get("python-bin") ? String(args.get("python-bin")) : "python3",
    },
    lcm: {
      enabled: useLcm,
      dbPath: String(args.get("lcm-db") ?? defaultLcmPath()),
      sessionKey: args.get("session-key") ? String(args.get("session-key")) : null,
      includeTools: Boolean(args.get("include-tools")),
      includeSummaries: !args.has("no-summaries"),
      conversationLimit: Number(args.get("conversation-limit") ?? 3),
      rawConversationLimit: Number(args.get("raw-conversation-limit") ?? 1),
      messageTail: Number(args.get("message-tail") ?? 30),
      summaryLimit: Number(args.get("summary-limit") ?? 2),
      limit: Number(args.get("limit") ?? 500),
    },
  };
}
