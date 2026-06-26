import {
  assertNoFields,
  assertSingleInstrumentInput,
  assertTargetDate,
  buildCommonRequest,
  isMain,
  parseCommonArgs,
  runCli
} from "../core/cli.mjs";
import { getBarSeries } from "../products/bar_series.mjs";
import { getChipDistribution } from "../products/chip_distribution.mjs";
import { getPriceLevels } from "../products/price_levels.mjs";
import { getLushanShadow } from "../products/lushan_shadow.mjs";
import { getLushan4Season } from "../products/lushan_4season.mjs";
import { getShuanglun } from "../products/shuanglun.mjs";
import { getLiumai } from "../products/liumai.mjs";
import { getSmartMoney } from "../products/smart_money.mjs";
import { getFinanceScore } from "../products/finance_score.mjs";
import {
  renderCandlestickSvg,
  renderLushanShadowSvg,
  renderLushan4SeasonSvg,
  renderShuanglunSvg,
  renderLiumaiSvg,
  renderSmartMoneySvg,
  renderFinanceScoreSvg
} from "./charts/indicator_chart_renderer.mjs";
import { svgToPng } from "./charts/svg_to_png.mjs";

const CHART_TYPES = new Set([
  "kline",
  "lushan_shadow",
  "lushan_4season",
  "shuanglun",
  "liumai",
  "smart_money",
  "finance_score"
]);

export async function runIndicatorChartFlow(values) {
  const chartType = values["chart-type"];
  if (!chartType) {
    throw new Error("Missing required --chart-type. Choose one of: kline, lushan_shadow, lushan_4season, shuanglun, liumai, smart_money, finance_score.");
  }
  if (!CHART_TYPES.has(chartType)) {
    throw new Error(`Unsupported --chart-type: ${chartType}. Choose one of: ${[...CHART_TYPES].join(", ")}.`);
  }

  const request = buildCommonRequest(values);
  assertSingleInstrumentInput(request);
  assertNoFields(
    request,
    ["sector_id", "sector_name", "query", "target_time"],
    "indicator-chart only supports stock parameters."
  );
  if (chartType !== "finance_score") {
    assertTargetDate(request, `indicator-chart (${chartType})`);
  }

  const withChipPeak = values["with-chip-peak"] === "true" || values["with-chip-peak"] === "1";
  const withPriceLevels = values["with-price-levels"] === "true" || values["with-price-levels"] === "1";

  let annotationsRaw = values["annotations"];
  let annotations = null;
  if (annotationsRaw) {
    try {
      annotations = JSON.parse(annotationsRaw);
    } catch {
      throw new Error("--annotations must be valid JSON: [{date,price,type,label,color}]");
    }
  }

  const instrumentName = request.instrument_name || request.instrument_id || "chart";
  const safeBaseName = `${instrumentName}-${chartType}`.replace(/[^a-zA-Z0-9\u4e00-\u9fff_-]/g, "_");

  let svg;
  let instrument;
  let extra = {};

  if (chartType === "kline") {
    const barResult = await getBarSeries(request);
    instrument = barResult.instrument;
    const options = {};

    const [chipResult, levelsResult] = await Promise.all([
      withChipPeak ? getChipDistribution(request) : null,
      withPriceLevels ? getPriceLevels(request) : null
    ]);

    if (chipResult) options.chipPeak = chipResult.chip_distribution;
    if (levelsResult) options.priceLevels = levelsResult.price_levels;
    if (annotations) options.annotations = annotations;

    svg = renderCandlestickSvg(barResult.bar_window, instrument, options);
  } else if (chartType === "lushan_shadow") {
    const result = await getLushanShadow(request);
    instrument = result.instrument;
    svg = renderLushanShadowSvg(result.lushan_shadow, instrument);
  } else if (chartType === "lushan_4season") {
    const result = await getLushan4Season(request);
    instrument = result.instrument;
    svg = renderLushan4SeasonSvg(result.lushan_4season, instrument);
  } else if (chartType === "shuanglun") {
    const result = await getShuanglun(request);
    instrument = result.instrument;
    svg = renderShuanglunSvg(result.shuanglun, instrument);
  } else if (chartType === "liumai") {
    const result = await getLiumai(request);
    instrument = result.instrument;
    svg = renderLiumaiSvg(result.liumai, instrument);
  } else if (chartType === "smart_money") {
    const result = await getSmartMoney(request);
    instrument = result.instrument;
    svg = renderSmartMoneySvg(result.smart_money, instrument);
  } else if (chartType === "finance_score") {
    const result = await getFinanceScore(request);
    instrument = result.instrument;
    svg = renderFinanceScoreSvg(result.finance_score, instrument);
    extra.finance_score = result.finance_score;
  }

  const paths = await svgToPng(svg, safeBaseName);
  return {
    instrument,
    chart_type: chartType,
    svg_path: paths.svg_path,
    png_path: paths.png_path,
    ...extra
  };
}

if (isMain(import.meta)) {
  await runCli(async () => {
    const { values } = parseCommonArgs({
      options: {
        "chart-type": { type: "string" },
        "with-chip-peak": { type: "string" },
        "with-price-levels": { type: "string" },
        annotations: { type: "string" }
      }
    });
    return runIndicatorChartFlow(values);
  });
}
