/**
 * Proactive Revision — Like human memory refinement
 * 
 * When a fact is recalled 10+ times, it proves useful but might be:
 *   - Too vague ("Bureau gère des projets")
 *   - Too broad (multiple concepts in one)
 *   - Outdated (context changed)
 * 
 * Revision flow:
 *   1. Detect mature facts with recall_count >= threshold
 *   2. LLM proposes refinement (more precise, split, or supersede)
 *   3. If improved → create new fact(s) + supersede old
 *   4. Track revision history
 */

import type { MemoriaDB, Fact } from "./db.js";
import type { LLMProvider } from "./providers/types.js";

export const REVISION_CONFIG = {
  recallThreshold: 10,      // Trigger revision after 10 recalls
  cooldownDays: 7,          // Don't revise same fact again within 7 days
  maxRevisionsPerBoot: 3,   // Limit revisions per boot to avoid LLM spam
};

export interface RevisionProposal {
  action: "keep" | "refine" | "split";
  refined?: string;         // For "refine": improved version
  split?: string[];         // For "split": 2+ new facts
  reasoning: string;
}

export class RevisionManager {
  private revisionsThisBoot = 0;

  constructor(
    private db: MemoriaDB,
    private llm: LLMProvider,
  ) {}

  /**
   * Get facts needing revision
   */
  getFactsNeedingRevision(): Fact[] {
    const cooloffMs = REVISION_CONFIG.cooldownDays * 24 * 60 * 60 * 1000;
    const cutoff = Date.now() - cooloffMs;

    // Find mature facts with high recall count and no recent revision
    const facts = this.db.raw.prepare(`
      SELECT * FROM facts
      WHERE superseded = 0
      AND lifecycle_state = 'settled'
      AND recall_count >= ?
      AND (last_accessed_at IS NULL OR last_accessed_at >= ?)
      ORDER BY recall_count DESC
      LIMIT 5
    `).all(REVISION_CONFIG.recallThreshold, cutoff) as Fact[];

    return facts;
  }

  /**
   * Propose revision for a fact using LLM
   */
  async proposeRevision(fact: Fact): Promise<RevisionProposal> {
    const recallCount = fact.recall_count ?? 0;
    const usedCount = fact.used_count ?? 0;
    const usageRatio = recallCount > 0 ? (usedCount / recallCount * 100).toFixed(0) : "0";

    const prompt = `You are reviewing a memory fact that has been recalled ${recallCount} times (used in ${usageRatio}% of those recalls).

**Current fact:**
"${fact.fact}"

**Category:** ${fact.category}
**Type:** ${fact.fact_type}

**Your task:**
1. If the fact is already precise and complete → respond with JSON: {"action":"keep","reasoning":"..."}
2. If it can be refined (more precise/complete) → respond with JSON: {"action":"refine","refined":"IMPROVED FACT HERE","reasoning":"..."}
3. If it mixes multiple concepts → split into 2+ facts: {"action":"split","split":["fact1","fact2"],"reasoning":"..."}

**Rules:**
- Keep facts short (< 200 chars)
- Be concrete, not meta
- Don't add dates/timestamps (those are episodic facts)
- Respond ONLY with valid JSON, no markdown

Response:`;

    try {
      const response = await this.llm.generate(prompt);
      const cleaned = response.replace(/```json\n?/g, "").replace(/```\n?/g, "").trim();
      const proposal = JSON.parse(cleaned) as RevisionProposal;
      
      if (!proposal.action || !["keep", "refine", "split"].includes(proposal.action)) {
        throw new Error("Invalid action");
      }

      return proposal;
    } catch (err) {
      // Fallback: keep
      return {
        action: "keep",
        reasoning: `Revision failed: ${err}`,
      };
    }
  }

  /**
   * Apply revision proposal
   */
  async applyRevision(fact: Fact, proposal: RevisionProposal): Promise<{ created: number; superseded: boolean }> {
    let created = 0;
    let superseded = false;

    if (proposal.action === "keep") {
      return { created: 0, superseded: false };
    }

    const now = Date.now();

    if (proposal.action === "refine" && proposal.refined) {
      // Create refined version
      const newId = `fact_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`;
      this.db.raw.prepare(`
        INSERT INTO facts (
          id, fact, category, confidence, source, tags, agent,
          created_at, updated_at, access_count, superseded,
          fact_type, relevance_weight, lifecycle_state
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0, ?, ?, 'fresh')
      `).run(
        newId,
        proposal.refined,
        fact.category,
        fact.confidence,
        `revision:${fact.id}`,
        fact.tags,
        fact.agent,
        now,
        now,
        fact.fact_type,
        fact.relevance_weight,
      );
      created++;

      // Supersede old fact
      this.db.raw.prepare(`
        UPDATE facts SET superseded = 1, superseded_by = ?, superseded_at = ? WHERE id = ?
      `).run(newId, now, fact.id);
      superseded = true;
    } else if (proposal.action === "split" && proposal.split && proposal.split.length >= 2) {
      // Create multiple new facts
      for (const newFact of proposal.split) {
        const newId = `fact_${Date.now()}_${Math.random().toString(36).slice(2, 9)}`;
        this.db.raw.prepare(`
          INSERT INTO facts (
            id, fact, category, confidence, source, tags, agent,
            created_at, updated_at, access_count, superseded,
            fact_type, relevance_weight, lifecycle_state
          ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0, ?, ?, 'fresh')
        `).run(
          newId,
          newFact,
          fact.category,
          fact.confidence,
          `split:${fact.id}`,
          fact.tags,
          fact.agent,
          now,
          now,
          fact.fact_type,
          fact.relevance_weight,
        );
        created++;
      }

      // Supersede old fact (point to first split)
      const firstId = `split:${fact.id}`;
      this.db.raw.prepare(`
        UPDATE facts SET superseded = 1, superseded_by = ?, superseded_at = ? WHERE id = ?
      `).run(firstId, now, fact.id);
      superseded = true;
    }

    return { created, superseded };
  }

  /**
   * Run revision check and apply (called after recall)
   */
  async checkAndRevise(): Promise<{ checked: number; revised: number; created: number }> {
    if (this.revisionsThisBoot >= REVISION_CONFIG.maxRevisionsPerBoot) {
      return { checked: 0, revised: 0, created: 0 };
    }

    const candidates = this.getFactsNeedingRevision();
    let revised = 0;
    let created = 0;

    for (const fact of candidates.slice(0, REVISION_CONFIG.maxRevisionsPerBoot - this.revisionsThisBoot)) {
      const proposal = await this.proposeRevision(fact);
      const result = await this.applyRevision(fact, proposal);

      if (result.superseded) {
        revised++;
        created += result.created;
        this.revisionsThisBoot++;
      }

      if (this.revisionsThisBoot >= REVISION_CONFIG.maxRevisionsPerBoot) break;
    }

    return { checked: candidates.length, revised, created };
  }

  /**
   * Reset boot counter (called on plugin reload)
   */
  resetBootCounter(): void {
    this.revisionsThisBoot = 0;
  }
}
