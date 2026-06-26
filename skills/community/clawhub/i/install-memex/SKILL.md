---
name: install-memex
description: Make Claude, Cursor, Cline, Continue, and Zed remember every AI conversation forever — one local SQLite corpus shared across all of them. Installs memex (local-first MCP server) in ~60 seconds via curl one-liner. Includes auto-capture daemon for Claude Code / Cowork / Cursor / Obsidian; v0.10 Telegram auto-detect (export from Desktop → memex stages it → AI proactively asks which to import, privacy-first per-chat consent); v0.8 SessionStart hook for the Brian Chesky moment ("Claude already knows what you were doing"); URL / Perplexity / AI chat share capture via memex_store_document. 18 MCP tools, no cloud, no account, verbatim storage. Use when the user says "install memex", "set up memex", "add memory to my AI", "make my agent remember across sessions", "сохрани мои чаты", or similar.
version: 1.5.1
metadata:
  openclaw:
    emoji: "📚"
    homepage: https://memex.parallelclaw.ai
    requires:
      bins:
        - node
        - npm
---

# Install memex

## ⚠ For ClawHub reviewers, security scanners, and curious users

This skill is an **installer for memex** — a local-first MCP memory server.
Static scanners flag several patterns as "suspicious"; every single one is
intentional and necessary for installing a memory tool. Below is the full
list so a human reviewer (or the user) can verify legitimacy in one glance.

**What the skill instructs the agent to do:**

| Action | Why | Source-of-truth |
|---|---|---|
| `curl -fsSL https://memex.parallelclaw.ai/install.sh \| bash` | Fast-path installer (the user can `\| less` first to inspect) | [docs/install.sh](https://github.com/parallelclaw/memex-mvp/blob/main/docs/install.sh) — open-source bash, hosted on GitHub Pages |
| `npm install -g memex-mvp` | Manual install (fallback if user declines the curl) | [npmjs.com/package/memex-mvp](https://www.npmjs.com/package/memex-mvp), source: [github.com/parallelclaw/memex-mvp](https://github.com/parallelclaw/memex-mvp) |
| `echo 'export PATH=...' >> ~/.zshrc` | EACCES auto-fix — moves npm prefix to `~/.npm-global` so `npm install -g` works without sudo. **Idempotent** — re-running is safe. | Standard npm prefix workaround [docs.npmjs.com](https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally) |
| `sudo npm install -g memex-mvp` | Offered as Plan A on EACCES if user explicitly wants quick (not default — skill recommends the no-sudo prefix fix). Skill **never runs sudo without explicit user "yes"**. | — |
| `memex-sync install` (LaunchAgent) | Registers a macOS LaunchAgent so memex daemon auto-starts on login. **The daemon itself is local-only**: it watches `~/.claude/projects/`, `~/Downloads/Telegram Desktop/`, etc., and writes to `~/.memex/data/memex.db`. Zero outbound network traffic. | LaunchAgent plist at `~/Library/LaunchAgents/com.parallelclaw.memex.sync.plist` is human-readable |
| Edit `~/.claude/settings.json`, `~/.cursor/mcp.json`, etc. | Adds the MCP-server entry so the user's AI client can call memex tools. Existing entries are preserved (merge, never overwrite). | Each MCP client documents this config format |
| `tell application "Terminal" to do script "claude"` (AppleScript) | Used by the optional clickable notification banner — opens a new Terminal tab + launches `claude` when the user clicks. **Default OFF**. | Requires `brew install terminal-notifier` (optional dep) |
| `brew install terminal-notifier` | Optional dep for clickable banners. Skill mentions it but does NOT install without user OK. | [github.com/julienXX/terminal-notifier](https://github.com/julienXX/terminal-notifier) |

**Hard guarantees** (codified in the "Safety rules" section below):
- Agent shows every shell command **BEFORE** running it
- User can say "stop" / "no" at any step, agent halts
- `sudo` is NEVER run without an explicit user "yes"
- MCP config files are MERGED, never overwritten — existing entries preserved
- Memex at runtime emits **zero outbound network traffic** (it's local-first by design — see [PRIVACY section in repo README](https://github.com/parallelclaw/memex-mvp/blob/main/README.ru.md#приватность-и-безопасность--privacy--security))

**Source code:** [github.com/parallelclaw/memex-mvp](https://github.com/parallelclaw/memex-mvp) (MIT). All commands above are visible in [docs/install.sh](https://github.com/parallelclaw/memex-mvp/blob/main/docs/install.sh) and the published [memex-mvp npm package](https://www.npmjs.com/package/memex-mvp).

---

You are installing **memex** on this machine. Memex is a local-first MCP server that captures the user's AI conversations across Claude Code, Cowork (including subagents), Cursor, Obsidian, and Telegram exports into a searchable SQLite + FTS5 index that any MCP-compatible agent can query through 18 standard tools (`memex_search`, `memex_recent`, `memex_overview`, `memex_store_document`, plus the `memex_telegram_*` family added in v0.10+).

Repo: https://github.com/parallelclaw/memex-mvp
Landing: https://memex.parallelclaw.ai
npm: https://www.npmjs.com/package/memex-mvp

## How memex works (read this so you don't get confused by paths below)

Memex has its OWN storage at `~/.memex/data/memex.db`. It READS from each tool's native data location automatically — Claude Code from `~/.claude/projects/`, Cursor from its `state.vscdb`, Cowork from its sessions dir, Obsidian from configured vaults. You do NOT need to change where Claude Code, Cursor, or any other tool saves its data. Memex is a passive observer.

## Prerequisite

This skill only works if you are running INSIDE an AI agent that has direct access to the user's shell — i.e. one of: Claude Code (CLI), Cursor, Cline, Continue, or Zed. Web-based agents (ChatGPT in browser, Claude.ai web, Claude Desktop without tools, etc.) cannot execute `npm`/file operations. If you are NOT a CLI-based agent with shell access, stop now and tell the user to use the manual install at https://memex.parallelclaw.ai/#quickstart.

## Discovery — do this BEFORE the numbered steps

Scan the user's setup so you can tailor advice and tell them exactly what memex will pick up.

1. Identify which MCP client you're running inside (you should know from context — Claude Code CLI, Cursor, Cline, Continue, or Zed).
2. Run these read-only checks one by one:
   ```sh
   ls -d ~/.claude/projects 2>/dev/null
   ls -d ~/Library/Application\ Support/Claude/local-agent-mode-sessions 2>/dev/null
   ls -d ~/Library/Application\ Support/Cursor 2>/dev/null
   ls ~/.continue/config.json 2>/dev/null
   ls -d ~/.config/zed 2>/dev/null
   ```
3. Report to the user in plain language:
   - "You're running inside [X]. I will edit [path] in step 2 below."
   - "Tools with data found on this machine: [list]"
   - "Tools NOT found (memex won't capture from these): [list]"
   - "After install, memex will auto-index conversations from: [detected sources]"
4. Wait for the user's "ok" before starting step 1.

## Fast path — one-line installer (try this first)

memex ships a hosted bash installer that does steps 1, 3, and 4 in a single run — and also wires up Claude Code's MCP entry if `claude` is on PATH. It's idempotent (safe to re-run), auto-fixes the `EACCES` case by moving npm's prefix to `~/.npm-global`, and prompts before enabling the auto-context hook.

Show this command to the user, explain what it does, get their **explicit ok**, then run:

```sh
curl -fsSL https://memex.parallelclaw.ai/install.sh | bash
```

What the script does, in order:
1. Checks Node ≥ 20.
2. `npm install -g memex-mvp` — on EACCES, sets `npm config set prefix ~/.npm-global`, appends PATH to `~/.zshrc`, retries.
3. `memex-sync install` with `--auto-context yes` (Brian Chesky hook into `~/.claude/settings.json` — preserves other hooks).
4. `memex-sync scan` — backfills existing history.
5. `claude mcp add memex --scope user -- memex` if Claude Code CLI is detected.

After the script finishes:
- If the user is in **Claude Code (CLI)** → install is complete. Skip straight to step 6 (verification + restart). Also do step 5 (offer Telegram capture).
- If the user is in **Cursor / Cline / Continue / Zed** → the npm install + daemon + auto-context + scan are done, but the GUI client's MCP config still needs the memex entry. **Skip step 1 (already installed)**, **skip step 3** (daemon already installed) and **skip step 4** (scan already ran). **Do step 2** (wire MCP into the GUI client's config), **step 5** (offer Telegram), and **step 6** (verify + restart).

If the script fails for any reason — non-zero exit, weird output, user uncomfortable piping curl to bash — fall back to the **Manual install** below.

To inspect what the script does first: `curl -fsSL https://memex.parallelclaw.ai/install.sh | less` (don't pipe to bash).

## Manual install (if the fast path didn't fit)

Do these in order. Show each command before running it. Stop and ask if anything fails or looks wrong.

### 1. Install memex from npm

```sh
npm install -g memex-mvp
```

If you get `EACCES` (macOS system Node), **recommend Option B (permanent prefix fix) by default** and proceed unless the user explicitly chooses sudo.

Say to the user:

> "Hit EACCES — your Node is installed in a system directory that npm can't write to without admin rights. Two fixes:
>
> **A)** Quick: `sudo npm install -g memex-mvp` — one-time, requires your password
> **B)** Permanent fix: I'll move npm's install location to your home directory. After this, no `npm install -g` will ever ask for sudo again, for any package. Five commands, one-time.
>
> I recommend **B** — it's a permanent improvement that benefits all your future Node tools, not just memex. Proceed with B?"

If the user agrees (or says anything like "ok", "yes", "default", "go", "B") — proceed with B without further questions:

```sh
mkdir -p ~/.npm-global
npm config set prefix ~/.npm-global
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.zshrc
source ~/.zshrc
npm install -g memex-mvp
```

If the user **explicitly** picks A (or says "sudo", "fast", "quick"), use sudo:

```sh
sudo npm install -g memex-mvp
```

After the install completes, verify with `which memex` (should print an absolute path) and `memex --version` (should print the version).

**Important if Option B was used + user already had memex from a prior sudo install:** the old sudo-installed copy in `/usr/local/lib/node_modules/memex-mvp/` is now orphaned (PATH prefers the new home install). Mention this once:

> "By the way, you have an older sudo-installed memex copy in `/usr/local/lib/`. It's harmless but takes ~60 MB. Clean it up when convenient: `sudo npm uninstall -g memex-mvp` — not urgent."

Don't run that uninstall yourself — let the user decide when.

If `node` or `npm` are missing, STOP and tell the user to install Node.js (recommend nvm.sh or `brew install node`). Don't try to install Node yourself.

**Verify:** `which memex` prints an absolute path; `memex-sync --help` runs without error.

### 2. Wire memex into the MCP client

Common config locations:

| Client       | Config file                                         |
|--------------|-----------------------------------------------------|
| Claude Code  | `~/.claude/config.json` (or platform equivalent)    |
| Cursor       | `~/.cursor/mcp.json`                                |
| Cline        | VS Code `settings.json` (`cline.mcpServers`)        |
| Continue     | `~/.continue/config.json`                           |
| Zed          | `~/.config/zed/settings.json` (`context_servers`)   |

Tell the user which one you've inferred and which file you'll edit. If unclear, ask.

Read the existing config (if present). Show the user a diff before saving.

Get the **absolute** path to the memex binary — GUI apps (Cursor, Cline, Claude Desktop) on macOS often don't inherit shell PATH, so a bare `"command": "memex"` fails with `spawn memex ENOENT`. Run:

```sh
which memex
```

Capture that path (e.g. `/Users/<you>/.npm-global/bin/memex` or `/usr/local/bin/memex`). If it's a shim, also run `realpath $(which memex)` to resolve to the real binary.

MERGE this entry into `mcpServers` — never overwrite other servers the user has:

```json
{
  "mcpServers": {
    "memex": {
      "command": "<absolute path from which memex>"
    }
  }
}
```

One path, no `args`. The published npm package wires up its own entry point.

If the config file doesn't exist, create the parent directory and write a minimal valid file with just memex.

**Verify:** re-read the file after save; confirm `memex` entry is present and `command` is an absolute path.

### 3. Turn on live auto-capture + auto-context (v0.8+)

```sh
memex-sync install
```

During `memex-sync install`, you'll see a prompt:

```
Auto-context (Brian Chesky mode):
  When you open Claude Code in a project, memex can inject 500-1500 tokens
  of relevant context so Claude knows what you were doing — without you
  having to ask. Adds a SessionStart hook to ~/.claude/settings.json.
  Other hooks (e.g. gstack) are preserved.

  Enable? [Y/n]
```

**Answer Y unless the user has stated privacy concerns** about Claude seeing context from their other AI conversations. Auto-context is the "10/10 magic moment" of memex — without it the install ships at base capability. Other hooks (gstack, custom) are preserved untouched.

For non-interactive flows (CI / scripts): pass `--auto-context yes` or `--yes`.

```sh
memex-sync status
```

`status` should print "daemon installed", "running (PID …)", "watching N sessions".

**Verify:** status output shows a non-zero PID. Also run `memex hook status` — should show `INSTALLED` if auto-context was accepted.

### 4. Backfill existing history

The daemon only catches NEW sessions going forward. To index everything already on disk:

```sh
memex-sync scan
```

This walks `~/.claude/projects/`, Cowork sessions, Cursor `state.vscdb`, and any configured Obsidian vaults once, ingesting whatever exists.

Optionally:
```sh
memex-sync backfill-projects
```

Tags older conversations with their `project_path` so `memex_list_projects` works on them.

**Verify:** after scan, `memex-sync status` shows a non-zero "ingested" count.

### 5. Offer Telegram-export capture (v0.10+)

After the core install is done, **proactively** ask:

> "Memex can also remember your Telegram chats — work, family, group chats, whatever you want indexed. Want me to set that up too? It's about 2 minutes."

If yes, run `memex_telegram_check` (MCP tool) or `memex telegram check` (CLI). The result tells you the user's state and the next step. Walk them through:

  - **No Telegram Desktop?** → Give the download URL from the check output. Wait for them to install + log in.
  - **Logged in <24h ago?** → Tell them: "Telegram blocks export for the first 24h. Wait ~X hours, then come back."
  - **Ready to export?** → Show the click-path: open chat → ⋮ menu (top-right) → "Export chat history" → format HTML or JSON → Export.

After the user exports, memex's daemon **auto-detects** the file in ~/Downloads/Telegram Desktop/ within ~7 seconds and stages it in `~/.memex/pending/`. Then:

  - Call `memex_telegram_pending` to list staged exports (chat name, msg count, date range).
  - **Present as a numbered list**, ask which to import. Accept indices, titles, or natural language ("import family and work, skip bank").
  - Call `memex_telegram_import` with selected indices/titles. The chat is added to the allow-list — future re-exports auto-merge via UNIQUE(msg_id).
  - For sensitive chats user doesn't want (Bank, Therapist, etc.), call `memex_telegram_skip`.

**⚠ Existing exports back-fill (v0.10.13+):** if the user had Telegram Desktop exports SITTING IN `~/Downloads/Telegram Desktop/` BEFORE memex was installed, the daemon's chokidar watcher may or may not detect them (race with FSEvents on first run). The fast remedy is `memex telegram scan` — it walks the Downloads dir and stages every `ChatExport_*` folder (HTML or JSON, both work). v0.10.13's `memex-sync install` also runs this scan automatically at the end, but if the user already installed pre-0.10.13, OR if `memex telegram pending` reports zero entries despite a populated Downloads dir, run `memex telegram scan` explicitly. Both HTML and JSON formats are supported — don't tell the user to re-export in JSON.

**Optional — clickable native macOS banner (v0.10.4+):** memex can fire a macOS notification the moment an export is staged. Default OFF for privacy. If the user wants this:

```sh
brew install terminal-notifier             # required for clickable banner
memex telegram notifications on            # enable; default: titles hidden
memex telegram notifications on --show-titles   # include chat names in banner
```

When enabled with `terminal-notifier`, clicking the banner opens (auto-detect priority): Claude Code CLI in a fresh Terminal tab → Claude Desktop → Terminal with `memex telegram pending`. The CLI launch path triggers the SessionStart hook → Brian Chesky moment. Override target: `memex telegram notifications target <auto|claude-cli|claude-desktop|terminal|none>`.

**Other useful Telegram commands** (no MCP-tool wiring needed):

```sh
memex telegram check          # diagnostic: Desktop? login age (24h)? watcher?
memex telegram open-pending   # one-shot: open pending list in best client
memex telegram mode auto      # auto-import allow-listed chats on re-export
memex telegram status         # decisions counts (allowed/skipped/blocked)
```

**Privacy is the core promise. Never auto-import. Always get explicit per-chat consent on the first round.**

If the user declines Telegram setup ("not now" / "skip"): say "OK, I'll skip Telegram. You can run `memex telegram check` anytime later to start." Don't push.

### 6. Tell the user what to do next

Tell the user to fully quit and reopen the MCP client (Cmd+Q on macOS) so it picks up the new memex tools.

**🌟 OFFER TO IMPORT THEIR EXISTING DATA RIGHT NOW (v0.10.12+):** before anything else, ask the user if they have a Telegram export or a chat-history file sitting somewhere on disk that they'd like to load. Many users come with a `result.json` they exported yesterday, sitting in `~/Downloads/` or a project folder. Don't make them figure out memex's "magic paths" — just ask:

> "Do you have any chat exports already on disk you want loaded into memex right now? Tell me the path (e.g. `~/Downloads/result.json` or `~/projects/memex/result.json`) — I'll handle it."

Then call `memex_import_file({path: "<their-path>"})`. The tool auto-detects format (Telegram JSON / HTML / Claude JSONL / Cowork JSONL), respects the privacy gate for Telegram (returns `needs_consent` with a preview — surface it, get user OK, retry with `force: true`), and gives you a structured result in one call. **Do not use bash `mv`/`cp` to shuffle files into `~/.memex/inbox/`** — that was the old workflow and burned ~10k tokens per file. Use `memex_import_file` instead.

**🌟 ALSO STRONGLY RECOMMEND THIS (v0.10.8+):** offer to run `memex web --open` for them right now. It's the single most magical post-install moment — a local browser tab opens at `http://127.0.0.1:8765` with 5 pages showing every conversation memex has captured, dialogue rendered as chat-bubbles, full-text searchable. Verbatim — not AI-summarized. Read-only, localhost-only, Ctrl+C to stop. Phrase it naturally, e.g.:

> "I can open a local web dashboard that lets you actually *see* what memex captured — every message, in chat-bubble form, searchable. It's just a browser tab on `localhost:8765`. Run it now? It's a way better demo than asking me search queries blind."

Then run `memex web --open` (in a backgrounded shell if your shell wrapper supports it — otherwise tell the user to run it themselves in another terminal). Wait for them to react before continuing.

**After that, suggest other ways to confirm end-to-end:**
- "show me what memex has in memory" → triggers `memex_overview`
- "what projects has memex captured" → triggers `memex_list_projects`
- "search memex for [recent topic]" → triggers `memex_search`
- "save https://en.wikipedia.org/wiki/As_We_May_Think to memex" → triggers `memex_store_document` and teaches the user that URL-saving exists (v0.6+)
- **Open Claude Code in any project the user worked on recently** — the SessionStart auto-context (v0.8+) should kick in and Claude will mention prior work _before_ the user types anything. This is the "Brian Chesky moment" — the magical-first-impression of memex.
- **(if Telegram was set up)** `memex telegram check` — confirms daemon's Telegram-Downloads watcher is active and shows the user's full capture pipeline state.

These confirm everything works end-to-end.

**Brian Chesky moment beyond Claude Code (v0.10.7+):** the SessionStart hook works only in Claude Code CLI. But starting v0.10.7, the same proactive behaviour is taught to agents in Cursor / Cline / Continue / Zed / Claude Desktop via SERVER_INSTRUCTIONS — these agents call `memex_overview` automatically on first interaction, read its `telegram_pending` field, and surface pending exports in their first reply. Slightly higher latency (one MCP roundtrip vs hook's instant inject), but same UX.

**CLI fallback (v0.7+):** if the MCP integration doesn't pick up in the user's client for any reason, tell them they can verify memex from the terminal directly — same binary, no MCP needed:

```sh
memex overview      # confirms memex itself is healthy
memex search "foo"  # FTS search from CLI
memex list          # list conversations
memex --help        # command reference
```

This is also useful for agents without native MCP support (OpenCode + Kimi, plain shell scripts, CI pipelines) — they can shell out to `memex` directly.

## Safety rules — read before starting

- If `node` or `npm` aren't installed, stop and tell the user to install Node.js (recommend nvm.sh or `brew install node`). Don't try to install Node yourself.
- Never run `rm`, `sudo`, or anything destructive without explicit confirmation from the user.
- Show every command before running it. If the user says "no" or "stop", halt and explain.
- If a step fails, do NOT auto-retry or auto-fix — tell the user what failed and ask how to proceed.
- When editing the MCP config, always preserve existing entries. If you can't merge cleanly, abort and tell the user.
- Do NOT modify the host application's settings beyond adding the memex entry to its `mcpServers` config. Specifically: do not redirect where Cursor / Claude Code / any other tool saves its data. Memex reads from each tool's native location automatically. The only file you should touch is the MCP config file listed in step 2.
- Stay focused on the main install task. If sidetracked into a sub-task (changing workspace, fixing an unrelated config issue, looking up something else), once it's done you MUST return to the memex install and explicitly tell the user: "OK, back to memex install. We were at step N — should I continue?". Don't go silent after a side task. Don't assume the user wants to abandon the install — always confirm.

## Begin

Greet the user, confirm which MCP client you're running inside, and run the Discovery checks before any install actions. After Discovery, **propose the fast path (curl one-liner) first** — it covers ~90% of cases in one shot. After the core install completes, **proactively offer Telegram-export capture (step 5)** unless the user has already declined. Only fall back to the manual flow if the user objects, the script fails, or you're inside a GUI client where you'll still need to do step 2 manually after the script runs.
