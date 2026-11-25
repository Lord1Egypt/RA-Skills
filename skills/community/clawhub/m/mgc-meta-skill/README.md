# MGC Blackbox — Multi‑Agent Cross‑Node Privacy Execution Base

> **Version 1.5.4** · Local encrypted execution base for agent runtimes, system scripts, and human users — store, execute, and delegate sensitive data, scripts, and entire workflows across trusted nodes **without ever exposing plaintext**. Seal free mode, link authorization, cross-folder workflow recognition, and the `mgc_delete` tool.

## What This Skill Is

MGC Blackbox is the **encrypted execution layer underneath agent runtimes** — not an agent itself. It enables:

- **Store** sensitive data (tokens, passwords, configs) and scripts (logic, workflows, automation)
- **Execute** stored scripts with structured `argparse` parameters (the source stays encrypted)
- **Seal** individual scripts for cross-node delegation — p2p mode (one specific node) or free mode (any 1.5.4+ node, source still encrypted)
- **Package** a folder of scripts + configs as one unit, then **seal the package** for cross-device delegation
- **List** stored entries (metadata only, never plaintext)
- **Delete** records — via WebUI or the `mgc_delete` tool, with explicit user confirmation for folders
- **Open WebUI** for human operations

All data is encrypted locally with AES‑256. **Sealed source stays encrypted on disk: the executing node decrypts it in memory at run time, and the plaintext is never written out.**

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

On the first startup after install, MGC prompts you to set:

- **Personal key** — chosen by you
- **Weight parameter** — a single digit 1–9

Three paths are available:

| Mode | Who uses it | How |
|------|------------|-----|
| CLI — auto-generate | Agent / automated setup | MGC generates a strong random key. Zero human intervention. |
| CLI — custom input | Developer who wants a known key | Enter your own key string at the prompt. |
| WebUI | Human who wants a GUI | Open browser, enter key in the form. |

MGC does **not** store either value in plaintext — if you lose them, the local database cannot be decrypted and must be discarded.

---

## Migrating to Another Machine (1.5.2+)

To move MGC to a new machine:

1. Copy `~/.mgc/database/mgc_black_box/mgc_black_box.db` to the new machine
2. Install MGC Blackbox there: `pip install mgc-blackbox`
3. Enter the **same personal key** and **same weight** on first startup

If the original key was auto-generated, retrieve it from `~/.mgc/secrets/personal_key.txt` on the source machine. If protection mode is enabled on the source machine, disable it before migrating.

---

## MCP Server Configuration (1.5.2+)

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
# Retrieve via MCP — gets result only
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

# Run it (the source stays encrypted)
mgc_run(info_owner="weather_report", ext02='["--city", "Shanghai"]')
# → { "pid": 12345, "status": "started" }
```

---

## MCP Tools (1.5.4)

| Tool | Description |
|------|-------------|
| `mgc_save` | Store sensitive data or scripts (auto-parses `argparse` for scripts) |
| `mgc_save_file` | Store a file or folder from disk (`info_type="file"`); also imports sealed capsules and `.mgc_file` packages |
| `mgc_get` | Retrieve decrypted content of an entry, or run `package` / `seal_package` actions |
| `mgc_run` | Execute a stored script (recommended over `mgc_get action="run"`) |
| `mgc_find` | Fuzzy search stored entries |
| `mgc_list` | List stored entries (metadata only) |
| `mgc_seal` | Seal a single script into a self-describing capsule file |
| `mgc_seal_package` | Seal a folder package for cross-node delegation |
| `mgc_package` | Export a folder as a plaintext archive (same-trust-boundary backup) |
| `mgc_delete` | Delete a record (single-record exact match; folder-level requires explicit confirmation) |
| `mgc_open_webui` | Open WebUI in browser |
| `mgc_skill` | Return the full MGC skill document (read it when the tool set is unclear) |

### Notable 1.5.4 Features

- **Seal free mode** — omit `ext04` when sealing and the artifact is wrapped with MGC's shared default node key: **any MGC 1.5.4+ node can import and run it**, while the source stays encrypted and unreadable. Ideal for skill marketplaces and public distribution.
- **Link authorization** — every sealed artifact carries its source node's identity in `ext07` and its mode in `ext09`. Any modification to either field (including whitespace) makes the artifact unrestorable. In p2p mode the recipient holds no key of their own and cannot re-seal your source onward to a third party.
- **`output_dir` is required** (breaking change) — all `mgc_seal` / `mgc_seal_package` / `mgc_package` operations need an absolute `output_dir`. There is no desktop fallback, because the desktop path differs across platforms.
- **Sealed capsule export & import** — `mgc_seal` writes `<output_dir>/<info_owner>_<timestamp>/sealed_capsule.json`. Import it with `mgc_save_file(path='<capsule.json>', info_owner='<your owner>')` (preferred — `info_type` is inferred) or `mgc_save(content=<entire capsule JSON>, info_type='script', info_owner='<your owner>')`. Pass a **different** `info_owner` than the source, otherwise the source record is overwritten.
- **Run-compatibility badge (`ext10`)** — every saved script is statically checked on save. The `mgc_run` badge in the list and detail views reads `supported` or `unsupported`. An `unsupported` badge means the script contains a fatal path check (e.g. `if not Path(...).exists(): sys.exit(1)`) that exits before MGC can intercept the call.
- **Cross-folder workflow recognition** — same-folder imports and cross-folder subprocess calls are recognized when saving a workflow, so the whole package runs under sealed mode with no plaintext on disk.
- **`mgc_run` no longer requires `diff_1`** — when several scripts match, MGC returns `AMBIGUOUS_SCRIPT` instead of guessing. Use `mgc_find` to list candidates, then pass the exact `diff_1` / `diff_3`; `diff_3` (the script's path inside the folder) identifies a single record on its own.
- **`mgc_delete`** — single-record mode requires the full 6-tuple address. When 2+ records share an `(info_type, info_owner, diff_2)` folder, the tool returns a candidate list and refuses to act until you explicitly approve and re-call with `confirm_folder_delete="true"` (a string, not a boolean). Node credential records are protected and cannot be deleted. A folder's records are stored under separate `info_type`s, so deleting a mixed folder takes one call per type.
- **Linux compatibility** — platform-specific bugs on Linux are resolved; sealed workflows now behave the same on macOS / Windows / Linux.

### Guarantee Scope

**Scope of the guarantee.** MGC protects **content confidentiality**: data is encrypted at rest, and sealed source is decrypted only in memory, at execution time. Runtime behaviour belongs to the script's author — once a package is unsealed on a node, MGC cannot guarantee the trustworthiness of its author, and what the script does at run time is the author's responsibility. Before importing, verify the source node's public key against a trusted channel, and rely on link authorization (`ext07` / `ext09`) to detect any modification of the artifact.

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

# p2p mode — only Node B can unseal
mgc_seal_package(
    info_owner="my_workflow",
    diff_2="my_workflow",
    ext04="<Node B PEM public key>",
    output_dir="/Users/alice/Documents/delivery",
)
# → /Users/alice/Documents/delivery/my_workflow_delivery/
#     ├── my_workflow.mgc_file   (sealed scripts + MGCFILE.json manifest)
#     └── README.md              (usk/3.0 yaml + import instructions)

# free mode — omit ext04; any MGC 1.5.4+ node can import and run
mgc_seal_package(
    info_owner="my_workflow",
    diff_2="my_workflow",
    output_dir="/Users/alice/Documents/delivery",
)

# Hand over the delivery folder (email, USB, etc.)
```

```python
# Node B — receiving side
mgc_save_file(path="./my_workflow.mgc_file", info_owner="my_workflow_received")
mgc_find(info_owner="my_workflow_received", diff_2="my_workflow")  # discover entries
mgc_run(info_owner="my_workflow_received", diff_2="my_workflow", diff_3="script/main.py")
```

Node B runs the workflow while the source stays encrypted. The sealed package is bound to its source node and cannot be modified or redistributed onward. Limits: max 100 files / 50 MB per package; the folder must contain at least one script.

---

## Links

- **Main Repo**: https://github.com/zkeviny/MGC-Blackbox
- **Issues**: https://github.com/zkeviny/MGC-Blackbox/issues
- **Contact**: mirgincipher@outlook.com

---