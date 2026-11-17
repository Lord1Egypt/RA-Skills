// Portable API capabilities; keep in sync with references and public platform queries.
export const PLATFORM_IDS = ["jarsy", "hyperliquid", "prestocks", "polymarket", "hiive"];
export const VERSION = "1.1.0";
export const DEFAULT_BASE_URL = "https://preipo.polyos.ai";
export const JARSY_REFERRAL_URL = "https://app.jarsy.com/?invite_code=bj6bnz";
export const PLATFORMS = {
  jarsy: {
    name: "Jarsy", identity: "token", cadence: "每日快照",
    sourceUrl: "https://app.jarsy.com/layout/Home",
    metrics: "平台估值、历史估值区间回报、新上线、无固定周期的快照成交量",
    filters: ["market", "stage", "trade", "category", "tag", "new"],
    enums: {
      market: ["live", "presale"],
      stage: ["Live", "Locking Period", "Presale", "Early Access"],
      trade: ["buy_sell", "buy_only", "sell_only", "inactive"],
    },
    sorts: ["valuation_desc", "valuation_asc", "relative_low_asc", "return_desc", "volume_desc", "first_seen_desc", "price_desc", "updated_desc", "name_asc"],
  },
  hyperliquid: {
    name: "Hyperliquid", identity: "完整 dex:symbol", cadence: "五分钟快照",
    sourceUrl: "https://app.hyperliquid.xyz",
    metrics: "标记价格、24 小时涨跌与成交量、持仓名义金额、每小时资金费率；分结算币种",
    filters: ["operator", "industry", "status"],
    enums: { status: ["active", "delisted", "removed", "all"] },
    sorts: ["volume_desc", "change_desc", "oi_desc"],
  },
  prestocks: {
    name: "PreStocks", identity: "Solana mint（区分大小写）", cadence: "五分钟快照",
    sourceUrl: "https://prestocks.com/products",
    metrics: "代币价格与市值、隐含公司估值、折溢价、累计成交量、30 天涨跌、风险提示",
    filters: ["industry", "status"],
    enums: { status: ["listed", "normal", "attention", "removed", "all"] },
    sorts: ["volume_desc", "valuation_asc", "premium_asc", "holders_desc", "change30d_desc"],
  },
  polymarket: {
    name: "Polymarket", identity: "companyId（公司聚合）", cadence: "五分钟行情；话题发现单独计时",
    sourceUrl: "https://polymarket.com",
    metrics: "公司关联话题、各预测选项的市场隐含概率、24 小时成交量、流动性",
    filters: ["industry", "type", "status"],
    enums: { status: ["current", "all"], type: ["ipo", "valuation", "financing", "acquisition", "product", "operations", "other"] },
    sorts: ["volume_desc", "topics_desc"],
  },
  hiive: {
    name: "Hiive", identity: "返回的 UUID 或稳定备用 ID", cadence: "手动快照",
    sourceUrl: "https://app.hiive.com/hiive50",
    metrics: "Hiive50、Hiive Price、近 3 个月涨跌、最高买价、最低卖价、挂单数量",
    filters: ["industry", "status"],
    enums: { status: ["listed", "removed", "all"] },
    sorts: ["name_asc", "change3m_desc", "hiive_price_desc", "orders_desc"],
  },
};

export function endpoint(platform, resource, id) {
  const prefix = platform === "jarsy" ? "/api" : `/api/platforms/${platform}`;
  return resource === "detail" ? `${prefix}/assets/${encodeURIComponent(id)}/detail` : `${prefix}/${resource}`;
}
