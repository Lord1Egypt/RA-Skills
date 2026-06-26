# Agent Compatibility Matrix

> How to mount and run `ifq-design-skills` across every major agent runtime. The skill follows the **Anthropic Agent Skills** convention and adds Hermes and ClawHub metadata blocks without breaking any runtime. ClawHub is the recommended install channel; GitHub installs are for local development and non-OpenClaw runtimes.

The skill itself uses neutral verbs (`read file`, `write file`, `run command`, `web search`, `take screenshot`). This file maps those verbs to each runtime's actual tool surface and documents install paths and slash commands.

## Universal prerequisites — ClawHub-safe default is zero-install

```
Tier 0 · ClawHub-safe core
  Node ≥ 18.17                  # npm run validate / npm run pack
  filesystem + shell            # workspace-scoped only

Tier 1 · Optional browser context
  browser/web_fetch             # facts, assets, screenshots in host agent

Tier 2 · Full GitHub repo only
  Python / Playwright / ffmpeg / pptxgenjs / pdf-lib / sharp
  # used for deep screenshots, MP4/GIF, PDF, and PPTX automation
```

The ClawHub-safe bundle intentionally ships with no dependency tree and no install hooks. Use the full GitHub repo only when a task explicitly needs local export automation.

## Recommended install path — ClawHub first

```bash
openclaw skills install ifq-design-skills
openclaw skills info ifq-design-skills
openclaw skills check ifq-design-skills
```

## Shared local development path

Hermes documents `~/.agents/skills/` as the cross-tool shared external directory. Install there once and every agent below can point at the same copy.

```bash
mkdir -p ~/.agents/skills
git clone https://github.com/peixl/ifq-design-skills ~/.agents/skills/ifq-design-skills
```

Each agent's section below shows how to register that shared path or install an independent copy.

---

## 1 · Claude Code (Anthropic)

Claude Code honors the Anthropic Agent Skills spec natively. Mount at either path:

```bash
# Personal (visible only to you)
ln -s ~/.agents/skills/ifq-design-skills ~/.claude/skills/ifq-design-skills

# Project-scoped (checked into the repo)
ln -s ~/.agents/skills/ifq-design-skills .claude/skills/ifq-design-skills
```

**Discovery** is automatic. Claude Code scans `~/.claude/skills/` and `.claude/skills/`, loads the frontmatter (`name`, `description`) into the system prompt, and reads `SKILL.md` only when the description matches the user request.

| Neutral verb | Claude Code tool |
|---|---|
| read file | `Read` |
| write file | `Write`, `Edit` |
| run command | `Bash` |
| web search | `WebSearch`, `WebFetch` |
| verify / screenshot | host browser/screenshot tool; full repo can additionally run `scripts/verify.py` |

No config changes required.

---

## 2 · Hermes (Nous Research)

Hermes is the most feature-rich runtime. It understands the extended frontmatter (`platforms`, `metadata.hermes`, `fallback_for_toolsets`, `required_environment_variables`, `config`) and ships a fully integrated skills hub.

### Install — three equivalent routes

```bash
# Route A — direct GitHub install via the Hermes skills hub
hermes skills install github:peixl/ifq-design-skills

# Route B — via ClawHub marketplace
hermes skills install clawhub:peixl/ifq-design-skills

# Route C — point Hermes at the shared external dir
# edit ~/.hermes/config.yaml:
#   skills:
#     external_dirs:
#       - ~/.agents/skills
```

### Slash commands (CLI and every messaging surface)

```
/ifq-design-skills make a 12-slide editorial keynote about AI agents
/ifq-design-skills design a dashboard for the quarterly launch review
/ifq-design-skills critique this landing page and propose 3 directions
/ifq-design-skills                                    # loads the skill, asks what you need
```

### Progressive disclosure (native)

Hermes loads this skill in three levels, following the Anthropic Agent Skills progressive-disclosure convention:

- **Level 0** — `skills_list()` returns `{name, description, category}` (~3 k tokens total)
- **Level 1** — `skill_view("ifq-design-skills")` returns the full `SKILL.md`
- **Level 2** — `skill_view("ifq-design-skills", "references/modes.md")` pulls one reference on demand

### Tool mapping

| Neutral verb | Hermes tool |
|---|---|
| read file | `file.read`, `skill_view` |
| write file | `file.write` |
| run command | `terminal.run`, `execute_code` |
| web search | `web.search`, `web.fetch` (or `duckduckgo_search` fallback) |
| verify / screenshot | host browser/screenshot tool; full repo can additionally run `scripts/verify.py` |

### Conditional activation

This skill does not declare `fallback_for_toolsets` because design output is its primary job, not a fallback. If browser, `ffmpeg`, or Chromium are unavailable, the ClawHub-safe bundle stays in HTML-only mode; export automation belongs to the full GitHub repo.

### Agent-managed patches

When the Hermes agent discovers a non-trivial workflow while using this skill, it can patch the skill via the `skill_manage` tool:

```
skill_manage action=patch name=ifq-design-skills \
  old_string="..." new_string="..."
```

Prefer `patch` over `edit` for small fixes — it is more token-efficient.

### Reset after manual edits

If you hand-edit the installed copy and later want to restore the pristine version:

```bash
hermes skills reset ifq-design-skills --restore
```

---

## 3 · OpenClaw + ClawHub

OpenClaw (2026.4+) has a first-class plugin system; [ClawHub](https://clawhub.ai) is its marketplace. Hermes also integrates ClawHub as a source.

This skill ships a dedicated `metadata.openclaw` block in `SKILL.md` frontmatter plus a root-level [`clawhub.json`](../clawhub.json) manifest, so OpenClaw gets triggers, permissions, and the neutral-verb → tool crosswalk automatically.

### Install

```bash
# Route A — via ClawHub marketplace (recommended)
openclaw skills install ifq-design-skills

# Route B — symlink the shared agents dir
ln -s ~/.agents/skills/ifq-design-skills ~/.openclaw/skills/ifq-design-skills

# Route C — install a locally-built bundle
openclaw skills install /path/to/ifq-design-clawhub-YYYY-MM-DD.tar.gz
```

Verify:

```bash
openclaw skills list                       # should show ifq-design-skills as ready
openclaw skills info ifq-design-skills     # dumps frontmatter + openclaw metadata
openclaw skills check ifq-design-skills    # reports missing plugins/permissions
```

### Config — `~/.openclaw/openclaw.json`

```json
{
  "plugins": {
    "allow": ["filesystem", "shell", "browser", "ifq-design-skills"],
    "entries": {
      "filesystem": { "enabled": true },
      "shell":      { "enabled": true },
      "browser":    { "enabled": true },
      "ifq-design-skills": {
        "enabled": true,
        "path": "~/.openclaw/skills/ifq-design-skills",
        "entrypoint": "SKILL.md",
        "manifest": "clawhub.json"
      }
    }
  },
  "gateway": { "mode": "local" }
}
```

Then reload and confirm:

```bash
openclaw config reload
openclaw gateway restart
openclaw gateway status         # expect: ok, mode=local
openclaw skills check ifq-design-skills
```

### Tool mapping

Declared in `metadata.openclaw.tool_map` (frontmatter) and `clawhub.json`. Repeated here for humans:

| Neutral verb | OpenClaw tool | Notes |
|---|---|---|
| `read_file`    | `filesystem/read`  | workspace-scoped |
| `write_file`   | `filesystem/write` | workspace-scoped |
| `list_dir`     | `filesystem/list`  | — |
| `run_command`  | `shell/exec`       | used for `npm run validate`, `npm run pack` |
| `web_search`   | `browser/search`   | optional — used when fetching references |
| `web_fetch`    | `browser/fetch`    | optional — Google Fonts / image CDNs |
| `screenshot`   | browser/screenshot-or-host-tool | full repo can additionally run `python scripts/verify.py` |

### Minimum permissions

- `filesystem` — read + write, **workspace only** (never touches `~/` or `/etc`).
- `shell` — execute bundled Node scripts inside the workspace (`npm run validate`, `npm run pack`). No system installs; Python / Playwright helpers are full-repo opt-ins only.
- `browser` *(optional)* — outbound HTTPS to Google Fonts + image CDNs (read-only). No inbound servers.
- `memory` *(optional)* — looks up `personal-asset-index.json` for user brand assets.

### Known issues and fixes

- `openclaw skills check` reports `missing gateway.mode` → set `gateway.mode: "local"` and restart.
- A tool returns `unavailable` → add its plugin id to `plugins.allow` and set `entries.<id>.enabled: true`.
- `openclaw skills install` fails with `non-text files: kilo, ORIG_HEAD, config` → install from the packed `.tar.gz` instead of the raw folder, or ensure `clawhub.ignore.txt` excludes `.git/`. Build via `npm run pack`.
- ClawHub web publish flags `.clawignore` itself as `non-text files` → remove the legacy dotfile and keep `clawhub.ignore.txt` instead.
- `EACCES` on global npm install → follow the OpenClaw install guide at https://github.com/peixl/ifq-design-skills (uses user-level `npm_config_cache` / `--prefix`).

### Publishing to ClawHub

```bash
# 1. Validate
npm run validate

# 2. Produce a clean, OpenClaw-verified bundle
npm run pack
# → ../ifq-design-clawhub-YYYY-MM-DD.tar.gz

# 3. Install locally to test
openclaw skills install ../ifq-design-clawhub-*.tar.gz

# 4. Publish via Hermes bridge or the ClawHub web publisher
hermes skills publish ~/.agents/skills/ifq-design-skills --to clawhub
# or https://clawhub.ai/publish/skill
```

See also [`clawhub-publishing.md`](clawhub-publishing.md) for the publish checklist.

---

## 4 · Codex CLI (OpenAI)

Codex has no native skill concept but honors `AGENTS.md` plus any markdown the user points it at.

```bash
ln -s ~/.agents/skills/ifq-design-skills ~/.codex/skills/ifq-design-skills
```

Add to your project or global `AGENTS.md`:

```markdown
## Skills

When the user asks for a visual design deliverable (prototype, deck, motion,
infographic, dashboard, whitepaper, changelog, card, social cover, or brand
system) or wants export planning (mp4/gif/pptx/pdf/svg), read
`~/.codex/skills/ifq-design-skills/SKILL.md` first and follow its routing.
```

| Neutral verb | Codex CLI tool |
|---|---|
| read file | `apply_patch` read / `shell` → `cat` |
| write file | `apply_patch` |
| run command | `shell` |
| web search | not native — user supplies URLs |
| verify / screenshot | host browser/screenshot tool; full repo can additionally run `scripts/verify.py` |

Optional env hint so Codex finds the skill quickly:

```bash
export CODEX_SKILLS_PATH="$HOME/.codex/skills"
```

---

## 5 · CodeBuddy (Tencent)

CodeBuddy follows an AGENTS.md-style discovery model with a `file.*` / `shell.*` / `web.*` tool surface. The skill's frontmatter includes a `metadata.codebuddy` block so CodeBuddy gets the tool crosswalk for free.

### Install

```bash
# Route A — shared agents dir
ln -s ~/.agents/skills/ifq-design-skills ~/.codebuddy/skills/ifq-design-skills

# Route B — independent clone
git clone https://github.com/peixl/ifq-design-skills ~/.codebuddy/skills/ifq-design-skills
```

### Discovery

CodeBuddy scans `~/.codebuddy/skills/` and the workspace's `AGENTS.md`. Add to your project or global `AGENTS.md`:

```markdown
## Skills

When the user asks for a visual design deliverable (prototype, deck, motion,
infographic, dashboard, whitepaper, changelog, card, social cover, or brand
system), read `~/.codebuddy/skills/ifq-design-skills/SKILL.md` first and follow
its routing.
```

The repo also ships a root [`AGENTS.md`](../AGENTS.md) so any AGENTS.md-aware runtime (CodeBuddy, Codex, Continue, Aider) picks the skill up without extra config.

### Tool mapping

| Neutral verb | CodeBuddy tool |
|---|---|
| read file | `file.read` |
| write file | `file.write` |
| list dir | `file.list` |
| run command | `shell.run` |
| web search | `web.search` |
| web fetch | `web.fetch` |
| verify / screenshot | host browser/screenshot tool; full repo can additionally run `scripts/verify.py` |

No config changes required beyond adding the skill folder to CodeBuddy's `skills_paths` (default already includes `~/.codebuddy/skills/`).

---

## 6 · Cursor

Cursor does not load skills automatically but honors `@file` pins in chat.

```bash
git clone https://github.com/peixl/ifq-design-skills
# or one-line via ClawHub
openclaw skills install ifq-design-skills
```

In Cursor chat, pin the skill at the start of the conversation:

```
@ifq-design-skills/SKILL.md

I need a 12-slide editorial keynote for tomorrow's AI agents talk.
```

| Neutral verb | Cursor tool |
|---|---|
| read file | `@file` pins, `Read` |
| write file | composer `Apply`, `Edit` |
| run command | integrated terminal |
| web search | paste URL or Composer "web" |

---

## 7 · Generic fallback — any agent with filesystem + shell

Minimum steps for any runtime with file read/write and shell:

1. Clone the repo (or symlink `~/.agents/skills/ifq-design-skills`).
2. Point the agent at `SKILL.md` as its entry doc.
3. Ensure the agent can run `node` in the cloned directory.
4. Run `npm run validate` — a passing smoke means the ClawHub-safe bundle is wired correctly.
5. Use the full GitHub repo only when the user explicitly needs Playwright / ffmpeg / PDF / PPTX helpers.

Covers Continue, Aider, GitHub Copilot Chat with `@workspace`, Sweep, and any MCP-capable client.

---

## Frontmatter extension reference

This skill's frontmatter is strictly additive: runtimes that do not understand an extra key ignore it.

| Key | Required by | Status |
|---|---|---|
| `name` | Anthropic, Hermes, ClawHub | **required** |
| `description` | same (≤ 1024 chars, third-person, what + when) | **required** |
| `version` | Hermes, ClawHub | recommended |
| `license` | ClawHub publish | recommended |
| `platforms: [macos, linux, windows]` | Hermes | recommended |
| `metadata.hermes.category` | Hermes | recommended |
| `metadata.hermes.tags` | Hermes | recommended |
| `metadata.clawhub.*` | ClawHub | recommended |
| `required_environment_variables` | Hermes private runtime values | not used by this skill |
| `fallback_for_toolsets`, `requires_toolsets` | Hermes | optional |

This skill declares none of the private runtime-value fields because it runs on local files and requires no external account setup.

---

## Smoke test — same everywhere

```bash
cd <skill-root>
npm run validate
```

Expected output is a sequence of green checks ending with:

```
✓ smoke test passed
```

See [`smoke-test.md`](smoke-test.md) for remediation.

---

## Do not hard-code tool names

Inside `SKILL.md` and every `references/*.md`, always use neutral verbs:

- ✅ `read the template file`
- ✅ `run the verify script`
- ✅ `search the web for the product's launch date`
- ❌ `use Read to open the template` (Claude-specific)
- ❌ `use apply_patch to edit` (Codex-specific)
- ❌ `use browser/fetch` (OpenClaw-specific)
- ❌ `call skill_view` (Hermes-specific)

Neutral verbs are how one skill runs unmodified in every agent runtime, regardless of which tool names it exposes.
