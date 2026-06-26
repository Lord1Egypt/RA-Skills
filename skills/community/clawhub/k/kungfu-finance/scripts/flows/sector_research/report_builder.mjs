import { withResearchHardening } from "../research_shared/hardening.mjs";
import { buildResearchOrchestrationAlignment } from "../research_shared/orchestration_alignment.mjs";
import { validateSectorResearchArtifacts } from "../research_shared/quality_gate.mjs";
import { renderSectorResearchSvg } from "./svg_renderer.mjs";

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

function formatMarketCap(value) {
  const parsed = toNumber(value);
  if (parsed === null) return "N/A";
  if (parsed >= 1e12) return `${(parsed / 1e12).toFixed(2)}万亿`;
  if (parsed >= 1e8) return `${(parsed / 1e8).toFixed(2)}亿`;
  if (parsed >= 1e4) return `${(parsed / 1e4).toFixed(0)}万`;
  return `${parsed.toFixed(0)}`;
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

function hasMoneyFlowEvidence(normalized) {
  if (normalized?.sector_money_flow) {
    return true;
  }

  const rows = Array.isArray(normalized?.leader_fundamentals) ? normalized.leader_fundamentals : [];
  return rows.some((row) => row?.money_flow != null);
}

function getLeaderFundamentalsRows(normalized) {
  return Array.isArray(normalized?.leader_fundamentals) ? normalized.leader_fundamentals : [];
}

function isLeaderFundamentalsEmpty(normalized) {
  return !getLeaderFundamentalsRows(normalized).length;
}

function countLeadersWithMarketSnapshot(normalized) {
  return getLeaderFundamentalsRows(normalized).filter((row) => leaderHasQuoteSnapshot(row)).length;
}

function countLeadersWithMoneyFlow(normalized) {
  return getLeaderFundamentalsRows(normalized).filter((row) => row?.money_flow != null).length;
}

function leaderHasQuoteSnapshot(row) {
  const p = row?.price || row?.quote;
  if (!p) return false;
  return p.latest_price != null || p.pe != null || p.market_cap != null;
}

function hasLeaderMarketSnapshotEvidence(normalized) {
  return countLeadersWithMarketSnapshot(normalized) > 0;
}

function hasLeaderFullFinancialsEvidence(normalized) {
  return getLeaderFundamentalsRows(normalized).some(
    (row) => row?.finance?.forecast_summary != null
  );
}

function summarizeMoneyFlowDataBlock(data, depth = 0) {
  if (data == null) {
    return "";
  }

  if (typeof data !== "object") {
    return String(data);
  }

  if (depth > 2) {
    return "…";
  }

  const pairs = [];
  for (const [key, value] of Object.entries(data)) {
    if (pairs.length >= 6) {
      break;
    }

    if (value != null && typeof value === "object" && !Array.isArray(value)) {
      const inner = summarizeMoneyFlowDataBlock(value, depth + 1);
      if (inner) {
        pairs.push(`${key}{${inner}}`);
      }
    } else if (toNumber(value) !== null) {
      pairs.push(`${key}: ${formatNumber(value)}`);
    } else if (typeof value === "string" || typeof value === "number" || typeof value === "boolean") {
      pairs.push(`${key}: ${value}`);
    }
  }

  return pairs.join("；");
}

function buildDegradations(runtimeData) {
  const searchEvidence = runtimeData.search_evidence;
  const normalized = runtimeData.normalized;
  const degradations = [];

  if (!normalized.similar_sectors?.length) {
    degradations.push({
      code: "related_sector_candidates_limited",
      message: "当前只拿到了主命中板块，缺少更多接近主题词的候选赛道，横向映射仍有限。",
      affected_steps: ["step-1-filter", "step-2-classify"]
    });
  }

  if (isLeaderFundamentalsEmpty(normalized)) {
    degradations.push({
      code: "constituent_fundamentals_unavailable",
      message:
        "runtime 未返回龙头行情采样行；龙头对比仅能依赖成分股涨跌排序表，东方财富个股 PE/PB/市值等未并入。",
      affected_steps: ["step-2-classify", "step-3-mining", "step-4-thesis"]
    });
  } else if (!hasLeaderMarketSnapshotEvidence(normalized)) {
    degradations.push({
      code: "constituent_fundamentals_unavailable",
      message:
        "已锁定龙头成分股列表，但东方财富个股行情快照（价、涨跌、PE/PB/市值）未返回可用字段；完整财务报表与预告仍未接入。",
      affected_steps: ["step-2-classify", "step-3-mining", "step-4-thesis"]
    });
  } else if (!hasLeaderFullFinancialsEvidence(normalized)) {
    degradations.push({
      code: "constituent_fundamentals_unavailable",
      message:
        "东方财富公共行情已提供龙头最新价、涨跌幅及 PE/PB/市值等轻量字段；完整财务报表、业绩预告与盈利预测等结构化基本面本版未接入。",
      affected_steps: ["step-2-classify", "step-3-mining", "step-4-thesis"]
    });
  }

  if (!hasMoneyFlowEvidence(normalized)) {
    degradations.push({
      code: "money_flow_unavailable",
      message:
        "板块级 aggregate 资金流公共接口未开放，且龙头个股资金流未返回可用摘要；资金面叙事仅能依赖搜索证据与涨跌广度。",
      affected_steps: ["step-3-mining", "step-4-thesis", "step-5-position"]
    });
  }

  const macroSearchDegradation = buildSearchDegradation({
    searchEvidence,
    searchId: "macro_context",
    affectedSteps: ["step-0-macro", "step-6-risk"],
    unavailableCode: "macro_search_unavailable",
    unavailableMessage: "当前版本未接入独立搜索证据链，宏观、政策和监管只能保留轻量占位。"
  });
  if (macroSearchDegradation) {
    degradations.unshift(macroSearchDegradation);
  }

  const catalystSearchDegradation = buildSearchDegradation({
    searchEvidence,
    searchId: "catalyst_context",
    affectedSteps: ["step-6-risk", "step-8-verdict"],
    unavailableCode: "catalyst_search_unavailable",
    unavailableMessage: "催化剂日历缺少新闻、政策和产业事件搜索，只保留待验证窗口。"
  });
  if (catalystSearchDegradation) {
    degradations.push(catalystSearchDegradation);
  }

  const riskSearchDegradation = buildSearchDegradation({
    searchEvidence,
    searchId: "risk_context",
    affectedSteps: ["step-4-thesis", "step-6-risk", "step-8-verdict"],
    unavailableCode: "risk_search_unavailable",
    unavailableMessage: "风险章节缺少独立负面/监管搜索，只能依赖结构化走势和保守推演。"
  });
  if (riskSearchDegradation) {
    degradations.push(riskSearchDegradation);
  }

  const industryTrendSearchDegradation = buildSearchDegradation({
    searchEvidence,
    searchId: "industry_trend_context",
    affectedSteps: ["step-0-macro", "step-2-classify", "step-4-thesis"],
    unavailableCode: "industry_trend_search_unavailable",
    unavailableMessage: "行业景气、规模与渗透率类独立搜索未返回结果，产业趋势叙事仍偏结构化占位。"
  });
  if (industryTrendSearchDegradation) {
    degradations.push(industryTrendSearchDegradation);
  }

  const competitionSearchDegradation = buildSearchDegradation({
    searchEvidence,
    searchId: "competition_context",
    affectedSteps: ["step-2-classify", "step-3-mining"],
    unavailableCode: "competition_search_unavailable",
    unavailableMessage: "竞争格局与龙头份额类独立搜索未返回结果，横向对标仍依赖板块内广度。"
  });
  if (competitionSearchDegradation) {
    degradations.push(competitionSearchDegradation);
  }

  const policySearchDegradation = buildSearchDegradation({
    searchEvidence,
    searchId: "policy_context",
    affectedSteps: ["step-0-macro", "step-6-risk"],
    unavailableCode: "policy_search_unavailable",
    unavailableMessage: "政策、补贴与监管专项搜索未返回结果，政策边际只能与宏观搜索或占位合并看待。"
  });
  if (policySearchDegradation) {
    degradations.push(policySearchDegradation);
  }

  const moneyFlowSearchDegradation = buildSearchDegradation({
    searchEvidence,
    searchId: "money_flow_context",
    affectedSteps: ["step-3-mining", "step-4-thesis", "step-5-position"],
    unavailableCode: "money_flow_search_unavailable",
    unavailableMessage:
      "资金流向、机构与 ETF 相关独立搜索未返回结果；资金面叙事可部分依赖东方财富龙头个股资金流（若已返回）与涨跌广度。"
  });
  if (moneyFlowSearchDegradation) {
    degradations.push(moneyFlowSearchDegradation);
  }

  return degradations;
}

function buildRating(runtimeData, degradations) {
  const { bar_stats: barStats, breadth, stage_signal: stageSignal } = runtimeData.normalized;

  let score = 0;
  if (barStats.trend === "up") {
    score += 1;
  } else if (barStats.trend === "down") {
    score -= 1;
  }

  if (breadth.positive_ratio >= 0.67) {
    score += 1;
  } else if (breadth.positive_ratio <= 0.34) {
    score -= 1;
  }

  if ((breadth.average_change_pct ?? 0) >= 2) {
    score += 1;
  } else if ((breadth.average_change_pct ?? 0) <= -1) {
    score -= 1;
  }

  const direction =
    score >= 2
      ? { icon: "🟡", label: "偏强跟踪" }
      : score >= 0
        ? { icon: "⚪", label: "中性观察" }
        : { icon: "🔴", label: "谨慎观察" };

  const confidence =
    degradations.length >= 5 ? { icon: "🔴", label: "低" } : degradations.length >= 3 ? { icon: "🟡", label: "中" } : { icon: "🟢", label: "高" };

  return {
    ...direction,
    confidence,
    structure_label: stageSignal.label,
    horizon: "2-6周"
  };
}

function buildStepResults(runtimeData, references, degradations, rating) {
  const { normalized, sources } = runtimeData;
  const sourceRefs = sources.map((item) => item.route);
  const summaries = {
    "step-0-macro": {
      status:
        hasSearchEvidence(runtimeData.search_evidence, "macro_context") ||
        hasSearchEvidence(runtimeData.search_evidence, "policy_context")
          ? "completed"
          : "degraded",
      summary:
        hasSearchEvidence(runtimeData.search_evidence, "macro_context") ||
        hasSearchEvidence(runtimeData.search_evidence, "policy_context")
          ? "宏观/政策搜索证据已补充，但仍缺少风/终端级别的深度验证。"
          : "宏观、监管与政策只完成占位说明，仍缺少独立搜索证据。"
    },
    "step-1-filter": {
      status: "completed",
      summary: `已锁定单一板块对象，当前研究对象为${runtimeData.sector.sector_name || runtimeData.sector.sector_id}。`
    },
    "step-2-classify": {
      status: "degraded",
      summary: normalized.similar_sectors?.length
        ? hasLeaderMarketSnapshotEvidence(normalized)
          ? `已识别板块类型为${normalized.sector_type_label}，并补充了相似赛道映射与龙头行情估值快照（东方财富行情）。`
          : `已识别板块类型为${normalized.sector_type_label}，并补充了相似赛道映射；龙头 PE/PB/市值快照仍待补齐。`
        : hasLeaderMarketSnapshotEvidence(normalized)
          ? `已识别板块类型为${normalized.sector_type_label}，并补充龙头行情估值快照，但相似赛道映射仍有限。`
          : `已识别板块类型为${normalized.sector_type_label}，但相似赛道映射与龙头行情快照仍缺失。`
    },
    "step-3-mining": {
      status: "degraded",
      summary:
        hasLeaderMarketSnapshotEvidence(normalized) && hasMoneyFlowEvidence(normalized)
          ? "题材挖掘已并入龙头行情估值、个股资金流摘要，并与指数广度交叉验证。"
          : hasLeaderMarketSnapshotEvidence(normalized)
            ? "题材挖掘已并入龙头行情与估值快照；板块级资金流公共侧未开放，结论仍可结合搜索补强。"
            : hasMoneyFlowEvidence(normalized)
              ? "题材挖掘已并入龙头个股资金流与涨跌广度，行情估值快照仍可继续补强。"
              : "题材挖掘以指数结构和成分股涨跌广度为主，未并入个股资金流与行情估值细化。"
    },
    "step-4-thesis": {
      status: "completed",
      summary: "已基于价格结构、板块广度和龙头分化构建首版论题。"
    },
    "step-5-position": {
      status: "completed",
      summary: normalized.stage_signal.summary
    },
    "step-6-risk": {
      status:
        hasSearchEvidence(runtimeData.search_evidence, "risk_context") ? "completed" : "degraded",
      summary: hasSearchEvidence(runtimeData.search_evidence, "risk_context")
        ? "风险章节已补充独立风险搜索，并与结构化数据交叉验证。"
        : "风险章节已显式写出搜索、资金流和基本面方面的已知缺口与已并入项。"
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
      summary: `当前方向判断为${rating.label}，但置信度保持${rating.confidence.label}。`
    },
    "step-9-output": {
      status: "completed",
      summary: "已生成结构化 Markdown 报告，并写出事实/推演和降级说明。"
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

function renderLeaderTable(rows) {
  if (!rows.length) {
    return "| 公司 | 代码 | 最新价 | 当日涨幅 |\n| --- | --- | --- | --- |\n| 暂无成分股数据 | N/A | N/A | N/A |";
  }

  const lines = rows.map((row, index) => {
    const name = index === 0 ? `**${row.instrument_name}**` : row.instrument_name;
    return `| ${name} | ${row.instrument_id}.${row.exchange_id} | ${formatNumber(row.latest_price)} | ${formatPercent(row.change_pct)} |`;
  });

  return ["| 公司 | 代码 | 最新价 | 当日涨幅 |", "| --- | --- | --- | --- |", ...lines].join("\n");
}

function formatSectorTypeShort(sectorType) {
  if (sectorType === "concept") {
    return "概念";
  }

  if (sectorType === "sw1") {
    return "申万一级行业";
  }

  if (sectorType === "sw2") {
    return "申万二级行业";
  }

  return sectorType ? String(sectorType) : "板块";
}

function renderLeaderFundamentalsTable(leaderFundamentals) {
  const rows = Array.isArray(leaderFundamentals) ? leaderFundamentals : [];
  const withSnapshot = rows.filter((row) => leaderHasQuoteSnapshot(row));

  if (!withSnapshot.length) {
    return "**[推演]** 龙头成分股东方财富行情快照（价、涨跌、PE/PB/市值）待接口返回后补全。";
  }

  const lines = withSnapshot.map((row) => {
    const price = row.price;
    const q = row.quote || {};
    const latestPrice = toNumber(price?.latest_price) ?? toNumber(q.latest_price);
    const changePct = toNumber(price?.latest_change_pct) ?? toNumber(q.change_pct);
    const pe = toNumber(q.pe) ?? toNumber(row.finance?.pe_ttm);
    const pb = toNumber(q.pb) ?? toNumber(row.finance?.pb);
    const mc = q.market_cap ?? row.finance?.market_cap;

    return `| ${row.instrument_name} | ${row.instrument_id}.${row.exchange_id} | ${latestPrice === null ? "N/A" : formatNumber(latestPrice)} | ${formatPercent(changePct)} | ${pe === null ? "N/A" : formatNumber(pe)} | ${pb === null ? "N/A" : formatNumber(pb)} | ${formatMarketCap(mc)} |`;
  });

  return [
    "| 龙头 | 代码 | 最新价 | 当日涨跌 | PE | PB | 市值 |",
    "| --- | --- | --- | --- | --- | --- | --- |",
    ...lines
  ].join("\n");
}

function renderSectorMoneyFlowNarrative(normalized) {
  const smf = normalized?.sector_money_flow;
  if (smf?.data && typeof smf.data === "object") {
    const summaryText = summarizeMoneyFlowDataBlock(smf.data);
    const body = summaryText || "板块行情返回中已挂载资金流相关块，字段待解读。";
    return `**[事实]** 板块级资金流（字段组：${smf.source_key || "unknown"}）已并入：${body}（东方财富板块K线/扩展字段）。`;
  }

  const flowCount = countLeadersWithMoneyFlow(normalized);
  if (flowCount > 0) {
    return `**[事实]** 板块级 aggregate 资金流公共接口未开放；${flowCount} 只龙头股已有个股资金流结构化摘要（东方财富个股资金流）。`;
  }

  return "**[推演]** 板块级资金流不可用；龙头个股资金流未返回或未形成可用摘要。";
}

function renderSimilarSectorsComparisonTable(similarSectors) {
  const rows = Array.isArray(similarSectors) ? similarSectors : [];

  if (!rows.length) {
    return "";
  }

  const lines = rows.map((item) => {
    let src = "相似板块 API";
    if (item.resolver_source === "instrument-prefix") {
      src = "板块前缀推断";
    } else if (String(item.resolver_source || "").startsWith("eastmoney")) {
      src = "东方财富";
    }
    return `| ${item.sector_name} | ${item.sector_id} | ${formatSectorTypeShort(item.sector_type)} | ${item.similarity != null ? formatNumber(item.similarity, 3) : "N/A"} | ${src} |`;
  });

  return [
    "| 候选赛道 | 板块代码 | 类型 | 相似度 | 来源 |",
    "| --- | --- | --- | --- | --- |",
    ...lines
  ].join("\n");
}

function renderBucketSearchEvidence(searchEvidence, searchId, title, fallback) {
  const block = renderSearchEvidence(searchEvidence, searchId, {
    fallback: "",
    limit: 2
  });

  if (!block) {
    return `**${title}**\n\n${fallback}`;
  }

  return `**${title}**\n\n${block}`;
}

function renderRiskTable(runtimeData) {
  const searchEvidence = runtimeData.search_evidence;
  const norm = runtimeData.normalized;
  const macroEvidence = hasSearchEvidence(searchEvidence, "macro_context")
    ? "已补充宏观/政策搜索，但仍需与指数结构交叉验证"
    : "宏观与政策外部搜索仍缺失";
  const flowFinanceLine = hasMoneyFlowEvidence(norm)
    ? hasLeaderMarketSnapshotEvidence(norm)
      ? "已补充龙头级资金流与东方财富行情估值快照，仍需与板块指数节奏交叉验证"
      : "已补充龙头级资金流摘要，行情估值快照仍可继续补强"
    : hasSearchEvidence(searchEvidence, "risk_context")
      ? "已补充风险搜索，但资金流与深度财务仍未接入"
      : "缺少独立风险搜索与资金流验证";

  return [
    "| 攻击点 | 证据 | 裁决 |",
    "| --- | --- | --- |",
    `| 宏观与政策验证不足 | ${macroEvidence} | ⚠️部分成立 |`,
    "| 板块强度可能只是龙头抱团 | 成分股正收益占比与指数趋势存在分化风险 | ⚠️部分成立 |",
    `| 缺少资金流与财务细化 | ${flowFinanceLine} | ${hasMoneyFlowEvidence(norm) && hasLeaderMarketSnapshotEvidence(norm) ? "⚠️部分成立" : "✅辩护成立"} |`
  ].join("\n");
}

function renderInvalidationTable() {
  return [
    "| 类型 | 触发条件 | 验证方法 |",
    "| --- | --- | --- |",
    "| 结构失效 | 板块指数跌破近端支撑且成分股正收益占比继续下降 | 复查东方财富板块K线与板块成分股列表 |",
    "| 情绪失效 | 龙头股仍强但板块平均涨幅转负，扩散被证伪 | 观察龙头与全体广度的背离 |",
    "| 叙事失效 | 后续搜索验证不到产业/政策催化 | 独立搜索与新闻交叉复核 |"
  ].join("\n");
}

function renderScenarioTable(runtimeData) {
  const barStats = runtimeData.normalized.bar_stats;

  return [
    "| 情景 | 触发条件 | 可能演化 | 当前可验证信号 |",
    "| --- | --- | --- | --- |",
    `| 🟢 乐观 | 指数有效站上 ${formatNumber(barStats.resistance)} 且广度继续扩散 | 近期结构从“${runtimeData.normalized.stage_signal.label}”继续强化，方向判断可上修 | 观察阻力突破与正收益占比抬升 |`,
    `| ⚪ 基准 | 指数围绕 ${formatNumber(barStats.latest_close)} 附近震荡，龙头仍强但扩散一般 | 板块维持可跟踪但不宜过度外推的结构 | 观察指数是否守住短均线与广度是否稳定 |`,
    `| 🔴 悲观 | 指数跌破 ${formatNumber(barStats.support)}，龙头与中后排同步走弱 | 当前偏强结构被证伪，研究结论需要下修 | 观察支撑失守与负收益家数扩张 |`,
    "| ⚫ 极端 | 外部政策、监管或情绪冲击打断主题交易 | 板块从结构观察转入防守复核 | 需要新的风险搜索与消息验证 |"
  ].join("\n");
}

function renderCatalystTable(runtimeData) {
  const catalystResults = getSearchResults(runtimeData.search_evidence, "catalyst_context");

  if (catalystResults.length) {
    const lines = catalystResults.slice(0, 3).map((item) => {
      return `| ${item.published_at || "日期待补"} | ${item.title} | ${item.source_name || "未知来源"} | ${item.snippet || "待结合后续行情验证"} |`;
    });

    return [
      "| 时间锚点 | 观察事项 | 来源 | 备注 |",
      "| --- | --- | --- | --- |",
      ...lines
    ].join("\n");
  }

  return [
    "| 时间锚点 | 观察事项 | 来源 | 备注 |",
    "| --- | --- | --- | --- |",
    "| 待确认 | 产业订单、展会、政策更新 | 外部搜索待补 | 当前只能保留为验证清单 |",
    "| 待确认 | 板块扩散是否从龙头走向中后排 | 结构化行情 | 观察正收益占比与平均涨跌幅 |",
    "| 待确认 | 龙头公司后续业绩或订单兑现 | 公告/新闻待补 | 需要后续事件验证 |"
  ].join("\n");
}

function renderReport(runtimeData, rating, degradations) {
  const { sector, normalized, sector_performance: sectorPerformance, sector_constituents: sectorConstituents } =
    runtimeData;
  const barStats = normalized.bar_stats;
  const breadth = normalized.breadth;
  const leaders = breadth.leaders;
  const leadNames = leaders.map((item) => item.instrument_name).join("、") || "暂无";
  const laggardNames = breadth.laggards.map((item) => item.instrument_name).join("、") || "暂无";
  const structureSummary =
    barStats.trend === "up"
      ? "板块指数保持上行结构，但仍需警惕分化阶段的追高风险。"
      : barStats.trend === "down"
        ? "板块指数转弱，当前更接近等待二次验证。"
        : "板块指数进入震荡整理，是否再起需要新的催化剂验证。";
  const breadthSummary =
    breadth.total_count > 0
      ? `成分股样本中 ${breadth.positive_count}/${breadth.total_count} 只上涨，平均涨跌幅 ${formatPercent(breadth.average_change_pct)}。`
      : "当前未返回有效成分股样本。";
  const macroEvidence = renderSearchEvidence(runtimeData.search_evidence, "macro_context", {
    fallback: "**[推演]** 当前版本未接入独立搜索证据链，因此宏观宽松、产业政策和监管边际变化都只能保留为待验证项。"
  });
  const catalystEvidence = renderSearchEvidence(runtimeData.search_evidence, "catalyst_context", {
    fallback: "**[推演]** 当前基础判断仍需等待后续新闻、政策和产业事件搜索补全，因此催化剂日历只能保留为待验证窗口。"
  });
  const riskEvidence = renderSearchEvidence(runtimeData.search_evidence, "risk_context", {
    fallback: "**[推演]** 当前没有独立负面/监管搜索证据，风险章节只能根据指数结构、广度分化和已知降级项保守展开。"
  });
  const industryTrendSearchBlock = renderBucketSearchEvidence(
    runtimeData.search_evidence,
    "industry_trend_context",
    "行业景气与规模（独立搜索）",
    "**[推演]** 行业规模、CAGR 与渗透率类独立搜索证据仍待补全。"
  );
  const competitionSearchBlock = renderBucketSearchEvidence(
    runtimeData.search_evidence,
    "competition_context",
    "竞争格局（独立搜索）",
    "**[推演]** 龙头份额与竞争格局类独立搜索证据仍待补全。"
  );
  const policySearchBlock = renderBucketSearchEvidence(
    runtimeData.search_evidence,
    "policy_context",
    "政策与监管（专项搜索）",
    "**[推演]** 政策、补贴与法规专项搜索证据仍待补全。"
  );
  const moneyFlowContextSearchBlock = renderBucketSearchEvidence(
    runtimeData.search_evidence,
    "money_flow_context",
    "资金面叙事（独立搜索）",
    "**[推演]** 资金流向、机构与 ETF 相关独立搜索证据仍待补全。"
  );
  const marketSnapshotReady = hasLeaderMarketSnapshotEvidence(normalized);
  const fullFinancialsReady = hasLeaderFullFinancialsEvidence(normalized);
  const moneyFlowReady = hasMoneyFlowEvidence(normalized);
  const leaderRowsAll = getLeaderFundamentalsRows(normalized);
  const leaderSampleTotal = leaderRowsAll.length;
  const leaderSnapshotCount = countLeadersWithMarketSnapshot(normalized);
  const leaderFlowCount = countLeadersWithMoneyFlow(normalized);
  const fundamentalsSampleLabel = !leaderSampleTotal
    ? "⚪无采样"
    : leaderSnapshotCount === leaderSampleTotal
      ? "🟢全覆盖"
      : leaderSnapshotCount > 0
        ? "🟡部分"
        : "⚪待补";
  const fundamentalsSampleDetail = !leaderSampleTotal
    ? "runtime 未返回龙头行情采样行"
    : `${leaderSnapshotCount}/${leaderSampleTotal} 只龙头股已并入东方财富行情快照（价、涨跌、PE/PB/市值）`;
  const sectorFlowBlockPresent = Boolean(normalized.sector_money_flow);
  const moneyFlowStructuredLabel = !moneyFlowReady
    ? "⚪待补"
    : sectorFlowBlockPresent && leaderFlowCount > 0
      ? "🟢板块+龙头"
      : sectorFlowBlockPresent
        ? "🟢板块级"
        : leaderFlowCount > 0
          ? "🟡龙头级"
          : "⚪待补";
  const moneyFlowStructuredDetail = !moneyFlowReady
    ? "板块级资金流公共侧未开放，且龙头个股资金流未形成可用摘要"
    : sectorFlowBlockPresent
      ? `板块级资金流已挂载 ${normalized.sector_money_flow?.source_key || "资金流"} 字段组${leaderFlowCount ? `；${leaderFlowCount} 只龙头有个股资金流（东方财富）` : ""}`
      : `${leaderFlowCount} 只龙头股有个股资金流结构化摘要（东方财富）`;
  const similarCount = normalized.similar_sectors?.length ?? 0;
  const similarSectorMapLabel = similarCount ? `🟢${similarCount} 条` : "⚪待补";
  const similarSectorMapDetail = similarCount
    ? `相似赛道候选来自东方财富概念板块列表（共 ${similarCount} 条）`
    : "未返回可用相似赛道候选";
  const similarSectorLine = similarCount
    ? `**[事实]** 与输入主题词接近的其他候选赛道包括 ${normalized.similar_sectors
        .map((item) => `${item.sector_name}（${formatSectorTypeShort(item.sector_type)}）`)
        .join("、")}（东方财富概念板块列表与板块解析, ${runtimeData.request.target_date}）。`
    : "**[推演]** 当前未拿到更多接近主题词的候选赛道，因此横向赛道对照仍有限。";
  const macroStatus = buildSearchStatus(runtimeData.search_evidence, "macro_context");
  const riskStatus = buildSearchStatus(runtimeData.search_evidence, "risk_context");
  const catalystStatus = buildSearchStatus(runtimeData.search_evidence, "catalyst_context");
  const industryTrendStatus = buildSearchStatus(runtimeData.search_evidence, "industry_trend_context");
  const competitionStatus = buildSearchStatus(runtimeData.search_evidence, "competition_context");
  const policyContextStatus = buildSearchStatus(runtimeData.search_evidence, "policy_context");
  const moneyFlowContextStatus = buildSearchStatus(runtimeData.search_evidence, "money_flow_context");

  return `# ${sector.sector_name || "未知板块"}（${sector.sector_id}）板块深度研究报告

## 决策摘要

${rating.icon} **${rating.label}** | 近期结构: ${rating.structure_label} | 置信度: ${rating.confidence.icon}${rating.confidence.label}

**核心结论**: ${normalized.stage_signal.summary}

**决策仪表盘**

| 维度 | 评估 | 详情 |
| --- | --- | --- |
| 宏观体制 | ${macroStatus} | ${hasSearchEvidence(runtimeData.search_evidence, "macro_context") ? "已补充宏观/政策搜索证据" : "宏观与政策搜索仍待补齐"} |
| 反身性风险 | 🟡中 | 板块强度可能集中在少数龙头 |
| 监管风险 | ${riskStatus} | ${hasSearchEvidence(runtimeData.search_evidence, "risk_context") ? "已补充风险/监管搜索，但仍需后续交叉验证" : "监管与负面搜索仍待外部证据验证"} |
| 赛道判定 | ${sector.sector_type === "concept" ? "📈概念赛道" : "🔁行业赛道"} | ${normalized.sector_type_label} |
| 概念类型 | 🟡已识别 | 当前对象为${sector.sector_name || sector.sector_id} |
| 核心逻辑 | ${barStats.trend === "up" ? "✅有效" : barStats.trend === "down" ? "⚠️待观察" : "⚠️待观察"} | ${structureSummary} |
| 龙头基本面采样 | ${fundamentalsSampleLabel} | ${fundamentalsSampleDetail} |
| 利润剪刀差 | ${fullFinancialsReady ? "🟢已补" : "⚪待补"} | ${fullFinancialsReady ? "龙头预告/盈利预测等深度财务已并入" : "仅东方财富行情级 PE/PB/市值；财报与预告未接入"} |
| 资金流结构化 | ${moneyFlowStructuredLabel} | ${moneyFlowStructuredDetail} |
| 相似赛道映射 | ${similarSectorMapLabel} | ${similarSectorMapDetail} |
| 行业趋势搜索 | ${industryTrendStatus} | ${hasSearchEvidence(runtimeData.search_evidence, "industry_trend_context") ? "已补充行业规模/景气类搜索" : "行业趋势类搜索仍待补齐"} |
| 竞争格局搜索 | ${competitionStatus} | ${hasSearchEvidence(runtimeData.search_evidence, "competition_context") ? "已补充竞争与份额类搜索" : "竞争格局搜索仍待补齐"} |
| 政策专项搜索 | ${policyContextStatus} | ${hasSearchEvidence(runtimeData.search_evidence, "policy_context") ? "已补充政策/监管专项搜索" : "政策专项搜索仍待补齐"} |
| 资金面搜索 | ${moneyFlowContextStatus} | ${hasSearchEvidence(runtimeData.search_evidence, "money_flow_context") ? "已补充资金与持仓类搜索" : "资金面独立搜索仍待补齐"} |
| 龙头验证 | ${leaders.length ? "📈有龙头" : "⚪缺样本"} | ${leadNames || "暂无"} |
| 催化剂验证 | ${catalystStatus} | ${hasSearchEvidence(runtimeData.search_evidence, "catalyst_context") ? "已补充外部催化剂搜索" : "外部催化剂搜索仍待补齐"} |
| 方向判断 | ${rating.icon}${rating.label} | ${normalized.stage_signal.summary} |

## 一、宏观与赛道环境

**当前只完成了结构化赛道定位，宏观、政策和监管证据链仍是明确缺口。**
*关键问题：当前板块走强，究竟来自真实产业景气，还是来自局部情绪扩散？*

**[事实]** 当前研究对象为 ${sector.sector_name || sector.sector_id}，板块类型为 ${normalized.sector_type_label}（东方财富板块K线, ${barStats.latest_trading_day || runtimeData.request.target_date}）。

${macroEvidence}

${industryTrendSearchBlock}

${competitionSearchBlock}

${policySearchBlock}

${moneyFlowContextSearchBlock}

## 二、概念分类与数据

**板块广度显示这是一个“有龙头、但仍有分化”的近期结构，适合跟踪而不是假设全板块无差别共振。**
*关键问题：这轮上涨是板块整体扩散，还是少数龙头在维持表观强度？*

### 1. 概念分类

${similarSectorLine}
${similarCount ? `\n\n${renderSimilarSectorsComparisonTable(normalized.similar_sectors)}\n` : ""}
**[事实]** 板块指数最新点位为 ${formatNumber(barStats.latest_close)}，区间涨跌幅 ${formatPercent(barStats.period_change_pct)}，最新单日涨跌幅 ${formatPercent(barStats.latest_change_pct)}（东方财富板块K线, ${barStats.latest_trading_day || runtimeData.request.target_date}）。

**[事实]** ${breadthSummary}（东方财富板块成分股, ${sectorConstituents?.latest_date || runtimeData.request.target_date}）。

**[推演]** 如果指数继续维持上行而成分股正收益占比无法进一步扩散，那么本轮更像“龙头带队”的高位分化，而非全赛道系统性抬升。

### 2. 龙头对比

${renderLeaderTable(leaders)}

### 3. 龙头行情与估值快照

${renderLeaderFundamentalsTable(normalized.leader_fundamentals)}

### 4. 板块与龙头资金流

${renderSectorMoneyFlowNarrative(normalized)}

**[推演]** 当前强势成分股主要集中在 ${leadNames || "暂无"}；若后续只有龙头继续冲高而中后排跟不上，板块情绪可能会先于指数转弱。

## 三、核心逻辑与结构观察

**当前结构化证据包含板块指数与成分股广度${marketSnapshotReady ? "、龙头行情与估值（东方财富）" : ""}${moneyFlowReady ? "、龙头个股资金流" : ""}${normalized.similar_sectors?.length ? "、相似赛道映射" : ""}；结论置信度仍取决于后续搜索与行情验证。**
*关键问题：当前上行趋势能够继续扩散，还是已经接近高位分歧？*

### 1. 核心驱动逻辑

**[事实]** 指数短均值 / 中均值分别为 ${formatNumber(barStats.short_average)} / ${formatNumber(barStats.medium_average)}，近端支撑 / 阻力分别为 ${formatNumber(barStats.support)} / ${formatNumber(barStats.resistance)}（东方财富板块K线, ${barStats.latest_trading_day || runtimeData.request.target_date}）。

**[推演]** 当最新点位位于短中期均值上方时，说明趋势仍偏强；但如果后续无法有效突破 ${formatNumber(barStats.resistance)}，板块更可能进入高位震荡，而不是继续顺畅扩散。

### 2. 近期结构与扩散观察

**[事实]** 基于当前研究窗口，近期结构标签为“${normalized.stage_signal.label}”，样本内领涨龙头为 ${leadNames || "暂无"}，相对偏弱的成分股为 ${laggardNames || "暂无"}（东方财富板块K线与板块成分股, ${barStats.latest_trading_day || runtimeData.request.target_date} / ${sectorConstituents?.latest_date || runtimeData.request.target_date}）。

**[推演]** 这只代表当前窗口下的近期结构，而不是完整产业周期结论；如果弱势成分股继续扩大，当前偏强观察会快速转成“指数未死、板块先分化”的结构。

## 四、反面审查与风险

**当前最强反面论据不是指数本身，而是外部证据和结构化支持数据都还不够完整。**
*关键问题：如果我们错了，最可能错在把局部强势误读成赛道共振吗？*

${renderRiskTable(runtimeData)}

**反面审查评级**: 🟡有弱点

${riskEvidence}

### 逻辑失效

${renderInvalidationTable()}

## 五、方向判断与情景

**当前更适合作为偏强赛道跟踪，而不是高置信度追涨结论。**
*关键问题：哪一个变量最可能改变方向判断？*

### 催化剂日历

${renderCatalystTable(runtimeData)}

### 情景矩阵

${renderScenarioTable(runtimeData)}

**[推演]** 当前基础判断是“${rating.label}”，因为指数结构${barStats.trend === "up" ? "偏强" : "待验证"}${marketSnapshotReady ? "、龙头东方财富行情快照已部分补齐" : "、龙头行情估值快照仍需继续补齐"}${moneyFlowReady ? "、龙头个股资金流已有结构化摘要" : "、板块级资金流不可用且龙头资金流仍需交叉验证"}${hasSearchEvidence(runtimeData.search_evidence, "macro_context") ? "、外部搜索已部分执行" : "、外部搜索仍待执行"}；所以任何更激进的结论都必须等待后续证据链补完。

${catalystEvidence}

**纠错状态**: 当前 preview 版只记录显式冲突修正；本次未新增纠错记录，已知缺口已明确写成降级项。

_本报告仅供研究参考，不构成投资建议。投资者应独立判断并承担投资风险。_`;
}

export function buildSectorResearchResult(runtimeData, references) {
  const degradations = buildDegradations(runtimeData);
  const rating = buildRating(runtimeData, degradations);
  const steps = buildStepResults(runtimeData, references, degradations, rating);
  const reportMarkdown = renderReport(runtimeData, rating, degradations);
  const reportSvg = renderSectorResearchSvg(runtimeData, rating);
  const qualityGate = validateSectorResearchArtifacts({
    reportMarkdown,
    reportSvg,
    searchEvidence: runtimeData.search_evidence
  });
  const orchestration = buildResearchOrchestrationAlignment(references);

  return withResearchHardening({
    flow: "sector-research",
    status: degradations.length ? "completed_with_degradation" : "completed",
    sector: runtimeData.sector,
    search_evidence: runtimeData.search_evidence,
    coverage: {
      step_count: steps.length,
      completed_steps: steps.filter((item) => item.status === "completed").length,
      degraded_steps: steps.filter((item) => item.status === "degraded").length,
      completed_step_count: steps.filter((item) => item.status === "completed").length,
      degraded_step_count: steps.filter((item) => item.status === "degraded").length,
      prompt_asset_count: references.prompt_assets.length,
      orchestration_asset_count: references.orchestration_assets.length,
      svg_enabled: true,
      quality_gate_status: qualityGate.status
    },
    degradations,
    orchestration,
    quality_gate: qualityGate,
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
    steps,
    report_markdown: reportMarkdown,
    report_svg: reportSvg
  }, {
    searchRuntime: runtimeData.search_evidence,
    reportMode: "markdown_svg_preview",
    parityStage: "svg_gated_preview"
  });
}
