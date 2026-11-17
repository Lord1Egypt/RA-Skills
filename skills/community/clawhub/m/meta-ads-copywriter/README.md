# ✍️ Meta Ads High-Conversion Copywriter & Creative Engine
### *Redação Direta & Criação de Criativos de Alta Conversão para Meta Ads via Habilis MCP*

<p align="center">
  <img src="assets/logo.png" alt="Meta Ads Copywriter Logo" width="120" height="120" />
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
**Meta Ads Copywriter** empowers AI agents with battle-tested direct response copywriting frameworks (AIDA, PAS, Hook + Story + Offer) and automated UTM tracking. It connects to the **Habilis MCP Gateway** (`https://xvix.com.br/api/mcp`) to autonomously generate, format, and publish high-converting ad variations to Meta Ads.

### 🚀 Quick Onboarding & First-Time Setup
1. **Get your Habilis MCP Token**:
   - Access the developer portal at [https://xvix.com.br](https://xvix.com.br) to generate your access token.
2. **Configure Environment Variables**:
   ```bash
   export HABILIS_API_KEY="hab_live_..."
   export META_ACCESS_TOKEN="EAA..."
   export META_AD_ACCOUNT_ID="act_..."
   ```
3. **Configure Hermes / OpenClaw / Claude Desktop (`config.yaml`)**:
   ```yaml
   mcp_servers:
     habilis:
       url: "https://xvix.com.br/api/mcp"
       headers:
         Authorization: "Bearer ${HABILIS_API_KEY}"
   ```
4. **Usage Example**:
   ```bash
   hermes run "meta-ads-copywriter: generate 3 high-converting AIDA copy variations for B2B SaaS"
   ```

---

## 🇧🇷 Português

### Visão Geral
O **Meta Ads Copywriter** fornece aos agentes de IA frameworks comprovados de resposta direta (AIDA, PAS, Gancho + Oferta) e parametrização de UTMs. Conectado ao **Habilis MCP Gateway** (`https://xvix.com.br/api/mcp`), gera variações persuasivas e publica criativos diretamente na conta de anúncios.

### 🚀 Onboarding Rápido & Primeiro Uso
1. **Obtenha seu Token Habilis MCP**:
   - Acesse o portal de desenvolvedores em [https://xvix.com.br](https://xvix.com.br) para gerar seu token.
2. **Configure as Variáveis de Ambiente**:
   ```bash
   export HABILIS_API_KEY="hab_live_..."
   export META_ACCESS_TOKEN="EAA..."
   export META_AD_ACCOUNT_ID="act_..."
   ```
3. **Conecte o MCP no Hermes / OpenClaw / Claude Desktop (`config.yaml`)**:
   ```yaml
   mcp_servers:
     habilis:
       url: "https://xvix.com.br/api/mcp"
       headers:
         Authorization: "Bearer ${HABILIS_API_KEY}"
   ```
4. **Exemplo de Uso**:
   ```bash
   hermes run "meta-ads-copywriter: criar 3 variações de copy AIDA para software B2B"
   ```

---

## 📦 Installation / Instalação

```bash
hermes skills install meta-ads-copywriter
# or via clawhub
clawhub install meta-ads-copywriter
```
