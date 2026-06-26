---
name: openclaw-version-monitor
description: Check OpenClaw release notes from GitHub, show highlights and categorized changes translated to the user's language.
user-invocable: true
metadata: {"openclaw": {"emoji": "📦", "primaryEnv": "GITHUB_TOKEN"}}
---

# OpenClaw Version Monitor

Fetch and present OpenClaw release notes in the user's language.

## When to use

Use this skill immediately when the user mentions any of:
- "OpenClaw latest version", "what's new in OpenClaw", "OpenClaw updates"
- "OpenClaw changelog", "OpenClaw release notes"
- A specific OpenClaw version (e.g. "what changed in v2026.3.31")
- "compare OpenClaw versions", "upgrade notes"
- "openclaw 最新版本", "openclaw 更新了什么"

Do **not** use for: OpenClaw installation help, configuration questions, or unrelated GitHub repos.

## Data source

All data comes from the GitHub REST API for `openclaw/openclaw`:

```bash
# Latest stable release
curl -s https://api.github.com/repos/openclaw/openclaw/releases/latest

# Latest release including pre-releases
curl -s "https://api.github.com/repos/openclaw/openclaw/releases?per_page=1"

# Recent N releases
curl -s "https://api.github.com/repos/openclaw/openclaw/releases?per_page=10"

# Specific version (always add v prefix)
curl -s https://api.github.com/repos/openclaw/openclaw/releases/tags/v2026.3.31
```

If `GITHUB_TOKEN` is set, add `-H "Authorization: token $GITHUB_TOKEN"` to raise the rate limit from 60 to 5000 requests/hour.

Extract these fields from the JSON response: `tag_name`, `published_at`, `prerelease`, `author.login`, `html_url`, `body`.

## Release notes structure

The `body` field uses this markdown structure:

```
### Breaking
- Module/area: description...

### Changes
- Module/area: description...

### Fixes
- Module/area: description...
```

Categorize entries by `###` heading:
- **Breaking** → 🚨 Breaking changes
- **Changes** / **Features** → ✨ New features & improvements
- **Fixes** / **Bug** → 🐛 Bug fixes

## Output rules

### Language
- Detect the user's language from their message.
- If the user writes in English, output in English — no translation needed, just clean up and condense.
- If the user writes in any other language (Chinese, Japanese, Korean, etc.), translate all entries into that language.

### Translation guidelines
- **Keep module prefixes as-is** (e.g. Gateway/auth, Agents/MCP, Plugin SDK)
- **Keep technical terms in English** (API, OAuth, WebSocket, MCP, SQLite, SDK, CLI, Docker, SecretRef, ETag)
- **Strip noise**: remove trailing `(#12345)` issue numbers and `Thanks @username` credits
- **Condense**: drop verbose subordinate clauses (so..., while..., instead of...), keep only the core change

### Default output (compact mode)

Show **only highlights + stats + interactive prompt**. Do NOT dump the full list unless asked.

```
# OpenClaw v2026.3.31

- Released: 2026-03-31 20:54 UTC
- Author: steipete
- Link: https://github.com/openclaw/openclaw/releases/tag/v2026.3.31

## ⭐ Highlights
1. **Background tasks overhaul** — Unified into a shared control plane managing ACP, subagents, cron, and background CLI via SQLite ledger
2. **Plugin security scan now fails closed** — Dangerous-code scan failures block installs by default; requires explicit --dangerously-force-unsafe-install
3. **Remote MCP HTTP/SSE support** — mcp.servers now accepts remote HTTP/SSE servers with auth headers and secure credential editing
4. **QQ Bot channel plugin** — New bundled channel plugin with multi-account setup, slash commands, reminders, and media support
5. **Gateway auth hardening** — trusted-proxy rejects mixed shared-token configs; node commands/events stay disabled until pairing is approved

**95 changes total** (🚨 6 breaking · ✨ 29 new · 🐛 60 fixes)

---
💡 You can:
- Tell me what you care about (e.g. "MCP changes", "security fixes") and I'll filter
- Say "full list" to see everything
- Say "breaking changes" to see only upgrade-critical items
```

(Translate the above into the user's language as needed.)

### Filtered output (when user asks about a topic)

Search all entries for the user's keyword, then show only matching items grouped by category:

```
## 🔍 MCP-related changes (3 items)

**New:**
- Agents/MCP: Bundle MCP tools with provider-safe names, support streamable-http transport and per-server timeouts
- MCP: Add remote HTTP/SSE server support for mcp.servers with auth headers

**Fixes:**
- Agents/OpenAI Responses: Normalize raw bundled MCP tool schemas on WebSocket/Responses path
```

### Full list (when user asks for it)

Show all entries under each category header with counts:

```
## 🚨 Breaking changes (6)
- ...

## ✨ New features & improvements (29)
- ...

## 🐛 Bug fixes (60)
- ...
```

### Version list

```
# OpenClaw recent releases

| Version | Date | Type | Changes |
|---------|------|------|---------|
| v2026.3.31 | 2026-03-31 | Stable | 95 |
| v2026.3.28 | 2026-03-29 | Stable | 120 |
| v2026.3.24 | 2026-03-25 | Stable | 33 |
```

### Version comparison

Show each version's highlights side by side, then a stats table:

```
## 📊 Comparison

| Category | v2026.3.28 | v2026.3.31 |
|----------|-----------|-----------|
| Breaking | 2 | 6 |
| New/Improved | 21 | 29 |
| Fixes | 97 | 60 |
```

## Highlight selection

Pick the 5 most important changes for the highlights section. Priority order:
1. Breaking changes (users must know before upgrading)
2. Architecture-level new features (e.g. task system overhaul)
3. User-facing new features (e.g. new channel plugin, new CLI command)
4. Critical security fixes

## Error handling

| Situation | Action |
|-----------|--------|
| HTTP 403 | API rate limited — suggest setting GITHUB_TOKEN |
| HTTP 404 | Version not found — list recent available versions |
| Network failure | Suggest checking network connection |
| Empty body | Link user to the GitHub release page directly |
| Missing v prefix | Auto-add it: `2026.3.31` → `v2026.3.31` |
