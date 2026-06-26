/**
 * Intention Detector
 * Detects when user might need EO capabilities
 */

export interface IntentionSignal {
  score: number // 0-1, higher = more likely needs EO
  signals: string[]
  suggestedCommand?: string
}

const EO_KEYWORDS = [
  'plan', 'architecture', 'design', 'review', 'verify', 'checkpoint',
  'expert', 'multi-agent', 'team', 'collaborate', 'build', 'project',
  'deploy', 'test', 'security', 'performance', 'backend', 'frontend',
  'microservices', 'api', 'database', 'kubernetes', 'docker',
  // Chinese keywords
  '规划', '架构', '设计', '审查', '验证', '检查点',
  '专家', '多专家', '协作', '团队', '项目', '建设',
  '部署', '测试', '安全', '性能', '后端', '前端',
  '微服务', '代码', '数据库', '优化', '开发',
  '帮我', '需要', '想要', '应该', '如何', '怎么',
]

const WEAK_SIGNALS = [
  'help', 'how to', 'what is', 'could you', 'can you',
  'i want', 'i need', 'trying to', 'build a', 'create a',
  // Chinese weak signals
  '能不能', '可不可以', '会不会', '是不是', '有没有',
]

export function detectIntention(message: string): IntentionSignal {
  const lower = message.toLowerCase()
  const signals: string[] = []
  let score = 0

  // Strong EO keywords
  for (const kw of EO_KEYWORDS) {
    if (lower.includes(kw)) {
      signals.push(`EO keyword: "${kw}"`)
      score += 0.2
    }
  }

  // Weak signals that suggest user is stuck or needs guidance
  let weakCount = 0
  for (const ws of WEAK_SIGNALS) {
    if (lower.includes(ws)) {
      weakCount++
    }
  }
  if (weakCount >= 2) {
    signals.push(`Multiple weak intent signals (${weakCount})`)
    score += 0.15
  }

  // Check for question patterns that might benefit from expert
  if (lower.includes('?') && lower.length < 200) {
    signals.push('Short question - may need expert context')
    score += 0.1
  }

  // No EO tools mentioned
  if (!lower.includes('eo_') && !lower.includes('/eo')) {
    signals.push('No EO tools mentioned yet')
    score += 0.1
  }

  // Clamp score
  score = Math.min(1, score)

  // Suggest command based on signals
  let suggestedCommand: string | undefined
  if (score >= 0.3) {
    if (lower.includes('plan') || lower.includes('project') || lower.includes('build') ||
        lower.includes('规划') || lower.includes('项目') || lower.includes('建设')) {
      suggestedCommand = 'eo_plan'
    } else if (lower.includes('architecture') || lower.includes('design') || lower.includes('microservices') ||
               lower.includes('架构') || lower.includes('设计') || lower.includes('微服务')) {
      suggestedCommand = 'eo_architect'
    } else if (lower.includes('review') || lower.includes('code') || lower.includes('审查') || lower.includes('代码')) {
      suggestedCommand = 'eo_code_review'
    } else if (lower.includes('verify') || lower.includes('checkpoint') || lower.includes('验证') || lower.includes('检查点')) {
      suggestedCommand = 'eo_verify'
    } else {
      suggestedCommand = 'eo_collab'
    }
  }

  return { score, signals, suggestedCommand }
}
