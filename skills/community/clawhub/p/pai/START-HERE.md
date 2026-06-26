# PAI Start Here (OpenClaw Workspace Import)

This copy of PAI is installed at:
`/Users/kash_doll/.openclaw/workspace/PAI`

## 1) What to read first (in order)
1. `README.md`
2. `DOCUMENTATIONINDEX.md`
3. `CLI.md`

## 2) Sanity checks (already verified)
```bash
bun --version
cd /Users/kash_doll/.openclaw/workspace/PAI
bun ./Tools/algorithm.ts --help
```

## 3) Path-fixed quickstart commands (workspace-safe)

### Create a new PRD
```bash
cd /Users/kash_doll/.openclaw/workspace/PAI
bun ./Tools/algorithm.ts new -t "My task title" -e Standard
```

### Check PRD status
```bash
cd /Users/kash_doll/.openclaw/workspace/PAI
bun ./Tools/algorithm.ts status
```

### Run loop mode on a PRD
```bash
cd /Users/kash_doll/.openclaw/workspace/PAI
bun ./Tools/algorithm.ts -m loop -p PRD-YYYYMMDD-task -n 20
```

### Run interactive mode on a PRD
```bash
cd /Users/kash_doll/.openclaw/workspace/PAI
bun ./Tools/algorithm.ts -m interactive -p PRD-YYYYMMDD-task
```

## 4) Important path note
Most PAI docs refer to `~/.claude/skills/PAI/...`.
This imported copy lives in workspace, so use:
`/Users/kash_doll/.openclaw/workspace/PAI/...`

## 5) Optional: make this workspace copy your active ~/.claude skill
⚠️ This overwrites your existing `~/.claude/skills/PAI` directory.
```bash
rsync -a --delete \
  /Users/kash_doll/.openclaw/workspace/PAI/ \
  ~/.claude/skills/PAI/
```

## 6) Security scan result (quick pass)
- High-confidence secrets detected: **0**
- Keyword matches: present (expected in docs/code), no direct key material found in quick scan
