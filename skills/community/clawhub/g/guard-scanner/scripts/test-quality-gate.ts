import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// @ts-nocheck
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.join(__dirname, '..');
const SPEC_FILE = path.join(ROOT, 'docs/spec/capabilities.json');
const FINDING_SCHEMA_FILE = path.join(ROOT, 'docs/spec/finding.schema.json');
const CORPUS_METRICS_FILE = path.join(ROOT, 'docs/data/corpus-metrics.json');
const BENCHMARK_LEDGER_FILE = path.join(ROOT, 'docs/data/benchmark-ledger.json');
const FP_LEDGER_FILE = path.join(ROOT, 'docs/data/fp-ledger.json');
const MIN_CORPUS_SAMPLES_PER_CLASS = 12;
const MAX_FALSE_POSITIVE_RATE = 0.1;
const MAX_FALSE_NEGATIVE_RATE = 0.1;
const DIRECT_CONTRACT_MODULES = [
  'src/core/content-loader.ts',
  'src/core/inventory.ts',
  'src/core/report-adapters.ts',
  'src/finding-schema.ts',
  'src/html-template.ts',
  'src/threat-model.ts',
];
const REQUIRED_FINDING_FIELDS = [
  'rule_id',
  'category',
  'severity',
  'description',
  'rationale',
  'preconditions',
  'false_positive_scenarios',
  'remediation_hint',
  'validation_status',
  'evidence',
];
const TEST_DIR = path.join(ROOT, 'tests');
const TEST_FILE_REGEX = /\.test\.(?:ts|js)$/;

console.log('🛡️  Guard-Scanner Test Quality Gate\n');

try {
  const spec = JSON.parse(fs.readFileSync(SPEC_FILE, 'utf8'));
  
  // Verify README
  const readme = fs.readFileSync(path.join(ROOT, 'README.md'), 'utf8');
  if (!readme.includes(`${spec.static_pattern_count}`)) {
    throw new Error('README.md out of sync with capabilities.json (static_pattern_count)');
  }
  if (!readme.includes(`${spec.runtime_check_count}`)) {
    throw new Error('README.md out of sync with capabilities.json (runtime_check_count)');
  }
  if (!readme.includes(`${spec.threat_category_count}`)) {
    throw new Error('README.md out of sync with capabilities.json (threat_category_count)');
  }
  
  // Verify SKILL.md
  const skill = fs.readFileSync(path.join(ROOT, 'SKILL.md'), 'utf8');
  if (!skill.includes(`${spec.static_pattern_count}`)) {
    throw new Error('SKILL.md out of sync with capabilities.json');
  }

  // Verify plugin.json
  const plugin = JSON.parse(fs.readFileSync(path.join(ROOT, 'openclaw.plugin.json'), 'utf8'));
  if (plugin.version !== spec.plugin_version) {
    throw new Error('openclaw.plugin.json version out of sync with capabilities.json');
  }

  // Verify package.json
  const pkg = JSON.parse(fs.readFileSync(path.join(ROOT, 'package.json'), 'utf8'));
  const deps = pkg.dependencies ? Object.keys(pkg.dependencies).length : 0;
  if (deps !== spec.dependencies_runtime) {
      throw new Error(`capabilities.json claims ${spec.dependencies_runtime} deps but package.json has ${deps}`);
  }

  console.log('  ✅ PASS: Source of Truth (capabilities.json) matches documentation');

  const findingSchema = JSON.parse(fs.readFileSync(FINDING_SCHEMA_FILE, 'utf8'));
  for (const field of REQUIRED_FINDING_FIELDS) {
    if (!findingSchema.required || !findingSchema.required.includes(field)) {
      throw new Error(`finding.schema.json missing required field: ${field}`);
    }
  }

  if (!readme.includes('## Finding Schema')) {
    throw new Error('README.md missing "Finding Schema" section');
  }

  for (const field of REQUIRED_FINDING_FIELDS) {
    if (!readme.includes(`\`${field}\``)) {
      throw new Error(`README.md Finding Schema section missing field: ${field}`);
    }
  }

  const readmeJa = fs.readFileSync(path.join(ROOT, 'README_ja.md'), 'utf8');
  if (!readmeJa.includes('## Finding Schema')) {
    throw new Error('README_ja.md missing "Finding Schema" section');
  }

  for (const field of REQUIRED_FINDING_FIELDS) {
    if (!readmeJa.includes(`\`${field}\``)) {
      throw new Error(`README_ja.md Finding Schema section missing field: ${field}`);
    }
  }

  console.log('  ✅ PASS: Finding schema is documented and complete');
} catch (err) {
  console.error(`  ❌ FAIL: ${err.message}`);
  process.exit(1);
}

// Check test files
const testFiles = fs.readdirSync(TEST_DIR).filter(f => TEST_FILE_REGEX.test(f));
const testContents = new Map(
  testFiles.map((file) => [file, fs.readFileSync(path.join(TEST_DIR, file), 'utf8')])
);

const missingDirectContracts = DIRECT_CONTRACT_MODULES.filter((modulePath) => {
  const base = path.basename(modulePath, '.ts');
  return ![...testContents.values()].some((content) => (
    content.includes(modulePath.replace(/^src\//, '../src/')) ||
    content.includes(modulePath) ||
    content.includes(base)
  ));
});

if (missingDirectContracts.length > 0) {
  console.error(`  ❌ FAIL: Missing direct contract tests for critical modules: ${missingDirectContracts.join(', ')}`);
  process.exit(1);
}

console.log(`  ✅ PASS: Direct contract coverage for critical modules (${DIRECT_CONTRACT_MODULES.length}/${DIRECT_CONTRACT_MODULES.length})`);

try {
  const corpusMetrics = JSON.parse(fs.readFileSync(CORPUS_METRICS_FILE, 'utf8'));
  if (!corpusMetrics.corpus || typeof corpusMetrics.corpus.benign !== 'number' || typeof corpusMetrics.corpus.malicious !== 'number') {
    throw new Error('corpus-metrics.json missing corpus counts');
  }
  for (const field of ['precision', 'recall', 'false_positive_rate', 'false_negative_rate']) {
    if (typeof corpusMetrics[field] !== 'number') {
      throw new Error(`corpus-metrics.json missing numeric field: ${field}`);
    }
  }
  if (corpusMetrics.corpus.benign < MIN_CORPUS_SAMPLES_PER_CLASS || corpusMetrics.corpus.malicious < MIN_CORPUS_SAMPLES_PER_CLASS) {
    throw new Error(`corpus too small: benign=${corpusMetrics.corpus.benign}, malicious=${corpusMetrics.corpus.malicious}, required>=${MIN_CORPUS_SAMPLES_PER_CLASS}`);
  }
  if (corpusMetrics.false_positive_rate > MAX_FALSE_POSITIVE_RATE) {
    throw new Error(`false_positive_rate ${corpusMetrics.false_positive_rate} exceeds ${MAX_FALSE_POSITIVE_RATE}`);
  }
  if (corpusMetrics.false_negative_rate > MAX_FALSE_NEGATIVE_RATE) {
    throw new Error(`false_negative_rate ${corpusMetrics.false_negative_rate} exceeds ${MAX_FALSE_NEGATIVE_RATE}`);
  }
  console.log(`  ✅ PASS: Corpus metrics contract present (${corpusMetrics.corpus.benign} benign / ${corpusMetrics.corpus.malicious} malicious)`);
} catch (err) {
  console.error(`  ❌ FAIL: ${err.message}`);
  process.exit(1);
}

try {
  const spec = JSON.parse(fs.readFileSync(SPEC_FILE, 'utf8'));
  const benchmarkLedger = JSON.parse(fs.readFileSync(BENCHMARK_LEDGER_FILE, 'utf8'));
  const fpLedger = JSON.parse(fs.readFileSync(FP_LEDGER_FILE, 'utf8'));

  if (!spec.benchmark_corpus_version || spec.benchmark_corpus_version !== benchmarkLedger.benchmark_version) {
    throw new Error('capabilities.json benchmark_corpus_version out of sync with benchmark-ledger.json');
  }
  if (!Array.isArray(benchmarkLedger.layers) || benchmarkLedger.layers.length < 3) {
    throw new Error('benchmark-ledger.json must contain at least 3 layers');
  }
  for (const field of ['precision', 'recall', 'false_positive_rate', 'false_negative_rate']) {
    if (typeof benchmarkLedger.aggregate?.metrics?.[field] !== 'number') {
      throw new Error(`benchmark-ledger.json missing aggregate metric: ${field}`);
    }
  }
  if (!Array.isArray(fpLedger.entries)) {
    throw new Error('fp-ledger.json missing entries array');
  }
  if (typeof spec.explainability_completeness_rate !== 'number' || spec.explainability_completeness_rate < 0.9) {
    throw new Error('capabilities.json explainability completeness missing or below floor');
  }
  if (typeof spec.runtime_check_latency_budget_ms !== 'number') {
    throw new Error('capabilities.json missing runtime_check_latency_budget_ms');
  }
  console.log(`  ✅ PASS: Benchmark and FP ledgers present (${benchmarkLedger.layers.length} layers, ${fpLedger.entries.length} FP entries)`);
} catch (err) {
  console.error(`  ❌ FAIL: ${err.message}`);
  process.exit(1);
}

console.log(`  ✅ PASS: Test files discovered (${testFiles.length})`);

console.log('\n✅ Quality gate PASSED\n');
