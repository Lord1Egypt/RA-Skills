# 安装源管理逻辑

> 本文档描述 MyKnowledge 如何检测、记录和管理安装源。

---

## 安装源类型

| 类型 | 标识 | 更新方式 |
|------|------|----------|
| skillhub_web | Skill Hub 网页/IDE | 重新安装：对 AI 说"安装 my-knowledge 技能" |
| skillhub_cli | SkillHub CLI | `skillhub upgrade myknowledge` |
| clawhub | ClawHub | `clawhub update myknowledge` |
| github_zip | GitHub ZIP | 手动下载新版覆盖 |
| github_clone | GitHub Clone | `git pull origin main` |
| manual | 手动复制 | 访问 GitHub Releases |
| unknown | 未知 | 询问用户 |

---

## 检测策略

### 优先级顺序

```
1. 环境变量（最可靠）
   - SKILLHUB_INSTALL=true → skillhub_web
   - SKILLHUB_CLI_INSTALL=true → skillhub_cli
   - CLAWHUB_INSTALL=true → clawhub

2. 目录标记
   - .clawhub/ 存在 → clawhub
   - package.json 含 "clawhub" → clawhub
   - .skillhub/ 存在 → skillhub_web/cli
   - .git/ 存在 → github_clone

3. 用户确认（兜底）
   询问："请问你是如何安装本 Skill 的？"
```

---

## 安装源变更检测

### 检测逻辑

```markdown
## 检测安装源变更

```
读取 ~/.myknowledge/config/install-source 中的记录
检测当前 Skill 实际安装方式：
  - 检查 .git/ 目录 → github_clone
  - 检查 .clawhub/ 目录 → clawhub
  - 检查 .skillhub/ 目录 → skillhub

IF 记录 source == "skillhub_web" 但检测到 .git/:
   ⚠️ 提示："检测到安装源变更，是否已改用 GitHub？"
   IF 用户确认:
      更新 source = "github_clone"

IF 记录 source == "github_clone" 但 .git/ 消失:
   ⚠️ 提示："Git 仓库标记消失，是否通过其他方式更新？"
   询问新的安装方式并更新
```

### 变更场景

| 原安装源 | 新检测 | 处理 |
|----------|--------|------|
| skillhub_* | .git/ 存在 | 提示切换 github_clone |
| github_clone | .git/ 消失 | 提示选择新方式 |
| skillhub_* | .clawhub/ 存在 | 提示切换 clawhub |
| clawhub | .clawhub/ 消失 | 提示选择新方式 |

---

## 配置文件格式

### install-source

```yaml
# ~/.myknowledge/config/install-source
source: "github_clone"           # 当前安装源
detected_by: "git_dir"           # 检测方式
installed_at: "2026-06-09"       # 安装时间
installed_version: "1.0.0"       # 安装时版本
updated_at: "2026-06-09"         # 上次变更时间（可选）
previous_source: "skillhub_web"  # 历史记录（可选）
skill_path: "~/.codebuddy/skills/myknowledge"
```

---

## 更新策略映射

```markdown
根据 source 执行不同策略：

IF source == "skillhub_web":
   "升级：在 SkillHub 中重新搜索安装 my-knowledge，或对 AI 说'安装 my-knowledge 技能'即可覆盖旧版"
   "✅ 用户数据（~/.myknowledge/）不受影响"

IF source == "skillhub_cli":
   "检查可用版本：skillhub list"
   "升级：skillhub upgrade myknowledge"
   "✅ 用户数据不受影响"

IF source == "clawhub":
   "检查：clawhub list --outdated"
   "升级：clawhub update myknowledge"

IF source == "github_zip":
   "访问 https://github.com/CoderMoray/MyKnowledge/releases 下载新版覆盖"

IF source == "github_clone":
   "cd 到 Skill 目录运行 git pull origin main"

IF source == "manual":
   "访问 GitHub Releases 页面获取新版"
```

---

## 边界情况处理

| 情况 | 处理 |
|------|------|
| install-source 文件不存在 | 视为首次使用，执行检测流程 |
| install-source 格式损坏 | 视为 unknown，重新检测 |
| 同时存在多个标记 | 按优先级：clawhub > skillhub > github |
| 用户拒绝变更 | 保持原记录，提示版本同步问题 |
