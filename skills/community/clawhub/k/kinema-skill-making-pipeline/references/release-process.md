# Release Process | 发版流程

> 本文档指导 AI Agent 按顺序完成发版。Agent 必须严格按 Step 1→9 顺序执行，每步完成后验证，全部完成后执行 Completion Checklist。

## Pre-flight Check | 发版前检查

在开始发版之前，必须完成以下检查。**任何一项不通过则中止发版**。

### 1. 平台检测

检测用户环境中安装了哪些平台，后续 Step 根据检测结果条件执行。

```bash
# 检测 Claude Code（~/.claude 存在）
HAS_CLAUDE_CODE=false
[ -d "$HOME/.claude" ] && HAS_CLAUDE_CODE=true

# 检测 OpenClaw（~/.openclaw 存在）
HAS_OPENCLAW=false
[ -d "$HOME/.openclaw" ] && HAS_OPENCLAW=true

echo "Claude Code installed: $HAS_CLAUDE_CODE"
echo "OpenClaw installed:    $HAS_OPENCLAW"
```

记录结果，后续 Step 7 和 Step 8 将据此判断是否执行。

### 2. 版本一致性校验

运行版本校验脚本，确认 SKILL.md、plugin.json、git tag 三处版本号一致。

```bash
bash scripts/version-check.sh
```

**期望输出**: `✅ All versions match: X.Y.Z`

- 如果通过 → 继续发版
- 如果不通过 → **中止**，提示用户修复版本号不一致问题后再发版

> **注意**: 如果版本号尚未更新（仍在旧版本），属于正常情况，用户需先在 Step 2 更新版本号。

---

## Step 1: 确认变更已提交

确保所有代码变更已 commit 到 Git 仓库。

### 检测

```bash
git status
```

### 动作

- 如果 `nothing to commit, working tree clean` → 跳过，进入 Step 2
- 如果有未提交变更 → 执行 `git add` + `git commit`

### 验证

```bash
git status
# 期望: nothing to commit, working tree clean
```

---

## Step 2: 更新版本号（SKILL.md + plugin.json 同步）

**⚠️ 关键步骤：两个文件必须同时更新，不可遗漏任何一个。**

每次发版需要更新以下两处版本号：

| 文件 | 字段 |
|------|------|
| `SKILL.md` | frontmatter `version: X.Y.Z` |
| `.claude-plugin/plugin.json` | `"version": "X.Y.Z"` |

### 动作

1. 确定新版本号（遵循 [Semantic Versioning](../SKILL.md#version-numbering--版本号规则)）
2. 更新 `SKILL.md` frontmatter 中的 `version`
3. 更新 `.claude-plugin/plugin.json` 中的 `version`

### 验证

```bash
# 快速确认两文件版本号一致
grep '^version:' SKILL.md
grep '"version"' .claude-plugin/plugin.json

# 或运行完整校验脚本
bash scripts/version-check.sh
# 期望: ✅ All versions match: X.Y.Z
```

---

## Step 3: 提交版本变更并打 Tag

将版本号变更 commit 并创建 Git tag。

### 动作

```bash
# 提交版本号变更
git add SKILL.md .claude-plugin/plugin.json
git commit -m "chore: bump version to vX.Y.Z

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"

# 打 annotated tag
git tag -a vX.Y.Z -m "Release vX.Y.Z: <简短描述>"
```

### 验证

```bash
git tag -l | tail -3
# 期望: 包含 vX.Y.Z

git log --oneline -1
# 期望: 最新 commit 是版本号变更
```

---

## Step 4: Push 到 GitHub

将 commit 和 tag 推送到远程仓库。

### 动作

```bash
git push origin master
git push origin vX.Y.Z
# 或一次性推送: git push origin master --tags
```

### 验证

```bash
git ls-remote --tags origin | grep vX.Y.Z
# 期望: 显示远程 tag 存在
```

---

## Step 5: 创建 GitHub Release

在 GitHub 仓库创建正式 Release。

### Release Notes 结构（强制两个 section）

更新说明必须包含以下两个 section，缺一不可：

| Section | 内容 |
|---------|------|
| `## 更新内容` | 每行一条新功能 / bug 修复的简短说明，**行尾附带对应 commit id**，格式 `@<commit-id>`（短 hash 即可） |
| `## 更新指令` | 用户拉取本次更新需执行的命令（见 Step 8） |

**先取本次区间的 commit 列表**，每条 commit 对应「更新内容」里的一行：

```bash
# 取上一个 tag 到 HEAD 的提交（用于逐条填写更新内容 + commit id）
PREV_TAG=$(git tag -l 'v*' --sort=-version:refname | sed -n '2p')
git log --oneline "${PREV_TAG}..HEAD"
# 输出形如：
#   a1b2c3d feat(x): 新增 A 功能
#   d4e5f6a fix(y): 修复 B 问题
```

### 动作

```bash
gh release create vX.Y.Z \
  --repo <org>/<repo> \
  --title "vX.Y.Z: <标题>" \
  --notes "## 更新内容

- 新增 A 功能：<一句说明> @a1b2c3d
- 修复 B 问题：<一句说明> @d4e5f6a

## 更新指令

\`\`\`bash
claude plugin update <skill-name>@<marketplace-name>
\`\`\`
更新后请重开 CLI 或执行 \`/reload-plugins\` 使新版本生效。

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

> **要点**：
> - 「更新内容」每行 = 一个新功能或一个 bug 修复 + `@commit-id`，让读者可直接追溯到具体提交。
> - 一条 commit 对应一行；若多个 commit 服务同一功能，可合并为一行并列出多个 `@id`。
> - 「更新指令」固定给出 `claude plugin update` 与 reload 提示，与 Step 8 一致。

### 验证

```bash
gh release view vX.Y.Z --repo <org>/<repo>
# 期望: 显示 Release 详情，含「更新内容」「更新指令」两个 section
```

---

## Step 6: 发布到 ClawHub（临时文件夹模式）

**⚠️ 必须使用临时文件夹模式**。ClawHub CLI 检测到 `.claude-plugin/` 会将项目误判为 plugin 而非 skill。

### 动作

```bash
# 创建临时文件夹，排除 .claude-plugin/ 和其他非发布文件
TMPDIR=$(mktemp -d /tmp/clawhub-publish-XXXXXX)

# macOS / Linux
rsync -a --exclude='.git' --exclude='.claude-plugin' --exclude='.claude' \
  --exclude='.clawhub' --exclude='skills' . "$TMPDIR/"

# Windows (无 rsync)
# find . -maxdepth 1 -not -name '.git' -not -name '.claude-plugin' \
#   -not -name '.claude' -not -name '.clawhub' -not -name 'skills' \
#   -not -name '.' | while read f; do cp -r "$f" "$TMPDIR/"; done

# 发布
clawhub publish "$TMPDIR" \
  --slug <skill-name> \
  --name "<displayName>" \
  --version X.Y.Z \
  --changelog "<变更描述>"

EXIT_CODE=$?
rm -rf "$TMPDIR"
```

> **Fallback**: 如果 `clawhub publish` 返回 502 错误，使用 [clawhub-api-fallback.md](clawhub-api-fallback.md) 中的 Node.js 脚本发布。

> **注意**: 不要使用 `clawhub package publish`，它需要 `openclaw.plugin.json` 文件，用途不同。

### 验证

```bash
clawhub inspect <skill-name>
# 期望: Latest: X.Y.Z
```

---

## Step 7: 更新 ClawHub 本地缓存

**条件**: 仅当 `HAS_OPENCLAW=true`（`~/.openclaw` 存在）时执行。

### 动作

```bash
clawhub update <skill-name>
```

如果本地有修改导致无法更新，使用 `--force`：

```bash
clawhub update <skill-name> --force
```

### 验证

```bash
clawhub list | grep <skill-name>
# 期望: <skill-name>  X.Y.Z
```

**如果 HAS_OPENCLAW=false** → 跳过此步，输出: `⏭ OpenClaw 未安装，跳过 ClawHub 缓存同步`

---

## Step 8: 更新 Claude Code 插件

**条件**: 仅当 `HAS_CLAUDE_CODE=true`（`~/.claude` 存在）时执行。

### Agent 直接执行更新（无需要求用户手动更新）

插件更新由 AI Agent 在终端中**直接执行**，不要把更新动作丢给用户：

```bash
# 更新单个插件到最新版本（首选，最简单）
claude plugin update <skill-name>@<marketplace-name>

# 若该插件尚未安装，或需要先刷新 marketplace 索引：
claude plugin marketplace update <marketplace-name>
claude plugin install <skill-name>@<marketplace-name>
```

`claude plugin update` 成功后通常输出 `updated from X.Y.(Z-1) to X.Y.Z ... Restart to apply changes.`。

### 执行完后提醒用户重载

Agent 跑完 `claude plugin update` 后，**主动提醒用户**让新版本生效（当前 session 正在加载插件文件，OS 文件锁导致需要重载）：

> ✅ 已更新 `<skill-name>` 到 vX.Y.Z。请**重开 CLI** 或执行 `/reload-plugins` 使新版本生效。

- `/reload-plugins`（或重开 CLI）这一步**必须由用户操作**——Agent 无法在当前 session 内热重载自身插件文件。
- Agent 的职责到「执行 update + 给出重载提示」为止，不要等待或假装已重载。

### 缓存问题与解决方案

#### 问题现象

```
EPERM: operation not permitted, rename 'temp_xxx' -> 'cache/.../X.Y.Z'
EBUSY: resource busy or locked, rm 'cache/.../X.Y.Z'
```

#### 原因

当前 Claude Code session 正在加载插件文件，OS 文件锁阻止缓存目录的覆盖和删除操作。

> **说明**: `marketplace.json` 不锁定版本号，每个 plugin 只声明 `source: github + repo`。Claude Code 会自动从 GitHub repo 拉取最新 release，因此通常只需在新 session 中重新执行 install 命令即可获取最新版本。

#### 解决方案

1. **首选方案**: 在新 Claude Code session 中执行安装命令
2. **备选方案**: 如果首选方案仍失败，手动清理缓存后重装

```bash
# 清理缓存
rm -rf ~/.claude/plugins/cache/<marketplace-name>/<skill-name>
rm -rf ~/.claude/plugins/cache/temp_github_*

# 重新安装
claude plugin marketplace update <marketplace-name>
claude plugin install <skill-name>@<marketplace-name>
```

### 验证

```bash
# 检查缓存目录中的版本
head -5 ~/.claude/plugins/cache/<marketplace-name>/<skill-name>/<version>/SKILL.md
cat ~/.claude/plugins/cache/<marketplace-name>/<skill-name>/<version>/.claude-plugin/plugin.json | grep version
# 期望: 两处版本号均为 X.Y.Z
```

**如果 HAS_CLAUDE_CODE=false** → 跳过此步，输出: `⏭ Claude Code 未安装，跳过插件同步`

---

## Step 9: 全量版本校验

检查所有已安装平台的版本一致性，输出校验报告。

### 动作

```bash
# 本地三源校验
bash scripts/version-check.sh
```

然后逐一检查各平台版本：

```bash
# projects 仓库
echo "=== Projects Repo ==="
grep '^version:' SKILL.md
cat .claude-plugin/plugin.json | grep '"version"'
git tag -l 'v*' --sort=-version:refname | head -1

# GitHub Release
echo "=== GitHub Release ==="
gh release list --repo <org>/<repo> --limit 1

# ClawHub
echo "=== ClawHub ==="
clawhub inspect <skill-name> | grep "Latest"

# ClawHub 缓存（条件: HAS_OPENCLAW）
echo "=== ClawHub Cache ==="
clawhub list | grep <skill-name>

# Claude Code Marketplace（条件: HAS_CLAUDE_CODE）
echo "=== Claude Code Marketplace ==="
claude plugin list | grep <skill-name>
```

### 输出校验报告

| Location | Version | Status |
|----------|---------|--------|
| Projects repo (SKILL.md) | X.Y.Z | ✅/❌ |
| Projects repo (plugin.json) | X.Y.Z | ✅/❌ |
| Git tag | X.Y.Z | ✅/❌ |
| GitHub Release | X.Y.Z | ✅/❌ |
| ClawHub | X.Y.Z | ✅/❌ |
| ClawHub Cache | X.Y.Z | ✅/⏭ (未安装) |
| Claude Code Marketplace | X.Y.Z | ✅/⏭ (未安装) |

---

## Completion Checklist | 完成检查清单

Agent 必须在发版完成后逐一核对以下清单，确认所有步骤已完成：

- [ ] **Step 1**: 所有变更已 commit（`git status` clean）
- [ ] **Step 2**: SKILL.md 和 plugin.json 版本号已同步更新
- [ ] **Step 3**: Git tag 已创建（`git tag -l` 确认）
- [ ] **Step 4**: Commit 和 tag 已 push 到 GitHub（`git ls-remote` 确认）
- [ ] **Step 5**: GitHub Release 已创建（`gh release view` 确认）
- [ ] **Step 6**: ClawHub 已发布（`clawhub inspect` 确认 Latest 版本）
- [ ] **Step 7**: ClawHub 缓存已更新（如果 OpenClaw 已安装）
- [ ] **Step 8**: Claude Code 插件已更新（如果 Claude Code 已安装）
- [ ] **Step 9**: 全量版本校验报告已输出，所有已安装平台版本一致

**如果任何一项未通过 → 返回对应 Step 修复后重新校验。**

**全部通过 → 发版完成。**
