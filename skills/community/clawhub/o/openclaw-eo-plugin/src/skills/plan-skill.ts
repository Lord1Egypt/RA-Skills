// ============================================================================
// EO Plan Skill - Project Planning with WBS Generation
// ============================================================================

import type { ExpertResult } from '../types/index.js'
import { EXPERTS, TEAM_TEMPLATES } from '../experts/data.js'
import { buildExpertPrompt, aggregateExpertResults } from '../adapter/skill-adapter.js'

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface PlanSkillInput {
  task: string
  team?: string[]
  constraints?: string[]
  priority?: 'low' | 'medium' | 'high'
  template?: string
}

export interface PlanSkillContext {
  runtime: {
    subagent: {
      run: (params: {
        sessionKey: string
        message: string
        extraSystemPrompt?: string
        provider?: string
        model?: string
      }) => Promise<{ runId: string }>
      waitForRun: (params: { runId: string; timeoutMs?: number }) => Promise<{ status: string; error?: string }>
      getSessionMessages: (params: { sessionKey: string; limit?: number }) => Promise<{ messages: unknown[] }>
    }
  }
  logger: { info: (msg: string) => void; warn: (msg: string) => void; error: (msg: string) => void }
  sessionId?: string
}

export interface PlanSkillResult {
  success: boolean
  output: string
  expertResults: ExpertResult[]
  durationMs: number
  wbs?: WBSMilestone[]
  error?: string
}

export interface WBSMilestone {
  id: string
  name: string
  tasks: WBSTask[]
  status: 'pending' | 'in_progress' | 'completed' | 'failed'
  completion: number
}

export interface WBSTask {
  id: string
  name: string
  estimatedHours?: number
  assignee?: string
  dependencies?: string[]
  priority?: 'low' | 'medium' | 'high'
}

// ---------------------------------------------------------------------------
// WBS Generator
// ---------------------------------------------------------------------------

function generateWBS(task: string, constraints: string[], priority: string): WBSMilestone[] {
  const milestones: WBSMilestone[] = [
    {
      id: 'ms-001',
      name: 'Requirements & Planning',
      status: 'pending',
      completion: 0,
      tasks: [
        { id: 't-001', name: 'Analyze requirements', estimatedHours: 4, priority: 'high' },
        { id: 't-002', name: 'Create user stories', estimatedHours: 3, priority: 'high' },
        { id: 't-003', name: 'Define acceptance criteria', estimatedHours: 2, priority: 'medium' },
        { id: 't-004', name: 'Technical design review', estimatedHours: 3, priority: 'medium', dependencies: ['t-001'] },
      ],
    },
    {
      id: 'ms-002',
      name: 'Core Development',
      status: 'pending',
      completion: 0,
      tasks: [
        { id: 't-005', name: 'Scaffold project structure', estimatedHours: 2, priority: 'high', dependencies: ['t-004'] },
        { id: 't-006', name: 'Implement core features', estimatedHours: 16, priority: 'high', dependencies: ['t-005'] },
        { id: 't-007', name: 'API integration', estimatedHours: 8, priority: 'medium', dependencies: ['t-005'] },
        { id: 't-008', name: 'Database schema & models', estimatedHours: 6, priority: 'high', dependencies: ['t-005'] },
      ],
    },
    {
      id: 'ms-003',
      name: 'Testing & QA',
      status: 'pending',
      completion: 0,
      tasks: [
        { id: 't-009', name: 'Write unit tests', estimatedHours: 8, priority: 'high', dependencies: ['t-006'] },
        { id: 't-010', name: 'Integration testing', estimatedHours: 6, priority: 'medium', dependencies: ['t-007', 't-008'] },
        { id: 't-011', name: 'End-to-end testing', estimatedHours: 4, priority: 'medium', dependencies: ['t-009', 't-010'] },
        { id: 't-012', name: 'Performance testing', estimatedHours: 4, priority: 'low', dependencies: ['t-011'] },
      ],
    },
    {
      id: 'ms-004',
      name: 'Deployment & Delivery',
      status: 'pending',
      completion: 0,
      tasks: [
        { id: 't-013', name: 'CI/CD pipeline setup', estimatedHours: 4, priority: 'high', dependencies: ['t-009'] },
        { id: 't-014', name: 'Staging deployment', estimatedHours: 2, priority: 'medium', dependencies: ['t-012', 't-013'] },
        { id: 't-015', name: 'Production deployment', estimatedHours: 2, priority: 'high', dependencies: ['t-014'] },
        { id: 't-016', name: 'Post-deployment monitoring', estimatedHours: 2, priority: 'medium', dependencies: ['t-015'] },
      ],
    },
  ]

  return milestones
}

// ---------------------------------------------------------------------------
// Plan Skill Definition
// ---------------------------------------------------------------------------

export const planSkill = {
  name: 'plan',
  description: 'Create a structured project plan with WBS, milestones, and expert team analysis',
  expert: 'planner',
  role: 'planner',

  /**
   * Execute the plan skill
   * 1. Parse input arguments
   * 2. Generate WBS structure
   * 3. Invoke planner + engineer + qa experts via subagent
   * 4. Return structured plan result
   */
  async execute(
    args: string,
    context: PlanSkillContext
  ): Promise<PlanSkillResult> {
    const startTime = Date.now()
    const logger = context.logger

    // 1. Parse arguments
    const input = parsePlanInput(args)
    logger.info(`[plan-skill] Starting plan for: ${input.task.slice(0, 50)}...`)

    // 2. Generate WBS
    const wbs = generateWBS(input.task, input.constraints ?? [], input.priority ?? 'medium')
    const totalHours = wbs.reduce(
      (sum, ms) => sum + ms.tasks.reduce((s, t) => s + (t.estimatedHours ?? 0), 0),
      0
    )

    // 3. Determine expert team
    const expertIds = input.team ?? TEAM_TEMPLATES['fullstack'] ?? ['plan-001', 'fe-001', 'be-001', 'qa-001']
    const experts = expertIds
      .map(id => EXPERTS[id])
      .filter((e): e is NonNullable<typeof e> => e !== undefined)

    if (experts.length === 0) {
      return {
        success: false,
        output: 'No valid experts found for planning team',
        expertResults: [],
        durationMs: Date.now() - startTime,
        error: 'Empty expert team',
      }
    }

    logger.info(`[plan-skill] Expert team: ${experts.map(e => e.name).join(', ')}`)

    // 4. Build expert prompts
    const expertPrompts: Record<string, string> = {
      'plan-001': buildExpertPrompt('plan-001', 'Project Planner', 
        `Create a detailed project plan for:\n\n${input.task}\n\nPriority: ${input.priority}\n${input.constraints?.length ? `Constraints: ${input.constraints.join(', ')}` : ''}\n\nTotal estimated hours: ${totalHours}\n\nGenerate a structured plan with milestones, tasks, and timeline.`,
        { priority: input.priority, constraints: input.constraints }
      ),
      'fe-001': buildExpertPrompt('fe-001', 'React Developer',
        `Provide frontend technical analysis for:\n\n${input.task}\n\nIdentify frontend components, state management needs, and API integration points.`,
        {}
      ),
      'be-001': buildExpertPrompt('be-001', 'API Developer',
        `Provide backend technical analysis for:\n\n${input.task}\n\nIdentify API endpoints, data models, and service boundaries.`,
        {}
      ),
      'qa-001': buildExpertPrompt('qa-001', 'Test Engineer',
        `Define testing strategy for:\n\n${input.task}\n\nIdentify test scenarios, coverage requirements, and automation opportunities.`,
        {}
      ),
    }

    // 5. Run expert analysis in parallel
    const results: ExpertResult[] = await Promise.all(
      experts.map(async (expert) => {
        const prompt = expertPrompts[expert.id] ?? buildExpertPrompt(expert.id, expert.name, input.task, {})
        const expertStart = Date.now()

        try {
          const runResult = await context.runtime.subagent.run({
            sessionKey: context.sessionId ?? `plan:${input.task}`,
            message: prompt,
            extraSystemPrompt: `You are ${expert.name}, a ${expert.description}.`,
          })

          await context.runtime.subagent.waitForRun({ runId: runResult.runId, timeoutMs: 120000 })

          const { messages } = await context.runtime.subagent.getSessionMessages({
            sessionKey: context.sessionId ?? `plan:${input.task}`,
            limit: 5,
          })

          const lastMsg = messages[messages.length - 1] as { content?: string } | undefined
          const output = typeof lastMsg?.content === 'string' ? lastMsg.content.slice(0, 2000) : 'No output'

          return {
            expertId: expert.id,
            expertName: expert.name,
            output,
            durationMs: Date.now() - expertStart,
            success: true,
          }
        } catch (err) {
          logger.error(`[plan-skill] Expert ${expert.name} failed: ${err}`)
          return {
            expertId: expert.id,
            expertName: expert.name,
            output: '',
            durationMs: Date.now() - expertStart,
            success: false,
            error: String(err),
          }
        }
      })
    )

    // 6. Format output
    const wbsSummary = formatWBS(wbs)
    const expertOutput = aggregateExpertResults(
      results.map(r => ({ expertName: r.expertName, output: r.output, success: r.success })),
      'plan'
    )

    const output = `## 📋 Project Plan

### Task
${input.task}

### WBS (Work Breakdown Structure)
${wbsSummary}

### Team
${experts.map(e => `- **${e.name}** (${e.role}): ${e.description}`).join('\n')}

### Estimated Total Hours
${totalHours}h

${expertOutput}`

    return {
      success: true,
      output,
      expertResults: results,
      durationMs: Date.now() - startTime,
      wbs,
    }
  },
}

// ---------------------------------------------------------------------------
// Helper Functions
// ---------------------------------------------------------------------------

function parsePlanInput(args: string): PlanSkillInput {
  const params: Record<string, string> = {}
  const remaining: string[] = []

  for (const part of args.split(/\s+/)) {
    const eqIdx = part.indexOf('=')
    if (eqIdx > 0) {
      params[part.slice(0, eqIdx)] = part.slice(eqIdx + 1)
    } else {
      remaining.push(part)
    }
  }

  return {
    task: params.task ?? remaining.join(' ') ?? 'Unspecified task',
    team: params.team ? params.team.split(',').map(s => s.trim()) : undefined,
    constraints: params.constraints ? params.constraints.split(',').map(s => s.trim()) : [],
    priority: (params.priority as PlanSkillInput['priority']) ?? 'medium',
    template: params.template,
  }
}

function formatWBS(wbs: WBSMilestone[]): string {
  return wbs
    .map(
      (ms, i) =>
        `**${i + 1}. ${ms.name}**${ms.tasks
          .map(
            (t, j) =>
              `\n   ${i + 1}.${j + 1} ${t.name}${t.estimatedHours ? ` (${t.estimatedHours}h)` : ''}${t.dependencies?.length ? ` ← depends on ${t.dependencies.join(', ')}` : ''}`
          )
          .join('')}`
    )
    .join('\n\n')
}
