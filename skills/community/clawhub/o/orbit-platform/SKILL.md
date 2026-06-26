---
name: orbit-platform
description: >
  Arquiteto principal, engenheiro sênior e operador do ORBIT — plataforma de inteligência aplicada agentiva.
  Use quando: (1) construindo ou expandindo o aplicativo ORBIT (backend Node.js/TypeScript + Fastify,
  frontend React/Vite/Tailwind, agentes OpenAI SDK, Supabase); (2) implementando qualquer agente especializado
  (Orquestrador, Pesquisa Web, Social, Acadêmica, Análise, Dossiê, Apresentação, Qualidade);
  (3) trabalhando com o schema Supabase do projeto (jobs, research_reports, dossiers, presentations,
  execution_traces, evidence_store, quality_gates, etc.); (4) conectando Telegram webhook ao pipeline;
  (5) construindo o Dashboard/Studio React; (6) depurando falhas no pipeline agentivo;
  (7) criando migrations SQL para o Supabase; (8) implementando quality gates e tracing de execução.
  Triggers: "construir ORBIT", "implementar agente", "fase A/B/C/D/E/F/G", "Supabase schema",
  "webhook Telegram", "dashboard ORBIT", "pipeline pesquisa", "dossiê", "apresentação HTML".
---

# ORBIT Platform — Skill Operacional

## Contexto do Projeto

ORBIT é uma plataforma agentiva de inteligência aplicada.
Recebe comandos via Telegram ou Dashboard Web, aciona agentes especializados e entrega dossiês analíticos + apresentações HTML premium.

**Credenciais e stack:** Ver `/workspace/projeto/backend/.env` e `/workspace/projeto/decisoes/2026-03-24-credenciais-finais.md`

---

## Stack Técnica

| Camada | Tecnologia |
|--------|-----------|
| Backend | Node.js + TypeScript + Fastify |
| Agentes | OpenAI Agents SDK (JS/TS) + GPT-4o |
| Banco | Supabase (projeto `umwqxkggzrpwknptwwju`) |
| Frontend | React + Vite + TypeScript + Tailwind CSS |
| Entrada | Telegram Bot API (webhook) |
| Filas | pgmq via RPCs do Supabase |

---

## Arquitetura em Camadas

```
Telegram / Dashboard
  → Webhook Handler (Fastify)
  → Command + Job criados no Supabase
  → Worker faz pop da fila (pop_intent_job_from_queue)
  → Orquestrador interpreta e distribui
      → Pesquisa Web + Social + Acadêmica (paralelo)
      → Análise
      → Dossiê
      → Apresentação HTML
      → Quality Review
  → Resultado persistido no Supabase
  → Notificação ao usuário (Telegram)
  → Dashboard atualizado (Realtime)
```

---

## Agentes — Referência Rápida

| Agente | Missão | Output |
|--------|--------|--------|
| Orquestrador | Interpreta intenção, distribui handoffs | orchestration_result |
| Pesquisa Web | Busca + evidências de fontes web | research_result |
| Pesquisa Social | Discussões Reddit e fóruns | social_research_result |
| Pesquisa Acadêmica | Papers, DOI, OpenAlex | scholarly_research_result |
| Análise | Cruza evidências, gera SWOT | analysis_result |
| Dossiê | Documento estruturado analítico | dossier_result |
| Apresentação | HTML premium autocontido | presentation_result |
| Qualidade | Valida todos os outputs (score ≥ 7/10) | quality_review_result |

Para contratos de dados completos: ver `references/contratos-dados.md`
Para perfis detalhados dos agentes: ver `references/perfis-agentes.md`

---

## Schema Supabase — Tabelas Principais

O banco (`umwqxkggzrpwknptwwju`) já tem 26 tabelas criadas e limpas. Não criar novas — usar as existentes.

| Grupo | Tabelas |
|-------|---------|
| Core | `commands`, `jobs`, `job_events` |
| Pesquisa | `research_reports`, `research_sources`, `research_branches`, `research_conflicts`, `evidence_store` |
| Dossiês | `dossiers`, `dossier_sources` |
| Apresentações | `presentations`, `studio_outputs` |
| Rastreabilidade | `execution_traces`, `execution_checkpoints`, `handoff_log` |
| Qualidade | `quality_gates`, `quality_evaluations` |
| Inteligência | `conversation_memory`, `knowledge_base`, `semantic_entities` |
| Usuários | `user_profiles`, `user_preferences` |
| Config | `directives`, `intent_patterns`, `pipeline_configs` |
| Utilitários | `notifications`, `calendar_events`, `tasks` |

RPCs prontos: `pop_intent_job_from_queue`, `push_intent_job`, `log_trace`, `log_quality_eval`,
`evaluate_quality_gates`, `get_conversation_context`, `match_intent_pattern`, `get_dashboard_stats`, etc.

Para schema completo com campos: ver `references/schema-supabase.md`

---

## Plano de Implementação

| Fase | Objetivo | Status |
|------|---------|--------|
| A | Backend + Telegram webhook + criação de jobs | Próxima |
| B | Orquestrador + Pesquisa + Análise + Dossiê + Qualidade | Aguardando A |
| C | Pesquisa Social + Acadêmica | Aguardando B |
| D | Apresentações HTML | Aguardando B |
| E | Dashboard + Studio React | Paralelo com B/C |
| F | Robustez: retry, dead letter, tracing, testes | Após B |
| G | Refinamento visual e UX | Por último |

---

## Padrões de Código

### Supabase Client (backend)
```typescript
import { createClient } from '@supabase/supabase-js'
const supabase = createClient(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_KEY!
)
```

### Criar job no Supabase
```typescript
const { data: job } = await supabase
  .from('jobs')
  .insert({ command_id: cmdId, chat_id: chatId, status: 'pending' })
  .select().single()
```

### Pop da fila
```typescript
const { data } = await supabase.rpc('pop_intent_job_from_queue')
```

### Log de trace
```typescript
await supabase.rpc('log_trace', {
  p_job_id: jobId, p_agent: 'orchestrator', p_version: '1.0.0',
  p_step: 'intent_parsed', p_input: input, p_output: output,
  p_duration: durationMs, p_tokens: tokensUsed, p_status: 'ok'
})
```

### Agente OpenAI SDK
```typescript
import { Agent, run } from '@openai/agents'
const agent = new Agent({
  name: 'Orquestrador',
  model: 'gpt-4o',
  instructions: '...',
  tools: [...],
  handoffs: [researchAgent, analysisAgent]
})
const result = await run(agent, input)
```

Para exemplos completos de cada agente: ver `references/exemplos-agentes.md`

---

## Regras de Execução

1. **Nunca codifique sem entender o fluxo** — verifique os contratos e o schema
2. **Use sempre a service_role key** do projeto `umwqxkggzrpwknptwwju`
3. **Respeite as foreign keys** ao deletar dados (filhos antes dos pais)
4. **Quality gate obrigatório** antes de qualquer entrega — score mínimo 7/10
5. **Logs estruturados** via `log_trace` RPC — nunca console.log em produção
6. **HTML das apresentações deve ser autocontido** — sem CDN externo
7. **Idioma padrão:** Português do Brasil em toda comunicação com o usuário
8. **Nunca expor credenciais** no código — sempre via variáveis de ambiente

---

## Quality Gates

| Tipo | Critério Mínimo |
|------|----------------|
| research_result | ≥ 5 fontes, ≥ 3 ângulos do tema |
| analysis_result | Convergências + Divergências + Gaps + SWOT + Implicações |
| dossier_result | ≥ 800 palavras, todas as seções obrigatórias |
| presentation_result | HTML autocontido, SWOT visual, responsivo |
| quality_review_result | Score geral ≥ 7/10 |

---

## Referências Adicionais

- Contratos de dados JSON: `references/contratos-dados.md`
- Perfis completos dos agentes: `references/perfis-agentes.md`
- Schema Supabase completo: `references/schema-supabase.md`
- Exemplos de código por agente: `references/exemplos-agentes.md`
- Metodologia de trabalho: `/workspace/projeto/metodologia/METODOLOGIA.md`
- Workflows reutilizáveis: `/workspace/projeto/workflows/WORKFLOWS.md`
- Plano mestre: `/workspace/projeto/PLANO-MESTRE.md`
