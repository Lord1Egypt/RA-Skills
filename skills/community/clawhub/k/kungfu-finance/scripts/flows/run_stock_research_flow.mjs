import {
  assertNoFields,
  assertSingleInstrumentInput,
  buildCommonRequest,
  isMain,
  parseCommonArgs,
  runCli
} from "../core/cli.mjs";
import { getDefaultResearchTargetDate } from "../core/runtime.mjs";
import { loadStockResearchReferences } from "./stock_research/reference_assets.mjs";
import {
  DEFAULT_STOCK_RESEARCH_WINDOW,
  fetchStockResearchRuntime
} from "./stock_research/runtime.mjs";
import { buildStockResearchResult } from "./stock_research/report_builder.mjs";

function hasValue(value) {
  return value !== undefined && value !== null && value !== "";
}

function buildNeedsInputResponse({ prompt, reason, missing, attempted }) {
  return {
    flow: "stock-research",
    status: "needs_input",
    prompt,
    reason,
    missing,
    ...(attempted ? { attempted } : {})
  };
}

function validateStockResearchRequest(request) {
  const hasName = hasValue(request.instrument_name);
  const hasPair = hasValue(request.instrument_id) || hasValue(request.exchange_id);

  if (!hasName && !hasPair) {
    return buildNeedsInputResponse({
      prompt: "请先提供一个要研究的 A 股标的，可以使用股票名称，或者代码加交易所。",
      reason: "missing_stock_identifier",
      missing: ["instrument"]
    });
  }

  try {
    assertSingleInstrumentInput(request);
  } catch (error) {
    return buildNeedsInputResponse({
      prompt: error.message,
      reason: "invalid_stock_identifier",
      missing: ["instrument"],
      attempted: {
        instrument_id: request.instrument_id,
        exchange_id: request.exchange_id,
        instrument_name: request.instrument_name
      }
    });
  }
  return null;
}

export async function runStockResearchFlow(values) {
  const request = buildCommonRequest(values);

  assertNoFields(
    request,
    ["sector_id", "sector_name", "query", "target_time"],
    "stock-research only supports one stock selector plus optional --target-date and --visual-days-len."
  );

  const normalizedRequest = {
    ...request,
    target_date: request.target_date ?? getDefaultResearchTargetDate(),
    visual_days_len: request.visual_days_len ?? DEFAULT_STOCK_RESEARCH_WINDOW,
    is_realtime: true
  };

  const needsInput = validateStockResearchRequest(normalizedRequest);
  if (needsInput) {
    return needsInput;
  }

  const [references, runtimeData] = await Promise.all([
    loadStockResearchReferences(),
    fetchStockResearchRuntime(normalizedRequest)
  ]);

  return buildStockResearchResult(runtimeData, references);
}

if (isMain(import.meta)) {
  await runCli(async () => {
    const { values } = parseCommonArgs();
    return runStockResearchFlow(values);
  });
}
