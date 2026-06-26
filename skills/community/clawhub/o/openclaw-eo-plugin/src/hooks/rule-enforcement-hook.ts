/**
 * Rule Enforcement Hook - Hook-level rule checking
 * 
 * This hook intercepts dangerous operations and:
 * - Warns users about potential issues
 * - Requires confirmation for risky operations
 * - Sets context flags for the agent to handle
 */

import { getRuleEnforcer, shouldBlockToolCall } from '../autonomy/rule-enforcer-hybrid.js'
import type { OpenClawPluginApi } from 'openclaw/plugin-sdk'

export interface RuleEnforcementConfig {
  enabled: boolean
  logViolations: boolean
}

const DEFAULT_CONFIG: RuleEnforcementConfig = {
  enabled: true,
  logViolations: true,
}

let config = { ...DEFAULT_CONFIG }

export function configureRuleEnforcement(cfg: Partial<RuleEnforcementConfig>) {
  config = { ...config, ...cfg }
}

/**
 * Create the rule enforcement hook
 */
export function createRuleEnforcementHook(api: OpenClawPluginApi) {
  return {
    id: 'eo_rule_enforcement',
    name: 'EO Rule Enforcement',
    description: 'Enforces mandatory rules at hook level',

    handle: async (event: any) => {
      if (!config.enabled) return

      const toolName = event?.toolName || event?.name || ''
      
      // Only check EO tools or dangerous operations
      if (!toolName.startsWith('eo_') && !isDangerousOperation(toolName)) {
        return
      }

      // Check if this should be blocked
      const check = shouldBlockToolCall(toolName, event)

      if (check.blocked) {
        api.logger.warn(`[EO RuleEnforcement] Blocked: ${toolName} - ${check.reason}`)
        
        // Store violation in context for the agent to see
        if (event?.context) {
          event.context.eoRuleViolation = {
            tool: toolName,
            reason: check.reason,
            suggestion: check.suggestion,
            blocked: true,
          }
        }
        return
      }

      if (check.reason && check.reason.includes('需要确认')) {
        api.logger.info(`[EO RuleEnforcement] Confirmation required: ${toolName}`)
        
        // Store confirmation requirement in context for the agent to handle
        if (event?.context) {
          event.context.eoConfirmationRequired = {
            tool: toolName,
            reason: check.reason,
            suggestion: check.suggestion,
          }
        }
      }

      if (check.reason && check.reason.includes('警告')) {
        api.logger.info(`[EO RuleEnforcement] Warning: ${toolName} - ${check.reason}`)
        
        // Store warning in context
        if (event?.context) {
          event.context.eoRuleWarning = {
            tool: toolName,
            reason: check.reason,
            suggestion: check.suggestion,
          }
        }
      }
    },
  }
}

/**
 * Check if an operation is considered dangerous
 */
function isDangerousOperation(toolName: string): boolean {
  const dangerous = [
    'gateway restart',
    'rm -rf',
    'git push --force',
    'drop table',
    'delete --force',
    '--force',
  ]
  
  const lower = toolName.toLowerCase()
  return dangerous.some(d => lower.includes(d))
}

/**
 * Get enforcement stats
 */
export function getEnforcementStats() {
  const enforcer = getRuleEnforcer()
  return {
    ...enforcer.getStats(),
    enabled: config.enabled,
  }
}
