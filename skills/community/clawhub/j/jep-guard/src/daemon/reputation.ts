import { ReputationScore, JPEvent } from '../core/types';

export class ReputationEngineService {
  private scores = new Map<string, ReputationScore>();

  recordEvent(skillId: string, event: JPEvent, latencyMs?: number): void {
    let s = this.scores.get(skillId);
    if (!s) {
      s = {
        skill_id: skillId,
        total_judgments: 0,
        completed: 0,
        terminated: 0,
        completionRate: 1.0,
        violationRate: 0,
        avg_latency_ms: 0,
        last_updated: Date.now()
      };
    }

    if (event.verb === 'J') s.total_judgments++;
    if (event.verb === 'V') s.completed++;
    if (event.verb === 'T') s.terminated++;

    const total = s.completed + s.terminated;
    s.completionRate = total > 0 ? s.completed / total : 1.0;
    s.violationRate = total > 0 ? s.terminated / total : 0;

    if (latencyMs && total > 0) {
      s.avg_latency_ms = (s.avg_latency_ms * (total - 1) + latencyMs) / total;
    }

    s.last_updated = Date.now();
    this.scores.set(skillId, s);
  }

  get(skillId: string): ReputationScore {
    return this.scores.get(skillId) || {
      skill_id: skillId,
      total_judgments: 0,
      completed: 0,
      terminated: 0,
      completionRate: 1.0,
      violationRate: 0,
      avg_latency_ms: 0,
      last_updated: 0
    };
  }

  list(): ReputationScore[] {
    return Array.from(this.scores.values());
  }
}