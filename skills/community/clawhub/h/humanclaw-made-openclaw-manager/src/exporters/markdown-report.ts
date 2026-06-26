import { CapabilityFact, CapabilityGraphSummary, CheckpointRecord, DriftViewItem, FocusDigest, RiskViewItem, SessionRecord, SessionMapEntry } from '../types';

const bullet = (items: string[]) => (items.length ? items.map((item) => `- ${item}`).join('\n') : '- none');

export const renderSessionMarkdown = (session: SessionRecord, checkpoint: CheckpointRecord | null) => `# ${session.title}

## Objective
${session.objective}

## Current state
${session.current_state}

## Summary
${session.derived_summary || 'No summary available.'}

## Blockers
${bullet(checkpoint?.blockers || session.blockers)}

## Pending human decisions
${bullet(checkpoint?.pending_human_decisions || session.pending_human_decisions)}

## Next machine actions
${bullet(checkpoint?.next_machine_actions || [])}

## Next human actions
${bullet(checkpoint?.next_human_actions || [])}
`;

export const renderDigestMarkdown = (params: {
  sessionMap: SessionMapEntry[];
  focus: FocusDigest;
  riskView: RiskViewItem[];
  driftView: DriftViewItem[];
}) => {
  const { sessionMap, focus, riskView, driftView } = params;
  return `# OpenClaw Manager Digest

## Session map
${sessionMap.length ? sessionMap.map((entry) => `- ${entry.title} [${entry.current_state}] :: ${entry.recommended_action}`).join('\n') : '- none'}

## Focus queue
${focus.top_items.length ? focus.top_items.map((item) => `- ${item.summary} -> ${item.recommended_action}`).join('\n') : '- none'}

## Promotion queue
${focus.candidate_shadows.length
  ? focus.candidate_shadows
      .map((item) => `- ${item.title} [${item.state}] :: score=${item.promotion_score} :: ${item.pending_reason}`)
      .join('\n')
  : '- none'}

## Risk view
${riskView.length ? riskView.map((item) => `- ${item.title} [${item.risk_kind}] :: ${item.summary}`).join('\n') : '- none'}

## Drift view
${driftView.length ? driftView.map((item) => `- ${item.title} :: stale=${item.stale} summary_drift=${item.summary_drift} desynced=${item.desynced}`).join('\n') : '- none'}
`;
};

export const renderCapabilityMarkdown = (facts: CapabilityFact[], graph: CapabilityGraphSummary) => `# Capability Report

## Graph summary
- generated_at: ${graph.generated_at}
- total_facts: ${graph.total_facts}

## Top scenarios
${graph.top_scenarios.length ? graph.top_scenarios.map((node) => `- ${node.label} :: closure_rate=${node.closure_rate} confidence=${node.confidence}`).join('\n') : '- none'}

## Capability facts
${facts.length
  ? facts
      .map(
        (fact) =>
          `### ${fact.skill_name || fact.workflow_name || fact.fact_id}\n- scenario_signature: ${fact.scenario_signature}\n- closure_type: ${fact.closure_type}\n- style_family: ${fact.style_family || ''}\n- variant_label: ${fact.variant_label || ''}\n- confidence: ${fact.confidence}\n- sample_size: ${fact.sample_size}\n- timestamp: ${fact.timestamp}\n`
      )
      .join('\n')
  : 'No capability facts yet.\n'}
`;
