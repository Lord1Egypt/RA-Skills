---
name: offlyn-clipper
description: >-
  Use when the user mentions Offlyn Clipper, Clipper notes, meetings, voice notes, live meeting,
  current meeting, catch me up, catch-up, what did I miss, recap this call, search my notes,
  prior thinking, or /offlyn-clipper. You HAVE live-meeting support via MCP tool clipper_catch_me_up
  while Clipper is recording on this Mac. NEVER say live meeting integration is missing or not in
  your skill list—call clipper_catch_me_up or clipper_list_chat_presets first. Also use
  clipper_search_notes for saved notes and clipper_get_note_context for a specific note ID.
homepage: https://clipper.offlyn.ai/openclaw.html
user-invocable: true
metadata: {"openclaw":{"os":["darwin"],"requires":{"bins":["node","openclaw"]},"emoji":"📎","primaryEnv":"CLIPPER_SOCKET_PATH"}}
---

# Offlyn Clipper

Connect OpenClaw to **Offlyn Clipper** on this Mac (local MCP, no cloud). You can search saved notes **and** recap the **live meeting** Clipper is recording right now.

## Critical rules (read first)

1. **Never** tell the user that live meeting / catch-up is “not in your skill list” or unavailable. That is wrong.
2. When the user says **catch me up**, **live meeting**, **current meeting**, **what did I miss**, or **recap the call** → call **`clipper_catch_me_up`** immediately. **Do not** answer from `clipper_search_notes` (that is old saved notes, not the live call).
3. If unsure which Clipper action fits → call **`clipper_list_chat_presets`** and offer 2–4 suggestion chips from the response, then run the preset’s `recommended_tool`.
4. If `clipper_catch_me_up` returns `no_active_meeting`, then say: start or resume recording in **Offlyn Clipper** (Quick Note / meeting banner), keep Clipper open, and ask again.
5. Clipper must be **running**; MCP uses `clipper.sock` on this Mac.

## `bundle-mcp runtime disposed` (OpenClaw session stale)

This is an **OpenClaw session** issue, not Clipper. The MCP tool list was frozen before the `clipper` bridge was ready.

**Recovery (in order):**

1. Call **`clipper_ping`** — if it works, the bridge is fine; the chat session is stale.
2. Tell the user: `openclaw gateway restart`, then **`/new`** (new chat). SIGUSR1 alone does **not** refresh tools in the current thread.
3. There is **no** `openclaw mcp reload` on all versions — do not suggest it.
4. After `/new`, retry **`clipper_catch_me_up`** for live meeting questions.

Verify from Terminal:

```bash
node "{baseDir}/mcp-bridge/verify.mjs"
```

## MCP tools (via server `clipper`)

| Tool | When to call |
|------|----------------|
| `clipper_catch_me_up` | Live call recap — **catch me up**, **current meeting**, **what did I miss** |
| `clipper_ping` | Health check + `live_meeting_active`; use after gateway restart or disposed errors |
| `clipper_list_chat_presets` | Offer chat chips (same as Clipper in-app); good at start of Clipper-related chat |
| `clipper_search_notes` | Search saved notes / prior thinking / project context |
| `clipper_get_note_context` | One note by UUID; use `include_raw_body` only if user granted raw access |

User can disable any tool in **Clipper → Settings → Integrations → Shared with OpenClaw**.

## Live meeting catch-up flow

```
User: "catch me up with the live meeting"
  → clipper_catch_me_up
  → summarize recap_context for the user (decisions, topics, action items, open questions)
```

Optional first step: `clipper_list_chat_presets` when `session_context` is `live_meeting` — presets include **Catch me up**, **What did I miss**, etc.

## One-time setup

1. **Launch Offlyn Clipper** and leave it running.
2. Run:

```bash
bash "{baseDir}/scripts/setup.sh"
```

3. Approve **Allow** when Clipper asks to connect OpenClaw.
4. Verify:

```bash
openclaw mcp show clipper
openclaw skills info offlyn-clipper
```

5. Test live recap (while Clipper is recording a meeting):

```bash
openclaw agent --message "Catch me up on my current Clipper meeting"
```

If tools are missing after an upgrade, re-run:

```bash
bash "{baseDir}/scripts/update-installed-skill.sh"
openclaw gateway restart
```

## Install / refresh this skill

```bash
openclaw skills install ./OpenClawPlugin/skills/offlyn-clipper --global
bash OpenClawPlugin/skills/offlyn-clipper/scripts/update-installed-skill.sh
```

Then start a **new** OpenClaw session (`/new`) or `openclaw gateway restart`.

## Troubleshooting

| Issue | Action |
|-------|--------|
| Agent says live meeting not available | Skill description stale — run `update-installed-skill.sh`, `/new` session |
| `no_active_meeting` | Start recording in Clipper, then retry `clipper_catch_me_up` |
| `tool_disabled` | Enable tool in Clipper → Integrations → Shared with OpenClaw |
| Socket refused | Clipper not running — open app, re-run `setup.sh` |
| Pairing denied | `node "{baseDir}/mcp-bridge/pair.mjs"` and Allow in Clipper |

## Architecture

```
OpenClaw → MCP stdio ({baseDir}/mcp-bridge/index.mjs) → clipper.sock → Clipper
```

Credentials: `~/.config/offlyn-clipper/openclaw-credentials.json`
