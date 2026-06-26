"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.buildConsolidationContext = buildConsolidationContext;
exports.ensureSleepCycle = ensureSleepCycle;
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
const graph_1 = require("./graph");
const episodic_1 = require("./episodic");
const TAG = '[openclaw-memory-max]';
function getBaseDir() {
    return process.env.OPENCLAW_HOME || path_1.default.join(process.env.HOME || '/root', '.openclaw');
}
function getScoresPath() {
    return path_1.default.join(getBaseDir(), 'memory', 'utility_scores.json');
}
function getCapturedPath() {
    return path_1.default.join(getBaseDir(), 'memory', 'auto_captured.jsonl');
}
function getConsolidationPath() {
    return path_1.default.join(getBaseDir(), 'memory', 'consolidation_context.md');
}
/** Decay utility scores for memories not accessed recently. */
function decayUtilityScores(decayFactor = 0.99) {
    const scoresPath = getScoresPath();
    if (!fs_1.default.existsSync(scoresPath))
        return 0;
    try {
        const scores = JSON.parse(fs_1.default.readFileSync(scoresPath, 'utf8'));
        let decayed = 0;
        for (const id of Object.keys(scores)) {
            const current = scores[id];
            if (current !== 0.5) {
                scores[id] = parseFloat((current * decayFactor).toFixed(4));
                if (Math.abs(scores[id] - 0.5) < 0.01)
                    scores[id] = 0.5;
                decayed++;
            }
        }
        fs_1.default.writeFileSync(scoresPath, JSON.stringify(scores, null, 2));
        return decayed;
    }
    catch {
        return 0;
    }
}
/** Truncate auto_captured.jsonl entries older than N days. */
function truncateCaptures(days = 30) {
    const capturePath = getCapturedPath();
    if (!fs_1.default.existsSync(capturePath))
        return 0;
    try {
        const cutoff = Date.now() - (days * 24 * 60 * 60 * 1000);
        const lines = fs_1.default.readFileSync(capturePath, 'utf8').split('\n').filter(Boolean);
        const kept = [];
        let removed = 0;
        for (const line of lines) {
            try {
                const entry = JSON.parse(line);
                if (entry.timestamp >= cutoff) {
                    kept.push(line);
                }
                else {
                    removed++;
                }
            }
            catch {
                removed++;
            }
        }
        fs_1.default.writeFileSync(capturePath, kept.join('\n') + (kept.length > 0 ? '\n' : ''));
        return removed;
    }
    catch {
        return 0;
    }
}
/** Build a summary of recent auto-captures and episodes. */
function buildConsolidationContext() {
    const parts = [];
    const capturePath = getCapturedPath();
    if (fs_1.default.existsSync(capturePath)) {
        const cutoff = Date.now() - (24 * 60 * 60 * 1000);
        const lines = fs_1.default.readFileSync(capturePath, 'utf8').split('\n').filter(Boolean);
        const recent = [];
        for (const line of lines) {
            try {
                const entry = JSON.parse(line);
                if (entry.timestamp >= cutoff) {
                    recent.push(`- [${entry.source}] ${entry.text.substring(0, 200)}`);
                }
            }
            catch { /* skip */ }
        }
        if (recent.length > 0) {
            parts.push(`AUTO-CAPTURED MEMORIES (last 24h, ${recent.length} items):\n${recent.join('\n')}`);
        }
    }
    const episodes = (0, episodic_1.readRecentEpisodes)(7);
    if (episodes.length > 0) {
        const epSummaries = episodes.slice(-5).map(ep => {
            const date = new Date(ep.start).toISOString().split('T')[0];
            return `- [${date}] ${ep.summary || 'No summary'} (tools: ${ep.toolsUsed.join(', ') || 'none'})`;
        });
        parts.push(`RECENT SESSIONS (last 7 days, ${episodes.length} total):\n${epSummaries.join('\n')}`);
    }
    return parts.join('\n\n');
}
/** Run all maintenance tasks: prune graph, decay scores, truncate old data. */
function runMaintenance() {
    try {
        const graphResult = (0, graph_1.pruneGraph)();
        if (graphResult.removed > 0) {
            console.log(`${TAG} Graph pruned: ${graphResult.removed} nodes removed, ${graphResult.remaining} remaining.`);
        }
        const decayed = decayUtilityScores();
        if (decayed > 0) {
            console.log(`${TAG} Utility decay applied to ${decayed} scores.`);
        }
        const capturesRemoved = truncateCaptures(30);
        if (capturesRemoved > 0) {
            console.log(`${TAG} Truncated ${capturesRemoved} old auto-captures.`);
        }
        const episodesRemoved = (0, episodic_1.truncateEpisodes)(30);
        if (episodesRemoved > 0) {
            console.log(`${TAG} Truncated ${episodesRemoved} old episodes.`);
        }
        // Write consolidation context for the next agent session to pick up
        const context = buildConsolidationContext();
        if (context) {
            const contextPath = getConsolidationPath();
            const memDir = path_1.default.dirname(contextPath);
            if (!fs_1.default.existsSync(memDir))
                fs_1.default.mkdirSync(memDir, { recursive: true });
            fs_1.default.writeFileSync(contextPath, `# Memory-Max Consolidation Context\n\nGenerated: ${new Date().toISOString()}\n\n${context}\n`);
        }
    }
    catch (e) {
        console.error(`${TAG} Maintenance tasks failed:`, e.message);
    }
}
/** Track last maintenance run to avoid running more than once per 20h. */
let lastMaintenanceRun = 0;
function runMaintenanceIfDue() {
    const now = Date.now();
    const twentyHours = 20 * 60 * 60 * 1000;
    if (now - lastMaintenanceRun < twentyHours)
        return;
    lastMaintenanceRun = now;
    runMaintenance();
}
/**
 * Initialize the sleep cycle system.
 * Runs maintenance on startup + schedules a daily check via setInterval.
 * No child_process — all maintenance runs in-process.
 */
function ensureSleepCycle() {
    console.log(`${TAG} Initializing Sleep Cycle (in-process scheduler)...`);
    // Run maintenance immediately on startup
    runMaintenanceIfDue();
    // Schedule periodic check — runs every 6 hours, but maintenance
    // only actually executes once per 20 hours (dedup guard above)
    const SIX_HOURS = 6 * 60 * 60 * 1000;
    setInterval(() => {
        runMaintenanceIfDue();
    }, SIX_HOURS);
    console.log(`${TAG} Sleep Cycle active (maintenance every ~24h, next check in 6h).`);
    return Promise.resolve();
}
