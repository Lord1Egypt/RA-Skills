/**
 * Self Evolver - Highest level self-improvement
 */

import type { EvolveResult } from './types.js'
import { effectTracker } from './effect-tracker.js'

export class SelfEvolver {
  private lastEvolution = 0
  private cooldown = 86400000

  async evolve(): Promise<EvolveResult> {
    const now = Date.now()
    if (now - this.lastEvolution < this.cooldown) {
      return { newRules: [], retiredRules: [], confidence: 0, evidence: ['进化冷却中'] }
    }
    this.lastEvolution = now
    const stats = effectTracker.stats()
    const newRules: string[] = []
    const retiredRules: string[] = []
    const evidence: string[] = []

    if (stats.total < 20) {
      evidence.push('样本不足，需要至少20个决策')
      return { newRules, retiredRules, confidence: 0, evidence }
    }

    evidence.push(`分析${stats.total}个样本，平均分${stats.avgScore.toFixed(1)}，成功率${(stats.successRate*100).toFixed(1)}%`)
    
    if (stats.avgScore > 75 && stats.successRate > 0.7) {
      newRules.push('high_performance_threshold:75')
      evidence.push('发现高效模式')
    }
    if (stats.successRate < 0.6) {
      retiredRules.push('aggressive_default')
      newRules.push('conservative_default')
      evidence.push('成功率低，切换为保守策略')
    }

    return { newRules, retiredRules, confidence: Math.min(stats.total / 100, 0.9), evidence }
  }
}

export const selfEvolver = new SelfEvolver()
