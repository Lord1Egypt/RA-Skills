---
name: orca-control
version: 1.0.2
description: "Manage, orchestrate, inspect, and automate the Orca IDE and Multi-Agent Runtime Server — projects, worktrees, supervised workers, interactive terminals, decision gates, accounts, and automations."
author: "Rafa Martins <rafacpti@gmail.com>"
credits: "Rafa Martins (rafacpti@gmail.com)"
homepage: "https://github.com/rafacpti23/orca-control-skill"
license: "MIT"
platforms: [linux]
metadata:
  hermes:
    category: devops
    tags: [orca, devops, agents, orchestration, worktrees, terminals, automations, multi-agent]
    author: "Rafa Martins"
    email: "rafacpti@gmail.com"
---

# Orca Control & Multi-Agent Orchestrator

**Author**: Rafa Martins (`rafacpti@gmail.com`)  
**Repository**: [github.com/rafacpti23/orca-control-skill](https://github.com/rafacpti23/orca-control-skill)  
**License**: MIT  

Comprehensive management, operation, diagnostics, and orchestration toolkit for the **Orca IDE / Multi-Agent Runtime Server**.

---

## 🚀 First-Run & Interactive Onboarding Protocol / Protocolo de Onboarding Guiado

> 💡 **DIRETRIZ OBRIGATÓRIA PARA A IA / ASSISTENTE:**
> Quando o usuário executar ou instalar a skill do Orca pela primeira vez:
> 1. **Verifique se o ambiente local do Orca ou as credenciais do Habilis MCP estão acessíveis.**
> 2. **Se o serviço não responder ou faltarem parâmetros de conexão:**
>    - Inicie imediatamente um diálogo de Onboarding amigável e intuitivo.
>    - Apresente o checklist de requisitos e onde configurá-los.
> 3. **Execute um Health Check automático** (`bash scripts/orca-env-check.sh` ou tool `orca_get_system_status`) para validar o status dos agentes e workspaces.

### 📋 Checklist de Configuração / Setup Checklist

1. **`HABILIS_API_TOKEN` / MCP Bearer Token** *(Obrigatório para controle via MCP Gateway)*:
   - *O que é:* Token de autorização Habilis (`hab_live_...`).
   - *Onde obter:* Painel Habilis (`https://xvix.com.br`).

2. **Acesso Local ao Servidor Orca** *(Para modo CLI/Servidor)*:
   - *Diretório:* `/home/orca`
   - *Serviço:* `orca.service` / `habilis.service` na porta `:3080`.

### 💬 Exemplo de Mensagem de Boas-Vindas & Onboarding:

```text
👋 Olá! Bem-vindo ao Orca Multi-Agent Orchestrator!
Para começarmos a orquestrar seus agentes, projetos e worktrees com precisão, preciso de apenas uma confirmação rápida:

1️⃣ Você está usando o Orca via Gateway Habilis MCP (`hab_live_...`) ou diretamente neste servidor Linux?

👉 Para começar:
• Se via MCP, me passe seu token Habilis ou salve no seu `.env`.
• Se via servidor local, executarei um autodiagnóstico agora mesmo!
```

---

## 📚 Linked Resources & Scripts

* **Quick Cheatsheet:** `references/commands_cheatsheet.md`
* **GitHub Integration & Preflight:** `references/github_integration_and_preflight.md`
* **Thin-Skill Distribution Pattern:** `references/thin_skill_distribution_pattern.md`
* **Habilis SaaS & MCP Gateway:** `references/habilis_saas_mcp_gateway.md`
* **Health Check Script:** `scripts/orca-env-check.sh`
* **ClawHub Manifest:** `templates/clawhub.json`
* **Full Bilingual README:** `README.md`

## 🏗️ Architecture & Server Layout

* **System User:** `orca` (`uid: 993`, `gid: 984`)
* **Home Directory:** `/home/orca`
* **Configuration & SQLite DB:** `/home/orca/.config/orca/` (`orchestration.db`, sockets, runtime config)
* **Projects & Workspaces:** `/home/orca/orca/projects/` & `/home/orca/orca/workspaces/`
* **Service Manager:** `orca-serve.service` (systemd unit running port `6768`, WebSocket `ws://127.0.0.1:6768` or `wss://<your-domain>`)
* **Global CLI Entrypoint:** `/usr/local/bin/orca` (wraps Node execution of unpacked Orca CLI engine with `HOME=/home/orca`)

---

## 🚦 Diagnostics & Health Checks

### 1. Runtime & Graph State
```bash
# Check runtime readiness, PID, window status and graph state
orca status

# Check systemd service status
systemctl status orca-serve --no-pager

# Restart service cleanly if required
systemctl restart orca-serve
```

### 2. Resource & Memory Diagnostics
```bash
orca diagnostics memory
```

---

## 📁 Project & Worktree Management

### 1. Projects and Repositories
```bash
# List all registered repositories
orca repo list

# List durable projects known to Orca
orca project list

# Register an existing filesystem directory as an Orca repo
orca repo add /home/orca/orca/projects/<project_name>

# Make a project available on host by cloning a repository
orca project setup-clone <git_url>
```

### 2. Worktrees (Isolated Task Environments)
```bash
# List all active Orca-managed worktrees
orca worktree list

# Compact orchestration summary across worktrees
orca worktree ps

# Create a new isolated worktree based on a git branch
orca worktree create <branch_name>

# Inspect a specific worktree
orca worktree show <worktree_id>

# Remove a worktree safely
orca worktree rm <worktree_id>
```

---

## 🤖 Multi-Agent Orchestration & Task Lifecycle

### 1. Runs and Tasks
```bash
# List active and past orchestration Runs
orca orchestration run-list

# Create and bind a new orchestration Run
orca orchestration run-create --title "Backend Refactor Sprint"

# List orchestration tasks
orca orchestration task-list

# Filter tasks by status (pending | ready | dispatched | completed | failed | blocked)
orca orchestration task-list --status pending

# Create a new task with explicit specifications
orca orchestration task-create --title "Implement Auth Middleware" --spec "Use JWT with HMAC-SHA256..."

# Update task status
orca orchestration task-update --task <task_id> --status completed
```

### 2. Supervised Workers (Agents in Action)
```bash
# List active supervised worker accounting
orca orchestration worker-list

# Start a worker attached to a task
orca orchestration worker-start --task <task_id>

# Read output / logs from a supervised worker
orca orchestration worker-read --worker <worker_id>

# Release worker terminal when task completes
orca orchestration worker-release --worker <worker_id>

# Retain worker terminal for live debugging
orca orchestration worker-retain --worker <worker_id>
```

### 3. Decision Gates & Inter-Agent Inbox
```bash
# List decision gates awaiting human/coordinator resolution
orca orchestration gate-list

# Resolve a decision gate (approve or reject agent proposed change)
orca orchestration gate-resolve --gate <gate_id> --decision approve

# Inspect inbox for inter-agent communication
orca orchestration inbox

# Send direct message to a terminal / worker thread
orca orchestration reply --thread <thread_id> --content "Approved. Proceed with database migration."
```

---

## 💻 Live Terminals & Session Control

```bash
# List all live Orca-managed terminals with output previews
orca terminal list

# Create a new terminal session in the current worktree
orca terminal create

# Send commands, prompts, or text directly to a running terminal
orca terminal send --terminal <terminal_id> --text "npm test" --enter

# Read rendered screen output (exact TUI/ANSI frame as displayed to user/agent)
orca terminal read --terminal <terminal_id> --screen

# Read raw output stream with limit
orca terminal read --terminal <terminal_id> --limit 50

# Close a specific terminal pane
orca terminal close --terminal <terminal_id>
```
orca terminal close --terminal <terminal_id>
```
# Read raw output delta using cursor
orca terminal read --terminal <terminal_id> --cursor <last_cursor> --limit 100

# Focus/switch to a terminal tab in the Orca UI
orca terminal switch --terminal <terminal_id>

# Close a specific terminal pane/session
orca terminal close --terminal <terminal_id>
```

### 🔄 Interactive Subagent Orchestration Pattern
When controlling interactive AI agents (e.g. Antigravity CLI `agy`, Claude Code, Codex) running inside Orca:
1. **Locate Session:** Run `orca terminal list` to find the target terminal handle (`term_...`).
2. **Inspect Screen:** Run `orca terminal read --terminal <id> --screen` to inspect current agent state and prompts.
3. **Dispatch Instruction:** Run `orca terminal send --terminal <id> --text "<prompt>" --enter`.
4. **Poll Output:** Wait 2-5s and read with `orca terminal read --terminal <id> --screen` to observe actions (`● Bash`, `▸ Thought`, responses) in real time.

---

## 🔑 Agent Accounts & Credentials (Claude & Codex)

```bash
# List registered agent accounts
orca account list

# Add/Authenticate OpenAI Codex CLI account
orca account add --agent codex

# Add/Authenticate Anthropic Claude CLI account
orca account add --agent claude
```

---

## ⏰ Automations & Scheduled Workflows

```bash
# List registered automations
orca automations list

# Trigger an automation run manually
orca automations run <automation_id>

# View execution history for an automation
orca automations runs <automation_id>
```

---

## 🌐 Browser Automation & Mobile Emulators

Orca provides native computer use and viewport control tools:

```bash
# Capture DOM / accessibility tree snapshot
orca snapshot

# Navigate browser tab to URL
orca goto https://example.com

# Capture page screenshot
orca screenshot

# List connected mobile emulators
orca emulator list

# Send tap gesture to emulator
orca emulator tap --x 120 --y 340
```

---

## ⚠️ Pitfalls & Pro Tips

1. **User Permissions:** Ensure files created in `/home/orca/` belong to `orca:orca` (`chown -R orca:orca /home/orca/orca/projects/`).
2. **Sender Terminal Resolution:** When invoking `orca orchestration` outside of an interactive terminal session, pass `--from <terminal_handle>` (discoverable via `orca terminal list`).
3. **Daemon Safety:** Use `systemctl restart orca-serve` instead of killing Electron PIDs directly to prevent stale lockfiles.
