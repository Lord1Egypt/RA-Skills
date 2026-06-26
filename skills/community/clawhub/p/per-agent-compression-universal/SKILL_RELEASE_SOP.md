# Skill Release SOP (Standard Operating Procedure)

**Skill**: per-agent-compression-universal  
**Purpose**: Standardize release process, ensure quality, and prevent regressions  
**Version**: 1.0.0  
**Last Updated**: 2026-03-20

---

## 📋 Table of Contents

1. [Pre-Release Checklist](#pre-release-checklist)
2. [Version Bumping Procedure](#version-bumping-procedure)
3. [Security Scans](#security-scans)
4. [Bilingual Completeness Validation](#bilingual-completeness-validation)
5. [Git Workflow](#git-workflow)
6. [Publishing to ClawHub & GitHub](#publishing-to-clawhub--github)
7. [Post-Release Actions](#post-release-actions)
8. [Optional Enhancements Implementation](#optional-enhancements-implementation)
   - [Pre-commit Hook](#pre-commit-hook)
   - [Bilingual Completeness Validator](#bilingual-completeness-validator)

---

## Pre-Release Checklist

Before any publish, run through this checklist:

- [ ] **CHANGELOG.md** entry added at TOP (newest first), with full details by category
- [ ] **README.md** version header matches `skill.json`
- [ ] **skill.json** version field bumped
- [ ] **Bilingual integrity**: English section complete, then Chinese section complete (not interleaved)
- [ ] **Scroll notice** present at top of README and CHANGELOG: `请往下翻页查看中文说明`
- [ ] **Anchor links** functional (if platform supports markdown anchors)
- [ ] **Security scans passed** (see below)
- [ ] **Install script** uses parameter inference (no hardcoded `--model`, `--channel`, `--to`)
- [ ] **No hardcoded credentials** in any file (IDs, tokens, secrets)
- [ ] **Config data leakage check** passed (no user-specific config values embedded)
- [ ] **Git tag** created and pushed
- [ ] **GitHub Release** body equals full CHANGELOG entry (not truncated)
- [ ] **ClawHub changelog** parameter matches full CHANGELOG entry
- [ ] **Local deploy** synced to `/root/.openclaw/skills/`

---

## Version Bumping Procedure

**Order matters:**

1. Update CHANGELOG.md first (add new entry at top, bilingual)
2. Update README.md version header
3. Bump `skill.json` version
4. Run pre-commit hook (if configured) to verify
5. Commit: `git commit -m "Bump version X.Y.Z - <brief description>"`
6. Tag: `git tag -a vX.Y.Z -m "vX.Y.Z - <description>"`
7. Push: `git push origin main --tags`

---

## Security Scans

Run these commands **before every publish**:

```bash
# 1. Hardcoded credentials/IDs
grep -rE "(client|id|token|secret|key)\s*[=:]\s*[\"\`'][^\"\`']+[\"\`']" /root/.openclaw/workspace/skills/per-agent-compression-universal/ | grep -v CHANGELOG.md || echo "✅ No obvious hardcoded secrets"

# 2. Long numeric strings (likely IDs)
grep -rE "[0-9]{10,}" /root/.openclaw/workspace/skills/per-agent-compression-universal/ | grep -v CHANGELOG.md || echo "✅ No long numeric IDs found"

# 3. Install script parameter inference (must NOT have hardcoded values)
grep -E "(--model|--channel|--to)" /root/.openclaw/workspace/skills/per-agent-compression-universal/install.sh | grep -v "model:\s*auto\|channel:\s*auto\|to:\s*auto" || echo "✅ Parameter inference check passed"

# 4. Configuration data leakage (ensure no personal config values)
grep -rE "dingtalk-connector|openrouter/|stepfun|clawhub|skillhub" /root/.openclaw/workspace/skills/per-agent-compression-universal/ | grep -vE "example.com|placeholder|<replace>" || echo "✅ No specific user configuration found"

# 5. CHANGELOG sensitive references (must be abstract)
grep -nE "05566651511149398|openrouter/stepfun/step-3.5-flash:free|client_id|client_secret" /root/.openclaw/workspace/skills/per-agent-compression-universal/CHANGELOG.md || echo "✅ CHANGELOG clear of specific sensitive references"
```

**If any command finds matches (other than the intended "✅" echo), STOP and fix before publishing.**

---

## Bilingual Completeness Validation

Quick heuristic checks:

```bash
# Count Chinese sections should equal number of English version entries
en_count=$(grep -c "^## \[[0-9]" /root/.openclaw/workspace/skills/per-agent-compression-universal/CHANGELOG.md)
zh_count=$(grep -c "( Chinese )" /root/.openclaw/workspace/skills/per-agent-compression-universal/CHANGELOG.md)
test "$en_count" -eq "$zh_count" && echo "✅ Bilingual count OK: $en_count English, $zh_count Chinese" || echo "❌ Mismatch: $en_count English vs $zh_count Chinese"

# Check Chinese sections aren't trivially short (< 100 chars after separator is suspicious)
if grep -A 20 "( Chinese )" /root/.openclaw/workspace/skills/per-agent-compression-universal/CHANGELOG.md | head -n 21 | wc -c | grep -qE '^[0-9]+$' && [ $(grep -A 20 "( Chinese )" /root/.openclaw/workspace/skills/per-agent-compression-universal/CHANGELOG.md | head -n 21 | wc -c) -lt 100 ]; then
  echo "❌ Chinese section too short (likely incomplete translation)"
else
  echo "✅ Chinese sections appear complete"
fi
```

---

## Git Workflow

```bash
# 1. Ensure on main and up to date
git checkout main
git pull origin main

# 2. Stage all changes (after updating CHANGELOG, README, skill.json)
git add .
git commit -m "Bump version X.Y.Z - <brief description>"

# 3. Create annotated tag
git tag -a vX.Y.Z -m "vX.Y.Z - <description>"

# 4. Push
git push origin main --tags
```

---

## Publishing to ClawHub & GitHub

**Use the automated release script:**

```bash
cd /root/.openclaw/workspace/skills/per-agent-compression-universal
./scripts/release.sh X.Y.Z "Brief changelog entry (one line)"
```

The script will:
1. Run pre-release checklist
2. Commit & tag (if git repo)
3. Publish to ClawHub
4. Create GitHub draft release (requires `gh` CLI)
5. Sync local deploy
6. Append release notes to workspace MEMORY.md

**After script completes:**
- Review the GitHub draft release at the provided URL
- Publish it manually when ready

---

## Post-Release Actions

1. **Notify users** if the release contains critical fixes or breaking changes
2. **Verify tasks** are functioning: `openclaw cron list | grep per_agent_compression`
3. **Monitor** first scheduled run for any unexpected failures
4. **Update** any deployment documentation referencing the version

---

## Optional Enhancements Implementation

Below are concrete implementations for the "Optional Enhancements (Future Work)" listed in `AGENTS.md`.

### Pre-commit Hook

A ready-to-use pre-commit hook is provided in `scripts/pre-commit`. It performs:

- Bilingual completeness validation (counts + length)
- Install script parameter inference check
- Quick scan for leaked IDs
- Version consistency check (when CHANGELOG/README/skill.json changed)

**Installation:**

```bash
cd /root/.openclaw/workspace/skills/per-agent-compression-universal
chmod +x scripts/pre-commit
# Symlink into .git/hooks (or copy)
ln -sf ../../scripts/pre-commit .git/hooks/pre-commit
# Or copy directly:
# cp scripts/pre-commit .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
```

The hook will now run automatically before each commit. To bypass (not recommended): `git commit --no-verify`

**Note**: This hook runs locally only. For team environments, consider using the `pre-commit` framework to manage shared hooks.

---

### Bilingual Completeness Validator

Standalone script: `scripts/validate-bilingual.sh`

```bash
#!/bin/bash
# Validate bilingual completeness in CHANGELOG.md

set -e

CHANGELOG="CHANGELOG.md"

if [ ! -f "$CHANGELOG" ]; then
  echo "❌ CHANGELOG.md not found"
  exit 1
fi

echo " Validating bilingual completeness in $CHANGELOG..."

# Extract all English version entries (e.g., ## [1.2.3])
mapfile -t versions < <(grep -oE '^## \[[0-9.]+' "$CHANGELOG" | sed 's/^## \[//;s/\]$//')

# Count Chinese sections
zh_count=$(grep -c "( Chinese )" "$CHANGELOG")

if [ "${#versions[@]}" -ne "$zh_count" ]; then
  echo "❌ Mismatch: ${#versions[@]} English version entries, $zh_count Chinese sections"
  exit 1
fi

echo "✅ Entry count matches: ${#versions[@]} English, $zh_count Chinese"

# Validate each Chinese section length (> 200 chars to ensure completeness)
failed=0
while IFS= read -r line; do
  if [[ $line =~ ^\[.*\]$ ]]; then
    section_start=$line
    continue
  fi
  if [[ $line == "( Chinese )" ]]; then
    # Capture everything until next empty line or next English header
    content=""
    while IFS= read -r next; do
      if [[ -z "$next" ]] || [[ $next =~ ^##\ \[ ]]; then
        break
      fi
      content+="$next"$'\n'
    done
    len=${#content}
    if [ "$len" -lt 200 ]; then
      echo "❌ Chinese section for $section_start is too short ($len chars). Likely incomplete translation."
      failed=1
    fi
  fi
done < "$CHANGELOG"

if [ $failed -eq 0 ]; then
  echo "✅ All Chinese sections exceed minimum length threshold"
else
  exit 1
fi

echo "🎉 Bilingual completeness validation passed"
exit 0
```

**Installation:**

```bash
cd /root/.openclaw/workspace/skills/per-agent-compression-universal
chmod +x scripts/validate-bilingual.sh
# Optional: add to pre-commit hook or CI
```

**Usage:** Run manually: `./scripts/validate-bilingual.sh`, or rely on pre-commit hook.

**Integration:**
- Called from `scripts/pre-commit` hook
- Can be invoked in `release.sh` pre-release checklist (already in script)
- Suitable for CI/CD pipelines

---

## Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-20 | Initial SOP with security scans, bilingual validation, pre-commit hook, and validator script specs |

---

*Follow this SOP for every release to maintain quality and consistency.*
