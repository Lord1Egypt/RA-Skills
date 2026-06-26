// ============================================================================
// EO Architect Skill - System Architecture Design
// ============================================================================

import type { ExpertResult } from '../types/index.js'
import { EXPERTS } from '../experts/data.js'
import { buildExpertPrompt, aggregateExpertResults } from '../adapter/skill-adapter.js'

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface ArchitectSkillInput {
  task: string
  style?: 'monolithic' | 'microservices' | 'serverless' | 'event-driven' | 'layered'
  language?: string
  cloud?: 'aws' | 'gcp' | 'azure' | 'multi-cloud' | 'on-premise'
  constraints?: string[]
}

export interface ArchitectSkillContext {
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

export interface ArchitectSkillResult {
  success: boolean
  output: string
  expertResults: ExpertResult[]
  durationMs: number
  architecture?: ArchitectureSummary
  error?: string
}

export interface ArchitectureSummary {
  style: string
  language: string
  layers: ArchitectureLayer[]
  modules: ArchitectureModule[]
  risks: ArchitectureRisk[]
}

export interface ArchitectureLayer {
  name: string
  responsibility: string
  technologies: string[]
}

export interface ArchitectureModule {
  name: string
  responsibility: string
  api?: string
  dependencies: string[]
}

export interface ArchitectureRisk {
  name: string
  impact: 'low' | 'medium' | 'high'
  probability: 'low' | 'medium' | 'high'
  mitigation: string
}

// ---------------------------------------------------------------------------
// Architecture Template Generator
// ---------------------------------------------------------------------------

function generateArchitectureTemplate(
  style: string,
  language: string,
  task: string
): ArchitectureSummary {
  const templates: Record<string, ArchitectureSummary> = {
    'microservices': {
      style: 'microservices',
      language,
      layers: [
        { name: 'API Gateway', responsibility: 'Request routing, auth, rate limiting', technologies: ['Kong', 'NGINX', 'Envoy'] },
        { name: 'Service Layer', responsibility: 'Business logic, service orchestration', technologies: [language === 'typescript' ? 'Node.js' : language === 'python' ? 'Python/FastAPI' : 'Java Spring Boot'] },
        { name: 'Data Layer', responsibility: 'Data persistence, caching', technologies: ['PostgreSQL', 'Redis', 'MongoDB'] },
        { name: 'Event Bus', responsibility: 'Async communication, event streaming', technologies: ['Kafka', 'RabbitMQ', 'SNS/SQS'] },
        { name: 'Monitoring', responsibility: 'Observability, tracing', technologies: ['Prometheus', 'Grafana', 'Jaeger'] },
      ],
      modules: [
        { name: 'user-service', responsibility: 'User management, authentication', api: 'REST /user/v1', dependencies: [] },
        { name: 'order-service', responsibility: 'Order processing', api: 'REST /order/v1', dependencies: ['user-service'] },
        { name: 'payment-service', responsibility: 'Payment processing', api: 'REST /payment/v1', dependencies: ['order-service'] },
        { name: 'notification-service', responsibility: 'Email, SMS, push notifications', api: 'REST /notify/v1', dependencies: [] },
      ],
      risks: [
        { name: 'Service discovery complexity', impact: 'medium', probability: 'medium', mitigation: 'Use Consul or etcd for service registry' },
        { name: 'Distributed transaction consistency', impact: 'high', probability: 'medium', mitigation: 'Implement saga pattern with compensating transactions' },
        { name: 'Network latency between services', impact: 'low', probability: 'high', mitigation: 'Use async communication and circuit breakers' },
      ],
    },
    'serverless': {
      style: 'serverless',
      language,
      layers: [
        { name: 'CDN / Edge', responsibility: 'Static content, caching', technologies: ['CloudFront', 'CloudFlare', 'Akamai'] },
        { name: 'API Gateway', responsibility: 'Serverless function triggers', technologies: ['AWS API Gateway', 'Azure Functions', 'GCP Cloud Functions'] },
        { name: 'Compute', responsibility: 'Business logic execution', technologies: ['Lambda', 'Azure Functions', 'Cloud Functions'] },
        { name: 'Data', responsibility: 'Serverless databases', technologies: ['DynamoDB', 'CosmosDB', 'Firestore'] },
        { name: 'Event Bus', responsibility: 'Event-driven triggers', technologies: ['EventBridge', 'Azure Event Grid', 'Pub/Sub'] },
      ],
      modules: [
        { name: 'auth-function', responsibility: 'JWT issuance, token validation', api: 'HTTP Trigger', dependencies: [] },
        { name: 'api-functions', responsibility: 'Business logic handlers', api: 'HTTP Trigger', dependencies: ['auth-function'] },
        { name: 'data-functions', responsibility: 'Data processing pipelines', api: 'Event Trigger', dependencies: [] },
      ],
      risks: [
        { name: 'Cold start latency', impact: 'medium', probability: 'high', mitigation: 'Provisioned concurrency, keep functions warm' },
        { name: 'Vendor lock-in', impact: 'medium', probability: 'high', mitigation: 'Use abstraction layers, avoid proprietary features' },
      ],
    },
    'event-driven': {
      style: 'event-driven',
      language,
      layers: [
        { name: 'Event Producers', responsibility: 'Emit domain events', technologies: ['REST', 'gRPC', 'Message Producers'] },
        { name: 'Event Bus', responsibility: 'Event routing, filtering', technologies: ['Kafka', 'RabbitMQ', 'Azure Event Hubs'] },
        { name: 'Event Consumers', responsibility: 'Process events, side effects', technologies: [language === 'typescript' ? 'Node.js' : 'Java', 'Consumer Groups'] },
        { name: 'State Store', responsibility: 'CQRS read models, projections', technologies: ['PostgreSQL', 'Elasticsearch', 'Redis'] },
      ],
      modules: [
        { name: 'order-events', responsibility: 'Emit order lifecycle events', api: 'Event', dependencies: [] },
        { name: 'inventory-handler', responsibility: 'Update inventory on order events', api: 'Event Consumer', dependencies: ['order-events'] },
        { name: 'notification-handler', responsibility: 'Send notifications on events', api: 'Event Consumer', dependencies: ['order-events'] },
        { name: 'analytics-handler', responsibility: 'Update analytics projections', api: 'Event Consumer', dependencies: ['order-events'] },
      ],
      risks: [
        { name: 'Eventual consistency complexity', impact: 'medium', probability: 'high', mitigation: 'Clear documentation, idempotent consumers' },
        { name: 'Event schema evolution', impact: 'medium', probability: 'medium', mitigation: 'Schema registry, backward compatibility' },
      ],
    },
    'layered': {
      style: 'layered',
      language,
      layers: [
        { name: 'Presentation', responsibility: 'UI, API adapters', technologies: ['React', 'Vue', 'Next.js'] },
        { name: 'Application', responsibility: 'Use cases, service orchestration', technologies: [language === 'typescript' ? 'NestJS' : language === 'python' ? 'FastAPI' : 'Spring MVC'] },
        { name: 'Domain', responsibility: 'Business logic, entities', technologies: ['Domain Classes', 'Services'] },
        { name: 'Infrastructure', responsibility: 'DB access, external services', technologies: ['TypeORM', 'SQLAlchemy', 'JPA'] },
      ],
      modules: [
        { name: 'user-module', responsibility: 'User CRUD and authentication', api: 'REST /users', dependencies: [] },
        { name: 'order-module', responsibility: 'Order management', api: 'REST /orders', dependencies: ['user-module'] },
        { name: 'payment-module', responsibility: 'Payment processing', api: 'REST /payments', dependencies: ['order-module'] },
      ],
      risks: [
        { name: 'Monolithic deployment', impact: 'low', probability: 'high', mitigation: 'Modular architecture, independent deployability' },
      ],
    },
  }

  return templates[style] ?? templates['layered']
}

// ---------------------------------------------------------------------------
// Architect Skill Definition
// ---------------------------------------------------------------------------

export const architectSkill = {
  name: 'architect',
  description: 'Design system architecture with technology stack, modules, and risk assessment',
  expert: 'architect',
  role: 'architect',

  async execute(
    args: string,
    context: ArchitectSkillContext
  ): Promise<ArchitectSkillResult> {
    const startTime = Date.now()
    const logger = context.logger

    // 1. Parse arguments
    const input = parseArchitectInput(args)
    const archStyle = input.style ?? 'layered'
    logger.info(`[architect-skill] Designing ${archStyle} architecture for: ${input.task.slice(0, 50)}...`)

    // 2. Generate architecture template
    const architecture = generateArchitectureTemplate(archStyle, input.language ?? 'typescript', input.task)

    // 3. Determine expert team
    const expertIds = ['arch-001', 'arch-003', 'be-001', 'devops-001']
    const experts = expertIds
      .map(id => EXPERTS[id])
      .filter((e): e is NonNullable<typeof e> => e !== undefined)

    logger.info(`[architect-skill] Expert team: ${experts.map(e => e.name).join(', ')}`)

    // 4. Build expert prompts
    const expertPrompts: Record<string, string> = {
      'arch-001': buildExpertPrompt(
        'arch-001', 'System Architect',
        `Design a comprehensive ${archStyle} system architecture for:\n\n${input.task}\n\nStyle: ${archStyle}\nLanguage: ${input.language ?? 'TypeScript'}\nCloud: ${input.cloud ?? 'multi-cloud'}`,
        { style: archStyle, language: input.language, cloud: input.cloud }
      ),
      'arch-003': buildExpertPrompt(
        'arch-003', 'Data Architect',
        `Design the data layer for:\n\n${input.task}\n\nArchitecture Style: ${archStyle}\nLanguage: ${input.language ?? 'TypeScript'}`,
        { style: archStyle, language: input.language }
      ),
      'be-001': buildExpertPrompt(
        'be-001', 'API Developer',
        `Design API contracts and service boundaries for:\n\n${input.task}\n\nStyle: ${archStyle}`,
        { style: archStyle }
      ),
      'devops-001': buildExpertPrompt(
        'devops-001', 'CI/CD Engineer',
        `Design deployment and infrastructure for:\n\n${input.task}\n\nStyle: ${archStyle}\nCloud: ${input.cloud ?? 'aws'}`,
        { style: archStyle, cloud: input.cloud }
      ),
    }

    // 5. Run expert analysis in parallel
    const results: ExpertResult[] = await Promise.all(
      experts.map(async (expert) => {
        const prompt = expertPrompts[expert.id] ?? buildExpertPrompt(expert.id, expert.name, input.task, {})
        const expertStart = Date.now()

        try {
          const runResult = await context.runtime.subagent.run({
            sessionKey: context.sessionId ?? `architect:${input.task}`,
            message: prompt,
            extraSystemPrompt: `You are ${expert.name}, a ${expert.description}.`,
          })

          await context.runtime.subagent.waitForRun({ runId: runResult.runId, timeoutMs: 180000 })

          const { messages } = await context.runtime.subagent.getSessionMessages({
            sessionKey: context.sessionId ?? `architect:${input.task}`,
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
          logger.error(`[architect-skill] Expert ${expert.name} failed: ${err}`)
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
    const archOutput = formatArchitecture(architecture)
    const expertOutput = aggregateExpertResults(
      results.map(r => ({ expertName: r.expertName, output: r.output, success: r.success })),
      'architect'
    )

    const output = `## 🏗️ Architecture Design

### Task
${input.task}

### Architecture Style: ${archStyle.toUpperCase()}
### Language: ${input.language ?? 'TypeScript'}

${archOutput}

### Expert Analysis
${expertOutput}`

    return {
      success: true,
      output,
      expertResults: results,
      durationMs: Date.now() - startTime,
      architecture,
    }
  },
}

// ---------------------------------------------------------------------------
// Helper Functions
// ---------------------------------------------------------------------------

function parseArchitectInput(args: string): ArchitectSkillInput {
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
    style: params.style as ArchitectSkillInput['style'],
    language: params.language,
    cloud: params.cloud as ArchitectSkillInput['cloud'],
    constraints: params.constraints ? params.constraints.split(',').map(s => s.trim()) : [],
  }
}

function formatArchitecture(arch: ArchitectureSummary): string {
  const lines: string[] = []

  lines.push('### Layers')
  for (const layer of arch.layers) {
    lines.push(`**${layer.name}**`)
    lines.push(`- Responsibility: ${layer.responsibility}`)
    lines.push(`- Technologies: ${layer.technologies.join(', ')}`)
    lines.push('')
  }

  lines.push('### Modules')
  for (const mod of arch.modules) {
    lines.push(`**${mod.name}**`)
    lines.push(`- Responsibility: ${mod.responsibility}`)
    if (mod.api) lines.push(`- API: ${mod.api}`)
    if (mod.dependencies.length) lines.push(`- Dependencies: ${mod.dependencies.join(', ')}`)
    lines.push('')
  }

  lines.push('### Risk Assessment')
  for (const risk of arch.risks) {
    const level = risk.impact === 'high' || risk.probability === 'high' ? '🔴' : risk.impact === 'medium' ? '🟡' : '🟢'
    lines.push(`${level} **${risk.name}** (Impact: ${risk.impact}, Probability: ${risk.probability})`)
    lines.push(`  Mitigation: ${risk.mitigation}`)
  }

  return lines.join('\n')
}
