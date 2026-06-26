import { fileURLToPath } from 'node:url';
import { parseRecords } from './parse.js';
import { validateRecords } from './schema.js';
import { deduplicateRecords } from './dedupe.js';
import { classifyRecords } from './classify.js';
import { checkStaleness } from './staleness.js';
import { detectConflicts } from './conflicts.js';
import { renderMarkdown, renderJSON } from './render.js';
import type { AdjudicationReport, RecordKind, SchemaViolation, ProvenanceInfo } from './types.js';

const DEFAULT_TTL_MS = 30 * 24 * 60 * 60 * 1000;

export function main(input: string): { markdown: string; json: string; report: AdjudicationReport } {
  let raw: unknown;
  try {
    raw = JSON.parse(input);
  } catch {
    raw = [];
  }

  const { records } = parseRecords(raw);

  const validationResults = validateRecords(records);
  const schema_violations: SchemaViolation[] = validationResults.flatMap(r =>
    r.errors.map(e => ({ recordId: r.id as SchemaViolation['recordId'], field: e.field, message: e.message }))
  );

  const { deduped } = deduplicateRecords(records);

  const classifyResults = classifyRecords(deduped);
  const classified = classifyResults.reduce<Record<RecordKind, number>>(
    (acc, r) => { acc[r.kind]++; return acc; },
    { fact: 0, goal: 0, speculation: 0 }
  );

  const { fresh, archiveCandidates } = checkStaleness(deduped, DEFAULT_TTL_MS);
  const archived = archiveCandidates.map(c => c.record);

  const conflicts = detectConflicts(fresh);

  const allProvenance = deduped.flatMap(r => r.provenance);
  const provenance_chain: ProvenanceInfo[] = allProvenance.filter(
    (p, i, arr) => arr.findIndex(q => q.sourceId === p.sourceId) === i
  );

  const report: AdjudicationReport = {
    input_count: records.length,
    deduped_count: deduped.length,
    classified,
    conflicts,
    archived,
    schema_violations,
    provenance_chain,
  };

  const markdown = renderMarkdown(report);
  const json = renderJSON(report);

  return { markdown, json, report };
}

if (fileURLToPath(import.meta.url) === process.argv[1]) {
  const chunks: Buffer[] = [];
  process.stdin.on('data', chunk => chunks.push(chunk as Buffer));
  process.stdin.on('end', () => {
    const input = Buffer.concat(chunks).toString('utf8');
    const { markdown, json } = main(input);
    process.stdout.write(markdown + '\n' + json + '\n');
  });
}
