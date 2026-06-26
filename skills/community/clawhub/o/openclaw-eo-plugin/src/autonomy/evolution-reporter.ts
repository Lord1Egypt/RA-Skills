/**
 * Evolution Report Generator
 * 
 * Generates automated evolution reports from Dream output
 * Part of the self-optimization loop: Dream → Report → Evolution
 */

import { effectTracker } from '../autonomy/index.js'
import { patchManager } from './patch-manager.js'

export interface EvolutionReport {
  id: string
  date: string
  period: string // e.g., "2026-04-09 12:00 - 2026-04-09 18:00"
  
  // Score summary
  scoreSummary: {
    avgScore: number
    grade: string
    trend: string
    totalTracked: number
    successRate: number
  }
  
  // Patterns detected
  patterns: Array<{
    name: string
    description: string
    confidence: number
  }>
  
  // Patches generated
  patches: Array<{
    id: string
    name: string
    risk: string
    status: string
  }>
  
  // Recommendations
  recommendations: string[]
  
  // Next steps
  nextSteps: string[]
  
  // Generated at
  generatedAt: number
}

/**
 * Generate an evolution report
 */
export function generateEvolutionReport(periodMs?: number): EvolutionReport {
  const now = Date.now()
  const period = periodMs || 6 * 60 * 60 * 1000 // Default: 6 hours
  const startTime = now - period
  
  const stats = effectTracker.stats()
  const patchStats = patchManager.getStats()
  const reviewQueue = patchManager.getReviewQueue()
  
  // Calculate period-specific scores (filter by time)
  const recentScores = effectTracker.getRecentScores(100).filter(s => s.scoredAt >= startTime)
  const periodAvgScore = recentScores.length > 0
    ? recentScores.reduce((sum, s) => sum + s.score, 0) / recentScores.length
    : stats.avgScore
  
  // Generate patterns from score breakdown
  const patterns = detectPatterns(stats, recentScores)
  
  // Generate recommendations
  const recommendations = generateRecommendations(stats, patchStats, patterns)
  
  // Generate next steps
  const nextSteps = generateNextSteps(stats, reviewQueue)
  
  const report: EvolutionReport = {
    id: `evo_${Date.now()}`,
    date: new Date().toISOString().slice(0, 10),
    period: `${new Date(startTime).toISOString()} - ${new Date(now).toISOString()}`,
    scoreSummary: {
      avgScore: Math.round(periodAvgScore * 100) / 100,
      grade: stats.grade,
      trend: stats.trend,
      totalTracked: stats.total,
      successRate: Math.round(stats.successRate * 100),
    },
    patterns,
    patches: reviewQueue.map(p => ({
      id: p.id,
      name: p.name,
      risk: p.risk,
      status: p.status,
    })),
    recommendations,
    nextSteps,
    generatedAt: now,
  }
  
  return report
}

/**
 * Detect patterns from stats and scores
 */
function detectPatterns(
  stats: ReturnType<typeof effectTracker.stats>,
  recentScores: ReturnType<typeof effectTracker.getRecentScores>
): EvolutionReport['patterns'] {
  const patterns: EvolutionReport['patterns'] = []
  
  // Pattern: High variance
  if (stats.scoreStats.stdDev > 20) {
    patterns.push({
      name: 'High Score Variance',
      description: `Standard deviation is ${stats.scoreStats.stdDev}, indicating inconsistent decision quality`,
      confidence: 0.8,
    })
  }
  
  // Pattern: Declining trend
  if (stats.trend === 'declining') {
    patterns.push({
      name: 'Declining Performance',
      description: 'Score trend is declining over recent decisions',
      confidence: 0.9,
    })
  }
  
  // Pattern: Improving trend
  if (stats.trend === 'improving') {
    patterns.push({
      name: 'Improving Performance',
      description: 'Score trend is improving over recent decisions',
      confidence: 0.9,
    })
  }
  
  // Pattern: Low success rate
  if (stats.successRate < 0.6) {
    patterns.push({
      name: 'Low Success Rate',
      description: `Success rate is ${(stats.successRate * 100).toFixed(1)}%, below acceptable threshold`,
      confidence: 0.85,
    })
  }
  
  // Pattern: Grade distribution
  const gradeDist = effectTracker.getScoresByGrade()
  const failureCount = gradeDist['D'].length + gradeDist['F'].length
  if (failureCount > stats.total * 0.2) {
    patterns.push({
      name: 'Frequent Failures',
      description: `${failureCount} decisions scored D or F (${((failureCount / stats.total) * 100).toFixed(1)}% failure rate)`,
      confidence: 0.75,
    })
  }
  
  return patterns
}

/**
 * Generate recommendations based on stats
 */
function generateRecommendations(
  stats: ReturnType<typeof effectTracker.stats>,
  patchStats: ReturnType<typeof patchManager.getStats>,
  patterns: EvolutionReport['patterns']
): string[] {
  const recommendations: string[] = []
  
  // Based on score
  if (stats.avgScore < 50) {
    recommendations.push('CRITICAL: Average score critically low. Immediate strategy change required.')
  } else if (stats.avgScore < 70) {
    recommendations.push('WARNING: Average score below target. Optimization recommended.')
  } else if (stats.avgScore >= 85) {
    recommendations.push('GOOD: Average score is healthy. Maintain current approach.')
  }
  
  // Based on trend
  if (stats.trend === 'declining') {
    recommendations.push('ALERT: Performance declining. Investigate recent changes.')
  } else if (stats.trend === 'improving') {
    recommendations.push('POSITIVE: Performance improving. Continue current strategy.')
  }
  
  // Based on patches
  if (patchStats.reviewQueueSize > 0) {
    recommendations.push(`${patchStats.reviewQueueSize} patches pending review. Process soon.`)
  }
  
  // Based on patterns
  for (const pattern of patterns) {
    if (pattern.confidence > 0.8) {
      if (pattern.name.includes('High Score Variance')) {
        recommendations.push('Standardize decision process to reduce variance.')
      }
      if (pattern.name.includes('Low Success Rate')) {
        recommendations.push('Add validation step before decision execution.')
      }
    }
  }
  
  // Based on grade
  if (stats.grade === 'F' || stats.grade === 'D') {
    recommendations.push('Overall grade is poor. Comprehensive review needed.')
  } else if (stats.grade === 'A') {
    recommendations.push('Excellent performance. Consider exploring new strategies.')
  }
  
  return [...new Set(recommendations)] // Remove duplicates
}

/**
 * Generate next steps
 */
function generateNextSteps(
  stats: ReturnType<typeof effectTracker.stats>,
  reviewQueue: ReturnType<typeof patchManager.getReviewQueue>
): string[] {
  const nextSteps: string[] = []
  
  // Immediate actions based on score
  if (stats.avgScore < 60) {
    nextSteps.push('1. Switch to conservative strategy mode')
    nextSteps.push('2. Add human review for high-risk decisions')
  }
  
  // Patch processing
  if (reviewQueue.length > 0) {
    nextSteps.push(`${reviewQueue.length}. Review and process pending patches`)
  }
  
  // Continuous improvement
  if (stats.avgScore >= 70) {
    nextSteps.push('1. Document successful patterns')
    nextSteps.push('2. Share learnings with team')
  }
  
  // Dream trigger
  nextSteps.push('Schedule next Dream cycle in 24 hours')
  
  return nextSteps
}

/**
 * Format report as markdown
 */
export function formatReportAsMarkdown(report: EvolutionReport): string {
  const lines: string[] = [
    `# Evolution Report - ${report.date}`,
    '',
    `**Period:** ${report.period}`,
    '',
    '## Score Summary',
    '',
    `| Metric | Value |`,
    `|--------|-------|`,
    `| Average Score | ${report.scoreSummary.avgScore} |`,
    `| Grade | ${report.scoreSummary.grade} |`,
    `| Trend | ${report.scoreSummary.trend} |`,
    `| Total Tracked | ${report.scoreSummary.totalTracked} |`,
    `| Success Rate | ${report.scoreSummary.successRate}% |`,
    '',
  ]
  
  if (report.patterns.length > 0) {
    lines.push('## Detected Patterns')
    lines.push('')
    for (const pattern of report.patterns) {
      lines.push(`- **${pattern.name}** (${(pattern.confidence * 100).toFixed(0)}% confidence)`)
      lines.push(`  - ${pattern.description}`)
    }
    lines.push('')
  }
  
  if (report.patches.length > 0) {
    lines.push('## Pending Patches')
    lines.push('')
    for (const patch of report.patches) {
      lines.push(`- [${patch.risk}] ${patch.name} (${patch.status})`)
    }
    lines.push('')
  }
  
  if (report.recommendations.length > 0) {
    lines.push('## Recommendations')
    lines.push('')
    for (const rec of report.recommendations) {
      lines.push(`- ${rec}`)
    }
    lines.push('')
  }
  
  if (report.nextSteps.length > 0) {
    lines.push('## Next Steps')
    lines.push('')
    for (const step of report.nextSteps) {
      lines.push(`- ${step}`)
    }
    lines.push('')
  }
  
  lines.push('---')
  lines.push(`*Report generated at ${new Date(report.generatedAt).toISOString()}*`)
  
  return lines.join('\n')
}

// Export singleton
export const evolutionReporter = {
  generate: generateEvolutionReport,
  format: formatReportAsMarkdown,
}
