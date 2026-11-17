/**
 * 🧠 Memoria — Post-capture orchestrator
 * 
 * This module exports:
 *   - createPostProcessNewFacts() — factory for the post-processing pipeline
 * 
 * The post-processing pipeline runs after every batch of new facts (capture/compaction/continuous).
 * It orchestrates 9 steps across all layers: embed, graph, hebbian, topics, observations, clusters, md sync, patterns, cross-layer.
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk/core";
import type { MemoriaDB } from "./core/db.js";
import type { EmbeddingManager } from "./core/embeddings.js";
import type { KnowledgeGraph } from "./core/graph.js";
import type { HebbianManager } from "./core/hebbian.js";
import type { TopicManager } from "./core/topics.js";
import type { ObservationManager } from "./core/observations.js";
import type { FactClusterManager } from "./core/fact-clusters.js";
import type { MdSync } from "./core/sync.js";
import type { MdRegenManager } from "./core/md-regen.js";
import type { PatternManager } from "./core/patterns.js";

/**
 * Create the postProcessNewFacts pipeline function.
 * Called after every capture batch (agent_end, after_compaction, continuous).
 * 
 * 9 steps:
 *   1. embedBatch() — vectorize unembedded facts
 *   2. graph.extractAndStore() — entities + relations from new facts
 *   3. hebbian.reinforce() — strengthen co-occurring entity relations
 *   4. topics.onFactCaptured() + scanAndEmerge() — keyword extraction, topic creation
 *   5. observations.onFactCaptured() — match/create living syntheses
 *   6. clusters.generateClusters() — entity-grouped summaries
 *   7. mdSync.syncToMd() + mdRegen — append to .md files, regenerate if > 200 lines
 *   8. patterns.detectAndConsolidate() — consolidate repeated similar facts
 *   9. Cross-layer: feedback→lifecycle, hebbian→topics hierarchy, lifecycle→patterns
 */
export function createPostProcessNewFacts(
  api: OpenClawPluginApi,
  db: MemoriaDB,
  embeddingMgr: EmbeddingManager,
  graph: KnowledgeGraph,
  hebbianMgr: HebbianManager,
  topicMgr: TopicManager,
  observationMgr: ObservationManager,
  clusterMgr: FactClusterManager,
  mdSync: MdSync,
  mdRegen: MdRegenManager,
  patternMgr: PatternManager
): (source: "capture" | "compaction") => Promise<void> {
  return async function postProcessNewFacts(source: "capture" | "compaction"): Promise<void> {
    // 1. Embed unembedded facts
    try {
      const toEmbed = embeddingMgr.unembeddedFacts(10);
      if (toEmbed.length > 0) {
        const n = await embeddingMgr.embedBatch(toEmbed.map(f => ({ id: f.id, text: f.fact })));
        if (n > 0) api.logger.info?.(`memoria: [${source}] embedded ${n} new facts`);
      }
    } catch (e) { api?.logger?.debug?.('memoria:embed-batch: ' + String(e)); }

    // 2. Graph: extract entities/relations (limit to 5 to avoid LLM spam)
    try {
      const recentFacts = db.recentFacts(5);
      let totalEnt = 0, totalRel = 0;
      for (const f of recentFacts) {
        if (f.entity_ids && f.entity_ids !== "[]") continue;
        const { entities: ne, relations: nr } = await graph.extractAndStore(f.id, f.fact);
        totalEnt += ne;
        totalRel += nr;

        // Hebbian reinforcement: co-occurring entities strengthen relations
        if (f.entity_ids && f.entity_ids !== "[]") {
          const entityIds = JSON.parse(f.entity_ids) as string[];
          hebbianMgr.reinforceFromFact(f.id, entityIds);
        }
      }
      if (totalEnt > 0 || totalRel > 0) {
        api.logger.info?.(`memoria: [${source}] graph extracted ${totalEnt} entities, ${totalRel} relations`);
      }
    } catch (e) { api?.logger?.debug?.('memoria:graph-extract: ' + String(e)); }

    // 3. Topics: keyword extraction + topic association
    try {
      const recentForTopics = db.recentFacts(3);
      for (const f of recentForTopics) {
        if (f.tags && f.tags !== "[]") continue;
        const { keywords, topics: topicNames } = await topicMgr.onFactCaptured(f.id, f.fact, f.category);
        if (keywords.length > 0) {
          api.logger.debug?.(`memoria: [${source}] tagged "${f.fact.slice(0, 40)}..." → [${keywords.join(", ")}]${topicNames.length > 0 ? ` → topics: ${topicNames.join(", ")}` : ""}`);
        }
      }
      if (topicMgr.shouldScan()) {
        const scanResult = await topicMgr.scanAndEmerge();
        if (scanResult.created > 0 || scanResult.merged > 0 || scanResult.subtopics > 0) {
          api.logger.info?.(`memoria: [${source}] topics scan — ${scanResult.created} created, ${scanResult.merged} merged, ${scanResult.subtopics} sub-topics`);
        }
      }
    } catch (topicErr) {
      api.logger.debug?.(`memoria: [${source}] topic tagging non-critical error: ${String(topicErr)}`);
    }

    // 4. Observations: check if new facts match or trigger new observations
    try {
      const recentForObs = db.recentFacts(3);
      let obsUpdated = 0, obsCreated = 0;
      for (const f of recentForObs) {
        const result = await observationMgr.onFactCaptured(f.id, f.fact, f.category);
        if (result.action === "updated_observation") obsUpdated++;
        if (result.action === "created_observation") obsCreated++;
      }
      if (obsUpdated > 0 || obsCreated > 0) {
        api.logger.info?.(`memoria: [${source}] observations — ${obsCreated} created, ${obsUpdated} updated`);
      }
    } catch (e) { api?.logger?.debug?.('memoria:observations: ' + String(e)); }

    // 5. Fact Clusters: generate/refresh thematic summaries
    try {
      const clusterResult = await clusterMgr.generateClusters();
      if (clusterResult.created > 0 || clusterResult.updated > 0) {
        api.logger.info?.(`memoria: [${source}] clusters — ${clusterResult.created} created, ${clusterResult.updated} updated, ${clusterResult.stale} stale`);
        // Embed new clusters
        const toEmbed = embeddingMgr.unembeddedFacts(5);
        if (toEmbed.length > 0) {
          await embeddingMgr.embedBatch(toEmbed.map(f => ({ id: f.id, text: f.fact })));
        }
      }
    } catch (e) { api?.logger?.debug?.('memoria:clusters: ' + String(e)); }

    // 6. Sync new facts to .md files
    try {
      const syncResult = mdSync.syncToMd(db);
      if (syncResult.synced > 0) {
        api.logger.info?.(`memoria: [${source}] synced ${syncResult.synced} facts to .md files`);
      }
    } catch (e) { api?.logger?.debug?.('memoria:md-sync: ' + String(e)); }

    // 7. Auto md-regen: smart trigger (captures count OR stale OR file size)
    try {
      mdRegen.recordCapture();
      const regenReason = mdRegen.shouldAutoRegen();
      if (regenReason) {
        const regenResult = mdRegen.regenerate();
        api.logger.info?.(`memoria: [${source}] auto md-regen triggered (${regenReason}) — ${regenResult.files} files, ${regenResult.recentFacts} recent, ${regenResult.archivedFacts} archived`);
      }
    } catch (e) { api?.logger?.debug?.('memoria:md-regen: ' + String(e)); }

    // 8. Pattern detection: consolidate repeated similar facts
    try {
      const patternResult = await patternMgr.detectAndConsolidate();
      if (patternResult.consolidated > 0) {
        api.logger.info?.(`memoria: [${source}] patterns — ${patternResult.detected} groups found, ${patternResult.consolidated} consolidated`);
      }
    } catch (e) { api?.logger?.debug?.('memoria:patterns: ' + String(e)); }

    // 9. Cross-layer connections (Phase 3)
    try {
      let crossUpdates = 0;

      // 9a. Feedback → lifecycle promotion
      // Facts recalled 5+ times with positive usefulness → force settled
      const highUseFacts = db.raw.prepare(
        `SELECT id, lifecycle_state, recall_count, usefulness FROM facts 
         WHERE superseded = 0 AND recall_count >= 5 AND usefulness >= 2 
         AND (lifecycle_state IS NULL OR lifecycle_state = 'fresh')`
      ).all() as Array<{ id: string; lifecycle_state: string; recall_count: number; usefulness: number }>;
      for (const f of highUseFacts) {
        db.raw.prepare("UPDATE facts SET lifecycle_state = 'settled' WHERE id = ?").run(f.id);
        crossUpdates++;
      }

      // 9b. Hebbian → topics: strong relations (weight >= 1.0) between entities
      // If both entities belong to different topics, suggest parent-child or merge
      const strongRelations = db.raw.prepare(
        `SELECT source_id, target_id, weight FROM relations WHERE weight >= 1.0 ORDER BY weight DESC LIMIT 20`
      ).all() as Array<{ source_id: string; target_id: string; weight: number }>;
      for (const rel of strongRelations) {
        // Find topics for each entity
        const fromTopics = db.raw.prepare(
          `SELECT DISTINCT t.id, t.name, t.parent_topic_id FROM topics t 
           JOIN fact_topics ft ON ft.topic_id = t.id 
           JOIN facts f ON f.id = ft.fact_id 
           WHERE f.entity_ids LIKE ? AND f.superseded = 0`
        ).all(`%${rel.source_id}%`) as Array<{ id: string; name: string; parent_topic_id: string | null }>;
        const toTopics = db.raw.prepare(
          `SELECT DISTINCT t.id, t.name, t.parent_topic_id FROM topics t 
           JOIN fact_topics ft ON ft.topic_id = t.id 
           JOIN facts f ON f.id = ft.fact_id 
           WHERE f.entity_ids LIKE ? AND f.superseded = 0`
        ).all(`%${rel.target_id}%`) as Array<{ id: string; name: string; parent_topic_id: string | null }>;

        // If one topic is smaller, make it child of the larger
        for (const ft of fromTopics) {
          for (const tt of toTopics) {
            if (ft.id === tt.id) continue;
            if (ft.parent_topic_id || tt.parent_topic_id) continue; // already has parent
            const ftCount = (db.raw.prepare("SELECT fact_count FROM topics WHERE id = ?").get(ft.id) as any)?.fact_count || 0;
            const ttCount = (db.raw.prepare("SELECT fact_count FROM topics WHERE id = ?").get(tt.id) as any)?.fact_count || 0;
            // Smaller becomes child of larger (only if ratio > 2:1)
            if (ftCount > ttCount * 2 && ttCount > 0) {
              db.raw.prepare("UPDATE topics SET parent_topic_id = ? WHERE id = ?").run(ft.id, tt.id);
              crossUpdates++;
            } else if (ttCount > ftCount * 2 && ftCount > 0) {
              db.raw.prepare("UPDATE topics SET parent_topic_id = ? WHERE id = ?").run(tt.id, ft.id);
              crossUpdates++;
            }
          }
        }
      }

      // 9c. Lifecycle → patterns: confirmed patterns (5+ occurrences) → settled
      const freshPatterns = db.raw.prepare(
        `SELECT id, tags FROM facts WHERE fact_type = 'pattern' AND superseded = 0 
         AND (lifecycle_state IS NULL OR lifecycle_state = 'fresh')`
      ).all() as Array<{ id: string; tags: string }>;
      for (const p of freshPatterns) {
        try {
          const meta = JSON.parse(p.tags || "{}");
          if (meta.occurrences && meta.occurrences.length >= 5) {
            db.raw.prepare("UPDATE facts SET lifecycle_state = 'settled' WHERE id = ?").run(p.id);
            crossUpdates++;
          }
        } catch (e) { api?.logger?.debug?.('memoria:parse: ' + String(e)); }
      }

      if (crossUpdates > 0) {
        api.logger.info?.(`memoria: [${source}] cross-layer — ${crossUpdates} updates (feedback→lifecycle, hebbian→topics, lifecycle→patterns)`);
      }
    } catch (e) { api?.logger?.debug?.('memoria:cross-layer: ' + String(e)); }
  };
}
