# Litehost Connect — Agent Skill

Agent skill for deploying and managing projects on [litehost.io](https://litehost.io) through the Connect API. Works with Claude Code, Cursor, and any agent framework that supports file-based skill loading.

## What's inside

```
SKILL.md                ← Entry point: pick the path (no key / signed in / sign in once), routing
scripts/
  litehost.sh           ← Keeps the API key in a file between commands; sign-in, temp upload, api calls
actions/
  otp-sign-in.md        ← POST /v1/auth/otp/request + /verify  (keyless auth)
  temp-project.md       ← POST /v1/projects/temp + /claim       (no auth needed)
  create-project.md     ← POST /v1/projects
  replace-project.md    ← PUT  /v1/projects/{id}                (push new files)
  update-project.md     ← PATCH /v1/projects/{id}               (change settings)
  list-projects.md      ← GET  /v1/projects
  get-project.md        ← GET  /v1/projects/{id}
  link-opens.md         ← GET  /v1/projects/{id}/analytics      (did the client open it?)
  qr-code.md            ← GET  /qr/{id}.png | .svg              (QR to print, no key needed)
  deployment-history.md ← GET  /v1/projects/{id}/status
  delete-project.md     ← DELETE /v1/projects/{id}
  archive-project.md    ← POST /v1/projects/{id}/archive
  unarchive-project.md  ← POST /v1/projects/{id}/unarchive
  domains.md            ← GET  /v1/domains, /v1/domains/{id}, assign/remove
  workspaces.md         ← CRUD /v1/workspaces
  get-user.md           ← GET  /v1/user (plan, quota)
utils/
  auth.md               ← API key resolution (dashboard keys + OTP)
  errors.md             ← Error code reference + required agent actions
  quotas.md             ← Limit-reached handling sequence
```

## Prerequisites

None to publish: without a key the skill uploads with `POST /v1/projects/temp` and gives you a
`claimUrl` to keep the project from your browser (Google or email sign-in).

To let the agent manage your projects, it signs you in **once** with an email code and saves the
key to `~/.config/litehost/credentials.json` (permissions 600). The key renews while in use, so you
are not asked for a code again. You can also provide a permanent key from
[litehost.io/dashboard → Integrations](https://litehost.io/dashboard):

```bash
scripts/litehost.sh save-key lh_live_...
# or, in environments that keep env vars between commands:
export LITEHOST_API_KEY="lh_live_..."
```

Agents also get a short guide at https://connect.litehost.io/llms.txt.

---

## Where to use it

| Where | Use |
|---|---|
| Claude Code, Cursor, Codex, other agents on your computer | This skill (`npx skills add litehost-io/skills`) |
| Chat apps: claude.ai, the Claude desktop and mobile apps, ChatGPT, Meta Muse | The **Litehost connector**, not this skill |

Chat apps run skills in a sandbox that can only reach a list of allowed domains, so this skill
cannot talk to Litehost there unless you change settings and open a new chat. The connector runs on
Litehost's side instead: nothing to install, nothing to allow.

**Add the connector in Claude:** Settings → Connectors → Add custom connector → paste
`https://connect.litehost.io/mcp` → sign in with Google or email. Then ask in any chat, e.g.
"Share this PDF with my client" or "Make a page with my menu and give me a QR code".

**If you still want the skill in claude.ai:** upload it in Settings → Capabilities (Skills), add
`connect.litehost.io` to the domains code execution may reach, and start a **new chat**: the setting
does not apply to a chat that is already open. If the domain is not allowed, the skill says so
(`NETWORK_BLOCKED`) and points to the connector instead of failing with a raw error.

---

## Quick Install

```bash
npx skills add litehost-io/skills
```

This downloads the skill and registers it with your agent. Works with Claude Code, Cursor, and any compatible agent framework.

OpenClaw:

```bash
clawhub install litehost-connect
```

The MCP connector is also listed in the [MCP Registry](https://registry.modelcontextprotocol.io) as
`io.github.Litehost-io/litehost` (`mcp/server.json`).

---

## Manual Installation

If you prefer to install manually or need to customize the setup:

### Claude Code

**1. Download the skill files**

```bash
curl -L https://github.com/Litehost-io/skills/archive/refs/heads/main.tar.gz | tar -xz
mv skills-main ~/.claude/skills/litehost-connect
```

**2. Register with your agent (manual step)**

Open your project's `CLAUDE.md` and add the following snippet yourself:

```
## Skills

When the user asks to deploy, host, publish, or manage a project on Litehost,
read and follow the skill at ~/.claude/skills/litehost-connect/SKILL.md.
```

### Cursor

**1. Download the skill files**

```bash
curl -L https://github.com/Litehost-io/skills/archive/refs/heads/main.tar.gz | tar -xz
mv skills-main .cursor/skills/litehost-connect
```

**2. Add a rule file at `.cursor/rules/litehost.mdc`**

```markdown
---
description: Deploy and manage projects on litehost.io
globs:
alwaysApply: false
---

When the user asks to deploy, host, publish, update, or manage a project on Litehost,
read and follow the skill at `.cursor/skills/litehost-connect/SKILL.md`.
```

### General Agents

1. Download and extract the skill files into a path the agent can read.
2. Load `SKILL.md` as the entry point when the user's intent matches deployment or hosting.
3. The agent reads sub-files (`actions/*.md`, `utils/*.md`) on demand — each is self-contained with endpoint, parameters, curl examples, response shapes, and error handling.

Add this to your agent's system prompt or tool description:

```
When the user asks to deploy, host, or manage a project on Litehost, read
<path-to>/SKILL.md and follow its instructions. It references sub-files in
actions/ and utils/ — read each one as needed before making API calls.
All requests go to https://connect.litehost.io with Bearer token auth.
```

---

## API Reference

Base URL: `https://connect.litehost.io`
