"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.registerHooks = registerHooks;
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
const db_1 = require("./db");
const reranker_1 = require("./reranker");
const graph_1 = require("./graph");
const weighter_1 = require("./weighter");
const TAG = '[openclaw-memory-max][hooks]';
function getBaseDir() {
    return process.env.OPENCLAW_HOME || path_1.default.join(process.env.HOME || '/root', '.openclaw');
}
function getCapturedPath() {
    return path_1.default.join(getBaseDir(), 'memory', 'auto_captured.jsonl');
}
// ── Importance heuristics ───────────────────────────────────────────────
const IMPORTANCE_PATTERNS = [
    /\balways\b/i,
    /\bnever\b/i,
    /\bremember\b/i,
    /\bfrom now on\b/i,
    /\bimportant\b/i,
    /\bdon'?t forget\b/i,
    /\bmake sure\b/i,
    /\brule\b/i,
    /\bpreference\b/i,
    /\bcorrection\b/i,
    /\bactually\b/i, // often signals a correction
    /\binstead\b/i, // often signals a correction
    /\bnot [\w]+ but\b/i,
];
function isHighValue(text) {
    if (!text || text.length < 20)
        return false;
    let hits = 0;
    for (const pattern of IMPORTANCE_PATTERNS) {
        if (pattern.test(text))
            hits++;
    }
    return hits >= 1;
}
function truncateTokens(text, maxTokens) {
    // Rough approximation: 1 token ≈ 4 chars
    const maxChars = maxTokens * 4;
    if (text.length <= maxChars)
        return text;
    return text.substring(0, maxChars) + '...';
}
// ── Auto-Capture: append to JSONL sidecar ───────────────────────────────
async function captureMemory(text, source, sessionId) {
    try {
        // Dedup check: skip if similar content already in chunks DB
        const similar = await (0, db_1.findSimilarChunks)(text, 3);
        if (similar.length > 0) {
            // Check if any result has very high text overlap (>60% token match)
            const queryTokens = new Set(text.toLowerCase().split(/\W+/).filter(t => t.length > 2));
            for (const chunk of similar) {
                const chunkTokens = new Set((chunk.text || '').toLowerCase().split(/\W+/).filter((t) => t.length > 2));
                const overlap = [...queryTokens].filter(t => chunkTokens.has(t)).length;
                const ratio = overlap / Math.max(queryTokens.size, 1);
                if (ratio > 0.6)
                    return false; // Already known
            }
        }
        const entry = {
            text: text.substring(0, 2000), // Cap at 2000 chars
            timestamp: Date.now(),
            source,
            session_id: sessionId || 'unknown'
        };
        const capturePath = getCapturedPath();
        const dir = path_1.default.dirname(capturePath);
        if (!fs_1.default.existsSync(dir))
            fs_1.default.mkdirSync(dir, { recursive: true });
        fs_1.default.appendFileSync(capturePath, JSON.stringify(entry) + '\n');
        console.log(`${TAG} Captured memory from ${source} (${text.length} chars)`);
        return true;
    }
    catch (e) {
        console.error(`${TAG} Capture failed:`, e.message);
        return false;
    }
}
// ── Extract user messages from hook context ─────────────────────────────
function extractUserMessages(context) {
    const messages = [];
    if (!context)
        return messages;
    // OpenClaw passes context in various shapes — handle the common ones
    if (Array.isArray(context.messages)) {
        for (const msg of context.messages) {
            if (msg.role === 'user' && typeof msg.content === 'string') {
                messages.push(msg.content);
            }
            else if (msg.role === 'user' && Array.isArray(msg.content)) {
                for (const part of msg.content) {
                    if (part.type === 'text')
                        messages.push(part.text);
                }
            }
        }
    }
    if (typeof context.message === 'string') {
        messages.push(context.message);
    }
    if (typeof context.userMessage === 'string') {
        messages.push(context.userMessage);
    }
    if (typeof context.text === 'string') {
        messages.push(context.text);
    }
    return messages.filter(m => m && m.length > 5);
}
function registerHooks(api, config = {}) {
    const enableAutoRecall = config.enableAutoRecall ?? true;
    const enableAutoCapture = config.enableAutoCapture ?? false;
    const enableRulePinning = config.enableRulePinning ?? false;
    // ── before_agent_start: Auto-Recall ──────────────────────────────────
    if (!enableAutoRecall) {
        console.log('[openclaw-memory-max] ⊘ Auto-Recall disabled (opt-in via config.enableAutoRecall).');
    }
    api.on('before_agent_start', async (context) => {
        if (!enableAutoRecall)
            return;
        try {
            const userMessages = extractUserMessages(context);
            if (userMessages.length === 0)
                return;
            const latestMessage = userMessages[userMessages.length - 1];
            if (latestMessage.length < 10)
                return; // Skip trivial messages
            // Stage 1: FTS5 pre-filter
            const candidates = await (0, db_1.searchChunksFTS)(latestMessage, 20);
            if (candidates.length === 0)
                return;
            // Stage 2: Cross-encoder rerank (uses cached model)
            const ranked = await (0, reranker_1.rerankCandidates)(latestMessage, candidates, 5, 0.3);
            if (ranked.length === 0)
                return;
            // Stage 3: Query causal graph for relevant experience
            let experienceXml = '';
            try {
                const chains = await (0, graph_1.queryGraphForHook)(latestMessage, 2);
                if (chains.length > 0) {
                    experienceXml = '\n<relevant-experience>\n' +
                        chains.map(c => `  <chain outcome="${c.outcome}">${c.cause} → ${c.action} → ${c.effect}</chain>`).join('\n') +
                        '\n</relevant-experience>';
                }
            }
            catch {
                // Graph query is optional, don't block recall
            }
            // Build injection block (capped at ~2000 tokens)
            let memoriesXml = '<relevant-memories>\n';
            let tokenBudget = 2000;
            for (const r of ranked) {
                const snippet = truncateTokens(r.text, Math.min(400, tokenBudget));
                const line = `  <memory id="${r.id}" confidence="${r.finalScore.toFixed(2)}" source="${r.source || 'chunks'}">${snippet}</memory>\n`;
                tokenBudget -= Math.ceil(line.length / 4);
                memoriesXml += line;
                if (tokenBudget <= 0)
                    break;
            }
            memoriesXml += '</relevant-memories>';
            // Stage 4: Pinned rules (opt-in only)
            let pinnedXml = '';
            if (enableRulePinning) {
                pinnedXml = (0, weighter_1.buildPinnedRulesXml)();
            }
            const injection = memoriesXml + experienceXml + pinnedXml;
            // Inject into context — OpenClaw supports systemPrompt prepend or context injection
            if (context.addSystemContent) {
                context.addSystemContent(injection);
            }
            else if (context.systemPrompt !== undefined) {
                context.systemPrompt = (context.systemPrompt || '') + '\n\n' + injection;
            }
            else if (context.prependMessages) {
                context.prependMessages([{ role: 'system', content: injection }]);
            }
            console.log(`${TAG} Auto-recall: injected ${ranked.length} memories + ${experienceXml ? 'experience' : 'no experience'}${pinnedXml ? ' + pinned rules' : ''}`);
        }
        catch (e) {
            console.error(`${TAG} Auto-recall failed:`, e.message);
        }
    });
    // ── agent_end: Auto-Capture ──────────────────────────────────────────
    if (!enableAutoCapture) {
        console.log('[openclaw-memory-max] ⊘ Auto-Capture disabled (opt-in via config.enableAutoCapture).');
    }
    api.on('agent_end', async (context) => {
        if (!enableAutoCapture)
            return;
        try {
            const userMessages = extractUserMessages(context);
            let captured = 0;
            for (const msg of userMessages) {
                if (isHighValue(msg)) {
                    const ok = await captureMemory(msg, 'auto-capture', context.sessionId);
                    if (ok)
                        captured++;
                }
            }
            if (captured > 0) {
                console.log(`${TAG} Auto-capture: stored ${captured} high-value messages`);
            }
        }
        catch (e) {
            console.error(`${TAG} Auto-capture failed:`, e.message);
        }
    });
    // ── before_compaction: Memory Rescue ─────────────────────────────────
    api.on('before_compaction', async (context) => {
        if (!enableAutoCapture)
            return;
        try {
            const userMessages = extractUserMessages(context);
            let rescued = 0;
            for (const msg of userMessages) {
                if (isHighValue(msg)) {
                    const ok = await captureMemory(msg, 'compaction-rescue', context.sessionId);
                    if (ok)
                        rescued++;
                }
            }
            if (rescued > 0) {
                console.log(`${TAG} Compaction rescue: saved ${rescued} messages before context eviction`);
            }
        }
        catch (e) {
            console.error(`${TAG} Compaction rescue failed:`, e.message);
        }
    });
    const active = [enableAutoRecall && 'auto-recall', enableAutoCapture && 'auto-capture', enableAutoCapture && 'compaction-rescue'].filter(Boolean).join(', ');
    console.log(`[openclaw-memory-max] ✓ Lifecycle hooks registered (${active || 'all disabled'}).`);
}
