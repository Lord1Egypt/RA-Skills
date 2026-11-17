---
spec: usk/3.0
id: mgc_task_chain_meta_skill_en
version: 1.1.0
name: Multi-Agent Safe-Cooperation (Single Device)
description: A single-device multi-Agent task chain collaboration methodology based on MGC. Through Master Agent orchestration, Script Agent scripting, and Executor Agent execution, achieves zero-exposure security collaboration for sensitive resources. Adapted to MGC 1.4.10.
author: MirginCipher Team
license: MIT
tags: mgc, multi-agent, task-chain, safe-cooperation, zero-exposure, local-sandbox, mgc_find
platform_compatibility: windows, macos, linux
changelog:
  - version: 1.1.0
    changes:
      - Upgraded to adapt to MGC 1.4.10
      - Fixed mgc_run ext02 signature: must be a JSON array string
      - Added mgc_find fuzzy search tool
      - Documented ext02 auto-parsing (1.4.10)
      - Documented that mgc_run returns only pid+status (no stdout)
      - Added 1.4.9 sandbox mode note
      - Updated MGC main skill doc reference to WebUI 'MGC Skills' button
  - version: 1.0.0
    changes:
      - Initial release with three prompt templates
---

# Multi-Agent Safe-Cooperation (Single Device)

---

## One-Line Description

A single-device multi-Agent task chain collaboration methodology based on MGC. Through Master Agent orchestration, Script Agent scripting, and Executor Agent execution, achieves zero-exposure security collaboration for sensitive resources.

---

## Problem Solved

| Pain Point | Solution |
|------------|----------|
| Multiple Agents sharing environment, keys easily leaked | Store keys in MGC, agents execute without exposure |
| Script content exposed to all Agents | Store scripts in MGC, zero exposure during execution |
| Lack of task collaboration methodology | Master Agent task chain orchestration template |
| Sub-Agent unauthorized access to sensitive resources | Executor Agent prompt constraints |

---

## Core Concepts

### MGC's Role in Collaboration

MGC is the **local sensitive resource hosting and execution layer** ([skill_spec.md](file:///D:/MirginCipher/mgc/docs/skill_spec.md) §1):

1. **User** stores keys and scripts via WebUI (browser or `mgc_open_webui`)
2. **Script Agent** writes scripts and stores them in MGC via `mgc_save` (MGC 1.4.10 auto-parses `argparse` defaults into `ext02`)
3. **Master Agent** orchestrates the task chain, specifies call timing; can execute directly when sub-Agents fail or with user authorization
4. **Executor Agent** only calls `mgc_run`, never touches keys or scripts

### Four Roles

| Role | Responsibility | Capabilities |
|------|----------------|--------------|
| User | Store keys/scripts, issue commands | WebUI / `mgc_open_webui` |
| Master Agent | Task decomposition, orchestration, execute on authorization/sub-Agent failure | `mgc_list`, `mgc_find`, `mgc_run` |
| Script Agent | Write scripts, store in MGC | `mgc_save`, `mgc_list`, `mgc_find` |
| Executor Agent | Complete non-sensitive tasks | `mgc_run`, `mgc_list`, `mgc_find` |

> Note: `mgc_get` retrieves plaintext and is a sensitive operation requiring user authorization; Script Agent typically does not need it.

---

## Collaboration Flow

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
        (Return pid+status)
```

---

## Quick Start

### Prerequisites

1. Install MGC v1.4.9+ (1.4.10 recommended): `pip install mgc-blackbox>=1.4.9`
2. Start MGC: `mgc` (API port 57219, WebUI port 57218)
3. Configure MCP (add to AI client):
   ```json
   {
     "mcpServers": {
       "mgc-blackbox": {
         "command": "mgc",
         "args": ["--mcp"],
         "env": { "PYTHONIOENCODING": "utf-8" }
       }
     }
   }
   ```
4. Store sensitive resources via WebUI or `mgc_open_webui`: API keys, database credentials, business scripts
5. Load prompt templates into each Agent

> **Sandbox mode (1.4.9+)**: When running inside a sandbox Agent (Trae Work / Workbuddy), install MGC in the system environment; otherwise MCP operations may be limited — in that case, call FastAPI directly.

### Step 1: Configure Master Agent

Load `prompts/master_agent.md` into the Master Agent's system prompt.

### Step 2: Configure Script Agent

Load `prompts/script_agent.md`.

### Step 3: Configure Executor Agent

Load `prompts/executor_agent.md`.

### Step 4: Start Collaboration

After user issues a command, the Master Agent automatically decomposes the task chain and coordinates sub-Agents.

---

## Prompt Templates

| File | Purpose |
|------|---------|
| [prompts/master_agent.md](file:///D:/MirginCipher/Toolkits/task_chain_skills/mgc_task_chain_meta_skill/mgc_task_chain_meta_skill_en/prompts/master_agent.md) | Master Agent: task decomposition, orchestration, `mgc_find` lookup |
| [prompts/script_agent.md](file:///D:/MirginCipher/Toolkits/task_chain_skills/mgc_task_chain_meta_skill/mgc_task_chain_meta_skill_en/prompts/script_agent.md) | Script Agent: `mgc_save` to store scripts, `mgc_find` for collision check |
| [prompts/executor_agent.md](file:///D:/MirginCipher/Toolkits/task_chain_skills/mgc_task_chain_meta_skill/mgc_task_chain_meta_skill_en/prompts/executor_agent.md) | Executor Agent: `mgc_run` to execute scripts |
| [prompts/cooperation_best_practice.md](file:///D:/MirginCipher/Toolkits/task_chain_skills/mgc_task_chain_meta_skill/mgc_task_chain_meta_skill_en/prompts/cooperation_best_practice.md) | Best-practice document, auto-maintained by Master Agent |

---

## MGC Tool Usage

### mgc_save (Used by Script Agent)

```python
# Store script (ext01 required; ext02 optional — MGC 1.4.10 auto-parses argparse defaults)
mgc_save(
    info_type="script",
    info_owner="Data Query Script",
    ext01="python",
    content="""import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--query', default='default')
args = parser.parse_args()
print(args.query)"""
)
```

### mgc_find (1.4.10 new, fuzzy search)

> Used to fuzzy-match entries by info_owner / diff fields. **Never returns content plaintext.**

```python
# Find scripts whose owner contains "query"
scripts = mgc_find(info_owner="query", match_mode="substring", limit=50)
# match_mode: substring (%x%) / prefix (x%) / suffix (%x) / exact (x)
```

### mgc_run (Used by Executor Agent, 1.4.7+ blackbox execution)

> ⚠️ **Important (1.4.10 contract)**: `ext02` must be a **JSON array string**, matching the script's `argparse` argv list. Dict-style `{"k":"v"}` is no longer accepted and triggers HTTP 422.
>
> **Auto-parsing**: After Script Agent stores a script, MGC auto-fills `ext02` from `argparse` defaults. Executor Agent can omit `ext02` to use defaults.

```python
import json

# Recommended: build JSON array string with json.dumps
params = ["--query", "2026-08-08"]
result = mgc_run(
    info_type="script",              # required, type is script
    info_owner="Data Query Script",  # required, script name
    diff_1="v1",                     # required to uniquely identify when multiple entries share the owner
    ext02=json.dumps(params)         # optional JSON array string: '["--query", "2026-08-08"]'
)
# Returns: {"pid": 12345, "status": "started"}
# Note: mgc_run does not return stdout; for results, the script should write to a file and print the path
```

### mgc_list (All Agents, exact match)

> Note: `mgc_list` only lists entry metadata. Since 1.4.10 prefer `mgc_find` for fuzzy lookup.

```python
scripts = mgc_list(info_type="script")
```

### mgc_open_webui (User)

> Used to have AI open MGC WebUI for users to store sensitive resources.

```python
mgc_open_webui()
```

---

## ext02 Auto-Parsing (1.4.10 Important Change)

Since MGC 1.4.10, when storing a script it **auto-parses `argparse` literal defaults** and stores them as a JSON array string in `ext02`:

```python
# After Script Agent's mgc_save, MGC auto-fills ext02:
# '["--start", "2026-08-08", "--verbose"]'

# Executor Agent can omit ext02 to use defaults
mgc_run(info_owner="my_script", diff_1="my_script")

# Or override at runtime
mgc_run(
    info_owner="my_script",
    diff_1="my_script",
    ext02='["--start", "2026-12-25"]'
)
```

**Dynamic defaults are not supported** (e.g. `datetime.now()`, `os.path.expanduser("~")`, f-strings). MGC returns `dynamic_args_detected` warning and asks you to set `ext02` manually. Script Agent should always use literal defaults.

---

## Security Boundaries

### What This Skill Provides

- Collaboration methodology framework
- Prompt templates
- MGC tool usage specifications

### What This Skill Does NOT Provide

- MGC permission enforcement (relies on prompt constraints)
- Automatic key management
- Agent identity authentication

### ⚠️ Important Reminders

1. All sensitive resources must be stored by users via MGC WebUI
2. Executor Agent can only call `mgc_run`; must never read script content
3. Master Agent must clearly inform sub-Agents of call timing and script location
4. After sensitive operation results return, Master Agent is responsible for updating task status and coordinating sub-Agent collaboration
5. `ext02` must be a JSON array string (e.g. `["--flag","value"]`); never use dict-style

---

## FAQ

| Question | Answer |
|----------|--------|
| Will information stored in MGC sync to cloud? | MGC is a local tool with no active network capability |
| What are MGC's main capabilities? | After installing MGC, click the **MGC Skills** button (1.4.7+) in the WebUI top bar |
| Can sub-Agents bypass MGC? | Prompt constraints cannot fully prevent; ensure sub-Agents cannot access local script files |
| How to isolate scripts for different tasks? | Use `info_owner` naming, e.g., `TaskA_QueryScript`, `TaskB_PublishScript` |
| How does Master Agent know what scripts are available? | Use `mgc_find` (fuzzy) or `mgc_list` (exact), or have Script Agent report |
| `mgc_run` returns HTTP 422, what to do? | `ext02` must be a JSON array string; use `json.dumps(["--flag","value"])` |
| How to handle `dynamic_args_detected` warning? | Use literal defaults (not `datetime.now()` etc.) or pass `ext02` manually |
| MCP unavailable in sandbox mode? | Install MGC in system environment, or call FastAPI directly at `/api/mgc/sensitive/run` |

---

## Related Resources

- **MGC Core Repository**: https://github.com/zkeviny/MGC-Blackbox
- **MGC Installation**: `pip install mgc-blackbox>=1.4.9`
- **WebUI**: http://127.0.0.1:57218
- **API**: http://127.0.0.1:57219
- **MGC API Auth Token**: `~/.mgc/database/mgc_black_box/.mgc_token`
- **Feedback**: mirgincipher@outlook.com

---

## Changelog

### v1.1.0

- Upgraded to adapt to MGC 1.4.10
- Fixed `mgc_run` `ext02` signature: must be a JSON array string
- Added `mgc_find` fuzzy search tool
- Documented `ext02` auto-parsing (1.4.10)
- Documented that `mgc_run` returns only pid+status (no stdout)
- Added 1.4.9 sandbox mode note
- Updated MGC main skill doc reference to WebUI "MGC Skills" button

### v1.0.0

- Initial release
- Provides Master / Script / Executor Agent prompt templates
- Includes complete collaboration flow documentation
