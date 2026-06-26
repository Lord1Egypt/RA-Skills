---
name: kinema-skill-making-pipeline
displayName: "Kinema's Skill Making Pipeline"
version: 1.10.0
description: |
  KinemaClaw Skill development and publishing specification. Defines the standard process for skill development, version management, and publishing. All skills built in KinemaClaw must follow this specification.
  Trigger: Creating new skills, publishing skills, modifying existing skills.
---

# Kinema's Skill Making Pipeline | Kinema Skill 开发与发布规范

- **Author**: [LeeShunEE](https://github.com/LeeShunEE)
- **Organization**: [KinemaClawWorkspace](https://github.com/KinemaClawWorkspace)
- **GitHub**: https://github.com/KinemaClawWorkspace/kinema-skill-making-pipeline

本规范定义了 KinemaClaw ecosystem 中 skill 的开发、版本管理、发布的标准化流程。

## ⚠️ Before First Use | 首次使用必读

**首次使用此 skill 前，必须先读取 [references/ONBOARDING.md](references/ONBOARDING.md) 完成环境配置。**

- **首次配置** → 读取 references/ONBOARDING.md 完成全部步骤
- **环境不可用**（命令不存在、依赖缺失、连接失败）→ 读取 references/ONBOARDING.md Troubleshooting 排查修复
- **配置完成后** → 直接使用下方开发流程

## Core Principles | 核心原则

1. **Git First** - All modifications must be managed in Git repository | 所有修改必须在 Git 仓库中管理
2. **Atomic Commits** - Each commit must be a meaningful independent change | 每次 commit 必须是有意义的独立变更
3. **Versioned Releases** - Must create Git tag before publishing | 发布前必须打 Git tag
4. **No In-Place Publishing** - Never publish raw skills from /app/skills/ | 禁止发布 /app/skills/ 中的原位 skill
5. **Onboarding Required** - Every skill must have installation/configuration guide | 每个 skill 必须有安装/配置引导
6. **Five-Way Sync** - After release, sync versions across: projects repo, ClawHub cache, GitHub Release, ClawHub, Claude Code Marketplace | 发版后同步五地版本：projects 仓库、ClawHub 缓存、GitHub Release、ClawHub、Claude Code Marketplace
7. **Marketplace on First Publish** - A brand-new skill must be registered in the marketplace index; version updates must NOT | 全新 skill 首发时必须登记 marketplace 索引；版本更新则不需要

## Development Workflow | 开发流程

### 1. Create Skill Repository | 创建 Skill 仓库

```
projects/<skill-name>/
├── .claude-plugin/       # Required: plugin manifest
│   └── plugin.json       # Required: plugin metadata
├── SKILL.md              # Required: skill definition
├── scripts/              # Optional: automation scripts
├── references/           # Required: references and onboarding
│   └── ONBOARDING.md     # Required: onboarding guide
└── other project files
```

### 2. Development Guidelines | 开发规范

- **Atomic commits**: One thing per commit | 每个 commit 只做一件事
- **Commit frequently**: Commit after completing each feature/fix | 完成一个功能/修复一个问题后立即 commit
- **Descriptive messages**: Use meaningful commit messages | 使用描述性的 commit message

```bash
# Good | 好
git commit -m "Add install command to searxng-search CLI"

# Bad | 不好
git commit -m "update" 
git commit -m "fix stuff"
```

### 3. Release Process | 发布流程

**发版流程已外置到** [references/release-process.md](references/release-process.md)。Agent 发版时必须读取该文档并按 Step 1→9 顺序执行。

**发布前先判断类型 | Determine release type first:**

| 类型 | 额外动作 |
|------|---------|
| **全新 skill 首发**（marketplace 索引中尚无该 skill） | 走常规流程 **+** 更新 marketplace 索引 → 读取 [references/marketplace-publishing.md](references/marketplace-publishing.md) |
| **已有 skill 版本更新** | 仅走常规流程，**不动** marketplace 索引 |

> 判断方法：在 marketplace 的 `.claude-plugin/marketplace.json` `plugins` 数组中检索本 skill 的 `name`。不存在 = 首发，存在 = 版本更新。

**发版流程概要**（详细步骤见 reference）：
1. 确认变更已提交
2. 同步更新 SKILL.md + plugin.json 版本号
3. 提交并打 Git tag
4. Push 到 GitHub
5. 创建 GitHub Release（Release Notes 强制含「更新内容」+「更新指令」两个 section；更新内容每行一条新功能/bug 修复并附 `@commit-id`）
6. 发布到 ClawHub（临时文件夹模式，排除 `.claude-plugin/`）
7. 更新 ClawHub 本地缓存（仅 `~/.openclaw` 存在时）
8. 更新 Claude Code 插件（仅 `~/.claude` 存在时）：Agent **直接执行** `claude plugin update`，随后提醒用户重开 CLI 或 `/reload-plugins`
9. 全量版本校验

> **版本校验工具**: `bash scripts/version-check.sh [expected-version]` — 校验 SKILL.md、plugin.json、git tag 三处版本号一致。

### 4. Version Numbering | 版本号规则

Follow Semantic Versioning: | 遵循语义化版本 (Semantic Versioning):
- **MAJOR**: Incompatible API changes | 不兼容的 API 变更
- **MINOR**: Backward-compatible new features | 向后兼容的新功能
- **PATCH**: Backward-compatible bug fixes | 向后兼容的 bug 修复

```
v1.0.0 → First release | 首次发布
v1.1.0 → New features | 新功能
v1.1.1 → Bug fixes | bug 修复
v2.0.0 → Breaking changes | 重大变更
```

## Required Elements | 必须要素

Each skill must include: | 每个 skill 必须包含：

### 1. SKILL.md

Must include: | 包含：
- name: skill name | skill 名称
- displayName: human-readable name with feature description | 人类可读名称（含功能描述）
- version: semantic version number | 语义化版本号
- description: functionality description and trigger condition | 功能描述和触发条件
- Complete usage instructions | 完整使用说明

**作者声明规范**:

SKILL.md 正文开头（标题之后）必须声明作者信息：

```markdown
# Skill Name

- **Author**: [AuthorName](https://github.com/authorname)
- **Organization**: [OrgName](https://github.com/orgname)
- **GitHub**: https://github.com/orgname/skill-name
```

| 字段 | 说明 |
|------|------|
| Author | 作者 GitHub 个人主页链接 |
| Organization | 所属组织 GitHub 主页链接 |
| GitHub | Skill 源码仓库链接 |

**displayName 格式规范**:
- 统一格式: \`Name (Feature Description)\`

### 2. Onboarding | Onboarding

**references/ONBOARDING.md 是必选文件。** SKILL.md 不包含安装/配置细节，仅引用 references/ONBOARDING.md。

#### 2.1 SKILL.md 中的 Onboarding 引导

SKILL.md 文件开头（`#` 标题之后、Environment Variables 之前）必须包含以下引导块：

```markdown
## ⚠️ Before First Use | 首次使用必读

**首次使用此 skill 前，必须先读取 [references/ONBOARDING.md](references/ONBOARDING.md) 完成环境配置。**

- **首次配置** → 读取 references/ONBOARDING.md 完成全部步骤
- **环境不可用**（命令不存在、依赖缺失、连接失败）→ 读取 references/ONBOARDING.md Troubleshooting 排查修复
- **配置完成后** → 直接使用下方 Run Commands
```

Agent 读取 SKILL.md 时会看到此块，根据场景决定是否继续读取 references/ONBOARDING.md。

#### 2.2 references/ONBOARDING.md 结构规范

references/ONBOARDING.md 是给 AI Agent 执行的引导文档，必须按以下结构编写：

```markdown
# <Skill Name> Onboarding

> 本文档指导 AI Agent 完成首次环境配置。按顺序执行，遇到问题时参考 Troubleshooting。

## Prerequisites | 前置条件
（列出运行此 skill 所需的系统和软件条件）

## Step 1: <步骤名称>
### 检测
（检测命令 + 期望输出，agent 据此判断是否需要执行本步骤）
### 安装
（多种降级方案，按优先级排列，agent 逐条尝试）
### 验证
（验证命令 + 期望输出，确认本步骤完成）

## Step 2: <步骤名称>
...

## Step N: <验证连接或最终检查>

## Troubleshooting | 故障排除
（按错误信息分类的排查表，每行包含：错误 → 原因 → 解决方案）
```

**编写规则：**

| 规则 | 说明 |
|------|------|
| 按顺序执行 | Steps 之间有依赖关系，不可跳步 |
| 每步可独立验证 | 每个 Step 必须有验证命令 + 期望输出 |
| 降级策略 | 每步提供多种方案（至少 2 种），适配不同环境 |
| 不硬编码路径 | 用 `<skill_dir>` 等占位符，agent 运行时替换 |
| 需要用户输入时明确标注 | 如"必须询问用户" "用户提供"，不猜测 |
| Troubleshooting 覆盖常见错误 | 列出所有已知失败场景和解决方案 |

#### 2.3 setup.reference.sh（可选）

对于安装配置较复杂的 skill，可提供 `scripts/setup.reference.sh` 作为**参考范式**。

**注意**：
- 文件名必须包含 `reference`，明确标识为参考文件而非可执行脚本
- **Agent 不应直接执行此文件**，而是读取其内容，根据当前环境适配执行
- 内容是安装流程的模板代码，展示检测→安装→验证的逻辑模式

```bash
# scripts/setup.reference.sh - SETUP REFERENCE (DO NOT EXECUTE DIRECTLY)
# Agent should read this file and adapt commands to current environment.

# Step 1: Check Python
python3 --version

# Step 2: Install dependencies (try in order)
uv pip install --system requests 2>/dev/null || \
pip3 install requests 2>/dev/null || \
sudo pip3 install --break-system-packages requests

# Step 3: Create symlink
sudo ln -sf <skill_dir>/scripts/tool.py /usr/local/bin/tool

# Step 4: Verify
tool --help
```

#### 2.4 Onboarding 触发场景

| 场景 | Agent 行为 |
|------|-----------|
| **首次使用** | 读取 references/ONBOARDING.md，按 Step 1-N 顺序执行 |
| **环境不可用** | 读取 references/ONBOARDING.md Troubleshooting，按错误信息匹配解决方案 |
| **依赖缺失** | 跳转到对应 Step 重新执行安装 |
| **版本升级后** | 重新执行 references/ONBOARDING.md 全流程（新版本可能引入新依赖） |

### 3. Plugin Manifest | 插件清单

**`.claude-plugin/plugin.json` 是 Required 文件。** Claude Code 插件规范要求此文件提供标准化元数据，支持 marketplace 分发和插件发现。

#### 3.1 位置与格式

- 路径：`<skill-name>/.claude-plugin/plugin.json`
- 格式：JSON
- **不加入 `.gitignore`**（它是项目源码的一部分，不是缓存）

#### 3.2 必需字段

| 字段 | 说明 |
|------|------|
| `name` | 插件标识，kebab-case，必须与 SKILL.md frontmatter `name` 一致 |

#### 3.3 推荐字段

| 字段 | 说明 |
|------|------|
| `displayName` | 人类可读名称，建议与 SKILL.md frontmatter `displayName` 一致 |
| `version` | 语义化版本号，必须与 SKILL.md frontmatter `version` 保持同步 |
| `description` | 简短功能描述 |
| `author` | 作者信息，格式：`{ "name": "...", "url": "..." }` |
| `homepage` | 项目主页 URL |
| `repository` | 代码仓库 URL |
| `license` | 开源许可证（如 `GPL-3.0`、`MIT`） |
| `keywords` | 关键词数组，用于 marketplace 搜索 |

#### 3.4 示例

```json
{
  "name": "my-skill-name",
  "displayName": "My Skill Name",
  "version": "1.0.0",
  "description": "Short description of the skill functionality.",
  "author": {
    "name": "AuthorName",
    "url": "https://github.com/authorname"
  },
  "homepage": "https://github.com/OrgName/my-skill-name",
  "repository": "https://github.com/OrgName/my-skill-name",
  "license": "GPL-3.0",
  "keywords": ["keyword1", "keyword2"]
}
```

#### 3.5 版本同步规则

- `plugin.json` 的 `version` 必须 **始终与** SKILL.md frontmatter `version` 一致
- 发版时两处同时更新，不可遗漏
- 参考文档：[Plugins Reference](https://code.claude.com/docs/en/plugins-reference)

### 4. Prohibited Content | 禁止内容

Skills must NOT contain: | skill 中**禁止**包含：
- Personal websites, domains | 个人网站、域名
- Passwords, accounts, tokens | 密码、账号、Token
- Personal email, phone | 个人邮箱、电话
- Real names, identity information | 真实姓名、身份信息
- Cache files, build artifacts | 缓存文件、构建产物（`.clawhub/`、`node_modules/`、`skills/` 等应通过 `.gitignore` 排除）

> **注意**：`.claude-plugin/` 目录**不是缓存**，不应被 `.gitignore` 排除。它是项目源码的一部分，必须被 Git 跟踪。

## GitHub Repository Guidelines | GitHub 仓库规范

- Default to **Private** repositories | 默认创建 **Private** 仓库
- Use meaningful repository names | 使用有意义的仓库名称
- Keep README.md in sync with SKILL.md | 保持 README.md 与 SKILL.md 一致
- No cache files in repo | 仓库中禁止缓存文件，`.gitignore` 必须排除 `.clawhub/`、`skills/` 等 CLI 产物

## Directory Structure | 目录结构

```
<skill-name>/                     # Git repository | Git 仓库
├── .claude-plugin/               # Required: plugin manifest | 必需：Claude Code 插件清单
│   └── plugin.json               # Required: plugin metadata | 必需
├── .gitignore                    # Required: must exclude CLI cache files | 必需：排除 CLI 缓存
├── SKILL.md                      # Required: skill definition | 必需
├── README.md                     # Recommended: project readme | 推荐
├── LICENSE                       # Recommended: license | 推荐
├── scripts/                      # Optional: scripts | 可选
│   ├── version-check.sh          # Optional: version consistency checker | 可选：版本一致性校验
│   └── setup.reference.sh        # Optional: setup reference | 可选（见 Onboarding 章节）
└── references/                   # Required: references and onboarding | 必需（低频/详细内容外置）
    ├── ONBOARDING.md             # Required: onboarding guide | 必需（见 Onboarding 章节）
    └── release-process.md        # Recommended: release process guide | 推荐：发版流程文档
```

## Automation Script Example | 自动化脚本示例

```bash
#!/bin/bash
# skill-publish.sh - Publish skill to GitHub + ClawHub
# 完整发版流程见 references/release-process.md

SKILL_NAME=$1
VERSION=$2
CHANGELOG=${3:-"Release v$VERSION"}

if [ -z "$SKILL_NAME" ] || [ -z "$VERSION" ]; then
    echo "Usage: $0 <skill-name> <version> [changelog]"
    exit 1
fi

cd projects/$SKILL_NAME

# Version consistency check | 版本一致性校验
bash scripts/version-check.sh "$VERSION"
if [ $? -ne 0 ]; then
    echo "Error: Version mismatch. Fix before releasing."
    exit 1
fi

# Check for uncommitted changes | 检查是否有未提交的修改
if ! git diff --quiet; then
    echo "Error: Commit all changes first | 先提交所有修改"
    exit 1
fi

# Create tag | 打 tag
git tag -a v$VERSION -m "Release v$VERSION"

# Push | 推送
git push origin master
git push origin v$VERSION

# Publish to ClawHub (temp folder mode) | 发布到 ClawHub（临时文件夹模式）
# .claude-plugin/ causes ClawHub to misidentify as plugin | .claude-plugin/ 会导致 ClawHub 误判
TMPDIR=$(mktemp -d /tmp/clawhub-publish-XXXXXX)
rsync -a --exclude='.git' --exclude='.claude-plugin' --exclude='.claude' --exclude='.clawhub' --exclude='skills' . "$TMPDIR/"
clawhub publish "$TMPDIR" --slug $SKILL_NAME --version $VERSION --changelog "$CHANGELOG"
EXIT_CODE=$?
rm -rf "$TMPDIR"
exit $EXIT_CODE
```

## Related Documentation | 相关文档

- [ClawHub Documentation](https://docs.openclaw.ai) | [ClawHub 文档](https://docs.openclaw.ai)
- [Skill Creator Specification](/app/skills/skill-creator/SKILL.md) | [Skill 创建规范](/app/skills/skill-creator/SKILL.md)

## References | 参考资料

- [references/release-process.md](references/release-process.md) — 完整发版流程（Step-by-Step，含平台检测、版本校验、缓存问题解决）
- [references/marketplace-publishing.md](references/marketplace-publishing.md) — 全新 skill 首发时更新 marketplace 索引的完整步骤
- [references/clawhub-api-fallback.md](references/clawhub-api-fallback.md) — `clawhub publish` 返回 502 时的 API 备用发布脚本
