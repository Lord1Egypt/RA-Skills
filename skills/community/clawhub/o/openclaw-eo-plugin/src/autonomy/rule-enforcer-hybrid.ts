/**
 * Rule Enforcer - Hybrid Architecture
 * 
 * Executes rules at Hook level (cannot be bypassed)
 * - Mandatory rules: Hook enforcement (hard)
 * - Suggestion rules: SOUL injection (soft)
 */

import { getRuleStorage, type Rule, type RulesPackage } from './rule-types.js'
import * as fs from 'fs'
import * as path from 'path'

export interface EnforcementResult {
  allowed: boolean
  rule?: Rule
  reason?: string
  suggestion?: string
}

export interface EnforcerConfig {
  rulesPath: string
  enableBuiltinRules: boolean
  allowRuleDisable: boolean
}

/**
 * Rule Enforcer - Checks if an action violates mandatory rules
 */
export class RuleEnforcer {
  private storage = getRuleStorage({ rulesFile: './.eo-rules/rules.json' })
  private config: EnforcerConfig

  constructor(config?: Partial<EnforcerConfig>) {
    this.config = {
      rulesPath: './.eo-rules/rules.json',
      enableBuiltinRules: true,
      allowRuleDisable: false,
      ...config,
    }
  }

  /**
   * Check if a tool call or action should be allowed
   */
  check(toolCall: string, context?: Record<string, any>): EnforcementResult {
    const rule = this.storage.matchRule(toolCall)
    
    if (!rule) {
      return { allowed: true }
    }

    // Handle different actions
    switch (rule.action) {
      case 'block':
        return {
          allowed: false,
          rule,
          reason: `操作被规则拦截: ${rule.name}`,
          suggestion: rule.description,
        }

      case 'require_confirmation':
        return {
          allowed: true,  // Allowed, but caller should request confirmation
          rule,
          reason: `需要确认: ${rule.description}`,
          suggestion: `执行"${toolCall}"前必须确认`,
        }

      case 'warn':
        return {
          allowed: true,
          rule,
          reason: `警告: ${rule.description}`,
          suggestion: rule.examples?.[0] || rule.description,
        }

      default:
        return { allowed: true }
    }
  }

  /**
   * Get all active rules
   */
  getActiveRules(): Rule[] {
    return this.storage.getRules()
  }

  /**
   * Get mandatory rules count
   */
  getMandatoryCount(): number {
    return this.storage.getRulesByType('mandatory').length
  }

  /**
   * Get suggestion rules for SOUL injection
   */
  getSuggestionForSoul(): Rule[] {
    return this.storage.getRulesByType('suggestion')
  }

  /**
   * Export rules for migration
   */
  exportRules(agentId: string): RulesPackage {
    return this.storage.exportRules(agentId)
  }

  /**
   * Import rules from package
   */
  importRules(pkg: RulesPackage, strategy: 'merge' | 'replace' = 'merge'): void {
    this.storage.importRules(pkg, strategy)
  }

  /**
   * Get rules stats
   */
  getStats(): { total: number; mandatory: number; suggestion: number } {
    return this.storage.count()
  }
}

// Singleton
let enforcer: RuleEnforcer | null = null

export function getRuleEnforcer(): RuleEnforcer {
  if (!enforcer) {
    enforcer = new RuleEnforcer()
  }
  return enforcer
}

/**
 * Generate SOUL.md section for suggestion rules
 */
export function generateSuggestionSection(): string {
  const enforcer = getRuleEnforcer()
  const suggestions = enforcer.getSuggestionForSoul()
  
  if (suggestions.length === 0) {
    return ''
  }

  const lines = [
    '',
    '## 📋 行为建议规则（由自进化生成）',
    '',
  ]

  for (const rule of suggestions) {
    lines.push(`### ${rule.name}`)
    lines.push(`- **条件**: ${rule.condition || '始终适用'}`)
    lines.push(`- **建议**: ${rule.description}`)
    if (rule.examples && rule.examples.length > 0) {
      lines.push(`- **示例**: ${rule.examples[0]}`)
    }
    lines.push('')
  }

  return lines.join('\n')
}

/**
 * Check if a tool call should be blocked (for Hook use)
 */
export function shouldBlockToolCall(toolCall: string, context?: Record<string, any>): {
  blocked: boolean
  reason?: string
  suggestion?: string
} {
  const enforcer = getRuleEnforcer()
  const result = enforcer.check(toolCall, context)

  if (!result.allowed) {
    return {
      blocked: true,
      reason: result.reason,
      suggestion: result.suggestion,
    }
  }

  if (result.rule?.action === 'require_confirmation') {
    return {
      blocked: false,
      reason: result.reason,
      suggestion: result.suggestion,
    }
  }

  return { blocked: false }
}
