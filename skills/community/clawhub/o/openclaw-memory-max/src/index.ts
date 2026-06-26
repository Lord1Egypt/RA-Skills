import { registerReranker } from './reranker';
import { registerWeighter } from './weighter';
import { ensureSleepCycle } from './sleep-cycle';
import { ensureUtilityColumn } from './db';
import { registerCompressor } from './compressor';
import { registerCausalGraph } from './graph';
import { registerHooks } from './hooks';
import { registerEpisodic } from './episodic';

export interface MemoryMaxConfig {
    enableRulePinning?: boolean;   // default: false
    enableAutoCapture?: boolean;   // default: true
    enableAutoRecall?: boolean;    // default: true
}

const memoryMaxPlugin = {
    id: 'openclaw-memory-max',
    name: 'OpenClaw Memory Max (SotA)',
    description: 'SOTA Memory Suite v3: Auto-Recall Hooks, Cross-Encoder Reranking, Multi-Hop Deep Search, Semantic Causal Graph with Dedup/Pruning, Episodic Session Memory, Utility-Weighted Vectors, YAML Rule Pinning, and Nightly Sleep-Cycle Consolidation.',
    configSchema: {
        type: 'object',
        additionalProperties: false,
        properties: {
            enableRulePinning: { type: 'boolean', default: false },
            enableAutoCapture: { type: 'boolean', default: false },
            enableAutoRecall: { type: 'boolean', default: true }
        }
    },
    register(api: any) {
        console.log('[openclaw-memory-max] Initializing SOTA Memory Cluster v3...');

        // Read plugin config — merge from openclaw.json + api (api takes precedence)
        let fileConfig: MemoryMaxConfig = {};
        try {
            const fs = require('fs');
            const path = require('path');
            const baseDir = process.env.OPENCLAW_HOME || path.join(process.env.HOME || '/root', '.openclaw');
            const configPath = path.join(baseDir, 'openclaw.json');
            if (fs.existsSync(configPath)) {
                const raw = JSON.parse(fs.readFileSync(configPath, 'utf8'));
                fileConfig = raw?.plugins?.entries?.['openclaw-memory-max']?.config || {};
            }
        } catch { /* fallback silently */ }

        const apiConfig: MemoryMaxConfig = api.config || api.getConfig?.() || {};
        const config: MemoryMaxConfig = { ...fileConfig, ...apiConfig };

        const enableRulePinning = config.enableRulePinning ?? false;
        const enableAutoCapture = config.enableAutoCapture ?? false;
        const enableAutoRecall = config.enableAutoRecall ?? true;

        console.log(`[openclaw-memory-max] Config: rulePinning=${enableRulePinning}, autoCapture=${enableAutoCapture}, autoRecall=${enableAutoRecall}`);

        // 0. Ensure Utility Score Schema Exists (async, fire-and-forget)
        ensureUtilityColumn().catch((e: any) =>
            console.error('[openclaw-memory-max] Schema migration failed:', e.message)
        );

        // 1. Cross-Encoder Precision Search + Deep Search + Reward/Penalize
        registerReranker(api);
        console.log('[openclaw-memory-max] ✓ Precision Reranker + Deep Multi-Hop Search active.');

        // 2. Rule Weighter (read-only — parses MEMORY.md YAML, never writes to global config)
        registerWeighter(api);
        if (enableRulePinning) {
            console.log('[openclaw-memory-max] ✓ Rule Pinning active (injected via hook, not global config).');
        } else {
            console.log('[openclaw-memory-max] ⊘ Rule Pinning disabled (opt-in via config.enableRulePinning).');
        }

        // 3. Context Compressor (wired to before_compaction rescue data)
        registerCompressor(api);
        console.log('[openclaw-memory-max] ✓ Context Compressor registered.');

        // 4. Causal Knowledge Graph (semantic search, dedup, pruning)
        registerCausalGraph(api);
        console.log('[openclaw-memory-max] ✓ Causal Knowledge Graph live (semantic + dedup).');

        // 5. Lifecycle Hooks: auto-recall, auto-capture, compaction rescue
        registerHooks(api, { enableAutoCapture, enableAutoRecall, enableRulePinning });

        // 6. Episodic Memory: session segmentation
        registerEpisodic(api);

        // 7. Sleep Cycle: in-process maintenance scheduler
        ensureSleepCycle().catch((e: any) =>
            console.error('[openclaw-memory-max] Sleep-Cycle setup failed:', e.message)
        );

        console.log('[openclaw-memory-max] All systems nominal. SOTA Memory Matrix ACTIVE.');
    }
};

export default memoryMaxPlugin;
