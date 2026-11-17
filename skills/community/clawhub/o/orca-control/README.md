# 🐋 Orca Multi-Agent Orchestrator & IDE Runtime Engine
### *Orquestração de Agentes Autônomos, Supervisão de Processos & Runtime no Orca IDE*

<p align="center">
  <img src="assets/logo.png" alt="Orca Logo" width="120" height="120" />
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
**Orca Control** provides comprehensive management, health monitoring, and automation for the **Orca IDE & Multi-Agent Server**. It enables agents to inspect workspace sessions, monitor system services, manage ports and processes, and integrate with the Habilis MCP Gateway.

### 🚀 Quick Onboarding & First-Time Setup
1. **Get your Habilis MCP Token**:
   - Access the developer portal at [https://xvix.com.br](https://xvix.com.br) to generate your access token.
2. **Configure Environment Variables**:
   ```bash
   export HABILIS_API_KEY="hab_live_..."
   export ORCA_WORKSPACE_DIR="/home/orca"
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
   hermes run "orca_get_status()"
   ```

### Key Capabilities
- 🔍 **Workspace Health Checks**: Instant diagnostic of active IDE sessions, disk usage, and processes.
- ⚙️ **Service Lifecycle Supervision**: Start, stop, restart, and inspect daemons in real time.
- 🌐 **MCP Gateway Integration**: Access multi-agent tools securely via JSON-RPC / SSE.
- 🔒 **Zero-Storage Security**: Server management tokens stay exclusively in your local environment.

---

## 🇧🇷 Português

### Visão Geral
O **Orca Control** oferece controle total, diagnóstico de integridade e automação para o **Orca IDE & Multi-Agent Runtime**. Permite inspecionar workspaces ativos, monitorar daemons de sistema, gerenciar portas e processos, e orquestrar ferramentas via Habilis MCP Gateway.

### 🚀 Onboarding Rápido & Primeiro Uso
1. **Obtenha seu Token Habilis MCP**:
   - Acesse o portal de desenvolvedores em [https://xvix.com.br](https://xvix.com.br) para gerar seu token de acesso.
2. **Configure as Variáveis de Ambiente**:
   ```bash
   export HABILIS_API_KEY="hab_live_..."
   export ORCA_WORKSPACE_DIR="/home/orca"
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
   hermes run "orca_get_status()"
   ```

### Principais Recursos
- 🔍 **Diagnóstico de Workspace**: Verificação instantânea de uso de recursos, sessões e portas ativas.
- ⚙️ **Supervisão de Serviços**: Reinício e inspeção de logs de daemons (`systemd`).
- 🌐 **Integração MCP Gateway**: Comunicação padronizada para enxames de agentes autônomos.
- 🔒 **Privacidade Zero-Storage**: Credenciais de servidor permanecem no ambiente local do usuário.

---

## 📦 Installation / Instalação

```bash
hermes skills install orca-control
# or via clawhub
clawhub install orca-control
```
