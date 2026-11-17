# Multi-Agent Safe-Cooperation (Single Device)

A single-device multi-Agent task chain collaboration methodology based on MGC, achieving zero-exposure security collaboration for sensitive resources.

---

## What is MGC Safe-Cooperation?

When deploying multiple Agents on a single device to collaborate on tasks, traditional approaches have issues:

- All Agents share environment, keys easily leaked
- Script content exposed to all Agents
- Lack of task collaboration methodology

MGC Safe-Cooperation solves these problems:

1. **Sensitive Resource Hosting**: Keys, scripts, data stored in MGC, agents execute without exposure
2. **Task Chain Orchestration**: Guide Master Agent to decompose tasks and assign to sub-Agents
3. **Zero-Exposure Execution**: Executor Agent only calls mgc_run, executed by MGC Blackbox, never touches keys

---

## Role Definitions

| Role | Responsibility | Tools |
|------|----------------|-------|
| User | Store keys/scripts, issue commands | WebUI / mgc_open_webui |
| Master Agent | Task decomposition, orchestration | mgc_list, mgc_run |
| Script Agent | Write scripts, store in MGC | mgc_save, mgc_get, mgc_list |
| Executor Agent | Complete non-sensitive tasks | mgc_run, mgc_list |

> Note: Sensitive operations (mgc_get to retrieve plaintext) require user authorization.

---

## Quick Start

### 1. Install MGC

```bash
pip install mgc-blackbox
```

### 2. Start MGC

```bash
mgc
```

- WebUI: http://127.0.0.1:57218
- API: http://127.0.0.1:57219

### 3. Configure MCP (Enable AI to Call MGC)

Add to AI client (e.g., TRAE) MCP configuration:

```json
{
  "mcpServers": {
    "mgc-blackbox": {
      "command": "mgc",
      "args": ["--mcp"]
    }
  }
}
```

### 4. Store Sensitive Resources

Store via WebUI:
- API Keys
- Database Credentials
- Business Scripts

### 5. Configure Agent Prompts

Load prompt templates from `prompts/` directory:
- `master_agent.md` → Master Agent
- `script_agent.md` → Script Agent
- `executor_agent.md` → Executor Agent

### 6. Start Collaboration

After user issues a command, the Master Agent automatically decomposes the task chain and coordinates sub-Agents to complete.

---

## Collaboration Flow Diagram

```
User ──Store Keys/Scripts (WebUI)──> MGC
                │
                ▼
User ──Issue Command──> Master Agent
                │
                ├──Decompose Task Chain
                │
                ▼
        ┌───────┴───────┐
        ▼               ▼
   Script Agent      Executor Agent
   (Write Scripts)  (Execute Tasks)
        │               │
        ▼               ▼
   mgc_save         mgc_run
        │               │
        └───────┬───────┘
                ▼
           MGC Execution
        (Return Results)
```

---

## Prompt Template Description

### Master Agent (master_agent.md)

- Task decomposition methods
- MGC call timing
- Sub-task allocation rules

### Script Agent (script_agent.md)

- mgc_save usage
- Script naming conventions
- Script location reporting format

### Executor Agent (executor_agent.md)

- mgc_run usage
- Prohibited behaviors
- Result handling specifications

---

## FAQ

**Q: Can sub-Agents bypass MGC?**
A: Prompt constraints cannot completely prevent; ensure sub-Agents cannot access local script files, or use mgc_seal to seal scripts. Sealed scripts can only run inside MGC and cannot be decrypted or viewed.

**Q: How to isolate scripts for different tasks?**
A: Use info_owner naming to distinguish, e.g., `TaskA_QueryScript`, `TaskB_PublishScript`.

**Q: How does Master Agent know what scripts are available?**
A: Use mgc_list to view, or report by Script Agent. For highly reusable scripts, update to "cooperation_best_practice.md" for management and to save tokens.

**Q: How to have AI open WebUI?**
A: Use `mgc_open_webui()` tool, AI will automatically open browser to access MGC WebUI.

---

## MGC Tool Reference

| Tool | Purpose |
|------|---------|
| mgc_save | Store scripts |
| mgc_run | Execute scripts |
| mgc_list | View script list |
| mgc_seal | Seal scripts (executable) |
| mgc_open_webui | Open WebUI |

---

## Related Resources

- [MGC Core Repository](https://github.com/zkeviny/MGC-Blackbox)
- [MGC Installation Guide](#)
- Feedback: mirgincipher@outlook.com
