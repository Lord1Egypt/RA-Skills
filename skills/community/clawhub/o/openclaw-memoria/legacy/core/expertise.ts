/**
 * Expertise Manager — Specialization via topic interaction
 * 
 * Human memory develops expertise in frequently-used domains.
 * 
 * Levels:
 *   - novice:      interaction_count < 5
 *   - familiar:    5 <= count < 15
 *   - experienced: 15 <= count < 30
 *   - expert:      count >= 30
 * 
 * Usage:
 *   - Boost recall for facts in expert topics
 *   - Prioritize facts from expertise domains
 */

import type { MemoriaDB } from "./db.js";

export type ExpertiseLevel = "novice" | "familiar" | "experienced" | "expert";

export const EXPERTISE_CONFIG = {
  thresholds: {
    novice: 0,
    familiar: 5,
    experienced: 15,
    expert: 30,
  },
  recallBoost: {
    novice: 1.0,
    familiar: 1.1,
    experienced: 1.3,
    expert: 1.5,
  },
};

export interface TopicExpertise {
  topic: string;
  interactionCount: number;
  level: ExpertiseLevel;
  boost: number;
}

export class ExpertiseManager {
  private db: MemoriaDB;
  
  constructor(db: MemoriaDB) {
    this.db = db;
  }

  /**
   * Calculate expertise level from interaction count
   */
  calculateLevel(interactionCount: number): ExpertiseLevel {
    if (interactionCount >= EXPERTISE_CONFIG.thresholds.expert) return "expert";
    if (interactionCount >= EXPERTISE_CONFIG.thresholds.experienced) return "experienced";
    if (interactionCount >= EXPERTISE_CONFIG.thresholds.familiar) return "familiar";
    return "novice";
  }

  /**
   * Get recall boost multiplier for a topic
   */
  getBoost(level: ExpertiseLevel): number {
    return EXPERTISE_CONFIG.recallBoost[level];
  }

  /**
   * Get all topics with expertise levels
   */
  getAllExpertise(): TopicExpertise[] {
    try {
      const topics = this.db.raw.prepare(
        "SELECT name as topic, access_count as interaction_count FROM topics ORDER BY access_count DESC"
      ).all() as Array<{ topic: string; interaction_count: number }>;

      return topics.map(t => ({
        topic: t.topic,
        interactionCount: t.interaction_count,
        level: this.calculateLevel(t.interaction_count),
        boost: this.getBoost(this.calculateLevel(t.interaction_count)),
      }));
    } catch (err) {
      console.error("[expertise] getAllExpertise failed:", err);
      return [];
    }
  }

  /**
   * Get expertise for specific topics
   */
  getTopicExpertise(topics: string[]): TopicExpertise[] {
    const result: TopicExpertise[] = [];

    for (const topic of topics) {
      const row = this.db.raw.prepare(
        "SELECT access_count as interaction_count FROM topics WHERE name = ?"
      ).get(topic) as { interaction_count: number } | undefined;

      const count = row?.interaction_count ?? 0;
      const level = this.calculateLevel(count);

      result.push({
        topic,
        interactionCount: count,
        level,
        boost: this.getBoost(level),
      });
    }

    return result;
  }

  /**
   * Get stats: count by expertise level
   */
  getStats(): Record<ExpertiseLevel, number> {
    try {
      const all = this.getAllExpertise();
      const stats: Record<ExpertiseLevel, number> = {
        novice: 0,
        familiar: 0,
        experienced: 0,
        expert: 0,
      };

      for (const exp of all) {
        stats[exp.level]++;
      }

      return stats;
    } catch (err) {
      console.error("[expertise] getStats failed:", err);
      return { novice: 0, familiar: 0, experienced: 0, expert: 0 };
    }
  }

  /**
   * Boost fact score based on topic expertise
   */
  applyExpertiseBoost(score: number, factTopics: string[]): number {
    if (factTopics.length === 0) return score;

    const expertise = this.getTopicExpertise(factTopics);
    const maxBoost = Math.max(...expertise.map(e => e.boost));

    return score * maxBoost;
  }
}
