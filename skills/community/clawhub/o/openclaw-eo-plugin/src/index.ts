/**
 * EO OpenClaw Plugin - Main Entry v3.0.0
 *
 * Everything Openclaw - Modular Multi-Expert Collaboration Plugin
 * Proactive Context Management + Workflow Orchestration + CLOSED-LOOP EVOLUTION
 * 
 * KEY FEATURE: Closed-Loop Self-Evolution
 * Decision → Execute → Track → Score → Analyze → Generate Rules → ENFORCE → Verify
 */

import type { OpenClawPluginApi } from 'openclaw/plugin-sdk'
import type { AgentToolResult } from '@mariozechner/pi-agent-core'
import { PLUGIN_VERSION } from './config.js'

// Tool handlers
import {
  handleCollab,
  handleListExperts,
  handlePlan,
  handleArchitect,
  handleVerify,
  handleCodeReview,
  handleDream,
  handleSelfLearn,
  handleRAGQuery,
  handleMemoryStats,
  handleEvolve,
  handleRAGIndex,
  handleRAGAccess,
  handlePatternLearn,
} from './tools/index.js'

// Hooks
import {
  createSessionStartHook,
  createSessionEndHook,
  createProactiveMonitorHook,
  configureProactiveMonitor,
  createDreamTriggerHook,
  createRuleEnforcementHook,
  createNewConversationHook,
  initContextWorkflowHooks,
  onMessageHook,
  afterToolCallHook,
  afterOutcomeHook,
} from './hooks/index.js'

// Scheduler (Dream Module automation)
import { dreamScheduler } from './scheduler/index.js'

// Dream Module (v2 with Feishu push support)
import { getDreamModule } from './session/eo-dream-enhanced.js'

// Proactive notifier (Feishu push)
import { proactiveNotifier } from './continuous/proactive-notifier.js'

// Autonomy (Self-optimization loop)
import { effectTracker, patchManager, evolutionReporter, closedLoopEvolver } from './autonomy/index.js'

// Auto-init
import { runAutoInit } from './auto-init.js'
import { textResult } from './formatters/index.js'

// ============================================================================
// Plugin Definition
// ============================================================================

const plugin = {
  id: 'eo-collaboration',
  name: 'Everything Openclaw (EO)',
  description: `Multi-expert collaboration plugin v${PLUGIN_VERSION} - 141 experts, proactive context management, workflow orchestration, 5 preset workflows`,

  register(api: OpenClawPluginApi) {
    api.logger.info(`[EO Plugin v${PLUGIN_VERSION}] Registering Everything Openclaw plugin...`)

    // ── Register Tools ──────────────────────────────────────────────────────

    // eo_collab - Main collaboration command
    api.registerTool(() => ({
      name: 'eo_collab',
      label: 'EO Collaboration',
      description: 'Main multi-expert collaboration tool. Lists available commands and expert roles.',
      parameters: {
        type: 'object',
        properties: { task: { type: 'string', description: 'The task or context for collaboration' } },
        required: [],
      },
      async execute(_id: string, params: { task?: string }) {
        return handleCollab(params)
      },
    }))

    // eo_list_experts - List available experts
    api.registerTool(() => ({
      name: 'eo_list_experts',
      label: 'EO List Experts',
      description: 'List available experts in the EO library. Filter by name, role, or capability.',
      parameters: {
        type: 'object',
        properties: { filter: { type: 'string', description: 'Filter experts by name, role, or description' } },
        required: [],
      },
      async execute(_id: string, params: { filter?: string }) {
        return handleListExperts(params)
      },
    }))

    // eo_plan - Project planning
    api.registerTool(() => ({
      name: 'eo_plan',
      label: 'EO Project Planner',
      description: 'Create project plan with Planner expert team. Generates WBS, milestones, team composition via MultiExpertOrchestrator.',
      parameters: {
        type: 'object',
        properties: {
          task: { type: 'string', description: 'Project or task to plan' },
          priority: { type: 'string', description: 'Priority: low, medium, high' },
          team: { type: 'string', description: 'Team template: fullstack, web, mobile, data' },
        },
        required: ['task'],
      },
      async execute(_id: string, params: { task?: string; priority?: string; team?: string }) {
        return handlePlan(params)
      },
    }))

    // eo_architect - System architecture design
    api.registerTool(() => ({
      name: 'eo_architect',
      label: 'EO System Architect',
      description: 'Design system architecture with Architect expert team. Tech stack, modules, risks via MultiExpertOrchestrator.',
      parameters: {
        type: 'object',
        properties: {
          task: { type: 'string', description: 'Project to design' },
          style: { type: 'string', description: 'Architecture style: layered, microservices, serverless, event-driven' },
          language: { type: 'string', description: 'Primary language: typescript, python, java, go' },
          cloud: { type: 'string', description: 'Cloud provider: aws, gcp, azure, multi-cloud' },
        },
        required: ['task'],
      },
      async execute(_id: string, params: { task?: string; style?: string; language?: string; cloud?: string }) {
        return handleArchitect(params)
      },
    }))

    // eo_verify - Checkpoint verification
    api.registerTool(() => ({
      name: 'eo_verify',
      label: 'EO Checkpoint Verifier',
      description: 'Verify checkpoint with QA expert team. Validates milestone completion via MultiExpertOrchestrator.',
      parameters: {
        type: 'object',
        properties: {
          checkpoint: { type: 'string', description: 'Checkpoint name: milestone1, milestone2, milestone3, final' },
          type: { type: 'string', description: 'Verification type: code, architecture, test, security, performance' },
          criteria: { type: 'string', description: 'Specific criteria to verify (comma-separated)' },
        },
        required: ['checkpoint'],
      },
      async execute(_id: string, params: { checkpoint?: string; type?: string; criteria?: string }) {
        return handleVerify(params)
      },
    }))

    // eo_code_review - Code review
    api.registerTool(() => ({
      name: 'eo_code_review',
      label: 'EO Code Review',
      description: 'Code review with CodeReviewer expert team. Security, performance, quality via MultiExpertOrchestrator.',
      parameters: {
        type: 'object',
        properties: {
          path: { type: 'string', description: 'Code path to review: ./src, ./lib, specific files' },
          depth: { type: 'string', description: 'Review depth: quick, standard, deep' },
          focus: { type: 'string', description: 'Focus areas: security, performance, style (comma-separated)' },
        },
        required: [],
      },
      async execute(_id: string, params: { path?: string; depth?: string; focus?: string }) {
        return handleCodeReview(params)
      },
    }))

    // eo_dream - Dream module
    api.registerTool(() => ({
      name: 'eo_dream',
      label: 'EO Dream Module',
      description: 'Trigger Dream Module for self-evolution',
      parameters: { type: 'object', properties: { trigger: { type: 'string' } }, required: [] },
      async execute(_id: string, params: any) {
        return handleDream(params)
      },
    }))

    // eo_self_learn - Self-learning
    api.registerTool(() => ({
      name: 'eo_self_learn',
      label: 'EO Self-Learning',
      description: 'Self-Learning Engine for feedback and patterns',
      parameters: { type: 'object', properties: { action: { type: 'string' } }, required: [] },
      async execute(_id: string, params: any) {
        return handleSelfLearn(params)
      },
    }))

    // eo_rag_query - RAG knowledge query
    api.registerTool(() => ({
      name: 'eo_rag_query',
      label: 'EO RAG Knowledge',
      description: 'Query RAG Knowledge Base',
      parameters: { type: 'object', properties: { query: { type: 'string' }, topK: { type: 'number' } }, required: ['query'] },
      async execute(_id: string, params: any) {
        return handleRAGQuery(params)
      },
    }))

    // eo_rag_index - RAG knowledge indexing
    api.registerTool(() => ({
      name: 'eo_rag_index',
      label: 'EO RAG Index Manager',
      description: 'Bulk index documents into RAG Knowledge Base. Actions: add (index content/file), list (show contents), stats (show statistics)',
      parameters: {
        type: 'object',
        properties: {
          action: { type: 'string', enum: ['add', 'remove', 'list', 'stats', 'clear'] },
          source: { type: 'string', description: 'Document source name' },
          content: { type: 'string', description: 'Content to index' },
          filePath: { type: 'string', description: 'File or directory path to index' },
          layer: { type: 'number', description: 'Layer: 1=Expert, 2=Pattern, 3=Checkpoint, 4=ETP, 5=Session' },
          tags: { type: 'array', items: { type: 'string' }, description: 'Tags for categorization' },
          visibility: { type: 'string', enum: ['public', 'protected', 'private'] },
        },
        required: ['action'],
      },
      async execute(_id: string, params: any) {
        return handleRAGIndex(params)
      },
    }))

    // eo_rag_access - RAG access control
    api.registerTool(() => ({
      name: 'eo_rag_access',
      label: 'EO RAG Access Control',
      description: 'Manage per-agent access to RAG Knowledge Base. Grant/revoke access, list permissions.',
      parameters: {
        type: 'object',
        properties: {
          action: { type: 'string', enum: ['grant', 'revoke', 'list', 'set-default'] },
          agentId: { type: 'string', description: 'Target agent ID' },
          layers: { type: 'array', items: { type: 'number' }, description: 'Allowed layers [1,2,3,4,5]' },
          tags: { type: 'array', items: { type: 'string' }, description: 'Allowed tags' },
          excludeChunks: { type: 'array', items: { type: 'string' }, description: 'Chunk IDs to exclude' },
        },
        required: ['action'],
      },
      async execute(_id: string, params: any) {
        return handleRAGAccess(params)
      },
    }))

    // eo_pattern_learn - Learn from successful execution paths
    api.registerTool(() => ({
      name: 'eo_pattern_learn',
      label: 'EO Pattern Learning',
      description: 'Learn successful patterns from historical sessions and retrieve relevant patterns for new tasks. Actions: learn (analyze sessions), retrieve (find patterns), stats (show statistics)',
      parameters: {
        type: 'object',
        properties: {
          action: { type: 'string', enum: ['learn', 'retrieve', 'stats', 'list'] },
          taskQuery: { type: 'string', description: 'Task description to retrieve patterns for' },
          sessionFile: { type: 'string', description: 'Path to specific session file to learn from' },
        },
        required: ['action'],
      },
      async execute(_id: string, params: any) {
        return handlePatternLearn(params)
      },
    }))

    // eo_memory_stats - Memory statistics
    api.registerTool(() => ({
      name: 'eo_memory_stats',
      label: 'EO Memory Stats',
      description: 'EO Memory system statistics',
      parameters: { type: 'object', properties: {}, required: [] },
      async execute(_id: string) {
        return handleMemoryStats()
      },
    }))

    // eo_evolve - Closed-loop evolution (KEY for self-improvement)
    api.registerTool(() => ({
      name: 'eo_evolve',
      label: 'EO Closed-Loop Evolve',
      description: '🔄 TRIGGERS CLOSED-LOOP EVOLUTION: Analyze effect data → Generate mandatory rules → Enforce rules in SOUL.md. This is the KEY tool for true self-improvement. Rules are NOT suggestions - they become part of agent identity.',
      parameters: {
        type: 'object',
        properties: {
          force: { type: 'boolean', description: 'Force evolution (bypass 24h cooldown)' },
          dryRun: { type: 'boolean', description: 'Preview what would happen without applying' },
          status: { type: 'boolean', description: 'Show evolution status and current rules' },
        },
        required: [],
      },
      async execute(_id: string, params: any) {
        return handleEvolve(params, api)
      },
    }))

    // eo_init - Auto-initialize all agent workspaces
    api.registerTool(() => ({
      name: 'eo_init',
      label: 'EO Auto-Init',
      description: 'Auto-configure all agent workspaces with EO-Enhanced SOUL.md. This enables full EO capabilities for all agents.',
      parameters: {
        type: 'object',
        properties: {
          force: { type: 'boolean', description: 'Force re-initialization even if already EO-Enhanced' },
          dryRun: { type: 'boolean', description: 'Preview mode - show what would be done without making changes' },
          agentId: { type: 'string', description: 'Specific agent ID to initialize (omit for all)' },
        },
        required: [],
      },
      async execute(_id: string, params: { force?: boolean; dryRun?: boolean; agentId?: string }) {
        api.logger.info('[EO Plugin] eo_init tool called')
        const results = await runAutoInit(api, {
          force: params.force,
          dryRun: params.dryRun,
          agentIds: params.agentId ? [params.agentId] : undefined,
        })
        const lines = [
          `🦞 **EO Auto-Init Results**`,
          ``,
          `**Summary:** ${results.success} configured, ${results.skipped} skipped, ${results.failed} failed`,
          ``,
          `**Details:**`,
        ]
        for (const r of results.results) {
          const icon = r.status === 'success' ? '✅' : r.status === 'skipped' ? '⏭️' : '❌'
          lines.push(`${icon} ${r.agentId}: ${r.status}${r.reason ? ` (${r.reason})` : ''}`)
        }
        if (params.dryRun) {
          lines.push('', '💡 This was a dry-run. Run without --dryRun to actually apply changes.')
        }
        return textResult(lines.join('\n'))
      },
    }))

    // ── Register Hooks ─────────────────────────────────────────────────────

    // Session start - inject context
    const sessionStartHook = createSessionStartHook(api)
    api.registerHook(sessionStartHook.id, sessionStartHook.handle)

    // Session end - analyze and learn
    const sessionEndHook = createSessionEndHook(api)
    api.registerHook(sessionEndHook.id, sessionEndHook.handle)

    // Proactive monitor - detect intent with auto-suggest
    configureProactiveMonitor({
      enabled: true,
      threshold: 0.35,
      autoSuggestThreshold: 0.75,  // 75%+ confidence → auto-suggest
      feishuChatId: 'oc_3c700ffbe8b539109784c48b7eaed339',
    })
    const proactiveHook = createProactiveMonitorHook(api)
    api.registerHook(proactiveHook.id, proactiveHook.handle)

    // Dream trigger - self-evolution
    const dreamTriggerHook = createDreamTriggerHook(api)
    api.registerHook(dreamTriggerHook.id, dreamTriggerHook.handle)

    // Rule Enforcement Hook - Hybrid Architecture (v3.1)
    // Enforces mandatory rules at hook level (cannot be bypassed)
    const ruleHook = createRuleEnforcementHook(api)
    api.registerHook(ruleHook.id, ruleHook.handle)

    // Initialize context and workflow system
    initContextWorkflowHooks(api)

    // before_tool_call routing hook
    api.registerHook('before_tool_call', async (event: any) => {
      const toolName = event?.toolName
      if (!toolName?.startsWith('eo_')) return
      api.logger.debug(`[EO Plugin] Routing tool call: ${toolName}`)
    })

    // on_message hook - context monitoring + workflow triggers
    api.registerHook('on_message', async (event: any) => {
      await onMessageHook(api, event)
    })

    // New Conversation Hook - detect new Feishu conversations + trigger auto-allocation
    const newConversationHook = createNewConversationHook(api)
    api.registerHook('on_message', async (event: any) => {
      await newConversationHook.handle(event)
    })

    // after_tool_call hook - workflow state updates
    api.registerHook('after_tool_call', async (event: any) => {
      await afterToolCallHook(api, event)
    })

    // after_outcome hook - automatic outcome collection for effect tracking
    api.registerHook('after_tool_call', async (event: any) => {
      if (event?.toolName) {
        afterOutcomeHook.trigger({
          type: 'tool_call',
          toolName: event.toolName,
          toolParams: event.params || {},
          success: !event.error,
          durationMs: event.durationMs || 0,
          result: event.result,
          error: event.error,
        })
      }
    })

    api.logger.info(`[EO Plugin v${PLUGIN_VERSION}] Everything Openclaw plugin registered successfully!`)

    // ── Auto-Initialize on First Load ───────────────────────────────────────
    // Run auto-init automatically on plugin load (if not done before)
    ;(async () => {
      try {
        const initResults = await runAutoInit(api, { dryRun: false })
        if (initResults.success > 0) {
          api.logger.info(`[EO Plugin] Auto-initialized ${initResults.success} agent workspaces with EO-Enhanced capabilities`)
        } else if (initResults.skipped > 0) {
          api.logger.debug('[EO Plugin] All agents already EO-Enhanced, skipping auto-init')
        }
      } catch (e: any) {
        api.logger.warn(`[EO Plugin] Auto-init warning: ${e.message}`)
      }
    })()

    // ── Initialize Dream Scheduler ─────────────────────────────────────────────
    // Set up daily Dream Module trigger at 00:30
    // Configure Feishu push: oc_3c700ffbe8b539109784c48b7eaed339
    ;(async () => {
      try {
        // Configure Feishu chat ID for Dream report push
        const FEISHU_CHAT_ID = 'oc_3c700ffbe8b539109784c48b7eaed339'
        dreamScheduler.updateConfig({ feishuChatId: FEISHU_CHAT_ID })
        
        const result = await dreamScheduler.initialize()
        if (result.success) {
          api.logger.info(`[EO Plugin] Dream scheduler initialized: ${result.message}`)
        } else {
          api.logger.warn(`[EO Plugin] Dream scheduler init failed: ${result.error}`)
        }

        // Wire DreamModule (eo-dream-enhanced.ts) to ProactiveNotifier for Feishu push
        // This ensures DreamModule.dream() calls can push to Feishu when called directly
        const dreamModule = getDreamModule({
          workspaceRoot: process.cwd(),
          memoryPath: '.eo-dream/memory.json',
          enableProactiveReport: true,
          feishuChatId: FEISHU_CHAT_ID,
        })
        dreamModule.setNotifier(proactiveNotifier, FEISHU_CHAT_ID)
        api.logger.info(`[EO Plugin] DreamModule Feishu push configured: ${FEISHU_CHAT_ID}`)
      } catch (e: any) {
        api.logger.warn(`[EO Plugin] Dream scheduler warning: ${e.message}`)
      }
    })()

    // ── Initialize Effect Tracker Stats ───────────────────────────────────────
    api.logger.info(`[EO Plugin] Effect Tracker: ${effectTracker.stats().total} decisions tracked`)
    api.logger.info(`[EO Plugin] Patch Manager: ${patchManager.getStats().total} patches, ${patchManager.getStats().reviewQueueSize} pending review`)
  },
}

export { plugin as default }
