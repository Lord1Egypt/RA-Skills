function toAssetRef(asset) {
  return {
    path: asset.path,
    title: asset.title
  };
}

export function buildResearchOrchestrationAlignment(references) {
  return {
    source_skill: references.source_skill,
    parity_mode: "contract_migrated_preview",
    architecture: "orchestrator_plus_step_modules",
    strict_step_sequence: true,
    gate_check_required: true,
    debate_required: true,
    pre_conclusion_dialectic: true,
    discovery_correction_protocol: true,
    shared_context_accumulation: true,
    execution_mode: "preview_report_synthesis",
    gate_check_executed: false,
    debate_executed: false,
    pre_conclusion_dialectic_executed: false,
    discovery_correction_protocol_executed: false,
    step_sequence: references.steps.map((item) => item.step_id),
    prompt_assets: references.prompt_assets.map(toAssetRef),
    orchestration_assets: references.orchestration_assets.map(toAssetRef)
  };
}
