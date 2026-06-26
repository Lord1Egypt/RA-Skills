import { pipeline } from '@huggingface/transformers';
import { queryChunks, rewardMemory, searchChunksFTS } from './db';

function jsonResult(payload: any) {
  return {
    content: [{ type: 'text' as const, text: JSON.stringify(payload, null, 2) }],
    details: payload
  };
}

// ── Cross-encoder model singleton ──────────────────────────────────────
let _classifier: any = null;

export async function getClassifier() {
    if (!_classifier) {
        _classifier = await pipeline('text-classification', 'Xenova/ms-marco-MiniLM-L-6-v2');
    }
    return _classifier;
}

/** Score an array of {id, text, utility_score} candidates against a query. Returns sorted desc by finalScore. */
export async function rerankCandidates(query: string, candidates: any[], topK: number = 5, threshold: number = 0.1): Promise<any[]> {
    if (candidates.length === 0) return [];

    const classifier = await getClassifier();
    const firstRow = candidates[0];
    const textKey = Object.keys(firstRow).find(k => typeof firstRow[k] === 'string' && firstRow[k].length > 10) || 'text';

    const scored: any[] = [];
    for (const row of candidates) {
        const docText = row[textKey] || '';
        if (!docText) continue;
        const output = await classifier(query, docText);
        const semanticScore = (output as any)[0]?.score || 0;
        const utilityScore = row.utility_score !== undefined ? row.utility_score : 0.5;
        const finalScore = semanticScore * utilityScore;

        if (finalScore >= threshold) {
            scored.push({
                id: row.id || row.rowid || '',
                text: docText,
                semanticScore,
                utilityScore,
                finalScore,
                path: row.path || '',
                source: row.source || ''
            });
        }
    }

    scored.sort((a, b) => b.finalScore - a.finalScore);
    return scored.slice(0, topK);
}

export function registerReranker(api: any) {
  // 1. Register the Cross-Encoder Search with Utility Math (multi-result)
  api.registerTool({
    name: 'precision_memory_search',
    description: 'Search memory with Cross-Encoder precision and Utility Weighting. Returns the top K most relevant memories ranked by semantic match × utility score.',
    parameters: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'The exact question or topic to search for.' },
        topK: { type: 'number', description: 'Number of results to return (default 5, max 10).' }
      },
      required: ['query']
    },
    async execute(_toolCallId: string, args: any) {
      const topK = Math.min(Math.max(args.topK || 5, 1), 10);

      // Stage 1: FTS5 pre-filter (fast, ~0ms) — falls back to brute-force if FTS unavailable
      let candidates = await searchChunksFTS(args.query, 30);
      if (candidates.length === 0) {
        candidates = await queryChunks(100);
      }

      if (candidates.length === 0) {
        return jsonResult({ status: 'empty', memory: 'No explicit DB memories found.' });
      }

      // Stage 2+3: Cross-encoder rerank + utility weighting
      const results = await rerankCandidates(args.query, candidates, topK, 0.1);

      if (results.length === 0) {
        return jsonResult({ status: 'no_match', message: 'No memories scored above confidence threshold.' });
      }

      return jsonResult({
        status: 'precision_filtered',
        candidatesScanned: candidates.length,
        retainedCount: results.length,
        results: results.map(r => ({
          memoryId: r.id,
          confidence: parseFloat(r.finalScore.toFixed(4)),
          snippet: r.text.length > 300 ? r.text.substring(0, 300) + '...' : r.text,
          path: r.path,
          source: r.source
        }))
      });
    }
  });

  // 2. Register the Explicit Utility Reward Trigger
  api.registerTool({
    name: 'reward_memory_utility',
    description: 'Increments the utility score of a specific memory ID if it proved highly useful to the user. Call this after verifying a memory was successful or highly relevant.',
    parameters: {
      type: 'object',
      properties: {
        memoryId: { type: 'string', description: 'The ID of the memory to reward.' },
        rewardScalar: { type: 'number', description: 'The amount to increment (usually 0.1 to 0.3)' }
      },
      required: ['memoryId']
    },
    async execute(_toolCallId: string, args: any) {
      const scalar = args.rewardScalar || 0.1;
      const updated = await rewardMemory(args.memoryId, scalar);
      if (updated) {
        return jsonResult({ status: 'success', message: `Rewarded memory ${args.memoryId} by ${scalar}` });
      }
      return jsonResult({ status: 'not_found', message: `Memory ${args.memoryId} not found in any table` });
    }
  });

  // 3. Register the Explicit Utility Penalize Trigger
  api.registerTool({
    name: 'penalize_memory_utility',
    description: 'Decrements the utility score of a specific memory ID if it caused a hallucination or was irrelevant.',
    parameters: {
      type: 'object',
      properties: {
        memoryId: { type: 'string', description: 'The ID of the memory to penalize.' },
        penaltyScalar: { type: 'number', description: 'The amount to decrement (usually -0.1 to -0.3)' }
      },
      required: ['memoryId']
    },
    async execute(_toolCallId: string, args: any) {
      const penalty = -(Math.abs(args.penaltyScalar || 0.1));
      const updated = await rewardMemory(args.memoryId, penalty);
      if (updated) {
        return jsonResult({ status: 'success', message: `Penalized memory ${args.memoryId} by ${penalty}` });
      }
      return jsonResult({ status: 'not_found', message: `Memory ${args.memoryId} not found in any table` });
    }
  });

  // 4. Deep Multi-Hop Search — chains retrieval → entity extraction → re-retrieval → graph → merge
  api.registerTool({
    name: 'deep_memory_search',
    description: 'Multi-hop memory search. First retrieves memories for the query, extracts key concepts, runs a second search on those concepts, queries the causal graph, and merges all results. Use this for complex questions that might need connecting information across multiple memories.',
    parameters: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'The question or situation to deeply search for.' }
      },
      required: ['query']
    },
    async execute(_toolCallId: string, args: any) {
      // Hop 1: Initial search
      let candidates = await searchChunksFTS(args.query, 30);
      if (candidates.length === 0) candidates = await queryChunks(100);
      const hop1 = await rerankCandidates(args.query, candidates, 5, 0.1);

      // Extract key terms from top results that aren't in the original query
      const queryTokens = new Set(args.query.toLowerCase().split(/\W+/).filter((t: string) => t.length > 2));
      const extractedTerms = new Set<string>();
      for (const result of hop1.slice(0, 3)) {
        const tokens = result.text.toLowerCase().split(/\W+/).filter((t: string) => t.length > 3);
        for (const token of tokens) {
          if (!queryTokens.has(token)) extractedTerms.add(token);
        }
      }

      // Hop 2: Search using extracted concepts (top 10 unique terms)
      const hop2Terms = [...extractedTerms].slice(0, 10).join(' ');
      let hop2: any[] = [];
      if (hop2Terms) {
        let hop2Candidates = await searchChunksFTS(hop2Terms, 20);
        if (hop2Candidates.length === 0) hop2Candidates = await queryChunks(100);
        hop2 = await rerankCandidates(args.query, hop2Candidates, 5, 0.15);
      }

      // Merge + deduplicate
      const seen = new Set<string>();
      const merged: any[] = [];
      for (const r of [...hop1, ...hop2]) {
        if (!seen.has(r.id)) {
          seen.add(r.id);
          merged.push(r);
        }
      }
      merged.sort((a, b) => b.finalScore - a.finalScore);

      return jsonResult({
        status: 'deep_search_complete',
        hops: { hop1_results: hop1.length, hop2_results: hop2.length, extracted_terms: hop2Terms || '(none)' },
        totalUnique: merged.length,
        results: merged.slice(0, 8).map(r => ({
          memoryId: r.id,
          confidence: parseFloat(r.finalScore.toFixed(4)),
          snippet: r.text.length > 300 ? r.text.substring(0, 300) + '...' : r.text,
          path: r.path
        }))
      });
    }
  });
}
