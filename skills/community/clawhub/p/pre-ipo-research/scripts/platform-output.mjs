import { PLATFORMS } from "./platforms.mjs";
import { timestamp, number, money } from "./jarsy-output.mjs";

const pct = (value) => number(value, { suffix: "%", digits: 5 });
const count = (value) => number(value, { digits: 0 });
const quote = (value, unit) => value == null ? "未提供" : number(value, { digits: 8 }) + " " + (unit || "未提供币种");
const value = (item) => item ?? "未提供";

export function printFreshness(platform, data = {}) {
  if (platform === "hiive") {
    console.log("更新方式：手动快照（不使用五分钟平台的延迟阈值）");
    console.log("来源更新时间：" + timestamp(data.sourceUpdatedAt));
    console.log("本站导入时间：" + timestamp(data.lastSuccessfulAt));
  } else {
    console.log("行情获取时间（最近成功快照）：" + timestamp(data.lastSuccessfulAt));
    if (platform === "polymarket") console.log("话题发现时间：" + timestamp(data.lastDiscoveryAt));
    if (data.stale) console.log("⚠ 数据延迟：当前返回最近成功快照，不代表实时行情。");
  }
  if (!data.lastSuccessfulAt) console.log("未提供成功导入时间；不能确认当前数据新鲜度。");
}

function printIndustries(data) {
  if (data.industries?.length) console.log("行业：" + data.industries.map((item) => typeof item === "string" ? item : item.industry + " " + count(item.count)).join("；"));
}

export function printPlatformSummary(platform, data) {
  console.log("数据源：" + PLATFORMS[platform].name + "（经 Pre-IPO Observer 保存）");
  printFreshness(platform, data);
  if (platform === "hyperliquid") {
    console.log("分类内市场：" + count(data.total) + "；未下架：" + count(data.activeCount) + "；已下架：" + count(data.delistedCount) + "；已移出分类：" + count(data.removedCount));
    for (const row of data.currencies || []) {
      console.log("结算币种 " + row.currency + "：24 小时成交量 " + quote(row.volume24h, row.currency) + "（覆盖 " + count(row.volumeCoverage) + "/" + count(row.marketCount) + "）；持仓名义金额 " + quote(row.openInterestNotional, row.currency) + "（覆盖 " + count(row.openInterestCoverage) + "/" + count(row.marketCount) + "）");
    }
    if (data.operators?.length) console.log("运营方：" + data.operators.map((item) => item.name + " (" + item.dex + ")").join("；"));
  } else if (platform === "prestocks") {
    console.log("在列产品：" + count(data.total) + "；特殊提示：" + count(data.attentionCount) + "；移出列表：" + count(data.removedCount));
    console.log("累计成交量：" + money(data.cumulativeVolumeUSD) + "（覆盖 " + count(data.volumeCoverage) + "/" + count(data.total) + "）；代币市值合计：" + money(data.marketCapUSD) + "（覆盖 " + count(data.marketCapCoverage) + "/" + count(data.total) + "；不是公司估值合计）");
  } else if (platform === "polymarket") {
    console.log("公司：" + count(data.companyCount) + "（当前 " + count(data.currentCompanyCount) + "）；话题：" + count(data.topicCount) + "（当前 " + count(data.currentTopicCount) + "）；唯一预测市场：" + count(data.marketCount) + "（当前 " + count(data.currentMarketCount) + "）");
    console.log("唯一当前市场汇总：24 小时成交量 " + money(data.volume24h) + "（覆盖 " + count(data.volumeCoverage) + "/" + count(data.currentMarketCount) + "）；流动性 " + money(data.liquidity) + "（覆盖 " + count(data.liquidityCoverage) + "/" + count(data.currentMarketCount) + "）");
    console.log("不将公司卡片金额再次相加；同一市场可能关联多个公司。");
    if (data.topicTypes?.length) console.log("话题类型：" + data.topicTypes.join(" / "));
  } else if (platform === "hiive") {
    console.log("Hiive50 当前成分：" + count(data.listedCount) + "；保留记录总数：" + count(data.total) + "；已移出：" + count(data.removedCount) + "；价格覆盖：" + count(data.marketCoverage) + "/" + count(data.listedCount));
  }
  printIndustries(data);
}

function printWarnings(asset) {
  if (asset.warningCheckFailed) console.log("⚠ 风险提示核验延迟；仍保留之前提示，不能解释为风险解除。");
  console.log("风险提示核验时间：" + timestamp(asset.warningsCheckedAt));
  for (const warning of asset.warnings || []) {
    const expired = warning.deadlineAt && Date.parse(warning.deadlineAt) <= Date.now();
    console.log("⚠ 平台提示：" + value(warning.summaryZh) + (expired ? "【期限已过，请核验】" : ""));
    console.log("提示原文：" + value(warning.original));
    console.log("公告期限：" + value(warning.deadlineAt) + "；核验：" + timestamp(warning.checkedAt));
    console.log("提示来源：" + value(warning.sourceUrl));
  }
}

function printTopics(topics, complete) {
  console.log(complete ? "关联话题（完整详情）：" : "最活跃话题摘要（最多三个；完整话题请查询 detail）：");
  for (const topic of topics || []) {
    console.log("\n话题 " + topic.eventId + "：" + (topic.titleZh || topic.title));
    console.log("原始标题：" + value(topic.title) + "；类型：" + value(topic.topicType) + "；中文整理状态：" + value(topic.enrichmentStatus));
    console.log("源状态：active=" + value(topic.active) + "；closed=" + value(topic.closed) + "；archived=" + value(topic.archived));
    if (topic.summaryZh) console.log("中文摘要（衍生；不替代原始结算规则）：" + topic.summaryZh);
    if (topic.description) console.log("话题原文：" + topic.description);
    console.log("话题来源：" + value(topic.sourceUrl) + "；来源更新时间：" + timestamp(topic.updatedAt));
    for (const market of topic.markets || []) {
      console.log("  预测市场 " + market.marketId + "：" + market.question);
      if (market.groupItemTitle) console.log("  分组选项：" + market.groupItemTitle);
      console.log("  选项市场隐含概率：" + (market.outcomes || []).map((outcome) => outcome.label + " " + pct(outcome.probabilityPct)).join(" / "));
      console.log("  状态：active=" + value(market.active) + "；closed=" + value(market.closed) + "；archived=" + value(market.archived) + "；来源结算状态=" + value(market.resolutionStatus));
      console.log("  24 小时成交量：" + money(market.volume24h) + "；流动性：" + money(market.liquidity));
      console.log("  API 市场结束时间（原值；不等同于规则截止条件）：" + value(market.apiEndDate));
      if (complete) {
        console.log("  原始规则：" + value(market.description));
        console.log("  结算依据：" + value(market.resolutionSource));
      }
      console.log("  来源：" + value(market.sourceUrl) + "；获取：" + timestamp(market.fetchedAt));
    }
  }
  console.log("概率不代表客观发生概率；不同市场不合并概率。0%/100% 不自动确认结算，未关闭不承诺实际可交易。");
}

export function printPlatformAsset(platform, asset, base, { detail = false } = {}) {
  const id = asset.assetId ?? asset.companyId;
  console.log("\n" + value(asset.companyName) + " (" + value(id) + ")");
  console.log("行业：" + value(asset.industry));
  if (asset.status) console.log("来源状态：" + asset.status);
  console.log("记录获取时间：" + timestamp(asset.fetchedAt));
  if (detail && asset.description) console.log("简介（保存的来源内容）：" + asset.description);
  if (platform === "hyperliquid") {
    const currency = asset.settlementCurrency;
    console.log("完整市场：" + value(asset.assetId) + "；运营方：" + value(asset.operator) + " (" + value(asset.dex) + ")；结算币种：" + value(currency));
    console.log("标记价格：" + quote(asset.markPx, currency) + "；24 小时涨跌：" + pct(asset.change24hPct));
    console.log("24 小时成交量：" + quote(asset.volume24h, currency) + "；持仓数量：" + number(asset.openInterest) + "；持仓名义金额：" + quote(asset.openInterestNotional, currency));
    console.log("每小时资金费率：" + pct(asset.fundingRate == null ? null : Number(asset.fundingRate) * 100) + "；最大杠杆：" + number(asset.maxLeverage));
    if (detail) console.log("预言机价格：" + quote(asset.oraclePx, currency) + "；中间价：" + quote(asset.midPx, currency) + "；前日价：" + quote(asset.prevDayPx, currency) + "；保证金模式：" + value(asset.marginMode));
    console.log("合约价格按来源计价单位展示，不等同于公司融资估值；未下架不代表可成交。");
  } else if (platform === "prestocks") {
    console.log("Solana mint：" + value(asset.assetId) + "；代号：" + value(asset.symbol));
    console.log("代币价格：" + money(asset.tokenPrice) + "；参考价格：" + money(asset.markPrice) + "；折溢价：" + pct(asset.premiumPct));
    console.log("隐含公司估值：" + money(asset.impliedValuation) + "；参考公司估值：" + money(asset.markValuation) + "；代币市值：" + money(asset.marketCapUSD));
    console.log("累计成交量：" + money(asset.cumulativeVolumeUSD) + "；持有人数：" + count(asset.holderCount) + "；30 天涨跌：" + pct(asset.change30dPct));
    printWarnings(asset);
    if (detail) {
      console.log("交易笔数：" + count(asset.txnCount) + "；流通供应：" + number(asset.circulatingSupply) + "；总供应：" + number(asset.totalSupply));
      console.log("生效基准价格：" + money(asset.effectiveBaselinePrice) + "；生效基准公司估值（十亿美元）：" + number(asset.effectiveBaselineValuationBillions) + "；单位调整系数：" + number(asset.unitFactor));
      for (const event of asset.basisEvents || []) console.log("单位调整事件：" + event.kind + "；生效 " + value(event.effectiveAt) + "；系数 " + number(event.factor));
    }
    console.log("累计成交量不是 24 小时成交量；30 天涨跌不是历史估值回报；代币市值、隐含估值与融资估值不同。");
  } else if (platform === "hiive") {
    console.log("来源更新时间：" + timestamp(asset.sourceUpdatedAt));
    console.log("Hiive Price：" + money(asset.hiivePrice) + "；近 3 个月涨跌：" + pct(asset.change3mPct));
    console.log("最高买价：" + money(asset.highestBid) + "；最低卖价：" + money(asset.lowestAsk));
    console.log("活跃卖单：" + count(asset.activeListings) + "；活跃买单：" + count(asset.activeBids));
    console.log("Hiive Price 为平台模型估算的每证券参考价格，不是公司估值；缺失报价不等于零价或不可交易。");
    if (asset.companyUrl) console.log("Hiive 公司页：" + asset.companyUrl);
  } else if (platform === "polymarket") {
    console.log("实体类型：company（公司聚合，不是可交易证券）");
    if (asset.topicCount !== undefined) console.log("话题：" + count(asset.topicCount) + "；当前话题：" + count(asset.currentTopicCount));
    console.log("归属证据：" + value(asset.sourceEvidence) + "；公司中文整理状态：" + value(asset.enrichmentStatus));
    printTopics(detail ? asset.topics : asset.topTopics, detail);
  }
  if (asset.sourceUrl) console.log("原始来源：" + asset.sourceUrl);
  console.log("观察站详情：" + new URL("/platforms/" + platform + "/assets/" + encodeURIComponent(id), base).href);
  if (asset.reportHref) console.log("已登记研报：" + new URL(asset.reportHref, base).href + "（静态版本，使用 report 阅读截至日期）");
}

export function printPlatformList(platform, data, base) {
  printPlatformSummary(platform, data.summary || {});
  console.log("\n匹配 " + count(data.total) + " 个" + (platform === "polymarket" ? "公司" : "标的") + "；第 " + data.page + " 页，每页 " + data.pageSize + " 个；本页 " + data.items.length + " 个。");
  if (!data.items.length) console.log("没有匹配结果。");
  if (platform === "prestocks") console.log("排序口径：常规产品优先、特殊提示置后，组内按所选指标排序。");
  for (const asset of data.items) printPlatformAsset(platform, asset, base);
  if (data.total > data.items.length) console.log("结果分页展示；未遍历所有页前不代表完整清单。");
}
