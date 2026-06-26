import fs from 'fs';
import path from 'path';
import { pruneGraph } from './graph';
import { readRecentEpisodes, truncateEpisodes } from './episodic';

const TAG = '[openclaw-memory-max]';

function getBaseDir(): string {
    return process.env.OPENCLAW_HOME || path.join(process.env.HOME || '/root', '.openclaw');
}

function getScoresPath(): string {
    return path.join(getBaseDir(), 'memory', 'utility_scores.json');
}

function getCapturedPath(): string {
    return path.join(getBaseDir(), 'memory', 'auto_captured.jsonl');
}

function getConsolidationPath(): string {
    return path.join(getBaseDir(), 'memory', 'consolidation_context.md');
}

/** Decay utility scores for memories not accessed recently. */
function decayUtilityScores(decayFactor: number = 0.99): number {
    const scoresPath = getScoresPath();
    if (!fs.existsSync(scoresPath)) return 0;

    try {
        const scores: Record<string, number> = JSON.parse(fs.readFileSync(scoresPath, 'utf8'));
        let decayed = 0;

        for (const id of Object.keys(scores)) {
            const current = scores[id];
            if (current !== 0.5) {
                scores[id] = parseFloat((current * decayFactor).toFixed(4));
                if (Math.abs(scores[id] - 0.5) < 0.01) scores[id] = 0.5;
                decayed++;
            }
        }

        fs.writeFileSync(scoresPath, JSON.stringify(scores, null, 2));
        return decayed;
    } catch {
        return 0;
    }
}

/** Truncate auto_captured.jsonl entries older than N days. */
function truncateCaptures(days: number = 30): number {
    const capturePath = getCapturedPath();
    if (!fs.existsSync(capturePath)) return 0;

    try {
        const cutoff = Date.now() - (days * 24 * 60 * 60 * 1000);
        const lines = fs.readFileSync(capturePath, 'utf8').split('\n').filter(Boolean);
        const kept: string[] = [];
        let removed = 0;

        for (const line of lines) {
            try {
                const entry = JSON.parse(line);
                if (entry.timestamp >= cutoff) {
                    kept.push(line);
                } else {
                    removed++;
                }
            } catch {
                removed++;
            }
        }

        fs.writeFileSync(capturePath, kept.join('\n') + (kept.length > 0 ? '\n' : ''));
        return removed;
    } catch {
        return 0;
    }
}

/** Build a summary of recent auto-captures and episodes. */
export function buildConsolidationContext(): string {
    const parts: string[] = [];

    const capturePath = getCapturedPath();
    if (fs.existsSync(capturePath)) {
        const cutoff = Date.now() - (24 * 60 * 60 * 1000);
        const lines = fs.readFileSync(capturePath, 'utf8').split('\n').filter(Boolean);
        const recent: string[] = [];
        for (const line of lines) {
            try {
                const entry = JSON.parse(line);
                if (entry.timestamp >= cutoff) {
                    recent.push(`- [${entry.source}] ${entry.text.substring(0, 200)}`);
                }
            } catch { /* skip */ }
        }
        if (recent.length > 0) {
            parts.push(`AUTO-CAPTURED MEMORIES (last 24h, ${recent.length} items):\n${recent.join('\n')}`);
        }
    }

    const episodes = readRecentEpisodes(7);
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
function runMaintenance(): void {
    try {
        const graphResult = pruneGraph();
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

        const episodesRemoved = truncateEpisodes(30);
        if (episodesRemoved > 0) {
            console.log(`${TAG} Truncated ${episodesRemoved} old episodes.`);
        }

        // Write consolidation context for the next agent session to pick up
        const context = buildConsolidationContext();
        if (context) {
            const contextPath = getConsolidationPath();
            const memDir = path.dirname(contextPath);
            if (!fs.existsSync(memDir)) fs.mkdirSync(memDir, { recursive: true });
            fs.writeFileSync(contextPath, `# Memory-Max Consolidation Context\n\nGenerated: ${new Date().toISOString()}\n\n${context}\n`);
        }
    } catch (e: any) {
        console.error(`${TAG} Maintenance tasks failed:`, e.message);
    }
}

/** Track last maintenance run to avoid running more than once per 20h. */
let lastMaintenanceRun = 0;

function runMaintenanceIfDue(): void {
    const now = Date.now();
    const twentyHours = 20 * 60 * 60 * 1000;
    if (now - lastMaintenanceRun < twentyHours) return;
    lastMaintenanceRun = now;
    runMaintenance();
}

/**
 * Initialize the sleep cycle system.
 * Runs maintenance on startup + schedules a daily check via setInterval.
 * No child_process — all maintenance runs in-process.
 */
export function ensureSleepCycle(): Promise<void> {
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
