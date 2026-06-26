# Install Channels (Graph Memory Zero)

Use this file when users ask for “more ways to download/install”.

## Channel A — ClawHub registry (recommended for online users)

### Install latest
```bash
clawhub install graph-memory-zero
```

### Install fixed version
```bash
clawhub install graph-memory-zero --version 1.0.2
```

### Update later
```bash
clawhub update graph-memory-zero
```

Best for: normal online environments, easy upgrades.

---

## Channel B — Offline package (.skill artifact)

A `.skill` file is a zip-compatible artifact.

### 1) Get package
- Example artifact: `graph-memory-zero.skill`

### 2) Unpack to workspace skills directory
PowerShell example:
```powershell
$dst = "$HOME\.openclaw\workspace\skills\graph-memory-zero"
New-Item -ItemType Directory -Force -Path $dst | Out-Null
Expand-Archive -Path ".\graph-memory-zero.skill" -DestinationPath $dst -Force
```

### 3) Verify structure
Must contain:
- `...\skills\graph-memory-zero\SKILL.md`

### 4) Reload OpenClaw
```bash
openclaw gateway restart
```

Best for: air-gapped / restricted network environments.

---

## Channel C — Source-folder install (manual copy)

### 1) Copy folder directly
Copy `graph-memory-zero/` to:
- `~/.openclaw/workspace/skills/graph-memory-zero` (Linux/macOS)
- `%USERPROFILE%\.openclaw\workspace\skills\graph-memory-zero` (Windows)

### 2) Verify root file
- `SKILL.md` must be at the folder root.

### 3) Reload OpenClaw
```bash
openclaw gateway restart
```

Best for: internal teams, local customization before distribution.

---

## Quick post-install verification

1. Skill folder exists under workspace `skills/`
2. `SKILL.md` has valid frontmatter (`name`, `description`)
3. Restart succeeds with no config errors
4. Trigger test: ask for graph-memory recall tuning and confirm this skill is selected

---

## Maintainer note

When publishing a new version, keep changelog explicit on:
- profile defaults changed?
- threshold/minScore behavior changed?
- verification criteria changed?
- rollback path changed?
