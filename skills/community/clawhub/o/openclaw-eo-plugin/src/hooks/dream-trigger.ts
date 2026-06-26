/**
 * Dream Trigger Hook
 * Triggers dream module for self-evolution based on conditions
 */

import type { OpenClawPluginApi } from 'openclaw/plugin-sdk'

import { DreamEngine } from '../dream/dream-engine.js'
import { PLUGIN_VERSION } from '../config.js'

const dreamEngine = new DreamEngine(process.cwd())

export interface DreamTriggerConfig {
  enabled: boolean
  afterSessions: number
  afterHours: number
}

const DEFAULT_CONFIG: DreamTriggerConfig = {
  enabled: true,
  afterSessions: 10,
  afterHours: 24,
}

let config = { ...DEFAULT_CONFIG }
let sessionCount = 0
let lastDreamTime = 0

export function configureDreamTrigger(cfg: Partial<DreamTriggerConfig>) {
  config = { ...config, ...cfg }
}

export function incrementSession() {
  sessionCount++
}

export function shouldTriggerDream(): boolean {
  if (!config.enabled) return false
  const hoursSinceLastDream = (Date.now() - lastDreamTime) / (1000 * 60 * 60)
  return sessionCount >= config.afterSessions || hoursSinceLastDream >= config.afterHours
}

export async function triggerDream(api: OpenClawPluginApi): Promise<void> {
  if (!shouldTriggerDream()) return

  api.logger.info(`[EO DreamTrigger v${PLUGIN_VERSION}] Triggering dream: sessions=${sessionCount}`)

  try {
    const result = await dreamEngine.executeDream({ type: 'scheduled' })
    if (result.success) {
      lastDreamTime = Date.now()
      sessionCount = 0
      api.logger.info(`[EO DreamTrigger] Dream completed successfully`)
    }
  } catch (err) {
    api.logger.error(`[EO DreamTrigger] Dream failed: ${err instanceof Error ? err.message : String(err)}`)
  }
}

export function createDreamTriggerHook(api: OpenClawPluginApi) {
  return {
    id: 'eo_dream_trigger',
    name: 'EO Dream Trigger',
    description: 'Automatically triggers dream module for self-evolution',
    handle: async (event: any) => {
      incrementSession()
      await triggerDream(api)
    },
  }
}
