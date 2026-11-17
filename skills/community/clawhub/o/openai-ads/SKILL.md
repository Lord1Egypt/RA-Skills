---
name: openai-ads
version: 1.2.0
description: "Autonomous AI Marketing & Ads Manager for OpenAI Ads via Habilis MCP Gateway (https://xvix.com.br). End-to-end campaign orchestration, chat_cards synthesis, catalog feeds, and performance telemetry."
credits: Rafa Martins (xvix.com.br | rafacpti@gmail.com)
tags: [openai-ads, chatgpt-ads, marketing, advertising, traffic-management, habilis, mcp]
---

# OpenAI Ads & ChatGPT Marketing Manager (MCP Interface)

Bilingual Operational Playbook (English & Português) for autonomous media buying, campaign orchestration, and interactive conversational cards for OpenAI Ads & ChatGPT using the **Habilis MCP Gateway** (`https://xvix.com.br/api/mcp`).

---

## 🚀 Onboarding & Setup Rápido (Primeiro Uso)

Ao executar a skill pela primeira vez sem o servidor MCP configurado:
1. Exibir checklist visual de status `[OK]` / `[PENDENTE]`.
2. **Obtenha seu Token de Acesso MCP**:
   - Acesse o portal de desenvolvedores em [https://xvix.com.br](https://xvix.com.br) para gerar sua chave `HABILIS_API_KEY`.
3. **Configure o Servidor MCP no Hermes / OpenClaw / Claude Desktop (`config.yaml`)**:
   ```yaml
   mcp_servers:
     habilis:
       url: "https://xvix.com.br/api/mcp"
       headers:
         Authorization: "Bearer ${HABILIS_API_KEY}"
   ```
4. **Variáveis de Ambiente Locais (Zero-Storage)**:
   ```bash
   export HABILIS_API_KEY="hab_live_..."
   export OPENAI_ADS_API_KEY="key_live_..."
   export OPENAI_ADS_ACCOUNT_ID="act_1234567890"
   ```
5. **Autodiagnóstico (Doctor Check)**:
   Invoque a ferramenta MCP `mcp__openai_ads__get_account` para validar a conectividade com o gateway.

---

## 🛠️ MCP Tools Disponíveis via Habilis Gateway

Todas as operações são executadas de forma segura e stateless através do Habilis MCP Gateway:

### 1. `mcp__openai_ads__get_account`
Obtém o status da conta, saldo disponível, moeda e permissões ativas.
- **Parâmetros**: `account_id` (opcional).

### 2. `mcp__openai_ads__list_campaigns`
Lista todas as campanhas ativas, pausadas e em rascunho com métricas agregadas.
- **Parâmetros**: `status` (`active`, `paused`, `all`), `limit`.

### 3. `mcp__openai_ads__create_campaign`
Cria uma nova campanha de anúncios conversacionais no ChatGPT.
- **Parâmetros**:
  - `name`: Nome padronizado da campanha.
  - `daily_budget_micros`: Orçamento diário em micros (ex: 5000000 para $5.00).
  - `status`: `active` ou `paused`.
  - `targeting_hints`: Array de tópicos contextuais e palavras-chave de intenção.

### 4. `mcp__openai_ads__create_chat_card`
Gera e associa um cartão interativo (`chat_card`) clicável à campanha.
- **Parâmetros**:
  - `campaign_id`: ID da campanha.
  - `headline`: Título do cartão (máx 60 caracteres).
  - `body`: Texto descritivo e proposta de valor.
  - `cta_text`: Texto do botão (ex: "Experimentar Agora", "Saiba Mais").
  - `destination_url`: Link de destino seguro (HTTPS).
  - `image_url`: URL do asset visual de alta resolução.

### 5. `mcp__openai_ads__get_insights`
Coleta telemetria de desempenho, impressões, CTR, conversões e CPA.
- **Parâmetros**:
  - `campaign_id`: ID da campanha ou conta.
  - `date_preset`: `today`, `last_7d`, `last_30d`.

---

## 🧠 Fluxos de Decisão & Melhores Práticas

### Diretrizes de Copy para ChatGPT Ads
1. **Contexto Nativo**: O texto deve parecer uma recomendação relevante e útil para a conversa, sem interrupções bruscas.
2. **Clareza de Proposta**: Apresente a solução de forma direta com call-to-action acionável.
3. **Guardrails de Orçamento**: Pause campanhas quando o CPA médio exceder o limiar de rentabilidade configurado.
