"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.readRecentEpisodes = readRecentEpisodes;
exports.truncateEpisodes = truncateEpisodes;
exports.registerEpisodic = registerEpisodic;
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
const TAG = '[openclaw-memory-max][episodic]';
function getBaseDir() {
    return process.env.OPENCLAW_HOME || path_1.default.join(process.env.HOME || '/root', '.openclaw');
}
function getEpisodesPath() {
    return path_1.default.join(getBaseDir(), 'memory', 'episodes.jsonl');
}
function appendEpisode(episode) {
    const p = getEpisodesPath();
    const dir = path_1.default.dirname(p);
    if (!fs_1.default.existsSync(dir))
        fs_1.default.mkdirSync(dir, { recursive: true });
    fs_1.default.appendFileSync(p, JSON.stringify(episode) + '\n');
}
/** Read recent episodes (last N days). */
function readRecentEpisodes(days = 7) {
    const p = getEpisodesPath();
    if (!fs_1.default.existsSync(p))
        return [];
    const cutoff = Date.now() - (days * 24 * 60 * 60 * 1000);
    const lines = fs_1.default.readFileSync(p, 'utf8').split('\n').filter(Boolean);
    const episodes = [];
    for (const line of lines) {
        try {
            const ep = JSON.parse(line);
            if (ep.start >= cutoff)
                episodes.push(ep);
        }
        catch { /* skip malformed lines */ }
    }
    return episodes;
}
/** Truncate episodes older than N days. */
function truncateEpisodes(days = 30) {
    const p = getEpisodesPath();
    if (!fs_1.default.existsSync(p))
        return 0;
    const cutoff = Date.now() - (days * 24 * 60 * 60 * 1000);
    const lines = fs_1.default.readFileSync(p, 'utf8').split('\n').filter(Boolean);
    const kept = [];
    let removed = 0;
    for (const line of lines) {
        try {
            const ep = JSON.parse(line);
            if (ep.start >= cutoff) {
                kept.push(line);
            }
            else {
                removed++;
            }
        }
        catch {
            // Drop malformed
            removed++;
        }
    }
    fs_1.default.writeFileSync(p, kept.join('\n') + (kept.length > 0 ? '\n' : ''));
    return removed;
}
// ── Extract session metadata from hook context ──────────────────────────
function extractToolsUsed(context) {
    const tools = new Set();
    if (Array.isArray(context.messages)) {
        for (const msg of context.messages) {
            if (msg.role === 'assistant' && Array.isArray(msg.content)) {
                for (const part of msg.content) {
                    if (part.type === 'tool_use' && part.name) {
                        tools.add(part.name);
                    }
                }
            }
            // Also check tool_calls format
            if (msg.tool_calls && Array.isArray(msg.tool_calls)) {
                for (const tc of msg.tool_calls) {
                    if (tc.function?.name)
                        tools.add(tc.function.name);
                }
            }
        }
    }
    return [...tools];
}
function extractDecisions(context) {
    const decisions = [];
    if (!Array.isArray(context.messages))
        return decisions;
    const decisionPatterns = [
        /\bdecided to\b/i,
        /\bchose to\b/i,
        /\bwill use\b/i,
        /\bswitching to\b/i,
        /\binstead of\b/i,
    ];
    for (const msg of context.messages) {
        if (msg.role === 'assistant' && typeof msg.content === 'string') {
            for (const pattern of decisionPatterns) {
                if (pattern.test(msg.content)) {
                    // Extract the sentence containing the decision
                    const sentences = msg.content.split(/[.!?]+/).filter(Boolean);
                    for (const s of sentences) {
                        if (pattern.test(s) && s.trim().length > 15 && s.trim().length < 200) {
                            decisions.push(s.trim());
                        }
                    }
                }
            }
        }
    }
    return decisions.slice(0, 5); // Cap at 5 decisions per session
}
// ── Hook Registration ───────────────────────────────────────────────────
const activeSessions = new Map();
function registerEpisodic(api) {
    // session_start: create episode
    api.on('session_start', async (context) => {
        try {
            const sessionId = context.sessionId || context.id || `session-${Date.now()}`;
            const episode = {
                id: `ep-${Date.now()}-${Math.random().toString(36).substring(2, 8)}`,
                sessionId,
                start: Date.now(),
                keyDecisions: [],
                toolsUsed: []
            };
            activeSessions.set(sessionId, episode);
            console.log(`${TAG} Episode started: ${episode.id}`);
        }
        catch (e) {
            console.error(`${TAG} session_start failed:`, e.message);
        }
    });
    // session_end: finalize and store episode
    api.on('session_end', async (context) => {
        try {
            const sessionId = context.sessionId || context.id || '';
            let episode = activeSessions.get(sessionId);
            if (!episode) {
                // Create a retroactive episode
                episode = {
                    id: `ep-${Date.now()}-${Math.random().toString(36).substring(2, 8)}`,
                    sessionId,
                    start: Date.now() - 60000, // Approximate
                    keyDecisions: [],
                    toolsUsed: []
                };
            }
            episode.end = Date.now();
            episode.toolsUsed = extractToolsUsed(context);
            episode.keyDecisions = extractDecisions(context);
            // Generate a brief summary from the last user message
            const messages = Array.isArray(context.messages) ? context.messages : [];
            const lastUser = [...messages].reverse().find((m) => m.role === 'user');
            if (lastUser) {
                const text = typeof lastUser.content === 'string' ? lastUser.content : '';
                episode.summary = text.length > 200 ? text.substring(0, 200) + '...' : text;
            }
            appendEpisode(episode);
            activeSessions.delete(sessionId);
            console.log(`${TAG} Episode ended: ${episode.id} (${episode.toolsUsed.length} tools, ${episode.keyDecisions.length} decisions)`);
        }
        catch (e) {
            console.error(`${TAG} session_end failed:`, e.message);
        }
    });
    console.log('[openclaw-memory-max] ✓ Episodic Memory hooks registered (session segmentation).');
}
