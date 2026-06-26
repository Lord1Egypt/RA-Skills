import {
  assertNoFields,
  assertSingleInstrumentInput,
  assertSingleSectorInput,
  assertTargetDate,
  buildCommonRequest,
  isMain,
  parseCommonArgs,
  runCli
} from "../core/cli.mjs";
import { assertProductEnabled } from "../core/rollout.mjs";
import { getInstrumentProfile } from "../products/instrument_profile.mjs";
import { getPriceSnapshot } from "../products/price_snapshot.mjs";
import { getBarSeries } from "../products/bar_series.mjs";
import { getFinanceContext } from "../products/finance_context.mjs";
import { getFinanceAnalysisContext } from "../products/finance_analysis_context.mjs";
import { getFinanceReportStatus } from "../products/finance_report_status.mjs";
import { getFinanceBasicIndicators } from "../products/finance_basic_indicators.mjs";
import { getFinanceValuationDetail } from "../products/finance_valuation_detail.mjs";
import { getFinanceProfitForecast } from "../products/finance_profit_forecast.mjs";
import { getFinanceIndustryRank } from "../products/finance_industry_rank.mjs";
import { getHolderContext } from "../products/holder_context.mjs";
import { getChipDistribution } from "../products/chip_distribution.mjs";
import { getPriceLevels } from "../products/price_levels.mjs";
import { getImportantNews } from "../products/important_news.mjs";
import { getHighFrequencyNews } from "../products/high_frequency_news.mjs";
import { getUnusualMovementContext } from "../products/unusual_movement_context.mjs";
import { getInstrumentConcepts } from "../products/instrument_concepts.mjs";
import { getMoneyFlow } from "../products/money_flow.mjs";
import { getLushanShadow } from "../products/lushan_shadow.mjs";
import { getLushan4Season } from "../products/lushan_4season.mjs";
import { getShuanglun } from "../products/shuanglun.mjs";
import { getLiumai } from "../products/liumai.mjs";
import { getSmartMoney } from "../products/smart_money.mjs";
import { getFinanceScore } from "../products/finance_score.mjs";
import { getResolveSector } from "../products/resolve_sector.mjs";
import { getSimilarSectors } from "../products/similar_sectors.mjs";
import { getSectorConstituents } from "../products/sector_constituents.mjs";
import { getSectorPerformance } from "../products/sector_performance.mjs";

const productHandlers = {
  instrument_profile: getInstrumentProfile,
  price_snapshot: getPriceSnapshot,
  bar_series: getBarSeries,
  finance_context: getFinanceContext,
  finance_analysis_context: getFinanceAnalysisContext,
  finance_report_status: getFinanceReportStatus,
  finance_basic_indicators: getFinanceBasicIndicators,
  finance_valuation_detail: getFinanceValuationDetail,
  finance_profit_forecast: getFinanceProfitForecast,
  finance_industry_rank: getFinanceIndustryRank,
  holder_context: getHolderContext,
  chip_distribution: getChipDistribution,
  price_levels: getPriceLevels,
  unusual_movement_context: getUnusualMovementContext,
  instrument_concepts: getInstrumentConcepts,
  money_flow: getMoneyFlow,
  lushan_shadow: getLushanShadow,
  lushan_4season: getLushan4Season,
  shuanglun: getShuanglun,
  liumai: getLiumai,
  smart_money: getSmartMoney,
  finance_score: getFinanceScore,
  resolve_sector: getResolveSector,
  similar_sectors: getSimilarSectors,
  sector_constituents: getSectorConstituents,
  sector_performance: getSectorPerformance,
  important_news: getImportantNews,
  high_frequency_news: getHighFrequencyNews
};

const STOCK_PRODUCTS = new Set([
  "instrument_profile",
  "price_snapshot",
  "bar_series",
  "finance_context",
  "finance_analysis_context",
  "finance_report_status",
  "finance_basic_indicators",
  "finance_valuation_detail",
  "finance_profit_forecast",
  "finance_industry_rank",
  "holder_context",
  "chip_distribution",
  "price_levels",
  "instrument_concepts",
  "money_flow",
  "unusual_movement_context",
  "lushan_shadow",
  "lushan_4season",
  "shuanglun",
  "liumai",
  "smart_money",
  "finance_score"
]);

function validateProductRequest(product, request) {
  if (STOCK_PRODUCTS.has(product)) {
    assertSingleInstrumentInput(request);
    assertNoFields(
      request,
      ["sector_id", "sector_name", "query", "target_time"],
      `${product} only supports stock parameters. Do not pass sector, query, or time-cutoff fields.`
    );
    if (product !== "instrument_profile") {
      assertTargetDate(request, product);
    }
    return;
  }

  if (product === "resolve_sector" || product === "similar_sectors") {
    if (!request.query) {
      throw new Error(`${product} requires --query.`);
    }
    assertNoFields(
      request,
      ["instrument_id", "exchange_id", "instrument_name", "sector_id", "sector_name", "target_date", "target_time", "visual_days_len"],
      `${product} only supports --query.`
    );
    return;
  }

  if (product === "sector_constituents" || product === "sector_performance") {
    assertSingleSectorInput(request);
    assertTargetDate(request, product);
    assertNoFields(
      request,
      ["instrument_id", "exchange_id", "instrument_name", "query", "target_time"],
      `${product} only supports one sector selector plus --target-date and optional --visual-days-len.`
    );
    return;
  }

  if (product === "important_news") {
    assertTargetDate(request, product);
    assertNoFields(
      request,
      ["instrument_id", "exchange_id", "instrument_name", "sector_id", "sector_name", "query", "target_time", "visual_days_len"],
      "important_news only supports --target-date."
    );
    return;
  }

  if (product === "high_frequency_news") {
    assertTargetDate(request, product);
    assertNoFields(
      request,
      ["instrument_id", "exchange_id", "instrument_name", "sector_id", "sector_name", "query", "visual_days_len"],
      "high_frequency_news only supports --target-date and optional --target-time."
    );
  }
}

export async function runDataRequest(values) {
  const product = values.product;
  if (!product) {
    throw new Error("Missing required --product option.");
  }

  const handler = productHandlers[product];
  if (!handler) {
    throw new Error(`Unsupported product: ${product}`);
  }

  assertProductEnabled(product);

  const request = buildCommonRequest(values);
  validateProductRequest(product, request);
  return handler(request);
}

if (isMain(import.meta)) {
  await runCli(async () => {
    const { values } = parseCommonArgs();
    return runDataRequest(values);
  });
}
