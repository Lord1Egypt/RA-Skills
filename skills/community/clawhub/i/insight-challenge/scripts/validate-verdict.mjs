#!/usr/bin/env node
// validate-verdict.mjs — validate an insight-challenge verdict (single or batch)
// against specs/verdict-schema.md. Zero dependencies; fail-closed.
// Input: a .json file path, a .md file path (extracts fenced ```json verdict
// blocks), or `-` to read from stdin.
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';

const RESULTS = new Set(['overturned', 'weakened', 'confirmed']);
const SEVERITIES = new Set(['none', 'critical', 'high', 'medium', 'low']);

function validateVerdict(v, path, errors, warnings) {
  const p = (s) => `${path}${s}`;
  if (typeof v !== 'object' || v === null || Array.isArray(v)) {
    errors.push(`${p('')}: verdict must be a JSON object [IC-V00]`);
    return;
  }
  if (typeof v.finding_id !== 'string' || v.finding_id.length === 0)
    errors.push(`${p('.finding_id')}: required non-empty string [IC-V01]`);
  if (!RESULTS.has(v.challenge_result))
    errors.push(`${p('.challenge_result')}: must be one of overturned|weakened|confirmed [IC-V02]`);
  if (!Number.isInteger(v.confidence) || v.confidence < 0 || v.confidence > 100)
    errors.push(`${p('.confidence')}: required integer 0-100 [IC-V03]`);
  if (typeof v.reasoning !== 'string' || v.reasoning.length === 0)
    errors.push(`${p('.reasoning')}: required non-empty string [IC-V04]`);
  for (const key of ['counter_evidence', 'supporting_evidence']) {
    if (v[key] !== undefined && (!Array.isArray(v[key]) || v[key].some((e) => typeof e !== 'string')))
      errors.push(`${p('.' + key)}: must be an array of strings [IC-V05]`);
  }
  if (v.adjusted_severity !== undefined && !SEVERITIES.has(v.adjusted_severity))
    errors.push(`${p('.adjusted_severity')}: must be one of none|critical|high|medium|low [IC-V06]`);
  if (v.recommendation !== undefined && (typeof v.recommendation !== 'string' || v.recommendation.length === 0))
    errors.push(`${p('.recommendation')}: must be a non-empty string [IC-V11]`);
  if (v.metadata !== undefined) {
    if (typeof v.metadata !== 'object' || v.metadata === null || Array.isArray(v.metadata)) {
      errors.push(`${p('.metadata')}: must be an object [IC-V12]`);
    } else {
      const META_INT = ['challenge_duration_ms'];
      const META_STR_ARRAY = ['files_reviewed', 'design_docs_checked', 'challenge_strategies_applied'];
      for (const k of META_INT) {
        const val = v.metadata[k];
        if (val !== undefined && !Number.isInteger(val))
          errors.push(`${p('.metadata.' + k)}: must be an integer [IC-V12]`);
      }
      for (const k of META_STR_ARRAY) {
        const val = v.metadata[k];
        if (val !== undefined && (!Array.isArray(val) || val.some((e) => typeof e !== 'string')))
          errors.push(`${p('.metadata.' + k)}: must be an array of strings [IC-V12]`);
      }
    }
  }
  if (v.challenge_result === 'overturned' && (!Array.isArray(v.counter_evidence) || v.counter_evidence.length === 0))
    warnings.push(`${p('.counter_evidence')}: expected non-empty for an overturned verdict [IC-W01]`);
  if (v.challenge_result === 'confirmed' && (!Array.isArray(v.supporting_evidence) || v.supporting_evidence.length === 0))
    warnings.push(`${p('.supporting_evidence')}: expected non-empty for a confirmed verdict [IC-W02]`);
  if (v.challenge_result === 'weakened' && (!Array.isArray(v.counter_evidence) || v.counter_evidence.length === 0))
    warnings.push(`${p('.counter_evidence')}: expected non-empty for a weakened verdict [IC-W03]`);
}

function validateDoc(doc, path, errors, warnings) {
  const isBatch = Array.isArray(doc.verdicts);
  if (isBatch) {
    if (doc.verdicts.length === 0) errors.push(`${path}.verdicts: batch must contain at least one verdict [IC-V08]`);
    doc.verdicts.forEach((v, i) => validateVerdict(v, `${path}.verdicts[${i}]`, errors, warnings));
    if (doc.batch_id !== undefined && (typeof doc.batch_id !== 'string' || doc.batch_id.length === 0))
      errors.push(`${path}.batch_id: must be a non-empty string [IC-V13]`);
    if (doc.total_findings !== undefined && (!Number.isInteger(doc.total_findings) || doc.total_findings !== doc.verdicts.length))
      errors.push(`${path}.total_findings: declared ${JSON.stringify(doc.total_findings)} but ${doc.verdicts.length} verdict(s) present [IC-V13]`);
    if (doc.summary !== undefined) {
      if (typeof doc.summary !== 'object' || doc.summary === null || Array.isArray(doc.summary)) {
        errors.push(`${path}.summary: must be an object [IC-V13]`);
      } else {
        const counts = { overturned: 0, weakened: 0, confirmed: 0 };
        for (const v of doc.verdicts) {
          if (v && typeof v === 'object' && RESULTS.has(v.challenge_result)) counts[v.challenge_result]++;
        }
        for (const [k, actual] of Object.entries(counts)) {
          const declared = doc.summary[k];
          if (declared !== undefined && declared !== actual)
            errors.push(`${path}.summary.${k}: declared ${declared} but ${actual} verdict(s) present [IC-V09]`);
        }
      }
    }
  } else {
    validateVerdict(doc, path, errors, warnings);
  }
  return isBatch ? doc.verdicts.length : 1;
}

function extractVerdictBlocks(mdText) {
  const blocks = [];
  const re = /```json\s*\n([\s\S]*?)```/g;
  let m;
  while ((m = re.exec(mdText)) !== null) {
    try {
      const parsed = JSON.parse(m[1]);
      const isVerdict =
        parsed && typeof parsed === 'object' &&
        (('finding_id' in parsed && 'challenge_result' in parsed) || Array.isArray(parsed.verdicts) || Array.isArray(parsed));
      if (isVerdict) blocks.push(parsed);
    } catch {
      // not valid JSON — skip non-verdict blocks
    }
  }
  return blocks;
}

function usage() {
  console.error('Usage: node scripts/validate-verdict.mjs <verdict.json | report.md | ->');
  console.error('  <path>.json  validate the JSON file (single verdict or batch)');
  console.error('  <path>.md    extract and validate fenced ```json verdict blocks');
  console.error('  -            read JSON from stdin');
}

const [inputPath] = process.argv.slice(2);
if (!inputPath) {
  usage();
  process.exit(1);
}
let raw;
if (inputPath === '-') {
  try {
    raw = readFileSync(0, 'utf8');
  } catch (err) {
    console.error(`Cannot read stdin: ${err.code || err.message}`);
    process.exit(1);
  }
} else {
  try {
    raw = readFileSync(resolve(inputPath), 'utf8');
  } catch (err) {
    console.error(`Cannot read input file: ${inputPath} (${err.code || err.message})`);
    usage();
    process.exit(1);
  }
}

let docs;
const isMarkdown = inputPath.endsWith('.md');
if (isMarkdown) {
  docs = extractVerdictBlocks(raw);
  if (docs.length === 0) {
    console.error('[IC-V10] No fenced ```json verdict block found in markdown input');
    process.exit(1);
  }
} else {
  let doc;
  try {
    doc = JSON.parse(raw);
  } catch (err) {
    console.error(`[IC-V07] Invalid JSON: ${err.message}`);
    process.exit(1);
  }
  if (Array.isArray(doc)) doc = { verdicts: doc }; // top-level array = batch shorthand
  docs = [doc];
}

const errors = [];
const warnings = [];
let count = 0;
docs.forEach((doc, i) => {
  count += validateDoc(doc, docs.length > 1 ? `block[${i}]` : '', errors, warnings);
});

if (errors.length > 0) {
  console.error(`validate-verdict: FAILED (${errors.length} error${errors.length > 1 ? 's' : ''})`);
  for (const e of errors) console.error(`  - ${e}`);
  process.exit(1);
}
console.log(`validate-verdict: PASSED (${count} verdict${count > 1 ? 's' : ''}${docs.length > 1 ? ` in ${docs.length} blocks` : ''})`);
for (const w of warnings) console.log(`  warning: ${w}`);
