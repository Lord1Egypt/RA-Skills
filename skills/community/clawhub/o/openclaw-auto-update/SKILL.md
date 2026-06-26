---
name: openclaw-update
description: OpenClaw 版本升级评估与执行技能。工作流程：(1) 检测 agent-reach 可用性（无则引导安装），(2) 检查 GitHub releases 获取最新稳定版，(3) 对比当前版本判断是否需要更新，(4) 分析版本差距和更新日志，(5) 检查 GitHub issues 评估风险，(6) 综合评估打分并给出升级建议，(7) 备份用户配置（防止冲突），(8) 检测安装方式执行对应更新命令，(9) 自动重启 gateway，(10) 提供恢复功能。Use when 用户要求检查 OpenClaw 更新、评估是否升级、或执行版本更新。支持中英双语。
---

# OpenClaw Update Skill

## Multilingual Support / 多语言支持

**Detect user language and respond accordingly:**
- If user speaks Chinese → respond in Chinese (简体中文)
- If user speaks English → respond in English
- Maintain consistent language throughout the session

**检测用户语言并相应回复：**
- 用户使用中文 → 用简体中文回复
- 用户使用英文 → 用英文回复
- 整个会话保持语言一致

---

## Prerequisites / 前置要求

### Agent-Reach Detection / Agent-Reach 检测

**Before using this skill, detect if agent-reach is available:**

```bash
# Detection command
agent-reach --version 2>&1 || echo "Not installed"
```

**If not installed, guide user to install:**

```bash
# Method 1: pipx install (recommended)
pipx install https://github.com/Panniantong/agent-reach/archive/main.zip
agent-reach install --env=auto

# Method 2: Check for alternative GitHub access
# Such as gh CLI, curl (not recommended, may be blocked)
```

**If user cannot install agent-reach:**
- Explain the reason (network restrictions, permission issues, etc.)
- Suggest manual GitHub access to check versions
- Or guide to learn the `agent-reach` skill first

---

## Workflow / 工作流程

### Step 0: Detect Agent-Reach Availability / 检测 Agent-Reach 可用性

**Use detection script (recommended):**

```bash
python3 scripts/check_agent_reach.py
```

**Or manual detection:**

```bash
# Test if agent-reach is available
agent-reach read "https://github.com/openclaw/openclaw" --timeout 10 2>&1
```

**If successful**: Continue to next step  
**If failed**:
1. Inform user agent-reach is unavailable
2. Provide installation guide (see Prerequisites or run `python3 scripts/check_agent_reach.py`)
3. Ask if user wants to continue (manual mode) or install agent-reach first

---

### Step 1: Check Current Version / 检查当前版本

**Progress message:**
> 📋 **Step 1/10: Checking current version** / **正在执行第 1 步：检查当前版本**

```bash
openclaw --version
```

Record current version (e.g., v2026.3.2)

---

### Step 2: Get Latest Version Info / 获取最新版本信息

**Progress message:**
> 📋 **Step 2/10: Fetching latest version from GitHub** / **正在执行第 2 步：从 GitHub 获取最新版本**

Use `agent-reach` to access GitHub releases page:

```bash
agent-reach read "https://github.com/openclaw/openclaw/releases"
```

Extract:
- Latest stable version (e.g., v2026.3.7)
- Release date
- Release notes summary

---

### Step 3: Version Comparison / 版本对比

**Progress message:**
> 📋 **Step 3/10: Comparing versions** / **正在执行第 3 步：版本对比**

**If versions match:**
- Report: Current version is already the latest
- End workflow

**If versions differ:**
- Calculate version gap (how many minor versions behind)
- Read release notes for each version sequentially

---

### Step 4: Analyze Update Content / 分析更新内容

**Progress message:**
> 📋 **Step 4/10: Analyzing release notes** / **正在执行第 4 步：分析更新日志**

For each version to update, use `agent-reach` to read detailed release notes:

```bash
agent-reach read "https://github.com/openclaw/openclaw/releases/tag/v2026.3.X"
```

Record:
- New features
- Bug fixes
- Breaking changes
- Security updates

**Strictly reference official release notes** - do not fabricate information.

---

### Step 5: Check Issues / 检查 Issues

**Progress message:**
> 📋 **Step 5/10: Checking GitHub issues for risks** / **正在执行第 5 步：检查 GitHub issues 评估风险**

Access GitHub issues page to assess risks:

```bash
agent-reach read "https://github.com/openclaw/openclaw/issues"
```

Check:
- Any critical bug reports
- Any upgrade compatibility issues
- Any security vulnerabilities
- Number of issues and recent activity

**Critical Rule:** If dangerous issues are found, MUST stop and inform user. If major bugs are found, FORBID the update on behalf of user!

---

### Step 6: Comprehensive Assessment / 综合评估

**Progress message:**
> 📋 **Step 6/10: Scoring and assessment** / **正在执行第 6 步：综合评估打分**

Score based on following dimensions (0-2 points each):

| Dimension | Scoring Criteria |
|-----------|-----------------|
| **Feature Value** | 0=No new features, 1=Minor improvements, 2=Major feature updates |
| **Security** | 0=Security issues exist, 1=No security updates, 2=Security fixes included |
| **Stability** | 0=Many bug reports, 1=Few issues, 2=Issues are clean |
| **Breaking** | 0=Has breaking changes, 1=Config adjustment needed, 2=Fully compatible |
| **Urgency** | 0=Optional update, 1=Recommended, 2=Strongly recommended |

**Total Score ≥8**: Strongly recommend update  
**Total Score 6-7**: Recommend update  
**Total Score 4-5**: Optional update  
**Total Score <4**: Recommend postponing

**Critical Rule:** Assessment must be objective, no emotional bias!

---

### Step 7: Backup User Configuration / 备份用户配置

**Progress message:**
> 📋 **Step 7/10: Backing up user configuration** / **正在执行第 7 步：备份用户配置**

**Detect OS and create unique backup name:**

```bash
# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    OS="Windows"
else
    OS="Unknown"
fi

# Generate unique backup name with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME=".openclaw.backup.${TIMESTAMP}"

# Check for naming conflicts (CRITICAL RULE)
if [ -d "~/${BACKUP_NAME}" ]; then
    # Add random suffix to avoid conflict
    RANDOM_SUFFIX=$(openssl rand -hex 4)
    BACKUP_NAME=".openclaw.backup.${TIMESTAMP}.${RANDOM_SUFFIX}"
fi

# Execute backup based on OS
case "$OS" in
    "macOS"|"Linux")
        cp -r ~/.openclaw ~/${BACKUP_NAME}
        ;;
    "Windows")
        # PowerShell command
        powershell.exe -Command "Copy-Item -Recurse $env:USERPROFILE\.openclaw $env:USERPROFILE\.${BACKUP_NAME}"
        ;;
esac

echo "✅ Backup created: ~/${BACKUP_NAME}"
```

**Critical Rules:**
1. NEVER overwrite existing backups
2. ALWAYS use unique timestamp + random suffix
3. ALWAYS inform user of backup location at the end

---

### Step 8: Detect Installation Method & Update / 检测安装方式并更新

**Progress message:**
> 📋 **Step 8/10: Detecting installation method and updating** / **正在执行第 8 步：检测安装方式并执行更新**

**Detect installation method:**

```bash
# Check for git installation
if [ -d ~/.openclaw/.git ]; then
    INSTALL_METHOD="git"
    echo "Detected: Source installation (git clone)"
else
    INSTALL_METHOD="npm"
    echo "Detected: Global installation (npm/pnpm)"
fi

# Check Gateway running method
if launchctl list | grep -q openclaw 2>/dev/null; then
    GATEWAY_MODE="launchd"
elif systemctl list-units | grep -q openclaw 2>/dev/null; then
    GATEWAY_MODE="systemd"
else
    GATEWAY_MODE="terminal"
fi
```

**Execute update based on installation method:**

**For Global Installation (npm/pnpm):**
```bash
# npm
npm i -g openclaw@latest

# Or pnpm
pnpm add -g openclaw@latest

# NOT recommended: Bun (WhatsApp/Telegram bugs)
```

**For Source Installation (git):**
```bash
openclaw update
# Or with channel
openclaw update --channel stable
```

**Official recommended method (re-run installer):**
```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard
```

---

### Step 9: Restart Gateway / 重启 Gateway

**Progress message:**
> 📋 **Step 9/10: Restarting Gateway** / **正在执行第 9 步：重启 Gateway**

```bash
# Preferred for service-managed Gateway
openclaw gateway restart

# Then verify
openclaw doctor
openclaw health
```

**If restart fails:**
- Inform user immediately
- Provide manual restart instructions based on Gateway mode (launchd/systemd/terminal)

---

### Step 10: Report & Recovery Info / 报告与恢复信息

**Progress message:**
> 📋 **Step 10/10: Generating final report** / **正在执行第 10 步：生成最终报告**

**Final report must include:**
1. Update result (success/failure)
2. Backup location (with full path)
3. Recovery instructions
4. Any issues encountered

**Recovery commands (if needed):**

```bash
# macOS / Linux
rm -rf ~/.openclaw && cp -r ~/.openclaw.backup.TIMESTAMP ~/.openclaw

# Windows PowerShell
Remove-Item -Recurse -Force $env:USERPROFILE\.openclaw
Copy-Item -Recurse $env:USERPROFILE\.openclaw.backup.TIMESTAMP $env:USERPROFILE\.openclaw
```

**When user wants to recover:**
- Ask which backup to restore (list available backups)
- Confirm before executing recovery

---

## Automated Daily Check / 自动定时检查

### Setup Cron Task / 设置 Cron 任务

**After installing this skill, offer to create a cron task for automatic daily checks:**

**Progress message:**
> 🤖 **Setting up automated daily update check...** / **正在设置自动每日更新检查...**

**Create cron task that runs at 4:00 AM daily:**

```bash
# Method 1: Using OpenClaw cron (recommended)
cron add --name "openclaw-daily-update-check" \
  --schedule "0 4 * * *" \
  --command "python3 ~/.openclaw/workspace/skills/openclaw-update/scripts/cron_check.py"
```

**What the cron task does:**
1. Runs every day at 4:00 AM
2. Checks GitHub for latest version
3. Compares with current version
4. Checks GitHub issues for critical bugs
5. Sends system notification if update available
6. Saves detailed report to `~/.openclaw/update_check_report.txt`
7. Waits for user approval before proceeding with update

**User approval workflow:**
- If new version found → Send notification with report
- User replies "确认更新" or "update now" → Start update workflow
- User replies "稍后" or "later" → Skip this update
- If critical issues found → FORBID update automatically

### Cron Script Location / Cron 脚本位置

```bash
~/.openclaw/workspace/skills/openclaw-update/scripts/cron_check.py
```

### Manual Setup Commands / 手动设置命令

**macOS / Linux:**
```bash
# Add to crontab
crontab -e

# Add this line (runs at 4:00 AM daily)
0 4 * * * /usr/bin/python3 ~/.openclaw/workspace/skills/openclaw-update/scripts/cron_check.py >> ~/.openclaw/cron_check.log 2>&1
```

**Windows Task Scheduler:**
```powershell
# Create scheduled task
$action = New-ScheduledTaskAction -Execute "python" -Argument "~/.openclaw/workspace/skills/openclaw-update/scripts/cron_check.py"
$trigger = New-ScheduledTaskTrigger -Daily -At 4am
Register-ScheduledTask -TaskName "OpenClaw Daily Update Check" -Action $action -Trigger $trigger
```

### Notification Examples / 通知示例

**New version available:**
```
╔═══════════════════════════════════════════════════════════╗
║  OpenClaw Update Available / 发现新版本                    ║
╠═══════════════════════════════════════════════════════════╣
║  Current: v2026.3.2                                       ║
║  Latest:  v2026.3.7                                       ║
║  Issues:  Issues 状态良好                                  ║
║                                                           ║
║  ✅ Backup will be created before update                  ║
║  📋 Reply "确认更新" to start update                      ║
╚═══════════════════════════════════════════════════════════╝
```

**Already up to date:**
```
✅ OpenClaw Up to Date / 已是最新版本
Current: v2026.3.7
No update needed.
```

**Critical issues found:**
```
⚠️ CRITICAL ISSUES FOUND! Update NOT recommended.
Issues: 发现多个严重问题
Please wait for next release.
```

---

## Output Format / 输出格式

### Assessment Report Template / 评估报告模板

```markdown
## 📊 OpenClaw Version Assessment Report / 版本评估报告

### Version Info / 版本信息
- **Current Version / 当前版本**: v2026.3.2
- **Latest Version / 最新版本**: v2026.3.7
- **Version Gap / 版本差距**: 5 minor versions

### 🔍 Update Analysis / 更新内容分析

#### New Features / 新增功能
- Feature 1
- Feature 2

#### Bug Fixes / Bug 修复
- Fix 1
- Fix 2

#### Breaking Changes / 破坏性变更
- ⚠️ Change description (if any)

### 📈 Issues Assessment / Issues 评估
- **Open Issues / 开放 issues 数量**: X
- **Critical Bugs / 严重 bug**: None/Yes (describe)
- **Upgrade Issues / 升级问题**: None/Yes (describe)

### 🎯 Scoring / 综合评分

| Dimension / 维度 | Score / 得分 |
|-----------------|-------------|
| Feature Value / 功能价值 | X/2 |
| Security / 安全性 | X/2 |
| Stability / 稳定性 | X/2 |
| Breaking / 破坏性 | X/2 |
| Urgency / 紧迫性 | X/2 |
| **Total / 总分** | **X/10** |

### 💡 Recommendation / 更新建议

**Recommendation Index / 推荐指数**: X/10 (Strongly Recommended/Recommended/Optional/Postpone)

**Reasons / 理由**:
- ✅ Pro 1
- ✅ Pro 2
- ⚠️ Considerations

### 🛠️ Update Steps / 更新步骤

```bash
# Commands
```

### 💾 Backup Info / 备份信息
**Backup Location / 备份位置**: `~/.openclaw.backup.20260311_155100.a3f2b1c4`
**Recovery Command / 恢复命令**: See above
```

---

## Critical Rules / 铁律

### RED LINES - NEVER VIOLATE / 红线 - 禁止违反

1. **NEVER create backup naming conflicts** / **禁止备份文件名冲突**
   - Always check for existing backups
   - Use timestamp + random suffix
   - Never overwrite user's existing backups

2. **NEVER run silently** / **禁止静默运行**
   - Always report current step progress
   - Inform user before each major action
   - Report backup location at the end

3. **NO emotional assessment** / **禁止带情绪评估**
   - Assessment must be objective
   - Score based on facts, not feelings
   - Let data drive the recommendation

4. **MUST strictly reference release notes** / **必须严格参照版本更新日志**
   - Read official release notes
   - Do not fabricate information
   - Cite sources for all claims

5. **MUST check issues for threats** / **必须检查 issues 的威胁**
   - Check GitHub issues before recommending update
   - If dangerous issues found: STOP and inform user
   - If major bugs found: FORBID update on behalf of user

---

## Related Skills / 相关技能

- **agent-reach**: Internet content reading & search tool (12+ platforms)
- **skill-creator**: Skill creation guide

---

## Example Output / 示例输出

See `references/example-report.md` for complete assessment report example.
