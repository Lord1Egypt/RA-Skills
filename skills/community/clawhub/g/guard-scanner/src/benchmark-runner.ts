// @ts-nocheck
'use strict';

import fs  from 'fs';
import path  from 'path';

import { GuardScanner  } from './scanner';
import { RuleRegistry  } from './core/rule-registry';
import { getCurrentModuleDir } from './module-path';
import { analyzeMetaGuard  } from './meta-guard';

const ROOT = path.join(getCurrentModuleDir(), '..');
const DEFAULT_QUALITY_CONTRACT_PATH = path.join(ROOT, 'docs', 'data', 'quality-contract.json');

function readJson(filePath) {
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function loadQualityContract(contractPath = DEFAULT_QUALITY_CONTRACT_PATH) {
    return readJson(contractPath);
}

function normalizeSample(sample, index, defaultPrefix) {
    return {
        id: sample.id || `${defaultPrefix}-${index + 1}`,
        title: sample.title || sample.id || `${defaultPrefix}-${index + 1}`,
        content: sample.content || '',
        expectedCategories: Array.isArray(sample.expectedCategories) ? sample.expectedCategories : [],
    };
}

function evaluateSample(scanner, sample, expectedKind) {
    const result = scanner.scanText(sample.content);
    const normalizedDetections = result.detections.map((detection) => ({
        id: detection.id || detection.rule_id,
        severity: detection.severity,
        category: detection.cat || detection.category,
        validation_status: detection.validation_status,
    }));
    const matchedCategories = [...new Set(normalizedDetections.map((d) => d.category).filter(Boolean))];
    const categoryCoverage = sample.expectedCategories.length === 0
        ? 1
        : sample.expectedCategories.filter((cat) => matchedCategories.includes(cat)).length / sample.expectedCategories.length;

    return {
        id: sample.id,
        title: sample.title,
        expected: expectedKind,
        detected: normalizedDetections.length > 0,
        risk: result.risk,
        safe: result.safe,
        matchedCategories,
        categoryCoverage: Number(categoryCoverage.toFixed(3)),
        detections: normalizedDetections,
    };
}

function summarizeLayer(layerName, corpus, scannerOptions = {}) {
    const scanner = new GuardScanner({ summaryOnly: true, quiet: true, ...scannerOptions });
    const benign = corpus.benign.map((sample, index) => normalizeSample(sample, index, `${layerName}-benign`));
    const malicious = corpus.malicious.map((sample, index) => normalizeSample(sample, index, `${layerName}-malicious`));

    const benignResults = benign.map((sample) => evaluateSample(scanner, sample, 'benign'));
    const maliciousResults = malicious.map((sample) => evaluateSample(scanner, sample, 'malicious'));

    const TP = maliciousResults.filter((entry) => entry.detected).length;
    const FN = maliciousResults.filter((entry) => !entry.detected).length;
    const FP = benignResults.filter((entry) => entry.detected).length;
    const TN = benignResults.filter((entry) => !entry.detected).length;
    const precision = TP / Math.max(1, TP + FP);
    const recall = TP / Math.max(1, TP + FN);
    const false_positive_rate = FP / Math.max(1, FP + TN);
    const false_negative_rate = FN / Math.max(1, TP + FN);
    const category_coverage = maliciousResults.length === 0
        ? 1
        : maliciousResults.reduce((sum, entry) => sum + entry.categoryCoverage, 0) / maliciousResults.length;

    return {
        layer: layerName,
        corpus_version: corpus.version || 'unversioned',
        counts: {
            benign: benignResults.length,
            malicious: maliciousResults.length,
            true_positives: TP,
            false_negatives: FN,
            false_positives: FP,
            true_negatives: TN,
        },
        metrics: {
            precision: Number(precision.toFixed(4)),
            recall: Number(recall.toFixed(4)),
            false_positive_rate: Number(false_positive_rate.toFixed(4)),
            false_negative_rate: Number(false_negative_rate.toFixed(4)),
            category_coverage: Number(category_coverage.toFixed(4)),
        },
        benign_results: benignResults,
        malicious_results: maliciousResults,
    };
}

function aggregateLayers(layers) {
    const aggregate = {
        benign: 0,
        malicious: 0,
        true_positives: 0,
        false_negatives: 0,
        false_positives: 0,
        true_negatives: 0,
    };

    for (const layer of layers) {
        aggregate.benign += layer.counts.benign;
        aggregate.malicious += layer.counts.malicious;
        aggregate.true_positives += layer.counts.true_positives;
        aggregate.false_negatives += layer.counts.false_negatives;
        aggregate.false_positives += layer.counts.false_positives;
        aggregate.true_negatives += layer.counts.true_negatives;
    }

    const precision = aggregate.true_positives / Math.max(1, aggregate.true_positives + aggregate.false_positives);
    const recall = aggregate.true_positives / Math.max(1, aggregate.true_positives + aggregate.false_negatives);
    const false_positive_rate = aggregate.false_positives / Math.max(1, aggregate.false_positives + aggregate.true_negatives);
    const false_negative_rate = aggregate.false_negatives / Math.max(1, aggregate.true_positives + aggregate.false_negatives);

    return {
        counts: aggregate,
        metrics: {
            precision: Number(precision.toFixed(4)),
            recall: Number(recall.toFixed(4)),
            false_positive_rate: Number(false_positive_rate.toFixed(4)),
            false_negative_rate: Number(false_negative_rate.toFixed(4)),
        },
    };
}

function computeExplainabilityCompletenessRate() {
    const registry = new RuleRegistry();
    const rules = registry.getAllRules();
    const complete = rules.filter((rule) => (
        typeof rule.rationale === 'string' && rule.rationale.trim().length > 0 &&
        typeof rule.preconditions === 'string' && rule.preconditions.trim().length > 0 &&
        typeof rule.remediation === 'string' && rule.remediation.trim().length > 0
    )).length;

    return {
        complete,
        total: rules.length,
        rate: Number((complete / Math.max(1, rules.length)).toFixed(4)),
    };
}

function buildBenchmarkLedger(contract = loadQualityContract()) {
    const layers = contract.layers.map((layer) => {
        const corpusPath = path.join(ROOT, layer.corpus);
        const corpus = readJson(corpusPath);
        return summarizeLayer(layer.id, corpus, layer.scanner_options || {});
    });
    const aggregate = aggregateLayers(layers);
    const explainability = computeExplainabilityCompletenessRate();

    return {
        benchmark_version: contract.benchmark_version,
        contract_version: contract.contract_version,
        generatedAt: new Date().toISOString(),
        layers,
        aggregate,
        explainability,
        meta_guard: analyzeMetaGuard({
            adversarialLayer: layers.find((layer) => /adversarial/i.test(layer.layer)),
        }),
        quality_targets: contract.quality_targets,
    };
}

function buildFalsePositiveLedger(benchmarkLedger) {
    return {
        benchmark_version: benchmarkLedger.benchmark_version,
        generatedAt: benchmarkLedger.generatedAt,
        entries: benchmarkLedger.layers.flatMap((layer) =>
            layer.benign_results
                .filter((entry) => entry.detected)
                .map((entry) => ({
                    layer: layer.layer,
                    sample_id: entry.id,
                    title: entry.title,
                    risk: entry.risk,
                    matched_categories: entry.matchedCategories,
                    detection_ids: entry.detections.map((detection) => detection.id),
                }))
        ),
    };
}

function writeLedger(filePath, data) {
    fs.mkdirSync(path.dirname(filePath), { recursive: true });
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}

export { 
    DEFAULT_QUALITY_CONTRACT_PATH,
    loadQualityContract,
    summarizeLayer,
    buildBenchmarkLedger,
    buildFalsePositiveLedger,
    computeExplainabilityCompletenessRate,
    writeLedger,
 };
