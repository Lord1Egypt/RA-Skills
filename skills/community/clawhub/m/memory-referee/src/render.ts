import type { AdjudicationReport } from './types.js';

/**
 * Render an AdjudicationReport as a Markdown string.
 *
 * Sections with zero items are omitted entirely.
 * Provenance sources appear as indented sub-lines under each record entry.
 */
export function renderMarkdown(report: AdjudicationReport): string {
  const lines: string[] = [];

  lines.push('# Memory Adjudication Report');
  lines.push('');

  lines.push('## Summary');
  lines.push('');
  lines.push(`- Input records: ${report.input_count}`);
  lines.push(`- After deduplication: ${report.deduped_count}`);
  lines.push(`- Facts: ${report.classified['fact'] ?? 0}`);
  lines.push(`- Goals: ${report.classified['goal'] ?? 0}`);
  lines.push(`- Speculation: ${report.classified['speculation'] ?? 0}`);
  lines.push('');

  if (report.conflicts.length > 0) {
    lines.push(`## Contradictions (${report.conflicts.length})`);
    lines.push('');
    for (const pair of report.conflicts) {
      lines.push(`**Reason:** ${pair.reason}`);
      lines.push('');
      lines.push(`- **Record A** [${pair.a.id}] ${pair.a.entity} (${pair.a.kind}): ${pair.a.content}`);
      for (const prov of pair.a.provenance) {
        lines.push(`  - Source: ${prov.sourceLabel} (${prov.sourceId}) at ${prov.capturedAt}${prov.confidence !== undefined ? ` — confidence: ${prov.confidence}` : ''}`);
      }
      lines.push(`- **Record B** [${pair.b.id}] ${pair.b.entity} (${pair.b.kind}): ${pair.b.content}`);
      for (const prov of pair.b.provenance) {
        lines.push(`  - Source: ${prov.sourceLabel} (${prov.sourceId}) at ${prov.capturedAt}${prov.confidence !== undefined ? ` — confidence: ${prov.confidence}` : ''}`);
      }
      lines.push('');
    }
  }

  if (report.archived.length > 0) {
    lines.push(`## Stale Archived (${report.archived.length})`);
    lines.push('');
    for (const record of report.archived) {
      lines.push(`- [${record.id}] **${record.entity}** (${record.kind}): ${record.content}`);
      for (const prov of record.provenance) {
        lines.push(`  - Source: ${prov.sourceLabel} (${prov.sourceId}) at ${prov.capturedAt}${prov.confidence !== undefined ? ` — confidence: ${prov.confidence}` : ''}`);
      }
    }
    lines.push('');
  }

  if (report.schema_violations.length > 0) {
    lines.push(`## Schema Violations (${report.schema_violations.length})`);
    lines.push('');
    for (const v of report.schema_violations) {
      lines.push(`- [${v.recordId}] field \`${v.field}\`: ${v.message}`);
    }
    lines.push('');
  }

  if (report.provenance_chain.length > 0) {
    lines.push(`## Provenance Chain (${report.provenance_chain.length})`);
    lines.push('');
    for (const prov of report.provenance_chain) {
      const conf = prov.confidence !== undefined ? ` — confidence: ${prov.confidence}` : '';
      lines.push(`- ${prov.sourceLabel} (${prov.sourceId}) — ${prov.capturedAt}${conf}`);
    }
    lines.push('');
  }

  return lines.join('\n');
}

/**
 * Serialize an AdjudicationReport to a pretty-printed JSON string.
 * No transformation is applied — the output round-trips to the input.
 */
export function renderJSON(report: AdjudicationReport): string {
  return JSON.stringify(report, null, 2);
}
