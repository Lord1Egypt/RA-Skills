import { buildResearchSearchRuntimeContract } from "./search_runtime.mjs";

export function buildResearchHardeningContract({
  searchRuntime,
  reportMode = "markdown_first_preview",
  parityStage = "preview"
} = {}) {
  return {
    report_mode: reportMode,
    parity_stage: parityStage,
    search_runtime: searchRuntime ?? buildResearchSearchRuntimeContract()
  };
}

export function withResearchHardening(result, {
  searchRuntime,
  reportMode,
  parityStage
} = {}) {
  return {
    ...result,
    hardening: buildResearchHardeningContract({
      searchRuntime,
      reportMode,
      parityStage
    })
  };
}
