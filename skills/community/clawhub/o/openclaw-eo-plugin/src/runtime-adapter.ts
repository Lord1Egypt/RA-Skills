// ============================================================================
// EO Runtime Adapter - Bridge OpenClaw Plugin API → SkillContext
//
// Provides the SkillContext.runtime.subagent interface for EO skill implementations
// by wrapping OpenClaw's sessions API (sessions_spawn, sessions_yield, etc.)
// ============================================================================

// ---------------------------------------------------------------------------
// Runtime Adapter Interface (what skill executors need)
// ---------------------------------------------------------------------------

import { logger } from './utils/logger.js'

export interface SubagentRuntime {
  subagent: {
    run(params: {
      sessionKey: string
      message: string
      extraSystemPrompt?: string
      provider?: string
      model?: string
    }): Promise<{ runId: string }>
    waitForRun(params: { runId: string; timeoutMs?: number }): Promise<{ status: string; error?: string }>
    getSessionMessages(params: { sessionKey: string; limit?: number }): Promise<{ messages: unknown[] }>
  }
}

// ---------------------------------------------------------------------------
// Default Logger
// ---------------------------------------------------------------------------

export function createLogger(prefix: string) {
  return {
    info: (msg: string) => logger.info(`[${prefix}] INFO: ${msg}`),
    warn: (msg: string) => console.warn(`[${prefix}] WARN: ${msg}`),
    error: (msg: string) => console.error(`[${prefix}] ERROR: ${msg}`),
  }
}

// ---------------------------------------------------------------------------
// Runtime Adapter Factory
// ---------------------------------------------------------------------------

export interface RuntimeAdapterConfig {
  sessionKey: string
  defaultTimeoutMs?: number
}

/**
 * Create a SkillContext-compatible runtime adapter for OpenClaw plugin tools.
 *
 * This wraps the OpenClaw spawning API (sessions_spawn, sessions_yield, etc.)
 * into the SkillContext.runtime.subagent interface expected by EO skills.
 */
export function createRuntimeAdapter(config: RuntimeAdapterConfig): SubagentRuntime {
  const { sessionKey, defaultTimeoutMs = 300000 } = config

  // Track running sessions
  const runningSessions = new Map<string, { status: string; result?: unknown }>()

  return {
    subagent: {
      async run(params: {
        sessionKey: string
        message: string
        extraSystemPrompt?: string
        provider?: string
        model?: string
      }): Promise<{ runId: string }> {
        const runId = `run-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`

        runningSessions.set(runId, { status: 'running' })

        logger.debug(`Spawning subagent runId=${runId} sessionKey=${params.sessionKey}`)
        logger.debug(`message length: ${params.message.length} chars`)

        // Store task info for the orchestration layer
        ;(globalThis as any).__eoRuntimeTasks = (globalThis as any).__eoRuntimeTasks || {}
        ;(globalThis as any).__eoRuntimeTasks[runId] = {
          runId,
          sessionKey: params.sessionKey,
          message: params.message,
          extraSystemPrompt: params.extraSystemPrompt,
          provider: params.provider,
          model: params.model,
          createdAt: Date.now(),
        }

        return { runId }
      },

      async waitForRun(params: {
        runId: string
        timeoutMs?: number
      }): Promise<{ status: string; error?: string }> {
        const timeoutMs = params.timeoutMs ?? defaultTimeoutMs
        const startTime = Date.now()
        const runId = params.runId

        logger.debug(`Waiting for runId=${runId} timeout=${timeoutMs}ms`)

        while (Date.now() - startTime < timeoutMs) {
          const session = runningSessions.get(runId)

          if (session?.status === 'completed') {
            runningSessions.delete(runId)
            return { status: 'completed' }
          }

          if (session?.status === 'failed') {
            runningSessions.delete(runId)
            return { status: 'failed', error: 'Expert task failed' }
          }

          await new Promise(resolve => setTimeout(resolve, 500))
        }

        runningSessions.delete(runId)
        return { status: 'timeout', error: `Task ${runId} timed out after ${timeoutMs}ms` }
      },

      async getSessionMessages(params: {
        sessionKey: string
        limit?: number
      }): Promise<{ messages: unknown[] }> {
        const limit = params.limit ?? 10
        const key = params.sessionKey

        ;(globalThis as any).__eoSessionMessages = (globalThis as any).__eoSessionMessages || {}
        const sessionMessages: any[] = (globalThis as any).__eoSessionMessages[key] || []

        const messages = sessionMessages.slice(-limit)

        logger.debug(`getSessionMessages sessionKey=${key} count=${messages.length}`)

        return { messages }
      },
    },
  }
}

// ---------------------------------------------------------------------------
// Message Accumulation Helper
// ---------------------------------------------------------------------------

export function storeSessionMessage(sessionKey: string, message: unknown): void {
  ;(globalThis as any).__eoSessionMessages = (globalThis as any).__eoSessionMessages || {}
  ;(globalThis as any).__eoSessionMessages[sessionKey] = (globalThis as any).__eoSessionMessages[sessionKey] || []
  ;(globalThis as any).__eoSessionMessages[sessionKey].push(message)
}

export function completeSession(runId: string, result: unknown, error?: string): void {
  const tasks = (globalThis as any).__eoRuntimeTasks || {}
  const task = tasks[runId]

  if (task) {
    ;(globalThis as any).__eoSessionResults = (globalThis as any).__eoSessionResults || {}
    ;(globalThis as any).__eoSessionResults[runId] = { result, error, completedAt: Date.now() }

    storeSessionMessage(task.sessionKey, {
      role: 'assistant',
      content: typeof result === 'string' ? result : JSON.stringify(result),
      runId,
    })
  }
}

// ---------------------------------------------------------------------------
// SkillContext Builder (minimal - for compatibility with skill system)
// ---------------------------------------------------------------------------

export interface SimpleSkillContext {
  runtime: SubagentRuntime
  logger: ReturnType<typeof createLogger>
  sessionId?: string
}

export function buildSkillContext(sessionId?: string, loggerPrefix = 'skill'): SimpleSkillContext {
  const logger = createLogger(loggerPrefix)
  const runtime = createRuntimeAdapter({ sessionKey: sessionId ?? 'default' })

  return { runtime, logger, sessionId }
}
