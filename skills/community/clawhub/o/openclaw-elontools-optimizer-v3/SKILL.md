---
name: openclaw-elontools-optimizer-v3
version: "3.0.0"
description: >
  Otimizações SEGURAS para OpenClaw — apenas configurações que economizam tokens
  sem NENHUM risco de perda de contexto ou loops infinitos.

  QUANDO USAR:
  - Setup inicial de nova instância OpenClaw
  - Reduzir custo de heartbeats (usa modelo barato)
  - Desabilitar plugins/canais não usados
  - Limpar sessões antigas automaticamente

  O QUE FAZ (4 otimizações seguras):
  1. Heartbeat Econômico — usa Haiku para heartbeats (não gasta Opus/Sonnet)
  2. Plugin Cleanup — desabilita plugins de canais não configurados
  3. Sub-agent Auto-Archive — limpa sessões de sub-agentes após 30min
  4. Session Cleanup — remove sessões inativas após 7 dias

  O QUE NÃO FAZ (PROIBIDO — causa loops):
  ❌ NÃO mexe em contextPruning (NUNCA!)
  ❌ NÃO mexe em compaction (NUNCA!)
  ❌ NÃO mexe em bootstrapMaxChars (NUNCA!)
  ❌ NÃO mexe em softTrim/hardClear (NUNCA!)
  ❌ NÃO altera web_fetch maxChars
  ❌ NÃO altera reserveTokensFloor ou maxHistoryShare

  LIÇÃO APRENDIDA (2026-03-26):
  A v1/v2 desta skill causou loop infinito de tool_calls em produção.
  Rublo consumiu 44.6M input tokens em 1 dia (1398 requests) por causa
  de contextPruning agressivo + bootstrapMaxChars que cortava instruções.
  NUNCA MAIS mexer nessas configs.
---

# OpenClaw ElonTools Optimizer v3 — Safe Edition

Apenas otimizações **comprovadamente seguras** que economizam tokens sem risco.

## ⚠️ AVISO IMPORTANTE

As versões 1.0 e 2.0 desta skill foram **removidas do ClawHub** porque causavam
loops infinitos de tool_calls em produção. Esta v3 contém APENAS otimizações seguras.

**Se você tem a v1 ou v2 instalada:** REMOVA IMEDIATAMENTE e aplique factory defaults:
```
gateway(action="config.patch", raw='{"agents":{"defaults":{"contextPruning":{"mode":"off"},"compaction":{"mode":"safeguard"}}}')
```

## O Que Faz

| # | Otimização | Economia | Risco |
|---|-----------|----------|-------|
| 1 | Heartbeat com Haiku | ~10x mais barato por heartbeat | Zero |
| 2 | Desabilitar plugins ociosos | Menos memória, startup rápido | Zero* |
| 3 | Sub-agent auto-archive | Limpa sessões órfãs | Zero |
| 4 | Session cleanup (7 dias) | Menos disco | Zero |

*\* Se você usa WhatsApp/Discord/Slack/etc, NÃO aplique o item de plugins.*

## Aplicação

```
# Ler o preset
read("references/preset-safe.json")

# Aplicar
gateway(action="config.patch", raw=<conteúdo do preset>)
```

## Verificação Pós-Aplicação

1. ✅ `gateway(action="config.get")` — verificar que NÃO tem contextPruning alterado
2. ✅ Heartbeats rodando com Haiku (checar via /status)
3. ✅ Plugins que você USA continuam habilitados
4. ✅ Sessões antigas sendo limpas

## O Que NUNCA Deve Ser Alterado

| Config | Por quê NÃO mexer |
|--------|-------------------|
| `contextPruning` | Causa loop infinito de tool_calls |
| `compaction.reserveTokensFloor` | Compactação prematura perde contexto |
| `compaction.maxHistoryShare` | Joga fora histórico demais |
| `bootstrapMaxChars` | Corta system prompt = agente perde instruções |
| `hardClear` | Remove tool results = agente re-executa tools |
| `softTrim` | Trunca resultados = agente não entende output |

Deixe o OpenClaw usar seus **factory defaults** para essas configs. Eles são testados e seguros.
