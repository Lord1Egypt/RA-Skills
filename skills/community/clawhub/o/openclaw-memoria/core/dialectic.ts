/**
 * Memoria — Dialectic Memory (Layer 24)
 *
 * Enables natural language queries against the entire memory.
 * Instead of keyword search, the agent can ASK questions:
 *   "What frustrates the user about deployments?"
 *   "What's the current status of Primask?"
 *   "What patterns do I repeat when I make mistakes?"
 *
 * Inspired by Honcho's "dialectic" concept — memory as a conversation partner.
 *
 * Flow:
 * 1. Parse the natural language query
 * 2. Fan out: FTS5 + embeddings + graph + topics + procedures
 * 3. Aggregate all evidence
 * 4. Synthesize a structured answer via LLM
 */

import type { MemoriaDB, Fact } from "./db.js";
import type { EmbeddingManager } from "./embeddings.js";
import type { KnowledgeGraph } from "./graph.js";
import type { TopicManager } from "./topics.js";
import type { ProceduralMemory } from "./procedural.js";
import type { ObservationManager } from "./observations.js";
import type { LLMProvider } from "./providers/types.js";

export interface DialecticAnswer {
  answer: string;
  confidence: number;
  sources: Array<{
    type: "fact" | "procedure" | "observation" | "graph" | "topic";
    id: string;
    text: string;
    relevance: number;
  }>;
  reasoning?: string;
}

export interface DialecticDeps {
  db: MemoriaDB;
  embeddingMgr: EmbeddingManager;
  graph: KnowledgeGraph;
  topicMgr: TopicManager;
  proceduralMem: ProceduralMemory;
  observationMgr: ObservationManager;
  llm: LLMProvider;
}

export class DialecticMemory {
  private deps: DialecticDeps;

  constructor(deps: DialecticDeps) {
    this.deps = deps;
  }

  /**
   * Ask a natural language question to the memory.
   */
  async query(question: string): Promise<DialecticAnswer> {
    const { db, embeddingMgr, graph, topicMgr, proceduralMem, observationMgr, llm } = this.deps;

    // ── 1. Fan out: gather evidence from all sources ──
    const sources: DialecticAnswer["sources"] = [];

    // FTS5 + embeddings search
    try {
      if (embeddingMgr.embeddedCount() > 0) {
        const results = await embeddingMgr.hybridSearch(question, 10, {
          ftsWeight: 0.35,
          cosineWeight: 0.45,
          temporalWeight: 0.20,
        });
        for (const r of results) {
          sources.push({
            type: "fact",
            id: r.id,
            text: r.fact,
            relevance: r.temporalScore || 0.5,
          });
        }
      } else {
        const facts = db.searchFacts(question, 10);
        for (const f of facts) {
          sources.push({
            type: "fact",
            id: f.id,
            text: f.fact,
            relevance: f.confidence,
          });
        }
      }
    } catch { /* non-blocking */ }

    // Graph entities
    try {
      const entities = graph.findEntitiesInText(question);
      if (entities.length > 0) {
        const related = graph.getRelatedFacts(entities.map(e => e.name), 3, 5);
        for (const r of related) {
          const fact = db.getFact(r.id);
          if (fact && !sources.find(s => s.id === r.id)) {
            sources.push({
              type: "graph",
              id: r.id,
              text: fact.fact,
              relevance: 0.6,
            });
          }
        }
      }
    } catch { /* non-blocking */ }

    // Topics
    try {
      const expandedQueries = embeddingMgr.expandQuery(question);
      const topics = await topicMgr.findRelevantTopics(question, 3, expandedQueries);
      for (const t of topics) {
        sources.push({
          type: "topic",
          id: t.topic.id?.toString() || t.topic.name,
          text: `Topic "${t.topic.name}": ${t.facts.slice(0, 3).join("; ")}`,
          relevance: 0.5,
        });
      }
    } catch { /* non-blocking */ }

    // Procedures
    try {
      const procs = proceduralMem.search(question, 3);
      for (const p of procs) {
        sources.push({
          type: "procedure",
          id: p.id,
          text: `${p.name}: ${p.goal} (${p.steps.length} steps, ${p.success_count} successes)`,
          relevance: p.quality.overall,
        });
      }
    } catch { /* non-blocking */ }

    // Observations
    try {
      const obs = await observationMgr.getRelevantObservations(question);
      for (const o of obs) {
        const ob = (o as any).observation || o;
        sources.push({
          type: "observation",
          id: ob.id?.toString() || "obs",
          text: ob.content || ob.summary || ob.title || "",
          relevance: (o as any).score || 0.7,
        });
      }
    } catch { /* non-blocking */ }

    // ── 2. If no sources found, return early ──
    if (sources.length === 0) {
      return {
        answer: "Je n'ai trouvé aucune information pertinente dans ma mémoire sur ce sujet.",
        confidence: 0,
        sources: [],
      };
    }

    // Sort by relevance
    sources.sort((a, b) => b.relevance - a.relevance);
    const topSources = sources.slice(0, 15);

    // ── 3. Synthesize answer via LLM ──
    const synthesisPrompt = `You are a memory assistant. Answer the following question based ONLY on the evidence provided.
Be specific and cite which sources support your answer.
If evidence is contradictory, mention both sides.
If evidence is insufficient, say so honestly.

Question: ${question}

Evidence (sorted by relevance):
${topSources.map((s, i) => `[${i + 1}] (${s.type}, relevance: ${(s.relevance * 100).toFixed(0)}%) ${s.text}`).join("\n")}

Answer in the user's language (French if the question is in French).
Be concise but thorough. Output JSON:
{
  "answer": "Your synthesized answer",
  "confidence": 0.0-1.0,
  "reasoning": "Brief explanation of how you reached this answer"
}`;

    try {
      const response = await llm.generateWithMeta!(synthesisPrompt, {
        maxTokens: 1024,
        temperature: 0.2,
        format: "json",
        timeoutMs: 30000,
      });

      if (response?.response) {
        const cleaned = response.response.replace(/```json\n?|\n?```/g, "").trim();
        const parsed = JSON.parse(cleaned);
        return {
          answer: parsed.answer || "Pas de réponse générée.",
          confidence: parsed.confidence || 0.5,
          sources: topSources,
          reasoning: parsed.reasoning,
        };
      }
    } catch {
      // Fallback: return raw sources without synthesis
    }

    // Fallback: concatenate top sources
    return {
      answer: topSources.slice(0, 5).map(s => `• ${s.text}`).join("\n"),
      confidence: 0.3,
      sources: topSources,
      reasoning: "LLM synthesis failed — returning raw evidence.",
    };
  }

  /**
   * Quick factual lookup (no LLM, just search).
   * Faster but less intelligent than full query().
   */
  quickLookup(question: string, limit = 5): Fact[] {
    return this.deps.db.searchFacts(question, limit);
  }
}
