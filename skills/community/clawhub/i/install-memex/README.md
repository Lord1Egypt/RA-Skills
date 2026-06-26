# 📚 Install memex — cross-AI memory in 2 minutes

> One prompt sets up local-first AI memory across **Claude Code, Cowork, Cursor, Cline, Continue, and Zed** — plus Obsidian notes and Telegram chats. No cloud. No account. No data leaves your machine.

## What this skill does

After you drop the skill into your agent (`~/.claude/skills/` for Claude Code, or your client's equivalent), saying **"install memex"** triggers a guided installation:

1. **Discovery** — read-only checks for which MCP client you're using and what AI data already exists on your machine
2. **Fast path (v1.1+)** — `curl -fsSL https://memex.parallelclaw.ai/install.sh | bash`: one hosted bash script does npm install (with EACCES auto-fix to `~/.npm-global`), daemon setup, v0.8 auto-context hook, history backfill, and `claude mcp add memex` if Claude Code CLI is on PATH. Idempotent.
3. **Fallback: manual five-step** — if curl fails, the user declines, or the agent is inside a GUI client (Cursor/Cline/Continue/Zed) where the MCP config still needs editing: `npm install -g memex-mvp` → MCP config merge → `memex-sync install` → `memex-sync scan`.
4. **MCP config merge** (only needed for GUI clients) — adds a single absolute-path `command` entry into your client's `mcpServers` config. Never overwrites your other servers.
5. **Restart hint + verification commands** — including the v0.7+ CLI fallback (`memex overview`, `memex search "foo"`) so you can verify memex works even if MCP didn't wire up cleanly.

End-to-end: **~60 seconds** via fast path, **~2 minutes** via manual flow, fully observable (agent shows each command before running).

## What is memex?

Memex is a **local-first MCP server** that captures every conversation you have with an AI — across **Claude Code, Cowork (including subagent transcripts), Cursor, Cline, Continue, Zed**, plus **Obsidian notes**, **Telegram chats**, and **web pages / AI chat shares** (v0.6+ via `memex_store_document` — agent fetches, memex stores verbatim) — into one searchable SQLite + FTS5 corpus.

Any MCP-compatible agent can then query that corpus through 18 standard tools (`memex_search`, `memex_recent`, `memex_overview`, `memex_store_document`, the `memex_telegram_*` family for v0.10+ chat capture, …).

| Pain                                            | Memex                                |
|-------------------------------------------------|--------------------------------------|
| Claude forgets every session                    | One unified history across all sessions, all clients |
| Switching from Claude Code to Cursor = lost context | Cursor can read your Claude history (same SQLite DB) |
| Cloud memory services hold your data hostage    | One `~/.memex/data/memex.db` file on your disk       |
| Mem0 / Supermemory pricing per token            | 0 LLM calls on write — free at any scale             |
| Vendor ban = lose everything                    | Your DB stays even if Claude blocks your account     |

📦 npm: [memex-mvp](https://www.npmjs.com/package/memex-mvp) · 🏠 [memex.parallelclaw.ai](https://memex.parallelclaw.ai) · 🐛 [GitHub](https://github.com/parallelclaw/memex-mvp)

## Why a skill (vs. just copy-pasting the install prompt)

The install playbook also exists as a copy-paste prompt on the landing page. But once you have the skill installed, you skip a friction layer:

| Without skill | With skill |
|---|---|
| Open landing page in browser | (already in your agent) |
| Click "Copy install prompt" | — |
| Paste a wall of text into Claude/Cursor | Just say "install memex" |
| Hope the prompt is up-to-date | Skill version updates auto-fetched |

The skill description is written so Claude / OpenClaw auto-invoke it from any phrasing of "install memex", "set up memex", "add memory to my AI", etc. — no need to remember `/install-memex` exactly.

## Example dialogue

> **User:** install memex
>
> **Agent:** 👋 You're running inside Cursor. Quick discovery before any install actions...
>
> ✓ Found Claude Code data at `~/.claude/projects/` (8 sessions)
> ✓ Found Cowork sessions (3 subagent transcripts)
> ✗ Continue not installed
> ✗ Zed not installed
> ✓ Cursor data found (this is where I'll write the MCP config)
>
> After install, memex will auto-index conversations from: **Claude Code, Cowork, Cursor**. v0.10+ also auto-detects Telegram Desktop exports — when you export a chat, memex stages it and I'll ask which to import (privacy-first per-chat consent).
>
> Best path is the curl one-liner — does npm install (auto-fixes EACCES), daemon, auto-context hook, and history backfill in ~60 seconds. Want me to run:
>
> ```
> curl -fsSL https://memex.parallelclaw.ai/install.sh | bash
> ```
>
> **User:** yes
>
> **Agent:** [streams curl output, then edits `~/.cursor/mcp.json` to add `memex` MCP entry, prints restart hint, and offers Telegram capture setup]

See [examples.md](examples.md) for more sample dialogues, including EACCES recovery and partial-install scenarios.

## Requirements

- **Node.js 20–24** (LTS recommended). Install via [nodejs.org](https://nodejs.org), `brew install node`, or [nvm](https://github.com/nvm-sh/nvm)
- **macOS or Linux** (Windows untested for memex itself; skill works anywhere your agent has shell access)
- **An MCP-compatible CLI agent**: Claude Code, OpenClaw, Cursor (with MCP), Cline, Continue, or Zed. Web-only agents (ChatGPT, Claude.ai) can't execute install steps

## Install the skill

```sh
mkdir -p ~/.claude/skills/install-memex
curl -fsSL https://raw.githubusercontent.com/parallelclaw/memex-mvp/main/skills/install-memex/SKILL.md \
  -o ~/.claude/skills/install-memex/SKILL.md
```

Or, if you've already done `npm install -g memex-mvp`, the skill ships inside the package:

```sh
cp -r "$(npm root -g)/memex-mvp/skills/install-memex" ~/.claude/skills/
```

Then in your agent: `install memex` (or `/install-memex` if your client supports slash-commands).

## What the skill won't do

- ❌ Install Node.js for you — it stops and asks you to install it
- ❌ Run `sudo` without asking — EACCES fallback always confirms with you first
- ❌ Overwrite your existing `mcpServers` config — always merges
- ❌ Redirect any host application's data location — memex reads from each tool's native path
- ❌ Send anything over the network (besides `npm install` itself)

## License

[MIT](https://github.com/parallelclaw/memex-mvp/blob/main/LICENSE) for memex itself.
This skill bundle is published on ClawHub under [MIT-0](https://opensource.org/license/mit-0) (effectively public domain — no attribution required) per ClawHub's publishing terms.

---

📚 Built by [@parallelclaw](https://github.com/parallelclaw) · Star the repo if memex helps you: [github.com/parallelclaw/memex-mvp](https://github.com/parallelclaw/memex-mvp)
