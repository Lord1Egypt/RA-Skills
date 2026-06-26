import {
  assertNoFields,
  assertSingleSectorInput,
  buildCommonRequest,
  isMain,
  parseCommonArgs,
  runCli
} from "../core/cli.mjs";
import { getDefaultResearchTargetDate } from "../core/runtime.mjs";
import { loadSectorResearchReferences } from "./sector_research/reference_assets.mjs";
import {
  DEFAULT_SECTOR_RESEARCH_WINDOW,
  fetchSectorResearchRuntime
} from "./sector_research/runtime.mjs";
import { buildSectorResearchResult } from "./sector_research/report_builder.mjs";

function hasValue(value) {
  return value !== undefined && value !== null && value !== "";
}

function buildNeedsInputResponse({ prompt, reason, missing, attempted }) {
  return {
    flow: "sector-research",
    status: "needs_input",
    prompt,
    reason,
    missing,
    ...(attempted ? { attempted } : {})
  };
}

function validateSectorResearchRequest(request) {
  const hasSectorId = hasValue(request.sector_id);
  const hasSectorName = hasValue(request.sector_name);

  if (!hasSectorId && !hasSectorName) {
    return buildNeedsInputResponse({
      prompt: "请先提供一个板块名称或已解析的板块 ID。",
      reason: "missing_sector_identifier",
      missing: ["sector"]
    });
  }

  try {
    assertSingleSectorInput(request);
  } catch (error) {
    return buildNeedsInputResponse({
      prompt: error.message,
      reason: "invalid_sector_identifier",
      missing: ["sector"],
      attempted: {
        sector_id: request.sector_id,
        sector_name: request.sector_name
      }
    });
  }
  return null;
}

export async function runSectorResearchFlow(values) {
  const request = buildCommonRequest(values);

  assertNoFields(
    request,
    ["instrument_id", "exchange_id", "instrument_name", "query", "target_time"],
    "sector-research only supports one sector selector plus optional --target-date and --visual-days-len."
  );

  const normalizedRequest = {
    ...request,
    target_date: request.target_date ?? getDefaultResearchTargetDate(),
    visual_days_len: request.visual_days_len ?? DEFAULT_SECTOR_RESEARCH_WINDOW,
    is_realtime: true
  };

  const needsInput = validateSectorResearchRequest(normalizedRequest);
  if (needsInput) {
    return needsInput;
  }

  try {
    const [references, runtimeData] = await Promise.all([
      loadSectorResearchReferences(),
      fetchSectorResearchRuntime(normalizedRequest)
    ]);

    return buildSectorResearchResult(runtimeData, references);
  } catch (error) {
    if (error?.code === "SECTOR_NEEDS_INPUT" && error?.detail) {
      return buildNeedsInputResponse(error.detail);
    }
    throw error;
  }
}

if (isMain(import.meta)) {
  await runCli(async () => {
    const { values } = parseCommonArgs();
    return runSectorResearchFlow(values);
  });
}
