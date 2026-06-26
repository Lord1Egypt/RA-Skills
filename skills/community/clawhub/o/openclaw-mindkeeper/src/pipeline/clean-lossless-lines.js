import { unique } from "../utils/text.js";

const HARD_DROP_PATTERNS = [
  /toolCall/i,
  /partialJson/i,
  /thinkingSignature/i,
  /encrypted_content/i,
  /type\s*[:=]\s*"?thinking"?/i,
  /type\s*[:=]\s*"?toolCall"?/i,
  /Command exited with code/i,
  /^TAP version /i,
  /^# Subtest:/i,
  /^(ok|not ok)\s+\d+\s+-/i,
  /^Created:\s+\//,
  /^Modified:\s+\//,
  /^Deleted:\s+\//,
  /^Renamed:\s+\//,
  /^Files?:\s*$/i,
  /^Commits? made:/i,
  /^Commit created/i,
  /^\[\{.*type.*thinking/i,
  /^\[\{.*type.*toolCall/i,
  /^\{\s*$/,
  /^\}\s*$/,
  /^\[\s*$/,
  /^\]\s*$/,
  /\/home\/adminul\//i,
  /^AAMkAD/i,
  /^https?:\/\/github\.com\//i,
  /tests\//i,
  /tasks\/todo\.md/i,
  /yieldMs/i,
  /timeout/i,
  /session key/i,
  /session id/i,
  /sender \(untrusted metadata\)/i,
  /email RFC822 builder/i,
  /Current state:/i,
];

const SOFT_DROP_PATTERNS = [
  /^Created tracked:/i,
  /^Modified tracked:/i,
  /^Repo had untracked/i,
  /^Branch active before merge:/i,
  /^PR URL/i,
  /^status note:/i,
  /^Small follow-up patch/i,
  /^exists, later modified/i,
  /^diagnostics:/i,
  /^preview:/i,
  /^has_attachments:/i,
  /^attachments:/i,
  /^folder:/i,
  /^It then committed/i,
  /^Created:/i,
  /^Modified:/i,
  /^Deleted:/i,
  /^Renamed:/i,
  /^src\//i,
  /^openclaw-mindkeeper\//i,
  /^\/home\//i,
  /^chosen focus terms/i,
  /^Final user request/i,
  /^User complained/i,
  /^Assistant acknowledged/i,
  /^plan:/i,
  /^next turn likely/i,
  /^email content highlighted/i,
  /^Branding \/ product consistency preference:/i,
  /^Final accepted digest direction:/i,
  /^că digestul GitHub final acceptat/i,
  /^Assistant /i,
  /^User /i,
  /^earlier memory commit /i,
  /^Expand for details about:/i,
  /^existing .*tests all still pass/i,
  /^In nexlink repo, assistant inspected/i,
  /^After user requested implementing live send/i,
  /^Decision: integrate Mindkeeper with NexLink by invoking that CLI/i,
  /^now supports mode /i,
  /^expanded to cover /i,
  /^expanded with /i,
  /^updated examples\/docs /i,
  /^updated .*docs /i,
  /^sendEmail can invoke /i,
  /^[0-9a-f]{7,}\s+—\s+/i,
  /^[0-9a-f]{7,}\s+(feat|fix|chore|docs|test|refactor|perf|ci)\(/i,
  /^PR metadata before merge:/i,
  /^new\s+scripts\//i,
  /^python3\s+scripts\//i,
  /^node\s+src\//i,
  /fake CLI script/i,
  /execFile-ing python3/i,
  /^CLI can /i,
];

function looksLikeCodeVomiting(line) {
  const trimmed = line.trim();
  if (trimmed.length === 0) return true;
  if (trimmed.length > 320) return true;
  if ((trimmed.match(/[{}\[\]]/g) ?? []).length >= 6) return true;
  if ((trimmed.match(/\//g) ?? []).length >= 4) return true;
  if ((trimmed.match(/"/g) ?? []).length >= 6) return true;
  if ((trimmed.match(/:/g) ?? []).length >= 6) return true;
  return false;
}

function normalizeBulletNoise(line) {
  return line
    .replace(/^[-*]\s+/, "")
    .replace(/^\s*[-*]\s+/, "")
    .replace(/^\d+\.\s+/, "")
    .trim();
}

export function cleanLosslessLines(lines) {
  return unique(
    lines
      .map((line) => normalizeBulletNoise(String(line ?? "")))
      .filter(Boolean)
      .filter((line) => !HARD_DROP_PATTERNS.some((pattern) => pattern.test(line)))
      .filter((line) => !SOFT_DROP_PATTERNS.some((pattern) => pattern.test(line)))
      .filter((line) => !looksLikeCodeVomiting(line)),
  );
}
