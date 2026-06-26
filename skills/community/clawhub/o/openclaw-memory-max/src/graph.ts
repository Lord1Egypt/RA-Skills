import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { getClassifier } from './reranker';

interface CausalNode {
    id: string;
    cause: string;
    action: string;
    effect: string;
    outcome: 'success' | 'failure' | 'unknown';
    timestamp: number;
    tags: string[];
    frequency: number;
    lastAccessed: number;
}

interface CausalGraph {
    version: string;
    nodes: CausalNode[];
}

const MAX_GRAPH_NODES = 500;

function getGraphPath(): string {
    const baseDir = process.env.OPENCLAW_HOME || path.join(process.env.HOME || '/root', '.openclaw');
    return path.join(baseDir, 'memory', 'causal_graph.json');
}

function loadGraph(): CausalGraph {
    const gPath = getGraphPath();
    if (!fs.existsSync(gPath)) {
        return { version: '2.0.0', nodes: [] };
    }
    try {
        const graph = JSON.parse(fs.readFileSync(gPath, 'utf8'));
        // Migrate v1 nodes: add missing fields
        for (const node of graph.nodes) {
            if (node.frequency === undefined) node.frequency = 1;
            if (node.lastAccessed === undefined) node.lastAccessed = node.timestamp;
        }
        return graph;
    } catch {
        return { version: '2.0.0', nodes: [] };
    }
}

function saveGraph(graph: CausalGraph): void {
    const gPath = getGraphPath();
    const dir = path.dirname(gPath);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(gPath, JSON.stringify(graph, null, 2));
}

/** Quick Jaccard pre-filter for large graphs before cross-encoder scoring. */
function textSimilarityQuick(a: string, b: string): number {
    const tokensA = new Set(a.toLowerCase().split(/\W+/).filter(Boolean));
    const tokensB = new Set(b.toLowerCase().split(/\W+/).filter(Boolean));
    const intersection = [...tokensA].filter(t => tokensB.has(t)).length;
    const union = new Set([...tokensA, ...tokensB]).size;
    return union === 0 ? 0 : intersection / union;
}

/** Build tag index for fast tag-based pre-filtering. */
function buildTagIndex(nodes: CausalNode[]): Map<string, string[]> {
    const index = new Map<string, string[]>();
    for (const node of nodes) {
        for (const tag of node.tags) {
            const key = tag.toLowerCase();
            if (!index.has(key)) index.set(key, []);
            index.get(key)!.push(node.id);
        }
    }
    return index;
}

/** Semantic scoring: use cross-encoder when available, fall back to Jaccard. */
async function scoreNodes(query: string, nodes: CausalNode[], topK: number = 5): Promise<Array<{ score: number; node: CausalNode }>> {
    if (nodes.length === 0) return [];

    // Pre-filter: if >30 nodes, narrow to top 20 by Jaccard first
    let candidates = nodes;
    if (candidates.length > 30) {
        const quick = candidates.map(node => ({
            score: textSimilarityQuick(query, `${node.cause} ${node.action} ${node.effect}`),
            node
        }));
        quick.sort((a, b) => b.score - a.score);
        candidates = quick.slice(0, 20).map(q => q.node);
    }

    // Cross-encoder scoring
    try {
        const classifier = await getClassifier();
        const scored: Array<{ score: number; node: CausalNode }> = [];

        for (const node of candidates) {
            const nodeText = `${node.cause} ${node.action} ${node.effect}`;
            const output = await classifier(query, nodeText);
            const score = (output as any)[0]?.score || 0;
            scored.push({ score, node });
        }

        scored.sort((a, b) => b.score - a.score);
        return scored.slice(0, topK);
    } catch {
        // Fallback to Jaccard if cross-encoder unavailable
        const scored = candidates.map(node => ({
            score: textSimilarityQuick(query, `${node.cause} ${node.action} ${node.effect}`),
            node
        }));
        scored.sort((a, b) => b.score - a.score);
        return scored.slice(0, topK);
    }
}

/** Find a semantically similar node for dedup (cross-encoder score > threshold). */
async function findDuplicate(graph: CausalGraph, cause: string, action: string, effect: string, threshold: number = 0.85): Promise<CausalNode | null> {
    if (graph.nodes.length === 0) return null;

    const query = `${cause} ${action} ${effect}`;
    const results = await scoreNodes(query, graph.nodes, 1);

    if (results.length > 0 && results[0].score > threshold) {
        return results[0].node;
    }
    return null;
}

/** Prune low-value old nodes. Called by sleep cycle. */
export function pruneGraph(): { removed: number; remaining: number } {
    const graph = loadGraph();
    const now = Date.now();
    const NINETY_DAYS = 90 * 24 * 60 * 60 * 1000;

    // Remove: old + low-frequency + not recently accessed
    const before = graph.nodes.length;
    graph.nodes = graph.nodes.filter(node => {
        const age = now - node.timestamp;
        if (age > NINETY_DAYS && node.frequency <= 1 && (now - node.lastAccessed) > NINETY_DAYS) {
            return false; // Prune
        }
        return true;
    });

    // Hard cap: keep top nodes by (frequency * recency)
    if (graph.nodes.length > MAX_GRAPH_NODES) {
        graph.nodes.sort((a, b) => {
            const scoreA = a.frequency * (1 / (1 + (now - a.lastAccessed) / (24 * 60 * 60 * 1000)));
            const scoreB = b.frequency * (1 / (1 + (now - b.lastAccessed) / (24 * 60 * 60 * 1000)));
            return scoreB - scoreA;
        });
        graph.nodes = graph.nodes.slice(0, MAX_GRAPH_NODES);
    }

    saveGraph(graph);
    return { removed: before - graph.nodes.length, remaining: graph.nodes.length };
}

/** Hook-friendly graph query (no tool wrapper). Used by hooks.ts for auto-recall. */
export async function queryGraphForHook(query: string, topK: number = 2): Promise<Array<{ cause: string; action: string; effect: string; outcome: string }>> {
    const graph = loadGraph();
    if (graph.nodes.length === 0) return [];

    const results = await scoreNodes(query, graph.nodes, topK);
    // Update lastAccessed on matched nodes
    for (const r of results) {
        r.node.lastAccessed = Date.now();
    }
    if (results.length > 0) saveGraph(graph);

    return results
        .filter(r => r.score > 0.2)
        .map(r => ({
            cause: r.node.cause,
            action: r.node.action,
            effect: r.node.effect,
            outcome: r.node.outcome
        }));
}

function jsonResult(payload: any) {
    return {
        content: [{ type: 'text' as const, text: JSON.stringify(payload, null, 2) }],
        details: payload
    };
}

export function registerCausalGraph(api: any) {

    // Tool 1: Log a causal chain (with dedup)
    api.registerTool({
        name: 'memory_graph_add',
        description: 'Log a causal chain to long-term memory: what caused you to take an action and what the effect was. Call this AFTER you complete any meaningful action (tool use, decision, fix). Automatically deduplicates against existing chains.',
        parameters: {
            type: 'object',
            properties: {
                cause: { type: 'string', description: 'What situation or trigger prompted the action.' },
                action: { type: 'string', description: 'What you did (tool used, decision made).' },
                effect: { type: 'string', description: 'What happened as a result.' },
                outcome: { type: 'string', enum: ['success', 'failure', 'unknown'], description: 'Did it work?' },
                tags: { type: 'array', items: { type: 'string' }, description: 'Optional topic tags (e.g. ["ssh", "permissions"])' }
            },
            required: ['cause', 'action', 'effect', 'outcome']
        },
        async execute(_toolCallId: string, args: any) {
            const graph = loadGraph();

            // Dedup: check if a similar chain already exists
            const existing = await findDuplicate(graph, args.cause, args.action, args.effect);
            if (existing) {
                // Merge: update outcome if different, bump frequency
                existing.frequency++;
                existing.lastAccessed = Date.now();
                if (args.outcome !== existing.outcome && args.outcome !== 'unknown') {
                    existing.outcome = args.outcome;
                }
                // Merge tags
                const existingTags = new Set(existing.tags);
                for (const tag of (args.tags || [])) {
                    existingTags.add(tag);
                }
                existing.tags = [...existingTags];
                saveGraph(graph);
                return jsonResult({ status: 'merged', id: existing.id, frequency: existing.frequency, total: graph.nodes.length });
            }

            const node: CausalNode = {
                id: crypto.randomUUID(),
                cause: args.cause,
                action: args.action,
                effect: args.effect,
                outcome: args.outcome || 'unknown',
                timestamp: Date.now(),
                tags: args.tags || [],
                frequency: 1,
                lastAccessed: Date.now()
            };
            graph.nodes.push(node);
            saveGraph(graph);
            return jsonResult({ status: 'stored', id: node.id, total: graph.nodes.length });
        }
    });

    // Tool 2: Query for similar causal chains (semantic search)
    api.registerTool({
        name: 'memory_graph_query',
        description: 'Query the causal memory graph for past chains relevant to the current situation. Uses cross-encoder semantic matching, not just keyword overlap. Call this BEFORE taking any major action to check if you have relevant learned experience.',
        parameters: {
            type: 'object',
            properties: {
                query: { type: 'string', description: 'Describe the current situation or intended action.' },
                outcomeFilter: { type: 'string', enum: ['success', 'failure', 'unknown', 'all'], description: 'Filter by outcome type. Default: all.' }
            },
            required: ['query']
        },
        async execute(_toolCallId: string, args: any) {
            const graph = loadGraph();

            if (graph.nodes.length === 0) {
                return jsonResult({ status: 'empty', message: 'No causal memory nodes yet.' });
            }

            const outcomeFilter = args.outcomeFilter || 'all';
            let candidates = graph.nodes;
            if (outcomeFilter !== 'all') {
                candidates = candidates.filter(n => n.outcome === outcomeFilter);
            }

            // Tag-based pre-filter: if query matches known tags, prioritize those
            const tagIndex = buildTagIndex(candidates);
            const queryWords = args.query.toLowerCase().split(/\W+/).filter(Boolean);
            const tagMatchIds = new Set<string>();
            for (const word of queryWords) {
                const ids = tagIndex.get(word);
                if (ids) ids.forEach(id => tagMatchIds.add(id));
            }

            // If tag matches found, put them first (but still include others)
            if (tagMatchIds.size > 0 && tagMatchIds.size < candidates.length) {
                const tagged = candidates.filter(n => tagMatchIds.has(n.id));
                const untagged = candidates.filter(n => !tagMatchIds.has(n.id));
                candidates = [...tagged, ...untagged];
            }

            const scored = await scoreNodes(args.query, candidates, 5);

            // Update lastAccessed
            for (const r of scored) {
                r.node.lastAccessed = Date.now();
            }
            if (scored.length > 0) saveGraph(graph);

            return jsonResult({
                status: 'results',
                total_in_db: graph.nodes.length,
                results: scored.map(({ score, node }) => ({
                    score: parseFloat(score.toFixed(4)),
                    outcome: node.outcome,
                    cause: node.cause,
                    action: node.action,
                    effect: node.effect,
                    tags: node.tags,
                    frequency: node.frequency,
                    timestamp: new Date(node.timestamp).toISOString()
                }))
            });
        }
    });

    // Tool 3: Get a full summary of everything the agent has learned
    api.registerTool({
        name: 'memory_graph_summary',
        description: 'Returns a digest of all learned causal chains, grouped by outcome. Useful for self-auditing or bootstrapping context at the start of a session.',
        parameters: { type: 'object', properties: {} },
        async execute(_toolCallId: string, _args: any) {
            const graph = loadGraph();
            const total = graph.nodes.length;
            const successes = graph.nodes.filter(n => n.outcome === 'success').length;
            const failures = graph.nodes.filter(n => n.outcome === 'failure').length;
            const unknown = graph.nodes.filter(n => n.outcome === 'unknown').length;
            const topFrequency = [...graph.nodes].sort((a, b) => b.frequency - a.frequency).slice(0, 3);

            const recentSuccesses = graph.nodes
                .filter(n => n.outcome === 'success')
                .slice(-3)
                .map(n => `[${n.tags.join(', ') || 'general'}] ${n.action} → ${n.effect}`);

            const recentFailures = graph.nodes
                .filter(n => n.outcome === 'failure')
                .slice(-3)
                .map(n => `[${n.tags.join(', ') || 'general'}] ${n.action} → ${n.effect}`);

            return jsonResult({
                status: 'ok',
                total,
                successes,
                failures,
                unknown,
                most_frequent: topFrequency.map(n => ({
                    action: n.action,
                    frequency: n.frequency,
                    outcome: n.outcome
                })),
                recent_successes: recentSuccesses,
                recent_failures: recentFailures
            });
        }
    });

    console.log('[openclaw-memory-max] Causal Knowledge Graph (3 tools) registered.');
}
