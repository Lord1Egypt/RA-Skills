const STABLE_PRODUCTS = new Set([
  "instrument_profile",
  "price_snapshot",
  "bar_series",
  "finance_context",
  "holder_context",
  "chip_distribution",
  "price_levels",
  "finance_basic_indicators",
  "sector_constituents",
  "sector_performance",
  "lushan_shadow",
  "lushan_4season",
  "shuanglun",
  "liumai",
  "smart_money",
  "finance_score"
]);

const EXPERIMENTAL_PRODUCT_MESSAGE =
  "当前公开版只开放已完成后端契约校验的 product。若需继续调试未收口能力，请设置 KUNGFU_ENABLE_EXPERIMENTAL_PRODUCTS=1。";

function experimentalEnabled({ env = process.env } = {}) {
  return env.KUNGFU_ENABLE_EXPERIMENTAL_PRODUCTS === "1";
}

export function assertProductEnabled(product, { env = process.env } = {}) {
  if (STABLE_PRODUCTS.has(product) || experimentalEnabled({ env })) {
    return;
  }

  throw new Error(
    `Product ${product} is not enabled in the current rollout. ${EXPERIMENTAL_PRODUCT_MESSAGE}`
  );
}

export function assertMovementAnalysisEnabled({ env = process.env } = {}) {
  if (experimentalEnabled({ env })) {
    return;
  }

  throw new Error(
    "Flow movement_analysis is not enabled in the current rollout. " +
      EXPERIMENTAL_PRODUCT_MESSAGE
  );
}

export function getStableProducts() {
  return [...STABLE_PRODUCTS];
}
