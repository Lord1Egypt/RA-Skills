# Example dialogues

Sample interactions when the user invokes this skill. These show typical happy paths and how the skill handles common edge cases.

> **Note (v1.1+):** The skill now leads with the **fast-path one-liner** (`curl -fsSL https://memex.parallelclaw.ai/install.sh | bash`) after Discovery — see Example 0 below. The legacy five-step examples (1–5 below) stay as the fallback when the agent is inside a GUI client (Cursor / Cline / Continue / Zed — still need step 2 manually after the script), the user declines curl, or the script fails.

---

## Example 0 · Fast path on Claude Code CLI (v1.1+)

> **User:** install memex
>
> **Agent:** 👋 You're running inside Claude Code CLI. Let me run a quick discovery first.
>
> ```
> ✓ Found Claude Code data at ~/.claude/projects/ (14 sessions)
> ✓ Found Cowork sessions (5 subagent transcripts)
> ✗ Cursor data not found
> ✗ Continue / Zed not found
> ```
>
> After install, memex will auto-index conversations from: **Claude Code, Cowork**. v0.10+ also auto-detects Telegram Desktop exports — when you export a chat, I'll ask which to import.
>
> The fast path is a single hosted bash script that does **npm install (with EACCES auto-fix), daemon setup, Brian Chesky auto-context hook, history backfill, and `claude mcp add memex`** all in one go. Idempotent. Want me to run:
>
> ```sh
> curl -fsSL https://memex.parallelclaw.ai/install.sh | bash
> ```
>
> **User:** ok
>
> **Agent:** [runs the curl command, streams output]
>
> ```
> ▸ memex one-line installer
> ▸ Node v20.11.1 — ok
> ▸ Installing memex-mvp from npm...
> ✓ memex 0.9.0 ready at /Users/you/.npm-global/bin/memex
> ▸ Installing memex-sync (LaunchAgent + auto-context hook)...
> ✓ daemon running (PID 41872)
> ✓ Brian Chesky auto-context hook added to ~/.claude/settings.json
> ▸ Backfilling history (memex-sync scan)...
> ✓ 87 conversations indexed
> ▸ Wiring MCP into Claude Code...
> ✓ claude mcp add memex — done
> ▸ All set. Quit Claude Code (Cmd+Q) and reopen any project. Memex will inject prior context before your first message.
> ```
>
> All five steps done in ~25 seconds. Quit Claude Code (Cmd+Q) and reopen — when you open any project you've worked in, memex will inject relevant context before you even type. Try: `memex overview` from terminal to confirm.

---

## Example 1 · Happy path on a fresh Cursor install

> **User:** install memex
>
> **Agent:** 👋 You're running inside Cursor. Let me run a quick discovery before any install actions...
>
> ```
> ✓ Found Claude Code data at ~/.claude/projects/ (12 sessions)
> ✓ Found Cowork sessions (4 subagent transcripts)
> ✓ Cursor data found — I'll write MCP config to ~/.cursor/mcp.json
> ✗ Continue config not found
> ✗ Zed config not found
> ```
>
> After install, memex will auto-index conversations from: **Claude Code, Cowork, Cursor**. v0.10+ Telegram capture also kicks in automatically — when you export a chat from Telegram Desktop, I'll ask which to import. If you also use Obsidian, we can wire that vault in after.
>
> Ready to proceed with Step 1?
>
> **User:** yes
>
> **Agent:** Running `npm install -g memex-mvp`...
>
> ```
> + memex-mvp@0.5.4
> ```
>
> ✓ Memex installed. Verifying: `which memex` → `/usr/local/bin/memex`. Good.
>
> Step 2: I'm about to merge a new entry into your `~/.cursor/mcp.json`. Here's the diff:
>
> ```diff
>   {
>     "mcpServers": {
>       "github": { ... },
> +     "memex": {
> +       "command": "/usr/local/bin/memex"
> +     }
>     }
>   }
> ```
>
> Looks correct? (Y/n)
>
> **User:** yes
>
> **Agent:** ✓ Config saved.
>
> Step 3: `memex-sync install` — sets up the macOS LaunchAgent that auto-captures new Claude Code / Cowork / Cursor sessions...
>
> ```
> ✓ memex-sync installed
> ✓ daemon running (PID 47291)
> ✓ watching 12 sessions across 3 source roots
> ```
>
> Step 4: `memex-sync scan` to backfill existing history. This indexes everything already on your disk — might take 30-90 seconds...
>
> ```
> ingested 847 messages from 12 conversations
> ```
>
> ✓ All done. **Restart Cursor (Cmd+Q + reopen)** so it picks up the new memex tools. After restart, try:
>
> - "what does memex have in memory?"
> - "search memex for [a recent topic you worked on]"
> - "list my memex projects"

---

## Example 2 · EACCES recovery (macOS system Node) — recommend B by default

> **User:** install memex
>
> **Agent:** [runs discovery, gets user OK] Step 1: `npm install -g memex-mvp`...
>
> ```
> npm error code EACCES
> npm error path: '/usr/local/lib/node_modules/memex-mvp'
> ```
>
> Hit EACCES — your Node is installed in a system directory that npm can't write to without admin rights. Two fixes:
>
> **A)** Quick: `sudo npm install -g memex-mvp` — one-time, requires your password
>
> **B)** Permanent fix: I'll move npm's install location to your home directory. After this, no `npm install -g` will ever ask for sudo again, for any package. Five commands, one-time.
>
> I recommend **B** — it's a permanent improvement that benefits all your future Node tools, not just memex. **Proceed with B?**
>
> **User:** ok
>
> **Agent:** Running the 5 prefix-fix commands:
>
> ```sh
> mkdir -p ~/.npm-global
> npm config set prefix ~/.npm-global
> echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.zshrc
> source ~/.zshrc
> npm install -g memex-mvp
> ```
>
> ✓ Done. Verifying:
>
> ```
> which memex → /Users/macbook/.npm-global/bin/memex
> ```
>
> Now continuing to Step 2 with this path...

---

## Example 3 · Wants only Claude Code, not the daemon

> **User:** install memex but skip the daemon
>
> **Agent:** Sure — that means memex will be available as a tool, but new sessions won't be auto-captured. You'll need to run `memex-sync scan` manually whenever you want to index recent sessions. Got it?
>
> **User:** yes
>
> **Agent:** [runs Steps 1, 2, 4 — skipping `memex-sync install` in Step 3]
>
> ✓ Memex installed, MCP config wired, backfill complete (847 messages from existing sessions).
>
> Since you skipped the daemon, here's how to refresh memex going forward:
> ```sh
> memex-sync scan
> ```
>
> You can install the daemon any time later: `memex-sync install`.

---

## Example 4 · Existing memex install detected

> **User:** install memex
>
> **Agent:** Quick check: `which memex` → `/usr/local/bin/memex`. You already have memex installed.
>
> Running `memex-sync status`:
> ```
> daemon running (PID 47291), watching 12 sessions
> last capture: 4 minutes ago
> ```
>
> Memex is working. What would you like to do?
>
> - **Reinstall** (e.g. to update to the latest version): I can run `npm install -g memex-mvp@latest`
> - **Add a new source** (Obsidian vault, Telegram exports, etc.)
> - **Add memex to another MCP client** (you have it in Cursor; want it in Cline / Continue / Zed too?)
> - **Nothing** — already good

---

## Example 5 · Web-only agent (no shell access)

> **User:** install memex
>
> **Agent:** I see you're running me through claude.ai web — I don't have access to your machine's shell, so I can't run `npm install` or write files for you.
>
> You have three options to install memex:
>
> 1. **CLI agents** (best UX): Open Claude Code, Cursor, Cline, Continue, or Zed and ask me there. Those have shell access and will run this skill end-to-end.
>
> 2. **Manual install** (~5 minutes, you run the commands): Follow https://memex.parallelclaw.ai/#quickstart — 4 steps in your terminal.
>
> 3. **One-liner from terminal**:
> ```sh
> npm install -g memex-mvp
> memex-sync install
> ```
> Then add `{"mcpServers": {"memex": {"command": "$(which memex)"}}}` to your MCP client's config file. Details: https://memex.parallelclaw.ai
>
> Which path works for you?

---

---

## Example 6 · Right after install — testing URL save (v0.6+)

> **User:** save https://en.wikipedia.org/wiki/As_We_May_Think to memex
>
> **Agent:** Fetching the page with WebFetch...
>
> ```
> ✓ Got 12,847 chars from en.wikipedia.org
> ```
>
> Calling `memex_store_document(content, url=https://en.wikipedia.org/wiki/As_We_May_Think, title=auto)`...
>
> ```
> ✓ stored
>   conversation_id: web-d3b07a384d1b
>   title: "As We May Think"
>   length: 12,847 chars
>   warnings: []
> ```
>
> Saved. Try searching it now: *"search memex for memex Bush 1945"* — the article will show up alongside any AI chats where you discussed it.
>
> 💡 By the way, you can save any URL this way — Perplexity threads, blog posts, ChatGPT shares, Twitter threads, GitHub discussions. For Perplexity specifically, the thread must be made Public first (Share → Public link). For Cloudflare-protected sites, memex auto-falls back through `r.jina.ai` proxy.

---

---

## Example 7 · MCP didn't connect — agent recommends CLI fallback (v0.7+)

> **User:** ok, I installed memex. but when I ask Claude "show me what memex has", nothing happens.
>
> **Agent:** Could be a MCP-config issue with your Claude client — let's verify memex itself is healthy first, separately from MCP:
>
> ```sh
> memex overview
> ```
>
> ```
> memex corpus snapshot
>
> Total: 1,247 messages in 23 conversations
>
> By source:
>   claude-code           742 msgs · 18 chats · 2026-04-06 → 2026-05-15
>   claude-cowork         312 msgs ·  4 chats · 2026-04-06 → 2026-05-07
>   ...
> ```
>
> Memex itself is healthy — your data is there. The problem is the MCP wiring in your Claude client.
>
> Try `memex search "recent topic you discussed"` directly in the terminal — if that returns hits, you've got a fully-working memex; it's just not exposed to your Claude session yet.
>
> Then check your Claude MCP config (`~/.claude/config.json` or equivalent) — the `memex` entry should have an absolute path. Run `which memex` to get it, and verify it's there. If you need to re-do the wiring, ask me again — I'll re-run step 2 of the install.

---

## What these examples illustrate about the skill's behavior

- **Always discover first**, then ask for confirmation before any write action
- **Show every command** before running it; show diffs for config edits
- **Recommend the better default** with a clear reason (e.g. Option B for EACCES) instead of forcing the user to weigh both options blind. Fall back to alternatives only if explicitly chosen.
- **Detect and adapt** to existing installs, missing prerequisites, partial setups
- **Refuse gracefully** when running in a context where the install can't actually work (web-only agents)

If you see the skill *not* doing one of these things, that's a bug — report it at https://github.com/parallelclaw/memex-mvp/issues.
