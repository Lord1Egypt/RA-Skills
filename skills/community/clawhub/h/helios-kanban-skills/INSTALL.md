# Agent Self-Install Guide — Helios Kanban Remote Skill

> **Audience**: AI agents (Cursor, Claude Code, Hermes, Codex, etc.)
>
> **Trigger**: User says "安装 helios-kanban-remote 技能", "install helios kanban skill", or gives you this repo / INSTALL.md URL.
>
> **Goal**: Clone this GitHub repo, install the skill, configure, and verify — **without human manual steps**. Execute every shell command yourself. Ask the user only when information is missing.

---

## Source (this repository)

| Item | Value |
|------|-------|
| **Repository** | https://github.com/SolomonFang/vibe-kanban |
| **Clone URL** | `https://github.com/SolomonFang/vibe-kanban.git` |
| **Skill path** | `skills/helios-kanban-remote/` |
| **Default branch** | `hly-dev` |
| **This document** | https://github.com/SolomonFang/vibe-kanban/blob/hly-dev/skills/helios-kanban-remote/INSTALL.md |

The skill is published **inside this repo**. Do not look for a separate package — clone or use this repository directly.

---

## Agent instructions — follow in order

```
Install progress:
- [ ] Step 1: Detect environment
- [ ] Step 2: Get skill files from this repo
- [ ] Step 3: Install to agent skills directory
- [ ] Step 4: Check dependencies (curl, jq)
- [ ] Step 5: Configure HELIOS_KANBAN_URL
- [ ] Step 6: Verify connectivity
- [ ] Step 7: Report result to user
```

---

### Step 1: Detect environment

```bash
uname -s
echo "HOME=$HOME"
pwd
```

Determine agent type and `SKILLS_ROOT`:

| Agent | `SKILLS_ROOT` |
|-------|---------------|
| Cursor (global) | `$HOME/.cursor/skills` |
| Claude Code | `$HOME/.claude/skills` |
| Cursor (project) | `<workspace>/.cursor/skills` |
| Hermes / other | user-provided, or `$HOME/.cursor/skills` |

```bash
SKILLS_ROOT="$HOME/.cursor/skills"   # adjust per table
SKILL_DIR="$SKILLS_ROOT/helios-kanban-remote"
REPO_URL="https://github.com/SolomonFang/vibe-kanban.git"
BRANCH="hly-dev"
REPO_DIR=""   # set in Step 2
```

**Do not** install into `~/.cursor/skills-cursor/` (reserved by Cursor).

---

### Step 2: Get skill files from this repo

**Option A — already inside this repository** (e.g. workspace is `vibe-kanban`):

```bash
REPO_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
test -f "$REPO_DIR/skills/helios-kanban-remote/SKILL.md" || {
  echo "error: skill not found in current repo"; exit 1
}
echo "Using local repo: $REPO_DIR"
```

**Option B — not in repo, clone from GitHub** (default):

```bash
REPO_DIR="${TMPDIR:-/tmp}/vibe-kanban"
rm -rf "$REPO_DIR"
git clone --depth 1 -b "$BRANCH" "$REPO_URL" "$REPO_DIR"
test -f "$REPO_DIR/skills/helios-kanban-remote/SKILL.md" || {
  echo "error: clone succeeded but skill path missing"; exit 1
}
echo "Cloned repo to: $REPO_DIR"
```

---

### Step 3: Install to agent skills directory

```bash
mkdir -p "$SKILLS_ROOT"
rm -rf "$SKILL_DIR"
cp -r "$REPO_DIR/skills/helios-kanban-remote" "$SKILL_DIR"
chmod +x "$SKILL_DIR/scripts/hk.sh"
HK="$SKILL_DIR/scripts/hk.sh"

# Verify
test -f "$SKILL_DIR/SKILL.md" && test -f "$HK" && echo "OK: installed to $SKILL_DIR"
```

---

### Step 4: Check dependencies

```bash
command -v curl >/dev/null || { echo "MISSING: curl"; exit 1; }
command -v jq   >/dev/null || { echo "MISSING: jq"; exit 1; }
```

If `jq` is missing, install when possible:

```bash
# macOS
brew install jq

# Debian/Ubuntu
sudo apt-get update && sudo apt-get install -y jq
```

---

### Step 5: Configure environment variables

**Required**: `HELIOS_KANBAN_URL` — URL of the running Helios Kanban instance.

1. Use existing env var if already set.
2. Otherwise **ask the user once**: "请提供 Helios Kanban 地址，例如 `http://100.x.x.x:7964`"
3. Optional defaults (ask if user wants shortcuts):
   - `HELIOS_KANBAN_PROJECT_ID` — default project UUID
   - `HELIOS_KANBAN_REPO_ID` — default repo UUID
   - `HELIOS_KANBAN_ITERATION` — default iteration code (e.g. `260717`)

```bash
export HELIOS_KANBAN_URL="<user-provided-url>"
# export HELIOS_KANBAN_PROJECT_ID="<uuid>"
# export HELIOS_KANBAN_REPO_ID="<uuid>"
# export HELIOS_KANBAN_ITERATION="260717"
```

Persist (skip if already in profile):

```bash
PROFILE="$HOME/.zshrc"
[ -f "$HOME/.bashrc" ] && PROFILE="$HOME/.bashrc"
grep -q 'HELIOS_KANBAN_URL' "$PROFILE" 2>/dev/null || \
  echo "export HELIOS_KANBAN_URL=\"$HELIOS_KANBAN_URL\"" >> "$PROFILE"
```

Kanban server (separate host) must be running:

```bash
HOST=0.0.0.0 PORT=7964 npx helios-kanban
```

---

### Step 6: Verify connectivity

```bash
bash "$HK" health
bash "$HK" projects
```

Success: `health` returns `"success": true`; `projects` returns a JSON array.

If failed → check URL, kanban process, network (Tailscale). Do not claim install succeeded.

---

### Step 7: Report result to user

```markdown
## Helios Kanban Remote 技能已安装

- **来源仓库**: https://github.com/SolomonFang/vibe-kanban
- **安装路径**: `{SKILL_DIR}`
- **CLI**: `{SKILL_DIR}/scripts/hk.sh`
- **Kanban 地址**: `{HELIOS_KANBAN_URL}`
- **连通性**: 正常

你现在可以对我说：
- 「有哪些项目」
- 「看看进行中的任务」
- 「创建一个任务：……」
- 「用 Claude 跑这个任务」
```

---

## User gives agent only a URL

Tell any agent:

```
请阅读并执行安装文档，完成 helios-kanban-remote 技能安装：
https://github.com/SolomonFang/vibe-kanban/blob/hly-dev/skills/helios-kanban-remote/INSTALL.md
```

Or shorter:

```
安装 Helios Kanban 远程控制技能：https://github.com/SolomonFang/vibe-kanban
```

Agent should fetch INSTALL.md from the repo, then run Steps 1–7.

Raw URL for fetching:

```
https://raw.githubusercontent.com/SolomonFang/vibe-kanban/hly-dev/skills/helios-kanban-remote/INSTALL.md
```

---

## Update

```bash
cd "$REPO_DIR" && git pull origin hly-dev   # if local clone exists
# or re-clone (Step 2 Option B) and re-copy (Step 3)
```

---

## Uninstall

```bash
rm -rf "$SKILL_DIR"
```

---

## Troubleshooting

| Symptom | Action |
|---------|--------|
| `git clone` fails | Check network and repo URL |
| `health` connection refused | Kanban not running or wrong `HELIOS_KANBAN_URL` |
| API 403 | Set `VK_ALLOWED_ORIGINS` on kanban server (reverse proxy) |
| Skill not loading | Confirm `$SKILL_DIR/SKILL.md` exists; restart agent session |

---

## After install

Read `$SKILL_DIR/SKILL.md` for usage. API details in `reference.md`, examples in `examples.md`.
