// @ts-nocheck
import { describe, it, assert, beforeEach, afterEach, vi } from 'vitest';


import { buildBenchmarkLedger,
    buildFalsePositiveLedger,
    loadQualityContract,
 } from '../src/benchmark-runner';

describe('Benchmark ledger contracts', () => {
    it('builds three benchmark layers and aggregate metrics', () => {
        const ledger = buildBenchmarkLedger(loadQualityContract());

        assert.ok(ledger.layers.length >= 5);
        assert.ok(typeof ledger.aggregate.metrics.precision === 'number');
        assert.ok(typeof ledger.aggregate.metrics.recall === 'number');
        assert.ok(typeof ledger.explainability.rate === 'number');
        assert.ok(typeof ledger.meta_guard.evasion_resistance === 'number');
    });

    it('emits a false-positive ledger with stable structure', () => {
        const ledger = buildBenchmarkLedger(loadQualityContract());
        const fpLedger = buildFalsePositiveLedger(ledger);

        assert.ok(Array.isArray(fpLedger.entries));
        assert.equal(fpLedger.benchmark_version, ledger.benchmark_version);
    });
});
