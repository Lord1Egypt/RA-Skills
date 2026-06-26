/**
 * 从用户原话规则提取分析主题（analysisFocus）。
 */

const THEME_PATTERNS = [
  {
    theme: "股票趋势",
    keywords: ["股票", "趋势", "行情", "大盘", "涨跌", "牛市", "熊市", "板块", "个股", "持仓", "K 线"],
    re: /股票\s*趋势 | 行情\s* 趋势 | 股价\s* 趋势|stock\s+trend/i,
  },
  {
    theme: "拓客复盘",
    keywords: ["拓客", "地推", "走访", "扫街", "外勤", "拜访"],
    re: /拓客\s* 复盘 | 走访\s* 复盘 | 地推\s* 复盘/i,
  },
  {
    theme: "销售话术",
    keywords: ["话术", "开场白", "异议", "推介", "获客"],
    re: /(?:销售)?话术 | 开口白 | 异议\s* 处理|talk\s+track/i,
  },
  {
    theme: "客户需求",
    keywords: ["需求", "用款", "额度", "利率", "期限", "还款", "放款"],
    re: /客户\s* 需求 | 用款\s* 需求 | 资金\s* 需求/i,
  },
  {
    theme: "AI 教练",
    keywords: ["教练", "AI 教练", "智能教练", "教练反馈", "教练点评", "对练", "场景对练"],
    re: /AI\s* 教练 | 智能教练 | 教练\s*(?:反馈 | 点评 | 复盘 | 报告)|coach(?:ing)?\s*(?:feedback|report|recap)?|AI\s*coach/i,
  },
];

const PRIMARY_THEME_KEYWORDS = {
  股票趋势：["股票", "行情", "大盘", "涨跌", "个股", "板块"],
  拓客复盘：["拓客", "地推", "走访", "扫街", "外勤", "拜访"],
  销售话术：["话术", "开场白", "异议", "推介"],
  客户需求：["用款", "额度", "利率", "期限", "还款", "放款"],
  AI 教练：["教练", "对练", "场景对练", "教练反馈", "教练点评", "AI 教练"],
};

export function parseAnalysisFocus(text) {
  const raw = String(text ?? "").trim();
  if (!raw) {
    return { theme: null, keywords: [], explicit: false, rawPhrase: null, confidence: "missing" };
  }

  if (/默认十维 | 按十维 | 十维 (?:拓客)?(?:报告 | 分析 | 统计)/i.test(raw)) {
    return {
      theme: null,
      keywords: [],
      explicit: false,
      rawPhrase: null,
      confidence: "explicit",
    };
  }

  for (const item of THEME_PATTERNS) {
    if (item.re.test(raw)) {
      return {
        theme: item.theme,
        keywords: item.keywords,
        explicit: true,
        rawPhrase: item.theme,
        confidence: "explicit",
      };
    }
  }

  const generic = raw.match(
    /(?:关于 | 针对 | 按 | 围绕)\s*([^，,。.\s]{2,12})(?:方向 | 趋势 | 情况 | 表现)?|([^，,。.\s]{2,10})\s*(?:趋势 | 方向)(?=\s|$|[，,.])/,
  );
  if (generic) {
    const phrase = (generic[1] || generic[2] || "").trim();
    if (phrase && !/录音 | 音频 | 转写|asr/i.test(phrase)) {
      return {
        theme: phrase,
        keywords: [phrase],
        explicit: true,
        rawPhrase: phrase,
        confidence: "explicit",
      };
    }
  }

  if (/综合 | 整体 | 大概 | 简单/.test(raw) && /分析 | 总结 | 看看/.test(raw)) {
    return {
      theme: null,
      keywords: [],
      explicit: false,
      rawPhrase: null,
      confidence: "ambiguous",
    };
  }

  return { theme: null, keywords: [], explicit: false, rawPhrase: null, confidence: "missing" };
}

export function isThemeRelatedToTranscripts(combinedAsrText, focus) {
  if (!focus?.explicit || !focus?.keywords?.length) {
    return true;
  }
  const hay = String(combinedAsrText ?? "");
  if (!hay) {
    return false;
  }

  const primary = PRIMARY_THEME_KEYWORDS[focus.theme];
  if (primary?.length) {
    return primary.some((kw) => hay.includes(kw));
  }

  return focus.keywords.some((kw) => kw.length >= 2 && hay.includes(kw));
}
