/**
 * Proactive Monitor Hook v2
 * Monitors user messages and detects when EO assistance might be helpful
 * 
 *主动感知核心：当检测到高置信度意图时，发送建议给用户
 */

import type { OpenClawPluginApi } from 'openclaw/plugin-sdk'

import { detectIntention, suggestExpert, logIntention } from '../proactive/index.js'
import { proactiveNotifier } from '../continuous/proactive-notifier.js'
import { PLUGIN_VERSION } from '../config.js'

export interface ProactiveMonitorConfig {
  enabled: boolean
  threshold: number
  autoSuggestThreshold: number  // 高于此阈值自动建议
  feishuChatId?: string
}

const DEFAULT_CONFIG: ProactiveMonitorConfig = {
  enabled: true,
  threshold: 0.35,
  autoSuggestThreshold: 0.75,  // 75%以上置信度才自动建议
}

let config = { ...DEFAULT_CONFIG }

// Performance: throttle expensive operations
let lastCheckTime = 0
const MIN_CHECK_INTERVAL_MS = 2000 // Minimum interval between checks
let recentHighConfidenceCount = 0
const MAX_HIGH_CONFIDENCE_PER_MINUTE = 3 // Limit auto-suggestions

export function configureProactiveMonitor(cfg: Partial<ProactiveMonitorConfig>) {
  config = { ...config, ...cfg }
}

export async function checkMessage(api: OpenClawPluginApi, message: string): Promise<string | null> {
  if (!config.enabled) return null

  const intent = detectIntention(message)
  logIntention(api, intent, message)

  if (intent.score >= config.threshold) {
    const suggestion = suggestExpert(message)
    if (suggestion) {
      api.logger.debug(`[EO Proactive] Suggesting ${suggestion.toolName} (confidence=${suggestion.confidence.toFixed(2)})`)
      return suggestion.message
    }
  }

  return null
}

export function createProactiveMonitorHook(api: OpenClawPluginApi) {
  return {
    id: 'eo_proactive_monitor',
    name: 'EO Proactive Monitor',
    description: 'Monitors messages and proactively suggests EO tools when helpful',
    handle: async (event: any) => {
      const now = Date.now()
      
      // Throttle: skip if checked recently
      if (now - lastCheckTime < MIN_CHECK_INTERVAL_MS) return
      lastCheckTime = now
      
      const context = event.context as Record<string, unknown>
      const message = (context?.message as string) || (context?.content as string) || ''
      
      // Skip very short messages
      if (message.length < 10) return
      
      // Run intention detection
      const intent = detectIntention(message)
      logIntention(api, intent, message)
      
      // HIGH PRIORITY: Set eoProactiveTrigger when confidence >= 0.7
      // This signals to the main agent that mandatory multi-expert collaboration is needed
      if (intent.score >= 0.7) {
        context.eoProactiveTrigger = {
          mandatory: true,
          toolName: intent.suggestedCommand || 'eo_collab',
          confidence: intent.score,
          reason: `Detected complex task: ${intent.signals.join(', ')}`,
          suggestedCommand: intent.suggestedCommand,
        }
        api.logger.info(`[EO Proactive] 🚨 MANDATORY TRIGGER: ${intent.suggestedCommand} (${intent.score.toFixed(2)}) - ${intent.signals.slice(0, 2).join(', ')}`)
      }
      
      // AUTO-SUGGEST: Only for very high confidence AND rate limited
      if (intent.score >= config.autoSuggestThreshold && recentHighConfidenceCount < MAX_HIGH_CONFIDENCE_PER_MINUTE) {
        recentHighConfidenceCount++
        const suggestion = suggestExpert(message)
        if (suggestion) {
          api.logger.info(`[EO Proactive] 📢 Auto-suggesting ${suggestion.toolName} (confidence=${intent.score.toFixed(2)})`)
          
          // Send suggestion to Feishu if configured
          if (config.feishuChatId) {
            try {
              await proactiveNotifier.notify(
                'info',
                '🔔 EO 主动建议',
                `${suggestion.message}\n\n_由 EO 主动感知系统触发 (置信度: ${(intent.score * 100).toFixed(0)}%)_`,
                ['feishu'],
                { chatId: config.feishuChatId }
              )
              api.logger.debug(`[EO Proactive] Suggestion sent to Feishu`)
            } catch (e) {
              api.logger.warn(`[EO Proactive] Failed to send Feishu suggestion: ${e}`)
            }
          }
        }
      }
      
      // Reset rate limit counter every minute
      if (now % 60000 < MIN_CHECK_INTERVAL_MS) {
        recentHighConfidenceCount = 0
      }
    }
  }
}
