# PI-CODING-SPECIALIST SKILL

**Name:** pi-coding-specialist  
**Description:** Orchestrate Pi Agent as coding specialist for complex tasks (>5 files)  
**Trigger:** Coding tasks requiring multi-file changes, refactoring, or complex implementations  

---

## 🎯 MISIÓN

Integrar Pi Agent como sub-agent preferido para tareas de coding complejas desde OpenClaw.

---

## 🔧 CONFIGURACIÓN

### Model Routing Integration

```json
{
  "subagents": {
    "enabled": true,
    "coding_specialist": "pi",
    "backend": "pi-subagents"
  }
}
```

### Trigger Conditions

Usar Pi cuando:
- ✅ Coding task >5 archivos
- ✅ Refactoring complejo
- ✅ Nueva feature multi-file
- ✅ Code review profundo
- ✅ Debugging sistémico

NO usar Pi cuando:
- ❌ One-liner fixes
- ❌ Simple file edits
- ❌ Lectura de código

---

## 🛠️ COMANDO DE SPAWN

```bash
# Spawn Pi como sub-agent
openclaw sessions spawn \
  --name="pi-coding-task" \
  --model="qwen3.5:397b-cloud" \
  --workdir="/path/to/project" \
  --prompt="Pi, implementa [task description]. Usa pi CLI para coding."
```

### Pi CLI Direct Execution

```bash
# Install (si no existe)
npm install -g @mariozechner/pi-coding-agent

# Execute con PTY
bash pty:true workdir:/path/to/project command:"pi 'Task description'"

# Background mode para tareas largas
bash pty:true workdir:/path/to/project background:true command:"pi 'Complex implementation'"
```

---

## 📊 HANDOFF PATTERNS

### C-Level → Pi Handoff

1. **Nexus/Forge detectan tarea compleja** (>5 files)
2. **Spawn Pi sub-agent** con contexto específico
3. **Monitor progreso** via `process:log`
4. **Receive results** push-based
5. **Integrate changes** al proyecto principal

### Example Workflow

```bash
# 1. Detectar necesidad
if files_changed > 5; then
  # 2. Spawn Pi
  bash pty:true workdir:$PROJECT background:true command:"pi '$TASK'"
  
  # 3. Monitor
  process action:log sessionId:$ID
  
  # 4. Complete
  # Pi auto-notifies on completion
fi
```

---

## 🔗 INTEGRATION POINTS

### Con C-Levels

| Agent | Handoff Scenario |
|-------|------------------|
| **Nexus (CTO)** | Architecture implementations |
| **Forge (CDO)** | Feature development |
| **Spark (CAO)** | Complex automations |
| **Hybrid Architect** | System integrations |

### Con Model Routing

- **Simple tasks:** qwen3.5:9b (inline)
- **Medium tasks:** hermes3:8b (inline)
- **Complex coding:** Pi Agent (sub-agent)
- **Complex strategy:** qwen3.5:397b-cloud (inline)

---

## 📁 FILES

- `~/.openclaw/skills/pi-coding-specialist/SKILL.md` (este archivo)
- `~/.openclaw/agents/*/config.json` (subagents.enabled: true)
- `/opt/homebrew/bin/pi` (Pi CLI binary)

---

## ✅ VERIFICATION

```bash
# Check Pi installed
which pi

# Test Pi execution
pi -p "Hello world"

# Verify subagent config
cat ~/.openclaw/agents/nexus/agent/config.json | grep -A3 subagents
```

---

**Version:** 1.0  
**Status:** ACTIVE  
**Created:** 2026-03-31
