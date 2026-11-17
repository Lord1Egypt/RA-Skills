# MGC Blackbox — Multi‑Agent Cross‑Node Privacy Execution Base

> **Version 1.5.3** · Local encrypted execution base for AI agents, system scripts, and human users — store, execute, and delegate sensitive data, scripts, and entire workflows across trusted nodes **without ever exposing plaintext**. Auto-recognition, sealed cross-script imports, and 1.5.2 enhancements (first-run UX, sandbox mode).

## What This Skill Is

MGC Blackbox is the **encrypted execution layer underneath AI agents** — not an agent itself. It enables:

- **Store** sensitive data (tokens, passwords, configs) and scripts (logic, workflows, automation)
- **Execute** stored scripts with structured `argparse` parameters (AI never sees source)
- **Seal** individual scripts for cross-node delegation — original owner retains control
- **Package** a folder of scripts + configs as one unit, then **seal the package** for cross-device delegation
- **List** stored entries (metadata only, never plaintext)
- **Open WebUI** for human operations

All data is encrypted locally with AES‑256. **AI can execute but cannot read plaintext.**

---

## Prerequisites

### Python × OS Matrix

| OS | Python 3.10 | Python 3.11 | Python 3.12 |
|---|---|---|---|
| Windows | Yes | Yes | Yes |
| Linux (Ubuntu) | Yes | Yes | Yes |
| macOS 14+ (Apple Silicon) | Yes | Yes | Not supported |

- Install: `pip install mgc-blackbox`
- Start MGC: `mgc` (API at `http://127.0.0.1:57219`, WebUI at `http://127.0.0.1:57218`)

---

## First-run Setup (1.5.2+)

On the first startup after install, MGC automatically opens the WebUI and asks you to enter:

- **Personal key** — ≥8 characters, chosen by you
- **Weight parameter** — a single digit 1–9

MGC will **not store either value in plaintext** — you must remember both. If you lose them, the local database cannot be decrypted and must be discarded.

---

## Migrating to Another Machine (1.5.2+)

To move MGC to a new machine:

1. Copy `~/.mgc/database/mgc_black_box/mgc_black_box.db` to the new machine
2. Install MGC Blackbox there: `pip install mgc-blackbox`
3. Enter the **same personal key** and **same weight** on first startup

If protection mode is enabled on the source machine, disable it before migrating.

---

## MCP Server Configuration (1.5.2+)

If your agent supports MCP, register MGC as an MCP server:

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

In MCP mode, MGC exposes all tools listed below. The REST API remains available for system scripts.

### Sandbox mode

Some sandbox agents run MCP in the **system environment** rather than inside the sandbox. To use MCP tools in that case, either install MGC in the system environment, or call the FastAPI directly via REST.

---

## Quick Start

### 1. Store Sensitive Data

```python
mgc_save(
    info_type="token",
    info_owner="my_skill_api_key",
    content="sk-abc123..."
)
```

### 2. Retrieve at Runtime

```python
# AI retrieves via MCP — gets result only
result = mgc_get(
    info_type="token",
    info_owner="my_skill_api_key"
)
```

### 3. Execute Scripts

```python
# Store executable script (MGC auto-parses argparse → ext02 defaults)
mgc_save(
    info_type="script",
    info_owner="weather_report",
    ext01="python",
    content='
import argparse, requests
parser = argparse.ArgumentParser()
parser.add_argument("--city", default="Beijing")
args = parser.parse_args()
print(requests.get(f"https://wttr.in/{args.city}?format=j1").text)
'
)
# MGC auto-fills ext02 with ["--city", "Beijing"]

# AI runs it (zero visibility into source)
mgc_run(info_owner="weather_report", ext02='["--city", "Shanghai"]')
# → { "pid": 12345, "status": "started" }
```

---

## MCP Tools (1.5.3)

| Tool | Description |
|------|-------------|
| `mgc_save` | Store sensitive data or scripts (auto-parses `argparse` for scripts) |
| `mgc_save_file` | Store a file or folder from disk (`info_type="file"`); also imports sealed `.mgc_file` packages |
| `mgc_get` | Retrieve decrypted content of an entry |
| `mgc_run` | Execute a stored script (recommended over `mgc_get action="run"`) |
| `mgc_find` | Fuzzy search stored entries |
| `mgc_list` | List stored entries (metadata only) |
| `mgc_seal` | Seal a single script for cross-node delegation |
| `mgc_seal_package` | Seal a folder package for cross-node delegation |
| `mgc_package` | Export a folder as a plaintext archive (same-trust-boundary backup) |
| `mgc_open_webui` | Open WebUI in browser |

### Notable 1.5.2 / 1.5.3 Notes

- **Cross-script auto-recognition (`ext08`)** — `import` / `from-import` / `Path(__file__).parent / "x.py"` / relative-`subprocess` patterns are statically parsed when you save a folder with `mgc_save_file`, and routed through sealed execution at runtime. Relative `open("sibling.json")` is *recognized* in `ext08` but **runtime routing is not yet supported** — if you need fully sealed config access, read the config inside your script logic rather than via `open()`.
- **Sandbox-mode friendly** — MCP runs in the system environment if your sandbox isolates it; REST API is always available.
- **First-run UX** — guided WebUI setup replaces the prior console prompt.

---

## Cross-Node Delegation (B.2 — Sealed Folder Package)

The flagship capability: ship an entire workflow folder to a trusted node as a single encrypted capsule.

```python
# Node A — source side
mgc_save_file(
    path="/Users/alice/projects/my_workflow",
    info_owner="my_workflow",
    diff_2="my_workflow",
)

mgc_seal_package(
    info_owner="my_workflow",
    diff_2="my_workflow",
    ext04="<Node B PEM public key>",
)
# → sealed capsule (.mgc_file)

# Hand over the capsule (email, USB, etc.)
```

```python
# Node B — receiving side
# (Agent reads README.md inside, then:)
mgc_save_file(path="./received_workflow.mgc_file")    # import
mgc_find(info_owner="my_workflow", diff_2="my_workflow")  # discover entries
mgc_get(info_type="file", info_owner="my_workflow", diff_2="my_workflow")  # read manifest
mgc_run(info_owner="my_workflow", diff_2="my_workflow")  # run entry script
```

Node B executes the workflow but **cannot read, modify, or redistribute the plaintext**.

---

## Links

- **Main Repo**: https://github.com/zkeviny/MGC-Blackbox
- **Issues**: https://github.com/zkeviny/MGC-Blackbox/issues
- **Contact**: mirgincipher@outlook.com

---

## Related Skills (Zero‑Exposure Ecosystem)

These skills are built on top of MGC Blackbox and follow the same zero‑exposure pattern:

- **SMTP Token Security** — Secure storage for SMTP credentials used in email workflows
- **Database Credential Security** — Zero‑exposure storage for database passwords and connection strings
- **Webhook Token Security** — Safe storage for Slack / Telegram / DingTalk / Feishu webhook tokens
- **Key‑Safe Generator** — Generates strong random keys for scripts and configurations

All of these skills use MGC Blackbox as their encrypted execution layer.