# Exemplos de Código — Agentes ORBIT

## Orquestrador

```typescript
// src/agents/orchestrator.ts
import { Agent, run, handoff } from '@openai/agents'
import { researchAgent } from './research'
import { analysisAgent } from './analysis'
import { dossierAgent } from './dossier'
import { qualityAgent } from './quality-review'

export const orchestratorAgent = new Agent({
  name: 'Orquestrador',
  model: 'gpt-4o',
  instructions: `
    Você é o Orquestrador do sistema ORBIT.
    Sua missão: interpretar a intenção do usuário e distribuir o trabalho
    para os agentes corretos via handoffs.
    
    Fluxo padrão para pesquisa/dossiê:
    1. Interpretar intenção
    2. Handoff para research (pesquisa web)
    3. Handoff para analysis (análise das evidências)
    4. Handoff para dossier (criação do documento)
    5. Handoff para quality (revisão final)
    
    Registre cada handoff e decisão no contexto.
    Sempre use Português do Brasil.
  `,
  handoffs: [researchAgent, analysisAgent, dossierAgent, qualityAgent]
})
```

## Agente de Pesquisa Web

```typescript
// src/agents/research.ts
import { Agent, tool } from '@openai/agents'
import { z } from 'zod'

export const researchAgent = new Agent({
  name: 'Pesquisa Web',
  model: 'gpt-4o',
  instructions: `
    Você é o Agente de Pesquisa Web do ORBIT.
    Dado um tema, você deve:
    1. Decompor em 3-5 subconsultas específicas
    2. Buscar em múltiplas fontes reais
    3. Coletar evidências com URL, trecho e relevância
    4. Detectar conflitos entre fontes
    5. Calcular cobertura estimada
    
    Mínimo obrigatório: 5 fontes distintas, 3 ângulos do tema.
    Output em JSON seguindo research_result schema.
  `,
  tools: [
    // web_search nativa do OpenAI SDK
    { type: 'web_search_preview' }
  ]
})
```

## Agente de Análise

```typescript
// src/agents/analysis.ts
import { Agent } from '@openai/agents'

export const analysisAgent = new Agent({
  name: 'Análise',
  model: 'gpt-4o',
  instructions: `
    Você é o Agente de Análise do ORBIT.
    Recebe as evidências coletadas e produz análise estruturada.
    
    Obrigatório no output:
    - convergencias: onde fontes concordam
    - divergencias: conflitos identificados
    - gaps: lacunas de informação
    - implicacoes: consequências práticas
    - swot: forcas, fraquezas, oportunidades, ameacas
    - diferenciação clara entre fato, inferência e opinião
    
    Score de confiança de 0-10 baseado na qualidade das evidências.
    Output em JSON seguindo analysis_result schema.
  `
})
```

## Worker de Fila

```typescript
// src/queue/worker.ts
import { supabase } from '../db/client'
import { orchestratorAgent } from '../agents/orchestrator'
import { run } from '@openai/agents'

async function processNextJob() {
  const { data: job } = await supabase.rpc('pop_intent_job_from_queue')
  if (!job) return
  
  try {
    // Atualizar status para running
    await supabase.from('jobs').update({ status: 'running' }).eq('id', job.id)
    
    // Buscar command original
    const { data: command } = await supabase
      .from('commands').select('*').eq('id', job.command_id).single()
    
    // Executar via Orquestrador
    const result = await run(orchestratorAgent, command.payload.text)
    
    // Salvar resultado
    await supabase.from('jobs').update({
      status: 'completed',
      result: result.finalOutput,
      updated_at: new Date().toISOString()
    }).eq('id', job.id)
    
  } catch (error) {
    await supabase.from('jobs').update({
      status: 'failed',
      result: { error: error.message },
      updated_at: new Date().toISOString()
    }).eq('id', job.id)
  }
}

// Poll a cada 5 segundos
setInterval(processNextJob, 5000)
```

## Webhook Telegram → Fastify

```typescript
// src/api/webhook.ts
import { FastifyInstance } from 'fastify'
import { supabase } from '../db/client'

export async function webhookRoutes(app: FastifyInstance) {
  app.post('/webhook/telegram', async (req, reply) => {
    const update = req.body as TelegramUpdate
    const message = update.message
    if (!message?.text) return reply.send({ ok: true })
    
    // Upsert user_profile
    const { data: user } = await supabase
      .from('user_profiles')
      .upsert({
        telegram_id: message.from.id,
        first_name: message.from.first_name,
        username: message.from.username,
        default_chat_id: message.chat.id
      }, { onConflict: 'telegram_id' })
      .select().single()
    
    // Criar command
    const { data: command } = await supabase
      .from('commands')
      .insert({
        user_id: user.id,
        payload: { text: message.text, source: 'telegram', chat_id: message.chat.id }
      }).select().single()
    
    // Criar job
    const { data: job } = await supabase
      .from('jobs')
      .insert({
        command_id: command.id,
        chat_id: message.chat.id,
        status: 'pending'
      }).select().single()
    
    // Enfileirar
    await supabase.rpc('push_intent_job', { p_job_id: job.id })
    
    // Resposta imediata ao usuário
    await sendTelegramMessage(message.chat.id, '🔄 Processando sua solicitação...')
    
    return reply.send({ ok: true })
  })
}
```

## Apresentação HTML Premium

```typescript
// Template básico para o Agente de Apresentação
const htmlTemplate = (dossier: DossierResult) => `<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${dossier.titulo}</title>
  <style>
    /* Estilos inline — sem CDN externo */
    :root { --primary: #6366f1; --bg: #0f0f1a; --text: #e2e8f0; }
    body { background: var(--bg); color: var(--text); font-family: system-ui; margin: 0; }
    .hero { padding: 4rem 2rem; background: linear-gradient(135deg, #1a1a3e, #0f0f1a); }
    .hero h1 { font-size: 2.5rem; color: #818cf8; }
    .section { padding: 2rem; max-width: 900px; margin: 0 auto; }
    .swot-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
    .swot-card { padding: 1.5rem; border-radius: 12px; }
    .forcas { background: #0d2b1a; border: 1px solid #22c55e; }
    .fraquezas { background: #2b0d0d; border: 1px solid #ef4444; }
    .oportunidades { background: #0d1f2b; border: 1px solid #3b82f6; }
    .ameacas { background: #2b1a0d; border: 1px solid #f59e0b; }
  </style>
</head>
<body>
  <div class="hero">
    <h1>${dossier.titulo}</h1>
    <p>${dossier.resumo_executivo?.substring(0, 200)}...</p>
  </div>
  <!-- seções dinâmicas aqui -->
</body>
</html>`
```
