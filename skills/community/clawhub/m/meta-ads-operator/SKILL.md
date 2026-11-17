---
name: meta-ads-operator
description: Planeja, cria e edita campanhas no Meta Ads com racional documentado e padrao operacional, usando qualquer MCP de Meta Ads conectado ao agente.
metadata: {"portable":"openclaw-ready","requires_capability":"meta-ads-mcp","mcp_agnostic":true,"scope":"operator"}
user-invocable: true
---

# Purpose
Esta skill transforma briefing em arquitetura operacional e executa build seguro em Meta Ads.

# Use this skill when
- for necessario criar campanha, conjunto, anuncio ou criativo
- o usuario pedir planejamento estrutural de campanha
- for preciso editar ativos de forma controlada
- a tarefa exigir checklist de publicacao ou manutencao

# Do not use this skill when
- a prioridade for somente diagnosticar performance
- a tarefa nao envolver Meta Ads, ou nao houver nenhum MCP de Meta Ads conectado

# Operating principles
- construa com simplicidade suficiente para leitura e escala
- toda criacao nasce em `PAUSED`
- documente o racional antes de publicar
- preserve naming, UTM e tracking como parte da infraestrutura
- nao force complexidade quando uma estrutura simples resolve

# Required capabilities (mapeie para o seu MCP de Meta Ads)
Esta skill e agnostica de servidor. Faca tool discovery e mapeie cada capacidade
abaixo para a tool correspondente do MCP conectado. Os nomes entre parenteses sao
apenas exemplos comuns de nomenclatura.
- Listar contas e campanhas (ex.: `get_ad_accounts`, `get_campaigns`)
- Criar / atualizar campanha (ex.: `create_campaign`, `update_campaign`)
- Pausar / retomar campanha (ex.: `pause_campaign`, `resume_campaign`)
- Listar / criar conjunto de anuncio (ex.: `list_ad_sets`, `list_campaign_ad_sets`, `create_ad_set`, `create_ad_set_enhanced`)
- Listar / criar criativo, com validacao quando disponivel (ex.: `list_ad_creatives`, `create_ad_creative`, `validate_creative_enhanced`)
- Listar / criar / atualizar / pausar anuncio (ex.: `list_ads`, `create_ad`, `update_ad`, `pause_ad`)
- Diagnostico de prontidao, setup e criativo (ex.: `diagnose_campaign_readiness`, `check_account_setup`, `troubleshoot_creative_issues`)

Se uma capacidade nao existir no MCP conectado, trate-a como fora de escopo e sinalize.

# Workflow
1. Identificar o MCP de Meta Ads conectado e mapear capacidades via tool discovery.
2. Ler o briefing e traduzir o objetivo de negocio.
3. Escolher arquitetura: campanha, conjuntos, anuncios e criativos.
4. Definir naming e UTM.
5. Validar readiness, conta e tracking.
6. Construir em `PAUSED`.
7. Registrar rationale e checklist final.

# References
- {baseDir}/references/campaign-build-playbooks.md
- {baseDir}/references/adset-structures.md
- {baseDir}/references/creative-assembly.md
- {baseDir}/references/launch-checklist.md
- {baseDir}/references/editing-guidelines.md
- {baseDir}/references/official-meta-build-guidelines.md
