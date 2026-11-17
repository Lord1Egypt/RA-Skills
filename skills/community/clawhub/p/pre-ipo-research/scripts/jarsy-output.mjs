function timestamp(value) {
  if (!value) return "未提供";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return String(value);
  return `${new Intl.DateTimeFormat("zh-CN", {
    dateStyle: "medium",
    timeStyle: "medium",
    timeZone: "Asia/Shanghai",
    hour12: false,
  }).format(date)}（中国标准时间；${date.toISOString()}）`;
}

function number(value, { suffix = "", digits = 2 } = {}) {
  if (value === null || value === undefined) return "未提供";
  const numeric = Number(value);
  if (!Number.isFinite(numeric)) return String(value);
  return `${new Intl.NumberFormat("en-US", { maximumFractionDigits: digits }).format(numeric)}${suffix}`;
}

function money(value, { millions = false } = {}) {
  if (value === null || value === undefined) return "未提供";
  return millions ? `US$${number(value, { suffix: "m" })}` : `US$${number(value)}`;
}

function tradeStatus(asset) {
  const buy = asset.buyActive ? "可买" : "不可买";
  const sell = asset.sellActive ? "可卖" : "不可卖";
  return `${buy} / ${sell}`;
}

function relativeLow(value) {
  if (value === null || value === undefined || !Number.isFinite(Number(value))) return "未提供";
  const numeric = Number(value);
  if (numeric === 0) return "与历史低点持平";
  return numeric > 0 ? `较历史低点 +${number(numeric, { suffix: "%" })}` : `低于历史低点 ${number(Math.abs(numeric), { suffix: "%" })}`;
}

function printSummary(data) {
  const stats = data.stats || {};
  console.log("数据源：Jarsy（Private Equity Live 与 Presale 点时快照）");
  console.log(`数据更新时间（最近成功导入）：${timestamp(data.lastImport?.importedAt)}`);
  console.log(`标的记录最新时间（全体最大值）：${timestamp(data.latestSourceRecordAt)}`);
  console.log(`标的：${number(stats.total, { digits: 0 })}；Live：${number(stats.liveCount, { digits: 0 })}；Presale：${number(stats.presaleCount, { digits: 0 })}`);
  console.log(`可买：${number(stats.buyEnabledCount, { digits: 0 })}；可卖：${number(stats.sellEnabledCount, { digits: 0 })}`);
  if (stats.categorizedCount !== undefined) console.log(`已分类：${number(stats.categorizedCount, { digits: 0 })}`);
  if (stats.returnCoverageCount !== undefined) console.log(`可计算历史估值区间回报：${number(stats.returnCoverageCount, { digits: 0 })}`);
  if (stats.newInvestableCount !== undefined) console.log(`新上线可交易：${number(stats.newInvestableCount, { digits: 0 })}`);
  if (stats.activeVolumeCount !== undefined) console.log(`成交量覆盖：${number(stats.activeVolumeCount, { digits: 0 })}（Jarsy 当前 volume）`);
  if (Array.isArray(data.stages) && data.stages.length) {
    console.log(`阶段分布：${data.stages.map((entry) => `${entry.stage} ${entry.count}`).join("；")}`);
  }
  if (Array.isArray(data.valuations) && data.valuations.length) {
    console.log("估值 Top 10：");
    for (const [index, item] of data.valuations.entries()) {
      console.log(`  ${index + 1}. ${item.companyName} (${item.token}) — ${money(item.valuationMillions, { millions: true })}`);
    }
  }
  console.log("说明：价格、估值和交易状态为 Jarsy 快照，不构成投资建议。");
}

function printAssets(data) {
  console.log(`匹配 ${number(data.total, { digits: 0 })} 个标的；第 ${data.page} 页，每页 ${data.pageSize} 个。`);
  if (!Array.isArray(data.items) || data.items.length === 0) {
    console.log("没有匹配结果。");
    return;
  }
  for (const [index, asset] of data.items.entries()) {
    const identity = asset.underlyingTicker || asset.underlyingName;
    console.log(`\n${(data.page - 1) * data.pageSize + index + 1}. ${asset.companyName} (${asset.token})`);
    console.log(`   市场/阶段：${asset.market} / ${asset.stage}${identity ? `；底层标的：${identity}` : ""}`);
    if (asset.primaryCategory) console.log(`   分类（模型衍生）：${asset.primaryCategory}`);
    if (Array.isArray(asset.tags) && asset.tags.length) console.log(`   标签（模型衍生）：${asset.tags.join(" / ")}`);
    console.log(`   交易状态：${tradeStatus(asset)}；价格：${money(asset.priceUsd)}；估值：${money(asset.valuationMillions, { millions: true })}`);
    if (asset.valuationVsHistoricalLowPct !== null && asset.valuationVsHistoricalLowPct !== undefined) console.log(`   当前估值位置：${relativeLow(asset.valuationVsHistoricalLowPct)}`);
    if (asset.valuationReturnPct !== null && asset.valuationReturnPct !== undefined) {
      console.log(`   历史估值区间回报：${number(asset.valuationReturnPct, { suffix: "%" })}（${asset.valuationLowLabel || "低点"} ${money(asset.valuationLowMillions, { millions: true })} → ${asset.valuationHighLabel || "高点"} ${money(asset.valuationHighMillions, { millions: true })}）`);
    }
    console.log(`   成交量：${money(asset.volumeUsd)}；标的记录更新时间：${timestamp(asset.sourceUpdatedAt)}`);
    if (asset.firstSeenAt) console.log(`   观察站首次发现：${timestamp(asset.firstSeenAt)}${asset.isNewlyDiscovered ? "；新上线可交易" : ""}`);
    if (asset.sourceUrl) console.log(`   Jarsy 来源：${asset.sourceUrl}`);
  }
  console.log("\n说明：每项“标的记录更新时间”与全站“数据更新时间”不同；所有数值均为 Jarsy 点时快照，不构成投资建议。");
}

function printDiscoveryAsset(asset, index, signal) {
  console.log(`  ${index + 1}. ${asset.companyName} (${asset.token}) — ${signal(asset)}`);
  console.log(`     市场/阶段：${asset.market} / ${asset.stage}；交易状态：${tradeStatus(asset)}；当前估值：${money(asset.valuationMillions, { millions: true })}`);
  if (asset.primaryCategory) console.log(`     分类：${asset.primaryCategory}${Array.isArray(asset.tags) && asset.tags.length ? `；标签：${asset.tags.join(" / ")}` : ""}`);
  if (asset.sourceUpdatedAt) console.log(`     标的记录更新时间：${timestamp(asset.sourceUpdatedAt)}`);
}

function printDiscovery(data) {
  const sections = [
    ["历史估值回报最高", data.topReturns, (asset) => `历史估值区间回报：${number(asset.valuationReturnPct, { suffix: "%" })}`],
    ["当前低估值", data.lowValuations, (asset) => `当前估值：${money(asset.valuationMillions, { millions: true })}`],
    ["接近历史低点", data.nearHistoricalLows, (asset) => `当前估值位置：${relativeLow(asset.valuationVsHistoricalLowPct)}`],
    ["新上线可交易", data.newInvestable, (asset) => `观察站首次发现：${timestamp(asset.firstSeenAt)}`],
    ["交易最活跃", data.activeTrading, (asset) => `Jarsy 当前成交量：${money(asset.volumeUsd)}`],
  ];

  console.log("数据源：Jarsy（Private Equity Live 与 Presale 点时快照）");
  console.log(`新上线观察窗口：${number(data.newWindowDays, { digits: 0 })} 天；要求当前可买或可卖。`);
  for (const [title, assets, signal] of sections) {
    console.log(`\n${title}：`);
    if (!Array.isArray(assets) || !assets.length) {
      console.log("  暂无可用标的。");
      continue;
    }
    assets.forEach((asset, index) => printDiscoveryAsset(asset, index, signal));
  }
  console.log("\n说明：榜单信号基于 Jarsy 当前快照及公开详情页历史估值，不构成投资建议。");
}

function printDetail(data) {
  console.log("数据源：Jarsy 标的详情页点时抓取");
  console.log(`标的：${data.token}；详情状态：${data.detailStatus || "未提供"}`);
  console.log(`公司：${data.displayName || data.legalName || "未提供"}${data.legalName && data.displayName !== data.legalName ? `（${data.legalName}）` : ""}`);
  console.log(`地点：${data.headquarters || "未提供"}；成立年份：${data.foundedYear || "未提供"}`);
  console.log(`详情页展示估值：${data.displayValuation || "未提供"}`);
  console.log(`详情抓取时间：${timestamp(data.detailFetchedAt)}；来源页面更新时间：${timestamp(data.sourceLastModifiedAt)}`);
  if (data.overview) console.log(`简介：${data.overview}`);
  if (data.overviewZh) console.log(`中文简介（模型衍生）：${data.overviewZh}`);
  if (data.primaryCategory) {
    const tags = Array.isArray(data.tags) ? data.tags : [];
    console.log(`分类（模型衍生）：${data.primaryCategory}${tags.length ? `；标签：${tags.join(" / ")}` : ""}`);
    if (data.classificationReasonZh) console.log(`分类依据：${data.classificationReasonZh}`);
    console.log(`衍生时间：${timestamp(data.enrichmentFetchedAt)}；模型：${data.enrichmentModel || "未提供"}；状态：${data.enrichmentStatus || "未提供"}`);
  }
  if (data.valuationReturnPct !== null && data.valuationReturnPct !== undefined) {
    console.log(`历史估值区间回报：${number(data.valuationReturnPct, { suffix: "%" })}（${data.valuationLowLabel || "低点"} ${money(data.valuationLowMillions, { millions: true })} → ${data.valuationHighLabel || "高点"} ${money(data.valuationHighMillions, { millions: true })}）`);
  }
  if (data.canonicalUrl || data.sourceUrl) console.log(`Jarsy 来源：${data.canonicalUrl || data.sourceUrl}`);
  if (data.chartDataJson) {
    try {
      const chart = JSON.parse(data.chartDataJson);
      console.log(`历史图：${Array.isArray(chart.labels) ? chart.labels.length : 0} 个时间点；${Array.isArray(chart.datasets) ? chart.datasets.map((dataset) => dataset.label).join(" / ") : "未提供"}`);
    } catch {
      console.log("历史图：已保存，但格式暂不可读。");
    }
  }
  console.log("说明：详情页内容与市场价格、估值均为 Jarsy 点时资料；中文简介与分类由模型基于该详情页生成，不构成投资建议。");
}


export { timestamp, number, money, printSummary, printAssets, printDetail, printDiscovery };
