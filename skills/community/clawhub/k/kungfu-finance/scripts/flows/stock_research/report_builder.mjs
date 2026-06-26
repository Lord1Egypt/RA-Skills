import { withResearchHardening } from "../research_shared/hardening.mjs";
import { buildResearchOrchestrationAlignment } from "../research_shared/orchestration_alignment.mjs";
import { validateStockResearchArtifacts } from "../research_shared/quality_gate.mjs";
import { renderStockResearchSvg } from "./svg_renderer.mjs";

function toNumber(value) {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

function formatNumber(value, digits = 2) {
  const parsed = toNumber(value);
  return parsed === null ? "N/A" : parsed.toFixed(digits);
}

function formatPercent(value) {
  const parsed = toNumber(value);
  return parsed === null ? "N/A" : `${parsed.toFixed(2)}%`;
}

function formatAmountInYi(value) {
  const parsed = toNumber(value);
  if (parsed === null) {
    return "N/A";
  }
  return `${(parsed / 100000000).toFixed(2)}亿`;
}

function getSearchBucket(searchEvidence, searchId) {
  if (!Array.isArray(searchEvidence?.searches)) {
    return null;
  }

  return searchEvidence.searches.find((item) => item.search_id === searchId) || null;
}

function getSearchResults(searchEvidence, searchId) {
  const bucket = getSearchBucket(searchEvidence, searchId);
  return Array.isArray(bucket?.results) ? bucket.results : [];
}

function hasSearchEvidence(searchEvidence, searchId) {
  return searchEvidence?.status === "completed" && getSearchResults(searchEvidence, searchId).length > 0;
}

function buildSearchStatus(searchEvidence, searchId, {
  readyLabel = "🟢已补搜索",
  pendingLabel = "⚪待补搜索"
} = {}) {
  return hasSearchEvidence(searchEvidence, searchId) ? readyLabel : pendingLabel;
}

function buildSearchDegradation({ searchEvidence, searchId, affectedSteps, unavailableCode, unavailableMessage }) {
  if (hasSearchEvidence(searchEvidence, searchId)) {
    return null;
  }

  if (searchEvidence?.status === "provider_error") {
    return {
      code: `${searchId}_provider_error`,
      message: `独立搜索运行失败：${searchEvidence.error?.message || searchEvidence.reason || "provider error"}。`,
      affected_steps: affectedSteps
    };
  }

  if (searchEvidence?.status === "misconfigured") {
    return {
      code: `${searchId}_misconfigured`,
      message: `独立搜索配置不完整：${searchEvidence.reason || "search runtime misconfigured"}。`,
      affected_steps: affectedSteps
    };
  }

  return {
    code: unavailableCode,
    message: unavailableMessage,
    affected_steps: affectedSteps
  };
}

function renderSearchEvidence(searchEvidence, searchId, { fallback, limit = 1 } = {}) {
  const results = getSearchResults(searchEvidence, searchId);
  if (!results.length) {
    return fallback;
  }

  return results
    .slice(0, limit)
    .map(
      (item) =>
        `**[事实]** 外部搜索证据：${item.title}（${item.source_name || "未知来源"}, ${item.published_at || "日期未知"}${item.url ? `, ${item.url}` : ""}）。${item.snippet ? ` ${item.snippet}` : ""}`
    )
    .join("\n\n");
}

function hasMeaningfulMoneyFlow(signal) {
  if (!signal) {
    return false;
  }
  return signal.record_count > 0 || signal.main_force_net_amount !== null;
}

function buildDegradations(runtimeData) {
  const searchEvidence = runtimeData.search_evidence;
  const { normalized } = runtimeData;
  const degradations = [
    {
      code: "structured_financials_unavailable",
      message: "公共API不提供财务报表时间序列，财务分析通过搜索补充。",
      affected_steps: ["step-2-financials", "step-3-valuation", "step-5-thesis", "step-8-verdict"]
    },
    {
      code: "company_profile_limited",
      message: "公共API不提供主营业务/行业分类/概念标签等结构化数据，公司画像通过搜索补充。",
      affected_steps: ["step-1-company-profile", "step-1b-forward-advantage", "step-5-thesis", "step-6-catalyst"]
    }
  ];

  if (!hasMeaningfulMoneyFlow(normalized.money_flow_signal)) {
    degradations.push({
      code: "money_flow_unavailable",
      message: "东方财富资金流向未返回有效数据，本版不输出主力资金流结论。",
      affected_steps: ["step-4-price-action", "step-5-thesis"]
    });
  }

  const macroSearchDegradation = buildSearchDegradation({
    searchEvidence,
    searchId: "macro_context",
    affectedSteps: ["step-0-macro-sector", "step-6-catalyst"],
    unavailableCode: "macro_search_unavailable",
    unavailableMessage: "当前版本未接入独立搜索证据链，宏观/政策/竞争格局只能保留轻量占位，不输出外部检索结论。"
  });
  if (macroSearchDegradation) {
    degradations.unshift(macroSearchDegradation);
  }

  const catalystSearchDegradation = buildSearchDegradation({
    searchEvidence,
    searchId: "catalyst_context",
    affectedSteps: ["step-6-catalyst"],
    unavailableCode: "catalyst_search_unavailable",
    unavailableMessage: "催化剂章节只使用业绩预告与报告期节奏，未接入新闻、政策与产业事件搜索。"
  });
  if (catalystSearchDegradation) {
    degradations.push(catalystSearchDegradation);
  }

  const riskSearchDegradation = buildSearchDegradation({
    searchEvidence,
    searchId: "risk_context",
    affectedSteps: ["step-5-thesis", "step-6-catalyst", "step-7a-skeptic", "step-8-verdict"],
    unavailableCode: "risk_search_unavailable",
    unavailableMessage: "风险章节缺少独立负面/监管搜索，只能依靠结构化指标和保守推演。"
  });
  if (riskSearchDegradation) {
    degradations.push(riskSearchDegradation);
  }

  const sectorTrendSearchDegradation = buildSearchDegradation({
    searchEvidence,
    searchId: "sector_trend_context",
    affectedSteps: ["step-0-macro-sector", "step-6-catalyst"],
    unavailableCode: "sector_trend_search_unavailable",
    unavailableMessage: "行业趋势/景气独立搜索未接入，宏观与行业章节缺少赛道层面的外部检索佐证。"
  });
  if (sectorTrendSearchDegradation) {
    degradations.push(sectorTrendSearchDegradation);
  }

  const governanceSearchDegradation = buildSearchDegradation({
    searchEvidence,
    searchId: "governance_context",
    affectedSteps: ["step-1-company-profile", "step-5-thesis", "step-6-catalyst"],
    unavailableCode: "governance_search_unavailable",
    unavailableMessage: "治理/管理层/质押相关独立搜索未接入，公司画像与风险章节缺少外部治理事件证据。"
  });
  if (governanceSearchDegradation) {
    degradations.push(governanceSearchDegradation);
  }

  const competitionSearchDegradation = buildSearchDegradation({
    searchEvidence,
    searchId: "competition_context",
    affectedSteps: ["step-1-company-profile", "step-5-thesis"],
    unavailableCode: "competition_search_unavailable",
    unavailableMessage: "竞争格局/市场份额独立搜索未接入，护城河与同业对比依赖公司画像搜索与定性推断。"
  });
  if (competitionSearchDegradation) {
    degradations.push(competitionSearchDegradation);
  }

  const financialsSearchDegradation = buildSearchDegradation({
    searchEvidence,
    searchId: "financials_context",
    affectedSteps: ["step-2-financials", "step-3-valuation", "step-5-thesis"],
    unavailableCode: "financials_search_unavailable",
    unavailableMessage: "财报与盈利质量独立搜索未接入，财务章节仅能依赖估值快照与保守表述。"
  });
  if (financialsSearchDegradation) {
    degradations.push(financialsSearchDegradation);
  }

  const companyProfileSearchDegradation = buildSearchDegradation({
    searchEvidence,
    searchId: "company_profile_context",
    affectedSteps: ["step-1-company-profile", "step-1b-forward-advantage", "step-5-thesis"],
    unavailableCode: "company_profile_search_unavailable",
    unavailableMessage: "主营业务/商业模式独立搜索未接入，公司画像与前瞻叙事证据不足。"
  });
  if (companyProfileSearchDegradation) {
    degradations.push(companyProfileSearchDegradation);
  }

  if (!runtimeData.normalized.forecast) {
    degradations.push({
      code: "profit_forecast_missing",
      message: "当前结构化输入没有返回业绩预告摘要，催化剂与盈利前瞻仅能保守表述。",
      affected_steps: ["step-1b-forward-advantage", "step-6-catalyst"]
    });
  }

  return degradations;
}

function buildRating(runtimeData, degradations) {
  const { financial_signal, forecast_signal, valuation_signal, bar_stats, concept_names } =
    runtimeData.normalized;

  let score = 0;
  if (financial_signal.direction === "improving") {
    score += 1;
  } else if (financial_signal.direction === "weakening") {
    score -= 1;
  }

  if (forecast_signal.tone === "positive") {
    score += 1;
  } else if (forecast_signal.tone === "negative") {
    score -= 1;
  }

  if (bar_stats.trend === "up") {
    score += 1;
  } else if (bar_stats.trend === "down") {
    score -= 1;
  }

  if (valuation_signal.level === "rich") {
    score -= 1;
  } else if (valuation_signal.level === "cheap") {
    score += 1;
  }

  if (concept_names.length >= 2) {
    score += 1;
  }

  const rating =
    score >= 3 ? { icon: "🟡", label: "审慎乐观" } : score >= 1 ? { icon: "⚪", label: "中性" } : { icon: "🔴", label: "谨慎" };

  const confidence =
    degradations.length >= 5 ? { icon: "🔴", label: "低" } : degradations.length >= 3 ? { icon: "🟡", label: "中" } : { icon: "🟢", label: "高" };

  return {
    ...rating,
    confidence,
    score,
    horizon: "3-6个月"
  };
}

function buildPublicSourceRefs(sources) {
  if (!Array.isArray(sources) || !sources.length) {
    return [];
  }
  return [...new Set(sources.map((s) => s.source).filter(Boolean))];
}

function buildStepResults(runtimeData, references, degradations, rating) {
  const { instrument, normalized, request, sources } = runtimeData;
  const sourceRefs = buildPublicSourceRefs(sources);
  const valuation = normalized.valuation_signal;
  const latestFinancial = normalized.financial_signal.latest;
  const previousFinancial = normalized.financial_signal.previous;
  const priceSummary = normalized.price_summary;
  const barStats = normalized.bar_stats;

  const summaries = {
    "step-0-macro-sector": {
      status:
        hasSearchEvidence(runtimeData.search_evidence, "macro_context") &&
        hasSearchEvidence(runtimeData.search_evidence, "sector_trend_context")
          ? "completed"
          : normalized.sector_name || hasSearchEvidence(runtimeData.search_evidence, "sector_trend_context")
            ? "completed"
            : "degraded",
      summary: normalized.sector_name
        ? `已完成行业轻量定位，当前行业标签为${normalized.sector_name}${
            hasSearchEvidence(runtimeData.search_evidence, "sector_trend_context")
              ? "，并已补充行业趋势相关搜索证据。"
              : "，但宏观/政策证据链仍可能不完整。"
          }`
        : hasSearchEvidence(runtimeData.search_evidence, "sector_trend_context")
          ? "已接入行业趋势搜索证据，结构化行业标签仍待补齐。"
          : "仅完成轻量宏观占位，缺少行业标签与外部宏观证据。"
    },
    "step-1-company-profile": {
      status: "completed",
      summary: normalized.main_business
        ? `公司主营业务聚焦${normalized.main_business}${
            normalized.holder_signal?.top_shareholders?.length
              ? `；已解析前十大股东/持仓结构要点（共 ${normalized.holder_signal.top_shareholders.length} 条样本）。`
              : ""
          }`
        : normalized.holder_signal?.top_shareholders?.length
          ? `已解析股东结构样本 ${normalized.holder_signal.top_shareholders.length} 条，主营业务描述仍为空。`
          : "已解析标的身份，但主营业务描述仍为空。"
    },
    "step-1b-forward-advantage": {
      status:
        normalized.forecast || hasSearchEvidence(runtimeData.search_evidence, "company_profile_context")
          ? "completed"
          : "degraded",
      summary: normalized.forecast
        ? `前瞻优势以业绩预告为主，当前信号为${normalized.forecast_signal.summary}。`
        : hasSearchEvidence(runtimeData.search_evidence, "company_profile_context")
          ? "前瞻叙事依赖公司画像搜索与价格行为；公共API无业绩预告结构化字段。"
          : "前瞻优势仅能从价格行为做保守推演，建议补充公司画像与财报搜索。"
    },
    "step-2-financials": {
      status: hasSearchEvidence(runtimeData.search_evidence, "financials_context") ? "completed" : "degraded",
      summary: `${normalized.financial_signal.summary}${
        hasSearchEvidence(runtimeData.search_evidence, "financials_context")
          ? " 已并入「财报/盈利」独立搜索证据。"
          : " 「财报/盈利」独立搜索待补。"
      }`
    },
    "step-3-valuation": {
      status: "completed",
      summary: (() => {
        const base =
          valuation.level === "rich"
            ? "当前估值快照偏高（东方财富实时报价 PE/PB）"
            : valuation.level === "cheap"
              ? "当前估值快照偏低（东方财富实时报价 PE/PB）"
              : "当前估值处于中性倍数区间（东方财富实时报价）";
        if (hasSearchEvidence(runtimeData.search_evidence, "financials_context")) {
          return `${base}；已用财报搜索与快照做交叉阅读，无公共API历史分位/同业排名。`;
        }
        return `${base}；同业相对估值与历史分位需依赖搜索补充，公共API仅提供当期倍数。`;
      })()
    },
    "step-4-price-action": {
      status: "completed",
      summary:
        (barStats.trend === "up"
          ? "价格行为维持上行结构，支撑/阻力来自日K统计窗口；周线为东方财富真实周K。"
          : barStats.trend === "down"
            ? "价格行为偏弱，支撑/阻力来自日K统计窗口；周线为东方财富真实周K。"
            : "价格行为处于震荡结构，支撑/阻力来自日K统计窗口；周线为东方财富真实周K。") +
        (hasMeaningfulMoneyFlow(normalized.money_flow_signal)
          ? ` 主力资金流信号为 ${normalized.money_flow_signal.direction === "inflow" ? "净流入" : normalized.money_flow_signal.direction === "outflow" ? "净流出" : "中性"}（东方财富资金流向）。`
          : "")
    },
    "step-5-thesis": {
      status: "completed",
      summary: "已基于财务、估值与价格行为构建首版投资论题。"
    },
    "step-6-catalyst": {
      status:
        normalized.forecast &&
        hasSearchEvidence(runtimeData.search_evidence, "catalyst_context") &&
        hasSearchEvidence(runtimeData.search_evidence, "sector_trend_context")
          ? "completed"
          : normalized.forecast || hasSearchEvidence(runtimeData.search_evidence, "catalyst_context")
            ? "completed"
            : "degraded",
      summary: normalized.forecast
        ? `催化剂章节已覆盖业绩预告与报告期节奏${
            hasSearchEvidence(runtimeData.search_evidence, "catalyst_context")
              ? "，并补充催化剂相关搜索"
              : ""
          }${
            hasSearchEvidence(runtimeData.search_evidence, "sector_trend_context")
              ? "与行业趋势搜索"
              : ""
          }。`
        : "催化剂章节只保留报告期节奏占位，未接入独立搜索与预告摘要。"
    },
    "step-7a-skeptic": {
      status: "completed",
      summary: "已生成保守立场质疑。"
    },
    "step-7b-advocate": {
      status: "completed",
      summary: "已生成正面立场辩护。"
    },
    "step-8-verdict": {
      status: "completed",
      summary: `当前裁决为${rating.label}，但置信度保持${rating.confidence.label}。`
    },
    "step-9-output": {
      status: "completed",
      summary: "已生成结构化 Markdown 报告，并标注事实/推演与关键时间戳。"
    }
  };

  return references.steps.map((step) => ({
    step_id: step.step_id,
    title: step.title,
    reference_path: step.path,
    ...summaries[step.step_id],
    source_refs: sourceRefs,
    degradation_codes: degradations
      .filter((item) => item.affected_steps.includes(step.step_id))
      .map((item) => item.code)
  }));
}

function formatMoneyFlowLine(mf, targetDate) {
  if (!mf) {
    return null;
  }
  const dirLabel =
    mf.direction === "inflow" ? "净流入" : mf.direction === "outflow" ? "净流出" : "中性/待判";
  const main = mf.main_force_net_amount != null ? formatAmountInYi(mf.main_force_net_amount) : "N/A";
  const recent = Array.isArray(mf.recent_main_net) ? mf.recent_main_net.filter((r) => r?.main_net != null) : [];
  const recentBits = recent
    .slice(-3)
    .map((r) => `${r.d || "?"}:${formatAmountInYi(r.main_net)}`)
    .join("；");
  return `**[事实]** 主力资金流信号为「${dirLabel}」，窗口内主力净额约 ${main}（东方财富资金流向, ${targetDate}）${
    recentBits ? `；近端样本：${recentBits}` : ""
  }。`;
}

function formatMoneyFlowDashboardCells(mf) {
  if (!hasMeaningfulMoneyFlow(mf)) {
    return { evalLabel: "⚪待补", detail: "东方财富资金流向未返回有效数据" };
  }
  const dirLabel =
    mf.direction === "inflow" ? "🟢净流入" : mf.direction === "outflow" ? "🔴净流出" : "⚪中性";
  const main = mf.main_force_net_amount != null ? formatAmountInYi(mf.main_force_net_amount) : "N/A";
  return { evalLabel: dirLabel, detail: `主力净额约 ${main}；近端记录条数 ${mf.record_count ?? "N/A"}` };
}

function formatSearchBucketDashboard(searchEvidence, searchId) {
  const n = getSearchResults(searchEvidence, searchId).length;
  if (n > 0) {
    return { evalLabel: "🟢已补搜索", detail: `检索到 ${n} 条外部结果，正文见对应章节` };
  }
  return { evalLabel: "⚪待补搜索", detail: "独立搜索未返回结果" };
}

function buildBullPoints(runtimeData) {
  const { normalized } = runtimeData;
  const points = [];
  const td = runtimeData.request.target_date;

  if (normalized.financial_signal.direction === "improving") {
    points.push(
      `**[事实]** 最新两个报告期的净利润/扣非利润同步改善，最新报告期为${normalized.financial_signal.latest?.d || "N/A"}（结构化财报序列；公共API无此字段时需以财报搜索交叉验证）。`
    );
  }

  if (hasSearchEvidence(runtimeData.search_evidence, "financials_context")) {
    points.push(
      "**[事实]** 「财报/盈利」独立搜索已返回结果，盈利与财务质量应以第三节搜索证据与估值快照交叉阅读（公共API无财务报表时间序列）。"
    );
  }

  if (normalized.forecast) {
    points.push(
      `**[事实]** 业绩预告摘要显示“${normalized.forecast.forecast_summary}”（东方财富实时报价/结构化预告, ${normalized.forecast.forecast_date}）。`
    );
  }

  if (normalized.bar_stats.trend === "up") {
    points.push(
      `**[事实]** 价格结构处于上行状态，最新价 ${formatNumber(normalized.price_summary?.latest_price)} 元，高于近端均值窗口（东方财富实时报价, ${normalized.price_summary?.latest_trading_day}）。`
    );
  }

  if (normalized.concept_names.length) {
    points.push(
      `**[事实]** 当前结构化概念标签包括 ${normalized.concept_names.join("、")}（东方财富实时报价, ${td}）。`
    );
  }

  if (hasSearchEvidence(runtimeData.search_evidence, "company_profile_context")) {
    points.push("**[事实]** 「公司画像」独立搜索已返回结果，业务与护城河叙事应优先采信第二节搜索证据。");
  }

  const mf = normalized.money_flow_signal;
  if (mf && hasMeaningfulMoneyFlow(mf) && mf.direction === "inflow") {
    points.push(
      `**[事实]** 主力资金流呈净流入，主力净额约 ${mf.main_force_net_amount != null ? formatAmountInYi(mf.main_force_net_amount) : "N/A"}（东方财富资金流向, ${td}）。`
    );
  }

  return points.length ? points : ["**[事实]** 当前公共API仅提供报价/K线/资金流；强正面证据需依赖多路独立搜索补齐。"];
}

const SEARCH_BUCKET_IDS = [
  "macro_context",
  "catalyst_context",
  "risk_context",
  "sector_trend_context",
  "competition_context",
  "governance_context",
  "financials_context",
  "company_profile_context"
];

function buildBearPoints(runtimeData) {
  const { normalized } = runtimeData;
  const points = [];
  const td = runtimeData.request.target_date;

  if (normalized.valuation_signal.level === "rich") {
    points.push(
      `**[事实]** 当前 PE/PB 快照分别为 ${formatNumber(normalized.valuation_signal.pe_ttm)} / ${formatNumber(normalized.valuation_signal.pb)}，绝对倍数不低（东方财富实时报价, ${td}）。`
    );
  }

  if (normalized.financial_signal.direction === "weakening") {
    points.push(
      `**[事实]** 最新两个报告期的利润趋势转弱，最新报告期 ${normalized.financial_signal.latest?.d || "N/A"} 相比上一期改善不足（结构化财报序列；公共API无此字段时需以财报搜索交叉验证）。`
    );
  }

  const mf = normalized.money_flow_signal;
  if (mf && hasMeaningfulMoneyFlow(mf) && mf.direction === "outflow") {
    points.push(
      `**[事实]** 主力资金流呈净流出，主力净额约 ${mf.main_force_net_amount != null ? formatAmountInYi(mf.main_force_net_amount) : "N/A"}（东方财富资金流向, ${td}）。`
    );
  }

  const searchFlags = SEARCH_BUCKET_IDS.map((id) => hasSearchEvidence(runtimeData.search_evidence, id));
  const searchDepth = searchFlags.filter(Boolean).length;

  if (searchDepth >= 5) {
    points.push(
      "**[推演]** 已补充多路独立搜索（8 类主题中多数已命中），但各证据仍需与东方财富报价/K线/资金流及口径时效交叉验证，任何中高置信度判断都应保守对待。"
    );
  } else if (searchDepth >= 2) {
    points.push(
      "**[推演]** 仅部分搜索桶返回结果，宏观、财报、公司画像与风险证据链仍不完整，任何中高置信度判断都应保守对待。"
    );
  } else {
    points.push(
      "**[推演]** 公共API仅提供报价/K线/资金流；独立搜索证据严重不足时，基本面与治理结论不可外推，任何中高置信度判断都应保守对待。"
    );
  }

  const gapParts = [];
  if (!hasMeaningfulMoneyFlow(normalized.money_flow_signal)) {
    gapParts.push("东方财富主力资金流");
  }
  gapParts.push("公共API财务报表时间序列");
  gapParts.push("行业排名/历史估值分位/一致预期（需搜索或专业数据源）");
  if (gapParts.length) {
    points.push(
      `**[推演]** ${gapParts.join("、")}未并入或永久缺失时，相对估值与盈利兑现判断应保持保守。`
    );
  }

  return points;
}

function formatFinancialChange(previousValue, currentValue) {
  const previous = toNumber(previousValue);
  const current = toNumber(currentValue);

  if (previous === null || current === null) {
    return "N/A";
  }

  if (previous === 0) {
    if (current === 0) {
      return "0.00%";
    }
    return current > 0 ? "由0转正" : "由0转负";
  }

  if (previous < 0 && current >= 0) {
    return "扭亏";
  }

  if (previous > 0 && current < 0) {
    return "转亏";
  }

  if (previous < 0 && current < 0) {
    const shrinkRatio = (Math.abs(previous) - Math.abs(current)) / Math.abs(previous);
    if (shrinkRatio > 0) {
      return `亏损收窄 ${formatPercent(shrinkRatio * 100)}`;
    }
    if (shrinkRatio < 0) {
      return `亏损扩大 ${formatPercent(Math.abs(shrinkRatio) * 100)}`;
    }
    return "持平";
  }

  return formatPercent(((current - previous) / previous) * 100);
}

function renderReport(runtimeData, stepResults, degradations, rating) {
  const { instrument, normalized } = runtimeData;
  const latestFinancial = normalized.financial_signal.latest;
  const previousFinancial = normalized.financial_signal.previous;
  const valuation = normalized.valuation_signal;
  const barStats = normalized.bar_stats;
  const bullPoints = buildBullPoints(runtimeData);
  const bearPoints = buildBearPoints(runtimeData);
  const conceptText = normalized.concept_names.length ? normalized.concept_names.join("、") : "暂无概念标签";
  const levelSummary = normalized.level_summary || {};
  const priceLevelSignals = Array.isArray(normalized.price_levels?.data?.signals)
    ? normalized.price_levels.data.signals.slice(0, 2)
    : [];

  const thesisSummary =
    normalized.financial_signal.direction === "improving" && normalized.forecast_signal.tone === "positive"
      ? "盈利趋势与预告方向都偏正面，但估值与外部验证仍约束结论强度。"
      : "当前正反信号交织，更多像一条需要继续验证的跟踪论题，而不是高确定性结论。";

  const barEndLabel = runtimeData.bar_series?.end_date || runtimeData.request.target_date;
  const catalystLine = normalized.forecast
    ? `**[事实]** 已披露业绩预告节点为 ${normalized.forecast.forecast_date}，摘要为“${normalized.forecast.forecast_summary}”（东方财富实时报价, ${normalized.forecast.forecast_date}）。`
    : "**[事实]** 公共API未返回业绩预告摘要；盈利前瞻依赖「财报/盈利」搜索与定期报告披露节奏。";
  const macroEvidence = renderSearchEvidence(runtimeData.search_evidence, "macro_context", {
    fallback:
      "**[推演]** 宏观/政策独立搜索待补时，本章节无法给出行业景气与政策节奏的高置信度结论；公共API亦未提供行业分类结构化字段。"
  });
  const catalystEvidence = renderSearchEvidence(runtimeData.search_evidence, "catalyst_context", {
    fallback:
      "**[推演]** 催化剂与产业事件依赖独立搜索；公共API仅提供行情与资金流，请将后续财报、预告与新闻检索列为验证清单。"
  });
  const riskEvidence = renderSearchEvidence(runtimeData.search_evidence, "risk_context", {
    fallback:
      "**[推演]** 当前没有独立负面/监管搜索证据时，风险章节只能基于东方财富估值/价格快照、资金流与已知降级项保守展开。"
  });
  const macroStatus = buildSearchStatus(runtimeData.search_evidence, "macro_context");
  const catalystStatus = buildSearchStatus(runtimeData.search_evidence, "catalyst_context");
  const riskStatus = buildSearchStatus(runtimeData.search_evidence, "risk_context");
  const priceLevelLine = priceLevelSignals.length
    ? `**[事实]** 最近技术位包括 ${priceLevelSignals
        .map((signal) => `${signal?.line_type === "support" ? "支撑" : "压力"} ${formatNumber(signal?.price)}（${signal?.d || "日期未知"}）`)
        .join("、")}（非公共API标准能力，若存在则为遗留字段）。`
    : levelSummary?.nearest_resistance_price || levelSummary?.nearest_support_price
      ? `**[事实]** 最近支撑 / 压力约为 ${formatNumber(levelSummary?.nearest_support_price)} / ${formatNumber(levelSummary?.nearest_resistance_price)}（遗留字段；公共API无筹码分布）。`
      : "**[推演]** 公共API不提供筹码集中度；下文支撑/阻力取自东方财富日K近期高低点统计，不等同于筹码成本意义上的关键位。";

  const targetDate = runtimeData.request.target_date;
  const conceptTableEval = normalized.concept_names.length ? "🟡已识别" : "⚪缺失（依赖搜索）";
  const conceptTableDetail = conceptText;

  const mfDash = formatMoneyFlowDashboardCells(normalized.money_flow_signal);
  const finSearchDash = formatSearchBucketDashboard(runtimeData.search_evidence, "financials_context");
  const profileSearchDash = formatSearchBucketDashboard(runtimeData.search_evidence, "company_profile_context");

  const hasProfileSearch = hasSearchEvidence(runtimeData.search_evidence, "company_profile_context");
  const hasGovSearch = hasSearchEvidence(runtimeData.search_evidence, "governance_context");
  const hasCompSearch = hasSearchEvidence(runtimeData.search_evidence, "competition_context");
  let moatEval = "⚪待补";
  let moatDetail = "公共API无结构化护城河字段；依赖公司画像/竞争/治理搜索";
  if (hasProfileSearch || hasGovSearch || hasCompSearch) {
    moatEval = "🟡搜索补强";
    const bits = [];
    if (hasProfileSearch) {
      bits.push("公司画像搜索已命中");
    }
    if (hasCompSearch) {
      bits.push("竞争格局搜索已命中");
    }
    if (hasGovSearch) {
      bits.push("治理/质押搜索已命中");
    }
    moatDetail = bits.join("；") || moatDetail;
  }

  const sectorTrendEvidence = renderSearchEvidence(runtimeData.search_evidence, "sector_trend_context", {
    fallback:
      "**[推演]** 行业趋势/景气独立搜索待补时，赛道β与政策节奏只能保留定性占位；公共API未返回行业标签。"
  });
  const competitionEvidence = renderSearchEvidence(runtimeData.search_evidence, "competition_context", {
    fallback:
      "**[推演]** 竞争格局独立搜索待补时，护城河与市场份额缺少外部核对；请结合「公司画像」搜索阅读。"
  });
  const governanceEvidence = renderSearchEvidence(runtimeData.search_evidence, "governance_context", {
    fallback:
      "**[推演]** 治理/质押/管理层事件依赖独立搜索；公共API不提供股东结构结构化快照。"
  });
  const companyProfileEvidence = renderSearchEvidence(runtimeData.search_evidence, "company_profile_context", {
    fallback:
      "**[推演]** 「公司画像」搜索待补时，主营业务与商业模式只能依赖名称解析与定性推断，证据强度偏低。"
  });
  const financialsEvidence = renderSearchEvidence(runtimeData.search_evidence, "financials_context", {
    fallback:
      "**[推演]** 「财报/盈利」搜索待补时，第三节表格中的利润同比字段缺乏外部事实锚定；公共API不提供财务报表时间序列。"
  });

  const moneyFlowFactLine =
    formatMoneyFlowLine(normalized.money_flow_signal, targetDate) ||
    "**[推演]** 东方财富资金流向未返回有效数据时，本章节对资金博弈维度保持保守。";

  const hasSectorTrendSearch = hasSearchEvidence(runtimeData.search_evidence, "sector_trend_context");
  const hasMacroSearch = hasSearchEvidence(runtimeData.search_evidence, "macro_context");
  const section1Lead =
    hasMacroSearch && hasSectorTrendSearch
      ? "**宏观与行业趋势搜索已部分并入；行业结构化标签仍依赖搜索归纳，与东方财富行情数据交叉验证。**"
      : hasSectorTrendSearch || hasMacroSearch
        ? "**宏观或行业趋势搜索仅部分命中；公共API无行业分类字段，证据链仍不完整。**"
        : "**公共API无行业/概念结构化字段；宏观与赛道结论几乎完全依赖独立搜索。**";

  const hasFinSearch = hasSearchEvidence(runtimeData.search_evidence, "financials_context");
  const section3Lead = hasFinSearch
    ? "**估值快照来自东方财富实时报价；盈利与报表质量请以本节「财报/盈利」搜索证据为主，表格内财务同比在公共API下可能缺省。**"
    : "**估值仅完成东方财富 PE/PB 快照；财务报表时间序列缺失且财报搜索未命中时，盈利趋势不可外推。**";

  const valuationFollowup =
    "**[推演]** 公共API不提供历史估值分位、同业排名与一致预期；任何“相对低估/高估”结论必须来自搜索或其它数据源，本报告默认只陈述绝对倍数水平。";

  const structuredGapsParts = [];
  if (!hasMeaningfulMoneyFlow(normalized.money_flow_signal)) {
    structuredGapsParts.push("东方财富主力资金流");
  }
  structuredGapsParts.push("财务报表时间序列（永久缺失于公共API）");
  structuredGapsParts.push("筹码分布/行业排名/历史分位（公共API不提供）");
  const structuredGapsBullet = `- **[事实]** 数据源边界：${structuredGapsParts.join("、")}；结论须与 8 类独立搜索及后续披露交叉验证。`;

  const forwardAdvantageLine = normalized.forecast
    ? `**[推演]** 业绩预告为“${normalized.forecast.forecast_summary}”，结合概念/搜索可读信息 ${conceptTableDetail}，前瞻叙事需用「公司画像」「竞争」搜索检验可持续性。`
    : `**[推演]** 公共API无业绩预告与结构化主业字段；前瞻优势主要来自「公司画像」「财报/盈利」搜索与价格/资金流，证据不足时应保守。`;

  return `# ${instrument.instrument_name || instrument.instrument_id}（${instrument.instrument_id}.${instrument.exchange_id}）深度研究报告

## 综合评级

${rating.icon} **${rating.label}** | 置信度: ${rating.confidence.icon}${rating.confidence.label} | 视野: ${rating.horizon}

**核心结论**: ${thesisSummary}

**决策仪表盘**

| 维度 | 评估 | 详情 |
| --- | --- | --- |
| 宏观环境 | ${macroStatus} | ${hasSearchEvidence(runtimeData.search_evidence, "macro_context") ? "已补充宏观/行业搜索证据" : "宏观与行业搜索仍待补齐"} |
| 行业阶段 | ${normalized.sector_name ? "🟡轻量定位" : "⚪未知"} | ${normalized.sector_name || "缺少行业标签"} |
| 概念脉络 | ${conceptTableEval} | ${conceptTableDetail} |
| 资金流 | ${mfDash.evalLabel} | ${mfDash.detail} |
| 财报搜索 | ${finSearchDash.evalLabel} | ${finSearchDash.detail} |
| 公司画像搜索 | ${profileSearchDash.evalLabel} | ${profileSearchDash.detail} |
| 护城河 | ${moatEval} | ${moatDetail} |
| 盈利质量 | ${
    normalized.financial_signal.direction === "improving"
      ? "🟢改善"
      : normalized.financial_signal.direction === "weakening"
        ? "🔴走弱"
        : "⚪分化"
  } | ${normalized.financial_signal.summary} |
| 估值水平 | ${
    valuation.level === "rich" ? "🔴偏高" : valuation.level === "cheap" ? "🟢偏低" : "⚪中性"
  } | PE ${formatNumber(valuation.pe_ttm)} / PB ${formatNumber(valuation.pb)} / PS ${formatNumber(valuation.ps)} |
| 股价趋势 | ${barStats.trend === "up" ? "↗上行" : barStats.trend === "down" ? "↘下行" : "←震荡"} | 支撑 ${formatNumber(barStats.support)} / 阻力 ${formatNumber(barStats.resistance)} |
| 催化剂验证 | ${catalystStatus} | ${hasSearchEvidence(runtimeData.search_evidence, "catalyst_context") ? "已补充催化剂搜索证据" : "催化剂搜索仍待补齐"} |
| 风险验证 | ${riskStatus} | ${hasSearchEvidence(runtimeData.search_evidence, "risk_context") ? "已补充风险搜索证据" : "风险搜索仍待补齐"} |
| 反面审查 | 🟡预览版 | 当前只输出结构化正反论据摘要，未独立运行多代理辩论 |

## 一、宏观与行业

${section1Lead}
*关键问题：当前行业处于真实基本面兑现，还是仅停留在结构化标签层面的轻量映射？*

**[事实]** 当前结构化行业标签为 ${normalized.sector_name || "未返回（公共API无此字段）"}，概念标签为 ${conceptTableDetail}（东方财富实时报价/搜索归纳, ${targetDate}）。

${macroEvidence}

${sectorTrendEvidence}

## 二、公司画像与前瞻优势

**公司画像以「公司画像」独立搜索为主，公共API仅提供代码、名称与行情；竞争与治理依赖竞争/治理类搜索。**
*关键问题：这家公司现有业务是否真能把赛道叙事转化成可验证的优势？*

**[事实]** 主营业务（结构化）为 ${normalized.main_business || "未返回"}；业务与商业模式请以「公司画像」搜索证据为准（东方财富实时报价仅提供标的标识, ${targetDate}）。

**[事实]** 标的解析结果为 ${instrument.instrument_id}.${instrument.exchange_id}，当前名称为 ${instrument.instrument_name || "未提供"}（东方财富实时报价, ${targetDate}）。

${companyProfileEvidence}

${competitionEvidence}

${governanceEvidence}

${forwardAdvantageLine}

## 三、财务与估值

${section3Lead}
*关键问题：盈利改善是否足以覆盖当前估值要求？*

| 指标 | 上一期 | 最新一期 | 变化 |
| --- | --- | --- | --- |
| 扣非净利润（pq） | ${formatNumber(previousFinancial?.pq)} | ${formatNumber(latestFinancial?.pq)} | ${formatFinancialChange(previousFinancial?.pq, latestFinancial?.pq)} |
| 净利润（nq） | ${formatNumber(previousFinancial?.nq)} | ${formatNumber(latestFinancial?.nq)} | ${formatFinancialChange(previousFinancial?.nq, latestFinancial?.nq)} |
| PE / PB / PS | - | ${formatNumber(valuation.pe_ttm)} / ${formatNumber(valuation.pb)} / ${formatNumber(valuation.ps)} | 快照 |
| 总市值 | - | ${formatAmountInYi(valuation.market_cap)} | 快照 |

**[事实]** 最新财务趋势判断为：${normalized.financial_signal.summary}（公共API无财务报表时间序列；请以「财报/盈利」搜索与定期报告为准, ${targetDate}）。

**[事实]** 当前估值快照为 PE ${formatNumber(valuation.pe_ttm)} / PB ${formatNumber(valuation.pb)} / PS ${formatNumber(valuation.ps)}（东方财富实时报价, ${targetDate}）。

${financialsEvidence}

${valuationFollowup}

## 四、价格行为

**价格行为来自东方财富日K与真实周K（周线由 klt=102 接口直接拉取，非日线聚合）。**
*关键问题：股价是否已经先于基本面兑现，还是仍留有预期差？*

**[事实]** 最新价 ${formatNumber(normalized.price_summary?.latest_price)} 元，区间涨跌幅 ${formatPercent(normalized.price_summary?.period_change_pct)}，最新交易日 ${normalized.price_summary?.latest_trading_day || "N/A"}（东方财富实时报价, ${normalized.price_summary?.latest_trading_day || runtimeData.request.target_date}）。

**[事实]** 当前趋势判定为 ${barStats.trend === "up" ? "上行" : barStats.trend === "down" ? "下行" : "震荡"}，支撑位约 ${formatNumber(barStats.support)}，阻力位约 ${formatNumber(barStats.resistance)}（东方财富日K线, ${barEndLabel}）。

${priceLevelLine}

${moneyFlowFactLine}

**[事实]** 周线序列已与日线同源接口分频拉取，可用于趋势级别复核（东方财富周K线, ${targetDate}）。

## 五、投资论题与正反论据

**当前最合理的结论不是“立刻定性”，而是把它视作一条低置信度但可继续跟踪的研究主线。**
*关键问题：如果必须现在给结论，正反两边最强论据分别是什么？*

### 1. 正方观点

${bullPoints.map((item) => `- ${item}`).join("\n")}

### 2. 反方观点

${bearPoints.map((item) => `- ${item}`).join("\n")}

### 3. 当前裁决

**[推演]** 正方论据高度依赖搜索与东方财富行情；反方约束来自公共API无财报序列、无筹码与同业结构化数据，以及搜索桶未全覆盖时的证据盲区。本版只给 ${rating.label}、${rating.confidence.label}置信度判断。这里的“当前裁决”是单报告合成结果，不等同于原版 skill 的独立委员会式辩论裁决。

## 六、催化剂与风险

**催化剂与风险在搜索证据链基础上展开；公共API仅提供行情与资金流，财报与事件须靠搜索与披露核对。**
*关键问题：接下来哪些事件最可能验证或推翻当前论题？*

${catalystLine}

${catalystEvidence}

**[推演]** 行业趋势、竞争格局与治理类检索若已在「宏观与行业」「公司画像」章节展示，本节将其与业绩预告、负面搜索及结构化降级项一并纳入风险核对；请勿仅依赖单一章节片段下结论。

### 关键风险

- **[事实]** ${
    hasSearchEvidence(runtimeData.search_evidence, "macro_context") ||
    hasSearchEvidence(runtimeData.search_evidence, "sector_trend_context")
      ? "宏观与行业/赛道搜索证据已部分补充，但仍需与东方财富行情及后续披露交叉验证。"
      : "宏观、政策、竞争格局仍缺少外部搜索佐证。"
  }
- **[事实]** ${
    hasSearchEvidence(runtimeData.search_evidence, "risk_context") ||
    hasSearchEvidence(runtimeData.search_evidence, "governance_context")
      ? "风险与治理相关搜索已部分补充，仍需核对监管披露与财报附注。"
      : "负面/监管与治理事件搜索仍可能不完整。"
  }
${structuredGapsBullet}
- **[推演]** 如果后续财报/预告不及当前摘要方向，低置信度结论会被快速推翻。

${riskEvidence}

纠错状态：当前 preview 版只记录显式冲突修正；本次未新增纠错记录，并已显式披露 ${degradations.length} 项已知降级。 
`;
}

export function buildStockResearchResult(runtimeData, references) {
  const degradations = buildDegradations(runtimeData);
  const rating = buildRating(runtimeData, degradations);
  const stepResults = buildStepResults(runtimeData, references, degradations, rating);
  const degradedStepCount = stepResults.filter((item) => item.status === "degraded").length;
  const reportMarkdown = renderReport(runtimeData, stepResults, degradations, rating);
  const reportSvg = renderStockResearchSvg(runtimeData, rating);
  const qualityGate = validateStockResearchArtifacts({
    reportMarkdown,
    reportSvg,
    searchEvidence: runtimeData.search_evidence
  });
  const orchestration = buildResearchOrchestrationAlignment(references);

  return withResearchHardening({
    flow: "stock-research",
    status: degradations.length > 0 ? "completed_with_degradation" : "completed",
    instrument: runtimeData.instrument,
    target_date: runtimeData.request.target_date,
    visual_days_len: runtimeData.request.visual_days_len,
    rating: {
      label: rating.label,
      icon: rating.icon,
      confidence: rating.confidence.label,
      horizon: rating.horizon
    },
    coverage: {
      step_count: references.steps.length,
      completed_steps: stepResults.filter((item) => item.status === "completed").length,
      degraded_steps: degradedStepCount,
      prompt_asset_count: references.prompt_assets.length,
      orchestration_asset_count: references.orchestration_assets.length,
      svg_enabled: true,
      quality_gate_status: qualityGate.status
    },
    degradations,
    orchestration,
    quality_gate: qualityGate,
    search_evidence: runtimeData.search_evidence,
    sources: runtimeData.sources,
    references: {
      source_skill: references.source_skill,
      flow_contract_path: references.flow_contract_path,
      runtime_parity_path: references.runtime_parity_path,
      prompt_assets: references.prompt_assets,
      orchestration_assets: references.orchestration_assets,
      step_paths: references.steps.map((item) => ({
        step_id: item.step_id,
        path: item.path
      }))
    },
    step_results: stepResults,
    report_markdown: reportMarkdown,
    report_svg: reportSvg
  }, {
    searchRuntime: runtimeData.search_evidence,
    reportMode: "markdown_svg_preview",
    parityStage: "svg_gated_preview"
  });
}
