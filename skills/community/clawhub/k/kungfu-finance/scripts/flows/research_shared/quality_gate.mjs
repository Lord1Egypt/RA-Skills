function buildCheck(id, passed, detail, {
  severity = "fatal"
} = {}) {
  return {
    id,
    passed,
    severity,
    detail
  };
}

function summarizeChecks(checks) {
  const failedChecks = checks.filter((item) => !item.passed);

  return {
    status: failedChecks.some((item) => item.severity === "fatal") ? "failed" : "passed",
    total_checks: checks.length,
    passed_checks: checks.filter((item) => item.passed).length,
    failed_checks: failedChecks.length,
    failed_ids: failedChecks.map((item) => item.id),
    checks
  };
}

function countMatches(content, pattern) {
  return [...content.matchAll(pattern)].length;
}

export function validateStockResearchArtifacts({
  reportMarkdown,
  reportSvg,
  searchEvidence
}) {
  const searchCompleted = searchEvidence?.status === "completed";
  const svgChecks = [
    buildCheck("stock-svg-root", /<svg[\s\S]*?<\/svg>/u.test(reportSvg), "SVG 根节点缺失"),
    buildCheck("stock-svg-title", /个股深度分析/u.test(reportSvg), "个股 SVG 标题缺失"),
    buildCheck("stock-svg-stage-labels", countMatches(reportSvg, /阶段\d:/gu) >= 4, "阶段标签不足 4 个"),
    buildCheck("stock-svg-now-marker", /📍 NOW/u.test(reportSvg) && /¥/u.test(reportSvg), "NOW 标记或当前股价缺失"),
    buildCheck("stock-svg-valuation-zone", /高估区域/u.test(reportSvg) && /合理估值区间/u.test(reportSvg) && /低估区域/u.test(reportSvg), "估值区间缺失"),
    buildCheck("stock-svg-lines", /class="main-price-line"/u.test(reportSvg) && /class="secondary-line"/u.test(reportSvg) && /class="projection-line"/u.test(reportSvg), "主线/副线/推演线缺失"),
    buildCheck("stock-svg-bubbles", countMatches(reportSvg, /class="data-bubble"/gu) >= 6, "个股 SVG 信息气泡不足"),
    buildCheck("stock-svg-rating-box", /id="rating-box"/u.test(reportSvg), "综合评级框缺失")
  ];
  const reportChecks = [
    buildCheck("stock-report-title", /# .*深度研究报告/u.test(reportMarkdown), "报告标题缺失"),
    buildCheck("stock-report-fact-inference", /\*\*\[事实\]\*\*/u.test(reportMarkdown) && /\*\*\[推演\]\*\*/u.test(reportMarkdown), "事实/推演分层缺失"),
    buildCheck("stock-report-sections", /## 一、宏观与行业/u.test(reportMarkdown) && /## 六、催化剂与风险/u.test(reportMarkdown), "关键章节缺失"),
    buildCheck("stock-report-no-trade-command", !/(建仓|加仓|减仓|买入|卖出|做空)/u.test(reportMarkdown), "报告出现了具体交易指令"),
    buildCheck("stock-report-correction-note", /纠错状态/u.test(reportMarkdown), "纠错状态说明缺失"),
    buildCheck("stock-report-no-stale-search-copy", !(searchCompleted && /未接入独立搜索证据链/u.test(reportMarkdown)), "搜索已执行但报告仍保留未接入搜索的陈旧文案"),
    buildCheck("stock-report-no-fake-debate-claim", !/已执行\s*\|?\s*外部搜索、资金流与同业对标仍缺位/u.test(reportMarkdown), "报告把预览版正反论据误写成已执行辩论")
  ];

  return {
    status: [...svgChecks, ...reportChecks].every((item) => item.passed) ? "passed" : "failed",
    svg_gate: summarizeChecks(svgChecks),
    report_gate: summarizeChecks(reportChecks),
    eval_baseline: {
      source: "stock-analysis-v2 EVAL migrated baseline",
      judge_dimensions: ["structure", "logic", "facts", "risk", "svg"],
      scenario_count: 6
    }
  };
}

export function validateSectorResearchArtifacts({
  reportMarkdown,
  reportSvg,
  searchEvidence
}) {
  const searchCompleted = searchEvidence?.status === "completed";
  const svgChecks = [
    buildCheck("sector-svg-root", /<svg[\s\S]*?<\/svg>/u.test(reportSvg), "SVG 根节点缺失"),
    buildCheck("sector-svg-title", /板块情绪周期图/u.test(reportSvg), "板块 SVG 标题缺失"),
    buildCheck("sector-svg-stage-labels", countMatches(reportSvg, /阶段\d:/gu) >= 4, "阶段标签不足 4 个"),
    buildCheck("sector-svg-emotion-bar", /id="emotion-bar"/u.test(reportSvg) && /url\(#emotionGradient\)/u.test(reportSvg), "情绪条缺失"),
    buildCheck("sector-svg-lines", /class="main-sector-line"/u.test(reportSvg) && /class="secondary-line"/u.test(reportSvg) && /class="projection-line"/u.test(reportSvg), "主线/副线/推演线缺失"),
    buildCheck("sector-svg-direction-box", /id="direction-box"/u.test(reportSvg), "方向判断框缺失"),
    buildCheck("sector-svg-bubbles", countMatches(reportSvg, /class="data-bubble"/gu) >= 4, "板块 SVG 信息气泡不足"),
    buildCheck("sector-svg-now-marker", /📍 NOW/u.test(reportSvg), "NOW 标记缺失")
  ];
  const reportChecks = [
    buildCheck("sector-report-title", /# .*板块深度研究报告/u.test(reportMarkdown), "报告标题缺失"),
    buildCheck("sector-report-fact-inference", /\*\*\[事实\]\*\*/u.test(reportMarkdown) && /\*\*\[推演\]\*\*/u.test(reportMarkdown), "事实/推演分层缺失"),
    buildCheck("sector-report-sections", /## 一、宏观与赛道环境/u.test(reportMarkdown) && /## 五、方向判断与情景/u.test(reportMarkdown), "关键章节缺失"),
    buildCheck("sector-report-no-trade-command", !/(建仓|加仓|减仓|买入|卖出|做空)/u.test(reportMarkdown), "报告出现了具体交易指令"),
    buildCheck("sector-report-correction-note", /纠错状态/u.test(reportMarkdown), "纠错状态说明缺失"),
    buildCheck("sector-report-no-stale-search-copy", !(searchCompleted && /未接入独立搜索证据链/u.test(reportMarkdown)), "搜索已执行但报告仍保留未接入搜索的陈旧文案"),
    buildCheck("sector-report-no-placeholder-windows", !/下一交易周|下一报告窗口/u.test(reportMarkdown), "报告仍保留缺乏证据支撑的固定时间窗口"),
    buildCheck("sector-report-no-fixed-return-ranges", !/[+-]?\d+%\s*~\s*[+-]?\d+%/u.test(reportMarkdown), "报告仍保留缺乏证据支撑的固定收益区间"),
    buildCheck("sector-report-no-time-force-copy", !/时间力量分析/u.test(reportMarkdown), "报告仍沿用误导性的时间力量表述")
  ];

  return {
    status: [...svgChecks, ...reportChecks].every((item) => item.passed) ? "passed" : "failed",
    svg_gate: summarizeChecks(svgChecks),
    report_gate: summarizeChecks(reportChecks),
    eval_baseline: {
      source: "sector-analysis EVAL migrated baseline",
      judge_dimensions: ["structure", "logic", "facts", "risk", "svg"],
      scenario_count: 6
    }
  };
}
