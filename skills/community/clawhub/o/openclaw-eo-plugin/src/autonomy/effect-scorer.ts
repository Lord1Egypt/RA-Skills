/**
 * Effect Scoring System
 * 
 * Provides quantitative evaluation of decision quality and agent performance.
 * Core of the self-optimization loop.
 * 
 * Part of the self-optimization loop:
 * Decision → Execute → Track → Score → Optimize → Evolve
 */

// Re-export types from types.ts
export type { Decision, DecisionOutcome, EffectScore, Strategy } from './types.js'

// ============================================================================
// Scoring Algorithms
// ============================================================================

/**
 * Simple linear scoring: score = result / expectation * baseScore
 * Range: 0-100
 */
export function linearScore(result: number, expectation: number, baseScore = 100): number {
  if (expectation === 0) return 0
  const raw = (result / expectation) * baseScore
  return Math.min(100, Math.max(0, raw))
}

/**
 * Binary scoring: success = 1, failure = 0
 */
export function binaryScore(success: boolean, baseScore = 100): number {
  return success ? baseScore : 0
}

/**
 * Weighted scoring for multi-criteria outcomes
 * Weights sum to 1.0
 */
export function weightedScore(criteria: Array<{ score: number; weight: number }>): number {
  return criteria.reduce((sum, c) => sum + c.score * c.weight, 0)
}

/**
 * Time-based scoring: faster = better
 * score = baseScore * speedFactor, where speedFactor > 1 means faster than expected
 */
export function timeScore(actualMs: number, expectedMs: number, baseScore = 100): number {
  if (actualMs === 0) return 0
  const ratio = expectedMs / actualMs // >1 means faster than expected
  return Math.min(100, ratio * baseScore * 0.5) // normalize
}

/**
 * Quality scoring: based on error rate or quality metrics
 * score = (1 - errorRate) * baseScore
 */
export function qualityScore(errors: number, total: number, baseScore = 100): number {
  if (total === 0) return baseScore
  return ((total - errors) / total) * baseScore
}

/**
 * Composite scoring: combines multiple dimensions
 */
export function compositeScore(params: {
  accuracy?: number
  speed?: number
  efficiency?: number
  satisfaction?: number
  weights?: { accuracy: number; speed: number; efficiency: number; satisfaction: number }
}): number {
  const { accuracy = 0, speed = 0, efficiency = 0, satisfaction = 0, weights = { accuracy: 0.3, speed: 0.2, efficiency: 0.2, satisfaction: 0.3 } } = params
  const totalWeight = weights.accuracy + weights.speed + weights.efficiency + weights.satisfaction
  if (totalWeight === 0) return 0
  return weightedScore([
    { score: accuracy, weight: weights.accuracy },
    { score: speed, weight: weights.speed },
    { score: efficiency, weight: weights.efficiency },
    { score: satisfaction, weight: weights.satisfaction },
  ])
}

// ============================================================================
// Effect Score Calculator
// ============================================================================

export interface ScoringDecision {
  id: string
  type: 'binary' | 'multi_criteria' | 'quantitative' | 'quality' | 'composite'
  description: string
  criteria?: Array<{ name: string; weight: number; expectation?: number }>
  expectation?: number
  timeoutMs?: number
  timestamp: number
}

export interface ScoringOutcome {
  success?: boolean
  value?: number
  criteriaScores?: number[]
  errors?: number
  total?: number
  accuracy?: number
  speed?: number
  efficiency?: number
  satisfaction?: number
  feedback?: string
}

export interface ScoringScore {
  decisionId: string
  score: number
  grade: 'A' | 'B' | 'C' | 'D' | 'F'
  confidence: number
  breakdown: Record<string, number>
  latencyMs: number
  scoredAt: number
}

export class EffectScoreCalculator {
  /**
   * Calculate score from a completed decision and its outcome
   */
  static calculate(decision: ScoringDecision, outcome: ScoringOutcome): ScoringScore {
    const scoredAt = Date.now()
    const latencyMs = scoredAt - decision.timestamp

    // Determine score based on decision type
    let score: number
    const breakdown: Record<string, number> = {}

    switch (decision.type) {
      case 'binary':
        score = binaryScore(outcome.success ?? false, 100)
        breakdown.binary = score
        break

      case 'multi_criteria':
        if (decision.criteria && outcome.criteriaScores) {
          score = weightedScore(decision.criteria.map((c, i) => ({
            score: outcome.criteriaScores?.[i] ?? 0,
            weight: c.weight,
          })))
        } else {
          score = 50
        }
        Object.assign(breakdown, { criteria: score })
        break

      case 'quantitative':
        score = linearScore(outcome.value ?? 0, decision.expectation ?? 100, 100)
        breakdown.quantitative = score
        break

      case 'quality':
        score = qualityScore(outcome.errors ?? 0, outcome.total ?? 0, 100)
        breakdown.quality = score
        break

      case 'composite':
        score = compositeScore({
          accuracy: outcome.accuracy,
          speed: outcome.speed,
          efficiency: outcome.efficiency,
          satisfaction: outcome.satisfaction,
        })
        Object.assign(breakdown, {
          accuracy: outcome.accuracy ?? 0,
          speed: outcome.speed ?? 0,
          efficiency: outcome.efficiency ?? 0,
          satisfaction: outcome.satisfaction ?? 0,
        })
        break

      default:
        score = outcome.success ? 100 : 0
        breakdown.default = score
    }

    // Apply time penalty if decision took too long
    if (decision.timeoutMs && latencyMs > decision.timeoutMs) {
      const penalty = Math.min(20, (latencyMs - decision.timeoutMs) / decision.timeoutMs * 20)
      score = Math.max(0, score - penalty)
      breakdown.timePenalty = penalty
    }

    // Calculate confidence based on data quality
    const confidence = this.calculateConfidence(decision, outcome)
    const grade = this.scoreToGrade(score)

    return {
      decisionId: decision.id,
      score: Math.round(score * 100) / 100,
      grade,
      confidence,
      breakdown,
      latencyMs,
      scoredAt,
    }
  }

  /**
   * Calculate confidence level (0-1) based on evidence quality
   */
  static calculateConfidence(decision: ScoringDecision, outcome: ScoringOutcome): number {
    let factors = 0
    let totalFactors = 0

    totalFactors++
    if (outcome.value !== undefined || outcome.success !== undefined || outcome.criteriaScores) {
      factors++
    }

    totalFactors++
    if (decision.criteria && decision.criteria.length >= 2) {
      factors++
    }

    totalFactors++
    if (decision.expectation !== undefined) {
      factors++
    }

    totalFactors++
    if (decision.timeoutMs) {
      factors++
    }

    return factors / totalFactors
  }

  /**
   * Convert numeric score to letter grade
   */
  static scoreToGrade(score: number): 'A' | 'B' | 'C' | 'D' | 'F' {
    if (score >= 90) return 'A'
    if (score >= 80) return 'B'
    if (score >= 70) return 'C'
    if (score >= 60) return 'D'
    return 'F'
  }
}

// ============================================================================
// Auto-Scorer (for automatic outcome collection)
// ============================================================================

export class AutoScorer {
  /**
   * Auto-generate a score based on implicit feedback
   */
  static fromImplicitFeedback(decision: ScoringDecision, context: {
    userFeedback?: 'positive' | 'negative' | 'neutral'
    repeatedTask?: boolean
    taskAbandoned?: boolean
    quickApproval?: boolean
    modifications?: number
  }): ScoringOutcome {
    let score = 75
    let success = true

    if (context.userFeedback === 'positive') {
      score = 90
    } else if (context.userFeedback === 'negative') {
      score = 40
      success = false
    }

    if (context.repeatedTask) {
      score -= 30
      success = false
    }

    if (context.taskAbandoned) {
      score = 20
      success = false
    }

    if (context.quickApproval) {
      score += 10
    }

    if (context.modifications && context.modifications > 0) {
      score -= Math.min(20, context.modifications * 5)
    }

    score = Math.min(100, Math.max(0, score))

    return {
      success,
      value: score,
      errors: context.modifications ?? 0,
    }
  }

  /**
   * Score based on outcome type
   */
  static fromOutcomeType(outcome: ScoringOutcome): number {
    if (outcome.success === false) return 0
    if (outcome.value !== undefined) {
      return Math.min(100, outcome.value)
    }
    if (outcome.criteriaScores) {
      return weightedScore(outcome.criteriaScores.map((s, i) => ({
        score: s,
        weight: 1 / outcome.criteriaScores!.length,
      })))
    }
    return 75
  }
}

// ============================================================================
// Score Aggregation
// ============================================================================

export class ScoreAggregator {
  /**
   * Aggregate multiple scores with trend analysis
   */
  static aggregate(scores: ScoringScore[]): {
    avgScore: number
    trend: 'improving' | 'stable' | 'declining'
    grade: 'A' | 'B' | 'C' | 'D' | 'F'
    percentile: number
    stats: { min: number; max: number; count: number; stdDev: number }
  } {
    if (scores.length === 0) {
      return { avgScore: 0, trend: 'stable', grade: 'F', percentile: 0, stats: { min: 0, max: 0, count: 0, stdDev: 0 } }
    }

    const numericScores = scores.map(s => s.score)
    const avgScore = numericScores.reduce((a, b) => a + b, 0) / numericScores.length

    // Calculate trend
    const recentScores = scores.slice(-5)
    const olderScores = scores.slice(-10, -5)
    let trend: 'improving' | 'stable' | 'declining' = 'stable'

    if (recentScores.length >= 3 && olderScores.length >= 3) {
      const recentAvg = recentScores.reduce((a, b) => a + b.score, 0) / recentScores.length
      const olderAvg = olderScores.reduce((a, b) => a + b.score, 0) / olderScores.length
      const diff = recentAvg - olderAvg
      if (diff > 5) trend = 'improving'
      else if (diff < -5) trend = 'declining'
    }

    // Standard deviation
    const squaredDiffs = numericScores.map(s => Math.pow(s - avgScore, 2))
    const avgSquaredDiff = squaredDiffs.reduce((a, b) => a + b, 0) / numericScores.length
    const stdDev = Math.sqrt(avgSquaredDiff)

    return {
      avgScore: Math.round(avgScore * 100) / 100,
      trend,
      grade: EffectScoreCalculator.scoreToGrade(avgScore),
      percentile: Math.round(avgScore),
      stats: {
        min: Math.min(...numericScores),
        max: Math.max(...numericScores),
        count: numericScores.length,
        stdDev: Math.round(stdDev * 100) / 100,
      },
    }
  }
}
