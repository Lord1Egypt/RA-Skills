"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.reportCompactionRescue = reportCompactionRescue;
exports.registerCompressor = registerCompressor;
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
function getBaseDir() {
    return process.env.OPENCLAW_HOME || path_1.default.join(process.env.HOME || '/root', '.openclaw');
}
function getCapturedPath() {
    return path_1.default.join(getBaseDir(), 'memory', 'auto_captured.jsonl');
}
function jsonResult(payload) {
    return {
        content: [{ type: 'text', text: JSON.stringify(payload, null, 2) }],
        details: payload
    };
}
// Track what the before_compaction hook rescued
let lastCompactionRescue = { count: 0, timestamp: 0, items: [] };
/** Called by the before_compaction hook in hooks.ts to report rescued items. */
function reportCompactionRescue(count, items) {
    lastCompactionRescue = { count, timestamp: Date.now(), items: items.slice(0, 5) };
}
function registerCompressor(api) {
    api.registerTool({
        name: 'compress_context',
        description: 'Signal that context compression is needed and review what was rescued from the last compaction. Call when the context window feels overloaded. Returns rescued memories from recent compaction events plus an advisory to the runtime.',
        parameters: {
            type: 'object',
            properties: {
                compression_reason: { type: 'string', description: 'Why you decided to compress the context now.' }
            },
            required: ['compression_reason']
        },
        async execute(_toolCallId, args) {
            // Read recent auto-captured entries (last 24h) for context
            const recentCaptures = [];
            try {
                const capturePath = getCapturedPath();
                if (fs_1.default.existsSync(capturePath)) {
                    const cutoff = Date.now() - (24 * 60 * 60 * 1000);
                    const lines = fs_1.default.readFileSync(capturePath, 'utf8').split('\n').filter(Boolean);
                    for (const line of lines) {
                        try {
                            const entry = JSON.parse(line);
                            if (entry.timestamp >= cutoff) {
                                recentCaptures.push(`[${entry.source}] ${entry.text.substring(0, 100)}`);
                            }
                        }
                        catch { /* skip */ }
                    }
                }
            }
            catch { /* non-critical */ }
            return jsonResult({
                status: 'compression_advisory',
                reason: args.compression_reason,
                message: 'Context compression requested. The runtime handles actual eviction. High-value content is auto-rescued by the before_compaction hook.',
                lastRescue: lastCompactionRescue.count > 0 ? {
                    rescued: lastCompactionRescue.count,
                    when: new Date(lastCompactionRescue.timestamp).toISOString(),
                    preview: lastCompactionRescue.items
                } : null,
                recentAutoCaptures: recentCaptures.length,
                capturePreview: recentCaptures.slice(0, 3)
            });
        }
    });
}
