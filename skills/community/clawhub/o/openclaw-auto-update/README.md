# OpenClaw Update Skill - ClawHub Release

## 📦 Skill Information

- **Name**: openclaw-update
- **Version**: 1.0
- **Author**: Davis
- **Description**: OpenClaw version upgrade assessment and execution skill
- **Category**: System Tools
- **Languages**: 简体中文 / English (bilingual support)

---

## 🎯 Features

1. **Automatic Version Detection** - Check current vs latest stable version
2. **Intelligent Assessment** - 5-dimension scoring system
3. **Risk Assessment** - Check GitHub issues for critical bugs
4. **Breaking Changes Detection** - Warn about config compatibility issues
5. **Agent-Reach Integration** - Auto-detect GitHub access capability
6. **Safe Backup System** - Timestamp + random suffix to prevent conflicts
7. **Installation Method Detection** - Use correct update command (npm/pnpm/git)
8. **Auto Gateway Restart** - Restart after update or inform if failed
9. **Recovery Function** - List and restore from backups
10. **Multilingual Support** - Chinese/English based on user language

---

## 📋 Prerequisites

### Required

- **OpenClaw** v2026.3.0+
- **agent-reach** v1.0.0+ (for GitHub access)
- **Python** 3.8+ (for backup scripts)

### Optional

- npm/pnpm (for global installation updates)
- git (for source installation updates)

---

## 🚀 Installation

### Method 1: ClawHub (Recommended)

```bash
clawhub install openclaw-update
```

### Method 2: Manual Installation

```bash
# Download skill file
# Copy to OpenClaw skills directory
cp openclaw-update.skill ~/.openclaw/workspace/skills/

# Extract
cd ~/.openclaw/workspace/skills/
unzip openclaw-update.skill
```

---

## 📖 Usage

### Trigger Phrases

- "Check OpenClaw update" / "检查 OpenClaw 更新"
- "Assess if should upgrade to latest" / "评估是否升级到最新版"
- "openclaw-update"
- "Should I update OpenClaw" / "要不要更新 OpenClaw"

### Workflow (10 Steps)

1. **Detect Agent-Reach** - Check GitHub access capability
2. **Check Current Version** - `openclaw --version`
3. **Get Latest Version** - From GitHub releases
4. **Version Comparison** - Calculate version gap
5. **Analyze Updates** - Read release notes for each version
6. **Check Issues** - Assess risks from GitHub issues
7. **Comprehensive Scoring** - 5-dimension assessment (0-10 points)
8. **Create Backup** - Unique name with timestamp + random suffix
9. **Detect & Update** - Use correct command based on installation method
10. **Restart Gateway** - Auto-restart or inform user

---

## 🔧 Scripts

### check_agent_reach.py

Detect if agent-reach is available:

```bash
python3 scripts/check_agent_reach.py
```

Output:
- ✅ agent-reach installed and GitHub accessible
- ⚠️ agent-reach installed but GitHub access failed
- ❌ agent-reach not installed

### check_version.py

Check current version:

```bash
python3 scripts/check_version.py
```

### backup_restore.py

Backup and recovery with conflict prevention:

```bash
# Create backup (prevents naming conflicts)
python3 scripts/backup_restore.py backup

# List all backups
python3 scripts/backup_restore.py list

# Restore from backup
python3 scripts/backup_restore.py restore .openclaw.backup.20260311_155100.a3f2b1c4
```

---

## 📊 Assessment Dimensions

| Dimension | Score Range | Description |
|-----------|-------------|-------------|
| Feature Value | 0-2 | No features → Major updates |
| Security | 0-2 | Has vulnerabilities → Has fixes |
| Stability | 0-2 | Many bugs → Clean issues |
| Breaking | 0-2 | Breaking changes → Fully compatible |
| Urgency | 0-2 | Optional → Strongly recommended |

**Recommendation**:
- **≥8 points**: Strongly recommend update
- **6-7 points**: Recommend update
- **4-5 points**: Optional update
- **<4 points**: Recommend postponing

---

## ⚠️ Critical Rules (RED LINES)

### NEVER VIOLATE

1. **NEVER create backup naming conflicts**
   - Always check for existing backups
   - Use timestamp + random suffix
   - Never overwrite user's existing backups

2. **NEVER run silently**
   - Always report current step progress
   - Inform user before each major action
   - Report backup location at the end

3. **NO emotional assessment**
   - Assessment must be objective
   - Score based on facts, not feelings
   - Let data drive the recommendation

4. **MUST strictly reference release notes**
   - Read official release notes
   - Do not fabricate information
   - Cite sources for all claims

5. **MUST check issues for threats**
   - Check GitHub issues before recommending update
   - If dangerous issues found: STOP and inform user
   - If major bugs found: FORBID update on behalf of user

---

## 🔄 Update Methods

### Global Installation (npm/pnpm)

```bash
# npm
npm i -g openclaw@latest

# pnpm
pnpm add -g openclaw@latest

# NOT recommended: Bun (WhatsApp/Telegram bugs)
```

### Source Installation (git)

```bash
openclaw update
# Or with channel
openclaw update --channel stable
```

### Official Recommended (Re-run Installer)

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard
```

---

## 💾 Backup & Recovery

### Backup Command

```bash
python3 scripts/backup_restore.py backup
```

Creates backup with unique name: `.openclaw.backup.20260311_155100.a3f2b1c4`

### Recovery Command

```bash
# List available backups
python3 scripts/backup_restore.py list

# Restore specific backup
python3 scripts/backup_restore.py restore .openclaw.backup.20260311_155100.a3f2b1c4
```

### Manual Recovery

```bash
# macOS / Linux
rm -rf ~/.openclaw && cp -r ~/.openclaw.backup.TIMESTAMP ~/.openclaw

# Windows PowerShell
Remove-Item -Recurse -Force $env:USERPROFILE\.openclaw
Copy-Item -Recurse $env:USERPROFILE\.openclaw.backup.TIMESTAMP $env:USERPROFILE\.openclaw
```

---

## 📝 Example Output

See `references/example-report.md` for complete assessment report example.

---

## 🌍 Multilingual Support

The skill automatically detects user language:

- **Chinese user** → Responds in 简体中文
- **English user** → Responds in English

Example triggers:
- "使用 openclaw-update 更新 openclaw" → Chinese response
- "Update OpenClaw with openclaw-update" → English response

---

## 📞 Support

- **Issues**: GitHub Issues
- **Discussion**: OpenClaw Discord Community
- **Documentation**: See `references/` directory in skill

---

## 📄 License

MIT License

---

## 🔄 Changelog

### v1.1 (2026-03-11) - Bug Fix Release

**Critical Fixes:**
- ✅ Fixed backup script to only backup necessary data (config, credentials, workspace)
- ✅ Added exclusion patterns (browser/, logs/, *.pid, *.lock, __pycache__/, etc.)
- ✅ Changed from `cp -r` to `rsync` for more reliable backup
- ✅ Reduced backup size from ~4.5GB to ~100MB (only user data)
- ✅ Added backup verification step
- ✅ Better error handling and cleanup on failure

### v1.0 (2026-03-11)

**Initial Release - Complete Feature Set:**

- ✅ 5-dimension assessment system (功能/安全/稳定/破坏性/紧迫性)
- ✅ Agent-Reach availability detection with install guide
- ✅ GitHub releases & issues analysis
- ✅ Breaking Changes detection
- ✅ Backup system with conflict prevention (timestamp + random suffix)
- ✅ Installation method detection (npm/pnpm/git)
- ✅ Real-time progress reporting (10 steps)
- ✅ Multilingual support (Chinese/English)
- ✅ Recovery function with backup listing
- ✅ Auto gateway restart
- ✅ Automated daily update check (cron at 4:00 AM)
- ✅ System notifications
- ✅ User approval workflow
- ✅ Strict adherence to official documentation
- ✅ Red lines enforcement (5 critical rules)
