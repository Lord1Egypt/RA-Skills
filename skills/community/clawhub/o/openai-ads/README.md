# 🤖 OpenAI Ads & ChatGPT Marketing Manager
### *Gestão Autônoma de Anúncios Conversacionais para OpenAI Ads & ChatGPT via Habilis MCP*

<p align="center">
  <img src="assets/logo.svg" alt="OpenAI Ads Logo" width="120" height="120" />
</p>

<p align="center">
  <a href="https://clawhub.ai"><img src="https://img.shields.io/badge/ClawHub-Skill-blue.svg" alt="ClawHub Skill" /></a>
  <a href="https://xvix.com.br"><img src="https://img.shields.io/badge/Habilis-MCP%20Gateway-purple.svg" alt="Habilis MCP Gateway" /></a>
  <img src="https://img.shields.io/badge/Security-Zero_Storage_Stateless-blueviolet.svg" alt="Zero Storage" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License MIT" />
</p>

---

## 🇺🇸 English

### Overview
**OpenAI Ads Manager** connects AI agents to the **Habilis MCP Gateway** (`https://xvix.com.br/api/mcp`) to autonomously orchestrate ChatGPT Ads. It handles conversational context hints, interactive `chat_cards` synthesis, and real-time performance analytics through standardized MCP tools.

### 🚀 Quick Onboarding & First-Time Setup
1. **Get your Habilis MCP Token**:
   - Access the developer portal at [https://xvix.com.br](https://xvix.com.br) to generate your access token.
2. **Configure Environment Variables**:
   ```bash
   export HABILIS_API_KEY="hab_live_..."
   export OPENAI_ADS_API_KEY="key_live_..."
   export OPENAI_ADS_ACCOUNT_ID="act_1234567890"
   ```
3. **Configure Hermes / OpenClaw (`config.yaml`)**:
   ```yaml
   mcp_servers:
     habilis:
       url: "https://xvix.com.br/api/mcp"
       headers:
         Authorization: "Bearer ${HABILIS_API_KEY}"
   ```
4. **Run Doctor Diagnostic**:
   ```bash
   hermes run "mcp__openai_ads__get_account()"
   ```

### Key Capabilities
- 💬 **Conversational Context Targeting**: Matches user intent with targeted conversational triggers.
- 🗂️ **Interactive Chat Cards**: Deploys rich interactive product cards inside ChatGPT conversations.
- 📈 **Performance Insights**: Real-time impressions, CTR, conversion rate, and CPA tracking.
- 🔒 **Zero-Storage Stateless Architecture**: Credentials remain exclusively on your local machine.

---

## 🇧🇷 Português

### Visão Geral
O **OpenAI Ads Manager** conecta agentes de IA ao **Habilis MCP Gateway** (`https://xvix.com.br/api/mcp`) para orquestrar campanhas no ecossistema ChatGPT. Gerencia segmentação contextual, criação de cartões interativos (`chat_cards`) e análise de conversões via ferramentas MCP seguras.

### 🚀 Onboarding Rápido & Primeiro Uso
1. **Obtenha seu Token Habilis MCP**:
   - Acesse o portal de desenvolvedores em [https://xvix.com.br](https://xvix.com.br) para gerar seu token de acesso.
2. **Configure as Variáveis de Ambiente**:
   ```bash
   export HABILIS_API_KEY="hab_live_..."
   export OPENAI_ADS_API_KEY="key_live_..."
   export OPENAI_ADS_ACCOUNT_ID="act_1234567890"
   ```
3. **Conecte o MCP no Hermes / OpenClaw (`config.yaml`)**:
   ```yaml
   mcp_servers:
     habilis:
       url: "https://xvix.com.br/api/mcp"
       headers:
         Authorization: "Bearer ${HABILIS_API_KEY}"
   ```
4. **Execute o Teste de Conexão**:
   ```bash
   hermes run "mcp__openai_ads__get_account()"
   ```

### Principais Recursos
- 💬 **Segmentação Contextual**: Alinhamento de ofertas com o fluxo da conversa no ChatGPT.
- 🗂️ **Chat Cards Interativos**: Banners interativos e botões de conversão direta.
- 📈 **Telemetria de Campanhas**: Métricas de CPA, CTR e ROAS em tempo real.
- 🔒 **Arquitetura Zero-Storage**: Proteção total das credenciais no ambiente local do usuário.

---

## 📦 Installation / Instalação

```bash
hermes skills install openai-ads
# or via clawhub
clawhub install openai-ads
```
