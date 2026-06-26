import { CapabilityFact, CapabilityGraphNode, CapabilityGraphSummary, nowIso } from '../types';

interface AggregateBucket {
  key: string;
  node_kind: CapabilityGraphNode['node_kind'];
  label: string;
  style_family: string | null;
  variant_label: string | null;
  totalFacts: number;
  totalSampleSize: number;
  confidenceSum: number;
  completions: number;
  failures: number;
  humanWaits: number;
}

const toMetricsNumber = (fact: CapabilityFact, key: string) => {
  const value = fact.metrics[key];
  return typeof value === 'number' ? value : 0;
};

const finalizeBucket = (bucket: AggregateBucket): CapabilityGraphNode => ({
  node_id: `${bucket.node_kind}:${bucket.key}`,
  node_kind: bucket.node_kind,
  label: bucket.label,
  style_family: bucket.style_family,
  variant_label: bucket.variant_label,
  sample_size: bucket.totalSampleSize || bucket.totalFacts,
  confidence: Number((bucket.confidenceSum / Math.max(1, bucket.totalFacts)).toFixed(2)),
  closure_rate: Number((bucket.completions / Math.max(1, bucket.totalFacts)).toFixed(2)),
  human_intervention_rate: Number((bucket.humanWaits / Math.max(1, bucket.totalSampleSize || bucket.totalFacts)).toFixed(2)),
  failure_rate: Number((bucket.failures / Math.max(1, bucket.totalFacts)).toFixed(2)),
});

export class CapabilityGraphService {
  buildSummary(facts: CapabilityFact[]): CapabilityGraphSummary {
    const buckets = new Map<string, AggregateBucket>();

    const upsert = (
      node_kind: CapabilityGraphNode['node_kind'],
      key: string | null,
      label: string | null,
      fact: CapabilityFact
    ) => {
      if (!key || !label) {
        return;
      }
      const bucketKey = `${node_kind}:${key}`;
      const existing =
        buckets.get(bucketKey) ||
        {
          key,
          node_kind,
          label,
          style_family: fact.style_family,
          variant_label: fact.variant_label,
          totalFacts: 0,
          totalSampleSize: 0,
          confidenceSum: 0,
          completions: 0,
          failures: 0,
          humanWaits: 0,
        };
      existing.totalFacts += 1;
      existing.totalSampleSize += fact.sample_size || 1;
      existing.confidenceSum += fact.confidence;
      existing.completions += fact.closure_type === 'completed' ? 1 : 0;
      existing.failures += fact.closure_type === 'failed' ? 1 : 0;
      existing.humanWaits += toMetricsNumber(fact, 'human_waits');
      buckets.set(bucketKey, existing);
    };

    for (const fact of facts) {
      upsert('scenario', fact.scenario_signature, fact.scenario_signature, fact);
      upsert('skill', fact.skill_name, fact.skill_name, fact);
      upsert('workflow', fact.workflow_name, fact.workflow_name, fact);
    }

    const nodes = Array.from(buckets.values())
      .map(finalizeBucket)
      .sort((a, b) => b.sample_size - a.sample_size || b.confidence - a.confidence);

    return {
      generated_at: nowIso(),
      total_facts: facts.length,
      nodes,
      top_scenarios: nodes.filter((node) => node.node_kind === 'scenario').slice(0, 5),
    };
  }

  buildAnonymizedExport(facts: CapabilityFact[]) {
    return {
      generated_at: nowIso(),
      total_facts: facts.length,
      facts: facts.map((fact) => fact.anonymized_payload),
      graph: this.buildSummary(facts),
    };
  }
}
