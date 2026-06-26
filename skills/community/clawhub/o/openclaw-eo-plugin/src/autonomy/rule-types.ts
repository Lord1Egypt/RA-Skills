/**
 * Rule Types and Storage - Hybrid Architecture
 * 
 * Rules are stored as JSON (portable) and executed by local Hooks (enforced)
 */

import * as fs from 'fs'
import * as path from 'path'
import { ruleLogger } from '../utils/logger.js'

export type RuleType = 'suggestion' | 'mandatory'
export type RuleTrigger = 'tool_call' | 'message' | 'action'
export type RuleAction = 'warn' | 'block' | 'suggest' | 'require_confirmation'

export interface Rule {
  id: string
  name: string
  type: RuleType  // 'suggestion' | 'mandatory'
  trigger: RuleTrigger
  triggerPattern: string  // e.g., 'gateway restart', 'rm -rf'
  action: RuleAction  // 'warn' | 'block' | 'suggest' | 'require_confirmation'
  condition?: string  // e.g., 'avgScore > 75'
  description: string
  examples?: string[]
  createdAt: string
  updatedAt: string
  source: 'evolution' | 'manual' | 'imported' | 'builtin'
  enabled: boolean
}

export interface RulesPackage {
  version: string
  exportedAt: string
  exportedBy: string  // agentId
  rules: Rule[]
  metadata: {
    totalRules: number
    mandatoryCount: number
    suggestionCount: number
  }
}

export interface RulesConfig {
  rulesDir: string
  rulesFile: string
  metadataFile: string
  autoReload: boolean  // Reload rules when file changes
}

// Default rules directory
export const DEFAULT_RULES_PATH = './.eo-rules/rules.json'
export const DEFAULT_METADATA_PATH = './.eo-rules/metadata.json'

// Built-in hard rules (cannot be disabled)
export const BUILTIN_HARD_RULES: Rule[] = [
  {
    id: 'builtin-gateway-restart',
    name: 'Gateway Restart Confirmation',
    type: 'mandatory',
    trigger: 'tool_call',
    triggerPattern: 'gateway restart',
    action: 'require_confirmation',
    condition: undefined,
    description: '必须确认后才能执行网关重启',
    examples: ['执行前必须说"网关将重启，是否继续？"并得到确认'],
    createdAt: '2026-04-13T00:00:00.000Z',
    updatedAt: '2026-04-13T00:00:00.000Z',
    source: 'builtin',
    enabled: true,
  },
  {
    id: 'builtin-dangerous-rm',
    name: 'Dangerous Delete Confirmation',
    type: 'mandatory',
    trigger: 'tool_call',
    triggerPattern: 'rm -rf',
    action: 'require_confirmation',
    description: '危险删除操作必须确认',
    examples: ['rm -rf 需要二次确认'],
    createdAt: '2026-04-13T00:00:00.000Z',
    updatedAt: '2026-04-13T00:00:00.000Z',
    source: 'builtin',
    enabled: true,
  },
  {
    id: 'builtin-git-force',
    name: 'Git Force Push Warning',
    type: 'mandatory',
    trigger: 'tool_call',
    triggerPattern: 'git push --force',
    action: 'warn',
    description: '强制推送可能覆盖远程历史',
    examples: ['git push --force 需要警告'],
    createdAt: '2026-04-13T00:00:00.000Z',
    updatedAt: '2026-04-13T00:00:00.000Z',
    source: 'builtin',
    enabled: true,
  },
]

// Rule storage class
export class RuleStorage {
  private rules: Rule[] = []
  private config: RulesConfig

  constructor(config?: Partial<RulesConfig>) {
    this.config = {
      rulesDir: config?.rulesDir || './.eo-rules',
      rulesFile: config?.rulesFile || DEFAULT_RULES_PATH,
      metadataFile: config?.metadataFile || DEFAULT_METADATA_PATH,
      autoReload: config?.autoReload ?? true,
    }
    this.load()
  }

  /**
   * Load rules from disk
   */
  load(): void {
    try {
      if (fs.existsSync(this.config.rulesFile)) {
        const data = JSON.parse(fs.readFileSync(this.config.rulesFile, 'utf-8'))
        this.rules = data.rules || []
        ruleLogger.info(`Loaded ${this.rules.length} rules from ${this.config.rulesFile}`);
      } else {
        // Initialize with built-in rules
        this.rules = [...BUILTIN_HARD_RULES]
        this.save()
        ruleLogger.info('Initialized with built-in hard rules');
      }
    } catch (e) {
      console.warn('[RuleStorage] Failed to load rules:', e)
      this.rules = [...BUILTIN_HARD_RULES]
    }
  }

  /**
   * Save rules to disk
   */
  save(): void {
    try {
      // Ensure directory exists
      const dir = path.dirname(this.config.rulesFile)
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true })
      }

      const data = {
        version: '1.0',
        exportedAt: new Date().toISOString(),
        rules: this.rules,
        metadata: this.getMetadata(),
      }

      fs.writeFileSync(this.config.rulesFile, JSON.stringify(data, null, 2))
      ruleLogger.info(`Saved ${this.rules.length} rules to ${this.config.rulesFile}`);
    } catch (e) {
      console.error('[RuleStorage] Failed to save rules:', e)
    }
  }

  /**
   * Get all rules
   */
  getRules(): Rule[] {
    return this.rules.filter(r => r.enabled)
  }

  /**
   * Get rules by type
   */
  getRulesByType(type: RuleType): Rule[] {
    return this.rules.filter(r => r.enabled && r.type === type)
  }

  /**
   * Get mandatory rules (for Hook enforcement)
   */
  getMandatoryRules(): Rule[] {
    return this.getRulesByType('mandatory')
  }

  /**
   * Get suggestion rules (for SOUL injection)
   */
  getSuggestionRules(): Rule[] {
    return this.getRulesByType('suggestion')
  }

  /**
   * Add a rule
   */
  addRule(rule: Omit<Rule, 'id' | 'createdAt' | 'updatedAt'>): Rule {
    const newRule: Rule = {
      ...rule,
      id: `rule-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    }
    this.rules.push(newRule)
    this.save()
    return newRule
  }

  /**
   * Update a rule
   */
  updateRule(id: string, updates: Partial<Rule>): Rule | null {
    const index = this.rules.findIndex(r => r.id === id)
    if (index === -1) return null
    
    this.rules[index] = {
      ...this.rules[index],
      ...updates,
      updatedAt: new Date().toISOString(),
    }
    this.save()
    return this.rules[index]
  }

  /**
   * Delete a rule
   */
  deleteRule(id: string): boolean {
    const index = this.rules.findIndex(r => r.id === id)
    if (index === -1) return false
    
    this.rules.splice(index, 1)
    this.save()
    return true
  }

  /**
   * Check if a trigger matches a rule
   */
  matchRule(trigger: string): Rule | null {
    for (const rule of this.getMandatoryRules()) {
      if (trigger.toLowerCase().includes(rule.triggerPattern.toLowerCase())) {
        return rule
      }
    }
    return null
  }

  /**
   * Get metadata
   */
  getMetadata(): { totalRules: number; mandatoryCount: number; suggestionCount: number } {
    return {
      totalRules: this.rules.length,
      mandatoryCount: this.rules.filter(r => r.type === 'mandatory').length,
      suggestionCount: this.rules.filter(r => r.type === 'suggestion').length,
    }
  }

  /**
   * Export rules as package (for migration)
   */
  exportRules(exportedBy: string): RulesPackage {
    return {
      version: '1.0',
      exportedAt: new Date().toISOString(),
      exportedBy,
      rules: this.rules,
      metadata: this.getMetadata(),
    }
  }

  /**
   * Import rules from package
   */
  importRules(pkg: RulesPackage, strategy: 'merge' | 'replace' = 'merge'): void {
    if (strategy === 'replace') {
      this.rules = pkg.rules
    } else {
      // Merge: add new rules, skip existing
      const existingIds = new Set(this.rules.map(r => r.id))
      for (const rule of pkg.rules) {
        if (!existingIds.has(rule.id)) {
          this.rules.push(rule)
        }
      }
    }
    this.save()
  }

  /**
   * Get rule count
   */
  count(): { total: number; mandatory: number; suggestion: number } {
    return {
      total: this.rules.length,
      mandatory: this.rules.filter(r => r.type === 'mandatory').length,
      suggestion: this.rules.filter(r => r.type === 'suggestion').length,
    }
  }
}

// Singleton instance
let ruleStorage: RuleStorage | null = null

export function getRuleStorage(config?: Partial<RulesConfig>): RuleStorage {
  if (!ruleStorage) {
    ruleStorage = new RuleStorage(config)
  }
  return ruleStorage
}

export function resetRuleStorage(): void {
  ruleStorage = null
}
