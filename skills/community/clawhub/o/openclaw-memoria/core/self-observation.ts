/**
 * Memoria — AI Self-Observation (Layer 22)
 *
 * Tracks the agent's own behavioral patterns over time:
 * - What tasks it handles well (high success rate)
 * - What tasks it struggles with (corrections, retries)
 * - Recurring error patterns
 * - Strengths and weaknesses profile
 *
 * Inspired by Hermes' "AI self-observation" concept.
 *
 * Table: self_observations
 *   - id: auto-increment
 *   - domain: string (coding, design, infra, memory, communication, etc.)
 *   - signal: "success" | "correction" | "frustration" | "retry"
 *   - detail: string (what happened)
 *   - created_at: timestamp ms
 */

import type Database from "better-sqlite3";

export interface SelfObservation {
  id: number;
  domain: string;
  signal: "success" | "correction" | "frustration" | "retry";
  detail: string;
  created_at: number;
}

export interface AgentProfile {
  strengths: Array<{ domain: string; score: number; evidence: number }>;
  weaknesses: Array<{ domain: string; score: number; evidence: number }>;
  recentPatterns: string[];
  totalObservations: number;
}

// Domain detection patterns
const DOMAIN_PATTERNS: Array<{ domain: string; patterns: RegExp[] }> = [
  { domain: "coding", patterns: [/\b(code|commit|push|git|deploy|build|npm|typescript|bug|fix|refactor)\b/i] },
  { domain: "design", patterns: [/\b(design|pencil|screen|ui|ux|figma|mockup|icon|layout)\b/i] },
  { domain: "infra", patterns: [/\b(server|ssh|gateway|restart|docker|ollama|sol|luna|deploy)\b/i] },
  { domain: "memory", patterns: [/\b(memoria|recall|fact|extract|embed|memory|convex)\b/i] },
  { domain: "communication", patterns: [/\b(tweet|discord|telegram|message|post|thread|social)\b/i] },
  { domain: "writing", patterns: [/\b(article|doc|readme|study|étude|report|analyse)\b/i] },
  { domain: "planning", patterns: [/\b(plan|roadmap|objectif|priorit|strateg|pipeline)\b/i] },
];

export class SelfObserver {
  private db: Database.Database;

  constructor(db: Database.Database) {
    this.db = db;
    this.ensureTable();
  }

  private ensureTable(): void {
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS self_observations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        domain TEXT NOT NULL,
        signal TEXT NOT NULL CHECK(signal IN ('success', 'correction', 'frustration', 'retry')),
        detail TEXT NOT NULL DEFAULT '',
        created_at INTEGER NOT NULL
      );
      CREATE INDEX IF NOT EXISTS idx_self_obs_domain
        ON self_observations(domain, signal);
    `);
  }

  /**
   * Record an observation about the agent's own behavior.
   */
  record(signal: SelfObservation["signal"], context: string, domainHint?: string): void {
    const domain = domainHint || this.detectDomain(context);
    const detail = context.slice(0, 500);
    this.db.prepare(
      "INSERT INTO self_observations (domain, signal, detail, created_at) VALUES (?, ?, ?, ?)"
    ).run(domain, signal, detail, Date.now());
  }

  /**
   * Detect the domain from message context.
   */
  detectDomain(text: string): string {
    for (const { domain, patterns } of DOMAIN_PATTERNS) {
      if (patterns.some(p => p.test(text))) return domain;
    }
    return "general";
  }

  /**
   * Build a profile of the agent's strengths and weaknesses.
   * Based on success/correction ratio per domain over the last N days.
   */
  buildProfile(dayRange = 30): AgentProfile {
    const cutoff = Date.now() - dayRange * 86_400_000;

    const rows = this.db.prepare(`
      SELECT domain, signal, COUNT(*) as cnt
      FROM self_observations
      WHERE created_at > ?
      GROUP BY domain, signal
      ORDER BY domain
    `).all(cutoff) as Array<{ domain: string; signal: string; cnt: number }>;

    // Aggregate by domain
    const domains: Record<string, Record<string, number>> = {};
    for (const r of rows) {
      if (!domains[r.domain]) domains[r.domain] = {};
      domains[r.domain][r.signal] = r.cnt;
    }

    const strengths: AgentProfile["strengths"] = [];
    const weaknesses: AgentProfile["weaknesses"] = [];

    for (const [domain, signals] of Object.entries(domains)) {
      const successes = signals.success || 0;
      const corrections = signals.correction || 0;
      const frustrations = signals.frustration || 0;
      const retries = signals.retry || 0;
      const total = successes + corrections + frustrations + retries;
      if (total < 2) continue; // Not enough data

      // Score: successes / total, penalized by corrections+frustrations
      const score = (successes - corrections * 0.5 - frustrations * 1.0) / total;

      if (score >= 0.6) {
        strengths.push({ domain, score: Math.round(score * 100), evidence: total });
      } else if (score <= 0.3 && (corrections + frustrations) >= 2) {
        weaknesses.push({ domain, score: Math.round(score * 100), evidence: total });
      }
    }

    // Sort: strengths descending, weaknesses ascending
    strengths.sort((a, b) => b.score - a.score);
    weaknesses.sort((a, b) => a.score - b.score);

    // Recent patterns: last 10 observations, summarized
    const recent = this.db.prepare(
      "SELECT domain, signal, detail FROM self_observations ORDER BY created_at DESC LIMIT 10"
    ).all() as Array<{ domain: string; signal: string; detail: string }>;

    const recentPatterns = recent.map(r =>
      `${r.signal === "success" ? "✅" : r.signal === "correction" ? "📝" : r.signal === "frustration" ? "😤" : "🔄"} ${r.domain}: ${r.detail.slice(0, 80)}`
    );

    const totalRow = this.db.prepare(
      "SELECT COUNT(*) as cnt FROM self_observations"
    ).get() as { cnt: number };

    return {
      strengths,
      weaknesses,
      recentPatterns,
      totalObservations: totalRow.cnt,
    };
  }

  /**
   * Format profile for injection into the prompt (compact).
   */
  formatForPrompt(): string {
    const profile = this.buildProfile();
    if (profile.totalObservations < 5) return ""; // Not enough data yet

    const parts: string[] = [];

    if (profile.strengths.length > 0) {
      parts.push("**Strengths:** " + profile.strengths.map(s =>
        `${s.domain} (${s.score}%, ${s.evidence} obs.)`
      ).join(", "));
    }

    if (profile.weaknesses.length > 0) {
      parts.push("**Watch out:** " + profile.weaknesses.map(w =>
        `${w.domain} (${w.score}%, ${w.evidence} obs.)`
      ).join(", "));
    }

    return parts.length > 0
      ? `\n### 🪞 Self-Observation\n${parts.join("\n")}\n`
      : "";
  }
}
