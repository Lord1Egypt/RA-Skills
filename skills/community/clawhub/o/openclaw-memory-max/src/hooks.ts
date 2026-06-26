import fs from 'fs';
import path from 'path';
import { searchChunksFTS, findSimilarChunks } from './db';
import { rerankCandidates } from './reranker';
import { queryGraphForHook } from './graph';
import { buildPinnedRulesXml } from './weighter';

const TAG = '[openclaw-memory-max][hooks]';

function getBaseDir(): string {
    return process.env.OPENCLAW_HOME || path.join(process.env.HOME || '/root', '.openclaw');
}

function getCapturedPath(): string {
    return path.join(getBaseDir(), 'memory', 'auto_captured.jsonl');
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
    /\bactually\b/i,   // often signals a correction
    /\binstead\b/i,     // often signals a correction
    /\bnot [\w]+ but\b/i,
];

function isHighValue(text: string): boolean {
    if (!text || text.length < 20) return false;
    let hits = 0;
    for (const pattern of IMPORTANCE_PATTERNS) {
        if (pattern.test(text)) hits++;
    }
    return hits >= 1;
}

function truncateTokens(text: string, maxTokens: number): string {
    // Rough approximation: 1 token ≈ 4 chars
    const maxChars = maxTokens * 4;
    if (text.length <= maxChars) return text;
    return text.substring(0, maxChars) + '...';
}

// ── Auto-Capture: append to JSONL sidecar ───────────────────────────────

async function captureMemory(text: string, source: string, sessionId?: string): Promise<boolean> {
    try {
        // Dedup check: skip if similar content already in chunks DB
        const similar = await findSimilarChunks(text, 3);
        if (similar.length > 0) {
            // Check if any result has very high text overlap (>60% token match)
            const queryTokens = new Set(text.toLowerCase().split(/\W+/).filter(t => t.length > 2));
            for (const chunk of similar) {
                const chunkTokens = new Set((chunk.text || '').toLowerCase().split(/\W+/).filter((t: string) => t.length > 2));
                const overlap = [...queryTokens].filter(t => chunkTokens.has(t)).length;
                const ratio = overlap / Math.max(queryTokens.size, 1);
                if (ratio > 0.6) return false; // Already known
            }
        }

        const entry = {
            text: text.substring(0, 2000), // Cap at 2000 chars
            timestamp: Date.now(),
            source,
            session_id: sessionId || 'unknown'
        };

        const capturePath = getCapturedPath();
        const dir = path.dirname(capturePath);
        if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
        fs.appendFileSync(capturePath, JSON.stringify(entry) + '\n');
        console.log(`${TAG} Captured memory from ${source} (${text.length} chars)`);
        return true;
    } catch (e: any) {
        console.error(`${TAG} Capture failed:`, e.message);
        return false;
    }
}

// ── Extract user messages from hook context ─────────────────────────────

function extractUserMessages(context: any): string[] {
    const messages: string[] = [];
    if (!context) return messages;

    // OpenClaw passes context in various shapes — handle the common ones
    if (Array.isArray(context.messages)) {
        for (const msg of context.messages) {
            if (msg.role === 'user' && typeof msg.content === 'string') {
                messages.push(msg.content);
            } else if (msg.role === 'user' && Array.isArray(msg.content)) {
                for (const part of msg.content) {
                    if (part.type === 'text') messages.push(part.text);
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

// ── Hook Registration ───────────────────────────────────────────────────

export interface HooksConfig {
    enableAutoCapture?: boolean;
    enableAutoRecall?: boolean;
    enableRulePinning?: boolean;
}

export function registerHooks(api: any, config: HooksConfig = {}) {
    const enableAutoRecall = config.enableAutoRecall ?? true;
    const enableAutoCapture = config.enableAutoCapture ?? false;
    const enableRulePinning = config.enableRulePinning ?? false;

    // ── before_agent_start: Auto-Recall ──────────────────────────────────
    if (!enableAutoRecall) {
        console.log('[openclaw-memory-max] ⊘ Auto-Recall disabled (opt-in via config.enableAutoRecall).');
    }

    api.on('before_agent_start', async (context: any) => {
        if (!enableAutoRecall) return;
        try {
            const userMessages = extractUserMessages(context);
            if (userMessages.length === 0) return;

            const latestMessage = userMessages[userMessages.length - 1];
            if (latestMessage.length < 10) return; // Skip trivial messages

            // Stage 1: FTS5 pre-filter
            const candidates = await searchChunksFTS(latestMessage, 20);
            if (candidates.length === 0) return;

            // Stage 2: Cross-encoder rerank (uses cached model)
            const ranked = await rerankCandidates(latestMessage, candidates, 5, 0.3);
            if (ranked.length === 0) return;

            // Stage 3: Query causal graph for relevant experience
            let experienceXml = '';
            try {
                const chains = await queryGraphForHook(latestMessage, 2);
                if (chains.length > 0) {
                    experienceXml = '\n<relevant-experience>\n' +
                        chains.map(c => `  <chain outcome="${c.outcome}">${c.cause} → ${c.action} → ${c.effect}</chain>`).join('\n') +
                        '\n</relevant-experience>';
                }
            } catch {
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
                if (tokenBudget <= 0) break;
            }
            memoriesXml += '</relevant-memories>';

            // Stage 4: Pinned rules (opt-in only)
            let pinnedXml = '';
            if (enableRulePinning) {
                pinnedXml = buildPinnedRulesXml();
            }

            const injection = memoriesXml + experienceXml + pinnedXml;

            // Inject into context — OpenClaw supports systemPrompt prepend or context injection
            if (context.addSystemContent) {
                context.addSystemContent(injection);
            } else if (context.systemPrompt !== undefined) {
                context.systemPrompt = (context.systemPrompt || '') + '\n\n' + injection;
            } else if (context.prependMessages) {
                context.prependMessages([{ role: 'system', content: injection }]);
            }

            console.log(`${TAG} Auto-recall: injected ${ranked.length} memories + ${experienceXml ? 'experience' : 'no experience'}${pinnedXml ? ' + pinned rules' : ''}`);
        } catch (e: any) {
            console.error(`${TAG} Auto-recall failed:`, e.message);
        }
    });

    // ── agent_end: Auto-Capture ──────────────────────────────────────────
    if (!enableAutoCapture) {
        console.log('[openclaw-memory-max] ⊘ Auto-Capture disabled (opt-in via config.enableAutoCapture).');
    }

    api.on('agent_end', async (context: any) => {
        if (!enableAutoCapture) return;
        try {
            const userMessages = extractUserMessages(context);
            let captured = 0;

            for (const msg of userMessages) {
                if (isHighValue(msg)) {
                    const ok = await captureMemory(msg, 'auto-capture', context.sessionId);
                    if (ok) captured++;
                }
            }

            if (captured > 0) {
                console.log(`${TAG} Auto-capture: stored ${captured} high-value messages`);
            }
        } catch (e: any) {
            console.error(`${TAG} Auto-capture failed:`, e.message);
        }
    });

    // ── before_compaction: Memory Rescue ─────────────────────────────────
    api.on('before_compaction', async (context: any) => {
        if (!enableAutoCapture) return;
        try {
            const userMessages = extractUserMessages(context);
            let rescued = 0;

            for (const msg of userMessages) {
                if (isHighValue(msg)) {
                    const ok = await captureMemory(msg, 'compaction-rescue', context.sessionId);
                    if (ok) rescued++;
                }
            }

            if (rescued > 0) {
                console.log(`${TAG} Compaction rescue: saved ${rescued} messages before context eviction`);
            }
        } catch (e: any) {
            console.error(`${TAG} Compaction rescue failed:`, e.message);
        }
    });

    const active = [enableAutoRecall && 'auto-recall', enableAutoCapture && 'auto-capture', enableAutoCapture && 'compaction-rescue'].filter(Boolean).join(', ');
    console.log(`[openclaw-memory-max] ✓ Lifecycle hooks registered (${active || 'all disabled'}).`);
}
