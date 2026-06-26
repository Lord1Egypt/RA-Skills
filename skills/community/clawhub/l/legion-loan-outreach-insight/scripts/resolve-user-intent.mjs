/**
 * 共享：解析 userMessage、反问判断、网关确认字段覆盖。
 */
import { parseTimeRange } from "./parse-time-range.mjs";
import { parseAnalysisFocus } from "./parse-analysis-focus.mjs";

export const DEFAULT_TIME_MONTHS = 1;
export const DIMENSION_NOTICE =
  "因未提取到明确的分析维度信息，已使用默认十维拓客统计框架处理。";
export const TIME_NOTICE = "未确认具体时间，已按默认最近 1 个月统计。";

export function mergeUserMessage(body) {
  const parts = [];
  if (body?.userMessage) parts.push(String(body.userMessage));
  if (body?.query && body.query !== body?.userMessage) parts.push(String(body.query));
  if (body?.followUpMessage) parts.push(String(body.followUpMessage));
  const fromEnv = process.env.LEGION_USER_MESSAGE?.trim();
  if (fromEnv) parts.push(fromEnv);
  return parts.join(" ").trim();
}

export function userAcceptedDefaults(text) {
  return /就按默认 | 按默认 | 用默认 | 你看着办 | 随便 | 默认即可|default\s+is\s+fine/i.test(
    String(text ?? ""),
  );
}

export function parseOutputFormat(text) {
  const raw = String(text ?? "");
  if (/只要文字 | 纯文本 | 不要页面 | 简略 | 口头汇报/i.test(raw)) {
    return { mode: "text", userSpecified: true, label: "用户要求文本输出" };
  }
  if (/导出|excel|表格|pdf|邮件|ppt|幻灯片/i.test(raw)) {
    return {
      mode: "custom",
      userSpecified: true,
      label: "用户指定了特殊交付格式，按用户要求处理",
    };
  }
  if (/页面 | 网页|html|h5|可视化 | 仪表盘|dashboard/i.test(raw)) {
    return { mode: "page", userSpecified: true, label: "用户要求页面形态" };
  }
  return { mode: "page", userSpecified: false, label: "未指定交付形态，默认生成报告页面" };
}

export function buildClarification(timeRange, analysisFocus) {
  const questions = [];
  if (timeRange.confidence === "ambiguous") {
    questions.push(
      "请确认要统计的时间范围（例如：最近 7 天、最近 1 个月、最近 3 个月）？",
    );
  }
  if (timeRange.confidence === "missing") {
    questions.push(
      "未识别到具体时间。请说明统计窗口；若暂不指定，将按默认最近 1 个月处理。",
    );
  }
  if (analysisFocus.confidence === "ambiguous") {
    questions.push(
      "请确认希望重点分析的方向（例如：拓客复盘、销售话术、AI 教练、客户需求；或说明「按默认十维」）？",
    );
  }
  if (analysisFocus.confidence === "missing") {
    questions.push(
      "请说明希望重点分析的方向；若暂不指定，将按默认十维拓客统计框架处理。",
    );
  }
  return {
    shouldAsk: questions.length > 0,
    questions,
    defaults: {
      timeMonths: DEFAULT_TIME_MONTHS,
      timeLabel: `默认近 ${DEFAULT_TIME_MONTHS} 个月`,
      dimensions: "ten",
      dimensionNotice: DIMENSION_NOTICE,
      timeNotice: TIME_NOTICE,
    },
  };
}

function applyConfirmedDimension(analysisFocus, confirmedDimension) {
  const v = String(confirmedDimension ?? "").trim();
  if (!v) return analysisFocus;
  if (/^(default_ten|ten|十维 | 默认十维)$/i.test(v)) {
    return {
      theme: null,
      keywords: [],
      explicit: false,
      rawPhrase: null,
      confidence: "explicit",
      confirmed: "ten_dimensions",
    };
  }
  return {
    theme: v,
    keywords: [v],
    explicit: true,
    rawPhrase: v,
    confidence: "explicit",
    confirmed: "user_theme",
  };
}

function applyConfirmedTime(timeRange, confirmedTime) {
  if (confirmedTime == null) return timeRange;
  if (typeof confirmedTime === "string" && /^default$/i.test(confirmedTime.trim())) {
    const parsed = parseTimeRange("");
    return { ...parsed, confidence: "explicit", source: "default", label: "用户确认：默认近 1 个月" };
  }
  if (typeof confirmedTime === "object" && confirmedTime.startTime && confirmedTime.endTime) {
    return {
      ...timeRange,
      startTime: String(confirmedTime.startTime),
      endTime: String(confirmedTime.endTime),
      confidence: "explicit",
      source: "user",
      label: "用户确认时间窗",
    };
  }
  return timeRange;
}

export function buildReportPlan(timeRange, analysisFocus) {
  const useDefaultTime = timeRange.confidence !== "explicit";
  const useDefaultDimensions = analysisFocus.confidence !== "explicit";
  return {
    mode: analysisFocus.explicit ? "user_theme" : "ten_dimensions",
    useDefaultDimensions,
    useDefaultTime,
    dimensionNotice: useDefaultDimensions ? DIMENSION_NOTICE : null,
    timeNotice: useDefaultTime ? TIME_NOTICE : null,
  };
}

/**
 * @param {object|null} body
 */
export function resolveUserIntent(body) {
  const userMessage = mergeUserMessage(body);
  let timeRange = parseTimeRange(userMessage);
  let analysisFocus = parseAnalysisFocus(userMessage);
  const outputFormat = parseOutputFormat(userMessage);
  let clarification = buildClarification(timeRange, analysisFocus);

  const skipClarification =
    body?.skipClarification === true ||
    userAcceptedDefaults(userMessage) ||
    process.env.LEGION_SKIP_CLARIFICATION === "1";

  if (body?.confirmedTime != null) {
    timeRange = applyConfirmedTime(timeRange, body.confirmedTime);
  }
  if (body?.confirmedDimension != null) {
    analysisFocus = applyConfirmedDimension(analysisFocus, body.confirmedDimension);
  }

  if (skipClarification) {
    clarification = { ...clarification, shouldAsk: false, skipped: true };
  }

  const needClarification = clarification.shouldAsk && !skipClarification;
  const reportPlan = buildReportPlan(timeRange, analysisFocus);

  return {
    userMessage: userMessage || null,
    timeRange,
    analysisFocus,
    outputFormat,
    clarification,
    needClarification,
    skipClarification,
    reportPlan,
  };
}
