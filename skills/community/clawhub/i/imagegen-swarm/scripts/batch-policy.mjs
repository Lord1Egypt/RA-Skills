// Decisions the batch queue makes before it starts an engine: quota, rate limits,
// tail stealing, paid-line eligibility, and which attempt to keep.
import { ATTEMPT_FAIL, ATTEMPT_IGNORED, ATTEMPT_WIN } from "./attempt-outcomes.mjs";

// 额度用完、没登录、没装：立刻停用。普通 429 / 限流先退避，连续这么多次才停用。
export const RATE_LIMIT_STRIKES = 3;
export const STEAL_FACTOR = 1.5;
const QUOTA_DOWN = /\bquota\b|\bcredits?\b|积分|余额|insufficient_quota|预算用完|budget used up|insufficient balance|usage limit|weekly limit|insufficient\s+(?:credits?|quota|balance|funds)|not enough\s+(?:credits?|quota|balance)|out of\s+(?:credits?|quota)/i;
const AUTH_DOWN = /please\s+sign\s+in|unauthori[sz]ed|\bnot logged[ -]?in\b|\blog[ -]?in\b|\bnot authenticated\b|\b(?:no|missing) credentials\b|authentication required|not_configured/i;
const COMPLIANCE_DOWN = /ComplianceConfirmation/i;
const PLAYWRIGHT_MISSING = /ModuleNotFoundError:\s*No module named ['"]playwright['"]|\bplaywright not found\b/i;
export const PLAYWRIGHT_BROWSER_FAILURE = /playwright_browser_missing|executable (?:doesn't|does not) exist|playwright install|\bspawn\b[^\r\n]{0,200}-88|browserType\.launch|failed to launch|chromium-\d+|error while loading shared libraries|cannot open shared object/i;
// 「not found / ENOENT」只认引擎本身没装。参考图或输出文件找不到不算整家引擎挂了。
const NOT_INSTALLED = /not[_\s-]?installed|找不到\s*lv|\b(?:agy|codex(?:\s+CLI|\s+path)?|grok|dreamina|lv|muse|playwright)\s+not found\b|\bnot found:\s*(?:agy|codex|grok|dreamina|lv|muse)\b|\bcommand not found\b|\bspawn\w*\b[^\n]{0,200}\bENOENT\b/i;
const RATE_LIMIT = /\b429\b|rate[\s-]?limit|too many requests|RESOURCE_EXHAUSTED/i;

export function failureText(report) {
  const reported = report?.reason ?? report?.error;
  const detail = reported == null ? "unknown error" : String(reported);
  if (report?.error_kind && !detail.includes(String(report.error_kind))) return detail + " (" + report.error_kind + ")";
  return detail;
}

export function engineSetupReason(text) {
  if (QUOTA_DOWN.test(text) || RATE_LIMIT.test(text) || COMPLIANCE_DOWN.test(text)) return null;
  if (PLAYWRIGHT_MISSING.test(text)) return "missing CLI or runtime (Playwright not found)";
  if (PLAYWRIGHT_BROWSER_FAILURE.test(text)) return "missing CLI or runtime (Playwright browser missing or broken)";
  if (NOT_INSTALLED.test(text)) return "missing CLI or runtime";
  if (AUTH_DOWN.test(text)) return "missing login or credentials";
  return null;
}

// 'down' 立刻停用；'rate_limit' 计入连续限流；'retry' 只是这一张失败。
export function classifyEngineError(reason) {
  const text = String(reason ?? "");
  if (QUOTA_DOWN.test(text) || AUTH_DOWN.test(text) || COMPLIANCE_DOWN.test(text) || NOT_INSTALLED.test(text) || PLAYWRIGHT_MISSING.test(text) || PLAYWRIGHT_BROWSER_FAILURE.test(text)) return "down";
  if (RATE_LIMIT.test(text)) return "rate_limit";
  return "retry";
}

export function applyEngineFailure(state, reason) {
  const strikes = state?.strikes ?? 0;
  const kind = classifyEngineError(reason);
  if (kind === "down") return { action: "down", strikes: 0, down: true };
  if (kind === "rate_limit") {
    const next = strikes + 1;
    if (next >= RATE_LIMIT_STRIKES) return { action: "down", strikes: next, down: true };
    return { action: "backoff", strikes: next, down: false, backoffSeconds: 2 ** next };
  }
  return { action: "retry", strikes: 0, down: false };
}

// 本批已完成耗时的中位数；还没有样本就用调用方给的起始估计。偶数个取靠后的那个，和原先下标算法一致。
export function medianSeconds(samples, fallback) {
  const seconds = [...samples].filter(n => n > 0).sort((a, b) => a - b);
  if (!seconds.length) return fallback;
  return seconds[Math.floor(seconds.length / 2)];
}

// 只有持有者已经超过自己通常耗时的 1.5 倍，才允许再开一份；已经有一份重复时不再开。
export function shouldSteal({ activeCount, holderTypical, holderElapsed }) {
  if (activeCount !== 1) return false;
  if (!(holderTypical > 0) || !(holderElapsed >= 0)) return false;
  return holderElapsed > holderTypical * STEAL_FACTOR;
}

// 付费线路只在没有一家订阅引擎接得了这张图时才接；清单点名要它的直接接
export function paidMayTake({ named, subscriptionCanTake }) {
  return named || !subscriptionCanTake;
}

// 再开一张付费图后，本批（含正在做的）和本月的估算花费都不能超过预算
export function paidBudgetLeft({ price, committed, budgetBatch, monthSpent, budgetMonth }) {
  const next = (committed + 1) * price;
  if (next > budgetBatch + 1e-9) return "本批 API 预算用完：上限 $" + (budgetBatch) + "，每张约 $" + (price) + "（budget used up）";
  if (monthSpent + next > budgetMonth + 1e-9) return "本月 API 预算用完：已花约 $" + (monthSpent) + "，上限 $" + (budgetMonth) + "（budget used up）";
  return null;
}

// 这一轮交回的图：generated 是引擎写出了文件的次数，kept 是收成正式文件的次数，
// redone 是比例不合格被丢掉、退回队列重做的次数，duplicates 是抢尾单多做且后来丢掉的次数，
// style_redos 是风格分低于阈值、文件被丢掉的次数（含最后一次不再退回队列的）。
// generated = kept + redone + duplicates + style_redos。
// 引擎报错、超时、额度用完没有文件，不进这些数。
export function keepCounts(attempts) {
  const counts = { generated: 0, kept: 0, redone: 0, duplicates: 0, style_redos: 0 };
  for (const attempt of attempts ?? []) {
    if (!attempt?.produced) continue;
    counts.generated++;
    if (attempt.outcome === "done") counts.kept++;
    else if (attempt.outcome === "style_redo" || attempt.outcome === "style_rejected") counts.style_redos++;
    else if (attempt.outcome === "failed") counts.redone++;
    else if (attempt.outcome === "cancelled") counts.duplicates++;
  }
  return counts;
}

// 已有一份做完，或这一份是被取消的：丢掉，不要当成失败，也不要再改写出的图。
export function attemptDisposition({ cancelled, won, code, status }) {
  if (cancelled || won) return ATTEMPT_IGNORED;
  if (code === 0 && status === "ok") return ATTEMPT_WIN;
  return ATTEMPT_FAIL;
}
