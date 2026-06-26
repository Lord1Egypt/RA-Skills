import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// @ts-nocheck

import path from 'node:path';
import {
    buildBenchmarkLedger,
    buildFalsePositiveLedger,
    loadQualityContract,
    writeLedger,
}  from '../src/benchmark-runner';

const ROOT = path.join(__dirname, '..');
const LEDGER_PATH = path.join(ROOT, 'docs', 'data', 'benchmark-ledger.json');
const FP_LEDGER_PATH = path.join(ROOT, 'docs', 'data', 'fp-ledger.json');

const args = process.argv.slice(2);
const contract = loadQualityContract();
const ledger = buildBenchmarkLedger(contract);
const fpLedger = buildFalsePositiveLedger(ledger);

if (args.includes('--write-ledgers')) {
    writeLedger(LEDGER_PATH, ledger);
    writeLedger(FP_LEDGER_PATH, fpLedger);
    console.log(`✅ benchmark ledger written to ${LEDGER_PATH}`);
    console.log(`✅ false-positive ledger written to ${FP_LEDGER_PATH}`);
}

if (args.includes('--check')) {
    const targets = contract.quality_targets;
    const agg = ledger.aggregate.metrics;
    if (agg.precision < targets.precision_min) throw new Error(`precision below contract: ${agg.precision}`);
    if (agg.recall < targets.recall_min) throw new Error(`recall below contract: ${agg.recall}`);
    if (agg.false_positive_rate > targets.false_positive_rate_max) throw new Error(`FPR above contract: ${agg.false_positive_rate}`);
    if (agg.false_negative_rate > targets.false_negative_rate_max) throw new Error(`FNR above contract: ${agg.false_negative_rate}`);
    if (ledger.explainability.rate < targets.explainability_completeness_rate_min) {
        throw new Error(`explainability completeness below contract: ${ledger.explainability.rate}`);
    }
    console.log('✅ benchmark contract satisfied');
}

if (args.includes('--json')) {
    process.stdout.write(JSON.stringify(ledger, null, 2) + '\n');
} else {
    console.log('\n🛡️ guard-scanner benchmark ledger\n');
    console.log(`Benchmark version: ${ledger.benchmark_version}`);
    for (const layer of ledger.layers) {
        console.log(`- ${layer.layer}: benign=${layer.counts.benign}, malicious=${layer.counts.malicious}, precision=${layer.metrics.precision}, recall=${layer.metrics.recall}, fpr=${layer.metrics.false_positive_rate}, fnr=${layer.metrics.false_negative_rate}`);
    }
    console.log(`\nAggregate: precision=${ledger.aggregate.metrics.precision}, recall=${ledger.aggregate.metrics.recall}, fpr=${ledger.aggregate.metrics.false_positive_rate}, fnr=${ledger.aggregate.metrics.false_negative_rate}`);
    console.log(`Explainability completeness: ${ledger.explainability.rate}`);
    console.log(`False-positive ledger entries: ${fpLedger.entries.length}`);
}
