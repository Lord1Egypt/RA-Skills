---
name: kemia
description: >
  Connect your OpenClaw instance to kemia (https://kemia.byte5.ai) for visual agent configuration management.
  Use when: (1) connecting to a kemia deployment for the first time (/connect),
  (2) importing an edited agent config from kemia (/import),
  (3) checking connection and deploy status (/kemia-status),
  (4) generating a one-time login link for the kemia web UI (/kemia-link).
  NOT for: editing agent configs directly — that happens in the kemia web UI.
---

# Kemia — Agent Configuration Manager

Manage your agent configurations through the kemia web interface.

**Architecture:** OpenClaw always initiates. Kemia never pushes. All communication is pull-based via the v1 API.

## Prerequisites

- `jq` must be installed
- `curl` must be available
- Config stored at: `~/.openclaw/workspace/skills/kemia/config.json`

## Commands

### `/connect <kemia-url>` (two-step, resumable)

Connect this OpenClaw instance to a kemia deployment. Works in two steps because the confirmation happens in a browser and can take arbitrary time — the script never runs a long polling loop that could be killed by OpenClaw/Exec.

**Step 1 — start enrollment:** `/kemia connect https://kemia.byte5.ai`
- `POST /api/v1/enroll` → enrollment URL
- Persists state to `skills/kemia/enrollment.json`
- Prints the URL. **Exits immediately.**

**Step 2 — user clicks, confirms in the browser, returns to the agent.**

**Step 3 — complete:** `/kemia connect` (no argument)
- Reads `enrollment.json`, polls `/status` **once**.
- If still pending → tells the user to wait and run `/kemia connect` again; exits.
- If completed → saves `config.json`, exports workspace `.md` files, cleans up state.
- If expired → cleans up, asks the user to re-run with a URL.

**Already connected?** A fresh `/kemia connect` without arguments is safe: the script verifies `config.json` against `/api/v1/status` first. If the key works, it reports "already connected" and exits without touching anything.

**Re-connecting from the same machine:** the script sends a stable machine fingerprint (`sha256(hostname + workspace_path)`) with the enrollment request. If kemia recognizes the machine, the confirmation page offers **Re-Authenticate** (rotate the API key on the existing instance, keep all agents) or **Set up as a new instance** (fresh start). Duplicates are no longer silently created.

**No shared secrets needed.** The enrollment URL is the authentication.

**Script:** `scripts/connect.sh [kemia-url]`

**Environment variables (optional):**
- `OPENCLAW_WORKSPACE` — workspace path (default: `~/.openclaw/workspace`)
- `OPENCLAW_INSTANCE_NAME` — instance name (default: hostname)
- `OPENCLAW_AGENT_NAME` — agent name (default: `CyberClaw`)

---

### `/kemia-link`

Generate a one-time login URL for the kemia web interface (15-minute expiry).

**Script:** `scripts/kemia-link.sh`

Use this when the user needs a fresh session — e.g. after logout or on a new device.

---

### `/import [agent-id]`

Import the latest deploy-ready snapshot from kemia into the workspace.

**Script:** `scripts/import.sh [agent-id]`

- Fetches the snapshot marked "deploy ready" in the kemia UI
- Backs up current workspace `.md` files to `.kemia-backup/` before overwriting
- If no `agent-id` given, uses the saved ID from `config.json`

After import, restart OpenClaw for changes to take effect.

---

### `/kemia-status`

Check connection health and whether a deploy-ready snapshot is pending.

**Script:** `scripts/status.sh`

---

## Config File

After `/connect`, credentials are stored in:
```
~/.openclaw/workspace/skills/kemia/config.json
```

```json
{
  "apiKey": "km_...",
  "instanceId": "clxyz...",
  "baseUrl": "https://kemia.byte5.ai",
  "agentId": "clxyz..."
}
```

---

## Setup Flow

1. Run `/kemia connect https://kemia.byte5.ai` (or your kemia instance URL) — prints enrollment URL, exits.
2. Click the enrollment URL — confirm in the browser → logged into kemia.
3. Run `/kemia connect` again (no arguments) — completes setup, exports agent config.
4. Shape the config in the kemia web UI (Persona, Role, Knowledge, Team).
5. Create a snapshot → mark it "deploy ready".
6. Run `/import` → restart OpenClaw.

---

## API Reference

For full endpoint documentation see `references/api.md`.
