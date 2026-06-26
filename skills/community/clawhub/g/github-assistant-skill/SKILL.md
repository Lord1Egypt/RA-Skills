---
name: github-assistant
description: GitHub Trending查看、项目搜索、Star/Fork/Watch操作、Issues管理、Pull Request操作、代码内容获取、评论管理等完整助手。当用户需要查看GitHub Trending排行榜、搜索GitHub项目、对仓库进行操作、管理Issues/PR、获取代码内容时使用此技能。
license: MIT
---

# GitHub Assistant

> **🌐 默认输出语言：中文**
> 除非用户明确要求使用其他语言，所有回复、Trending 展示、搜索结果、操作反馈均使用中文。
> 项目描述、贡献者用户名、仓库名等原始英文内容保持不变。

通过 GitHub REST API + Playwright 浏览器双模式，提供 GitHub Trending、搜索、仓库操作、Issues/PR管理、代码内容获取等完整能力。

## 能力概览

1. **Trending 查询** — 查看每日/每周/每月热门项目
2. **项目搜索** — 搜索仓库、查看详情
3. **仓库操作** — Star/Unstar/Fork/Watch/Unwatch、创建仓库、列出Forks
4. **Issues 管理** — 创建、列出、关闭、重新打开、评论、标签管理、锁定
5. **Pull Requests** — 创建、列出、关闭、合并、审查、评论、请求审查者
6. **代码内容** — 获取文件、目录、README、创建/更新文件
7. **分支管理** — 列出、创建、删除分支
8. **Releases 管理** — 列出、创建、更新、删除 Release
9. **Actions 操作** — 列出工作流、触发/取消/重新运行工作流
10. **用户操作** — 获取用户信息、列出仓库、关注/取消关注
11. **通知管理** — 列出通知、标记已读
12. **组织操作** — 列出组织、获取组织信息、列出成员
13. **评论管理** — Issue/PR 评论
14. **账户管理** — 登录/登出/状态检查

---

## Onboarding（首次使用必读）

### 环境准备

```bash
cd <skill-dir>/scripts
pip install -r requirements.txt
```

**安装浏览器引擎（仅浏览器模式需要）**

#### 方式1：智能安装脚本（推荐）

```bash
python3 install_browser.py
```

**脚本功能：**
- ✅ 自动检测前10秒下载进度
- ✅ 无进度时提示选择国内镜像源
- ✅ 自动验证浏览器安装状态
- ✅ 支持淘宝/清华/华为云镜像

#### 方式2：默认安装

```bash
python3 -m playwright install chromium
```

#### 方式3：使用国内镜像源（下载失败时使用）

Playwright 支持通过环境变量 `PLAYWRIGHT_DOWNLOAD_HOST` 设置浏览器下载镜像源。

**Mac/Linux:**
```bash
# 使用淘宝镜像（推荐）
PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright python3 -m playwright install chromium

# 或使用清华大学镜像
PLAYWRIGHT_DOWNLOAD_HOST=https://mirrors.tuna.tsinghua.edu.cn/playwright python3 -m playwright install chromium
```

**Windows (PowerShell):**
```powershell
$env:PLAYWRIGHT_DOWNLOAD_HOST="https://npmmirror.com/mirrors/playwright"
python -m playwright install chromium
```

**Windows (CMD):**
```cmd
set PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright
python -m playwright install chromium
```

**常用镜像源：**
- 淘宝：`https://npmmirror.com/mirrors/playwright`
- 清华：`https://mirrors.tuna.tsinghua.edu.cn/playwright`
- 华为云：`https://mirrors.huaweicloud.com/playwright`

### 登录 GitHub（二选一）

#### 方式A：浏览器手动登录（推荐）

告诉用户："我来帮你打开浏览器登录 GitHub，请在弹出的窗口中手动输入账号密码完成登录。"

执行步骤：
1. 运行 `python3 github_login.py browser`
2. 等待用户在浏览器中完成登录
3. 登录成功后会自动保存 session

> 注意：浏览器模式仅用于 Trending 页面抓取。API操作（Star/Fork/Watch）仍需 Token。

#### 方式B：Token 登录（支持全部操作）

支持两种 Token 类型：**Fine-grained PAT**（推荐）或 **Classic PAT**

---

**选项 1：Fine-grained Personal Access Token（推荐）**

更安全的权限控制，可为每个仓库单独配置权限。

1. **打开设置页面**
   - 访问 https://github.com/settings/tokens?type=beta
   - 或 GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens

2. **生成新 Token**
   - 点击 "Generate new token"
   - 输入 Token 名称（如：GitHub-Assistant-Skill）
   - 设置过期时间（建议 90 天或更长）
   - 描述：用于 GitHub Assistant Skill 的完整操作

3. **配置权限（重要！）**

   **Repository permissions（仓库权限）- 全部设置为 Read and Write：**
   
   | 权限 | 用途 |
   |------|------|
   | **Actions** | 读取工作流运行状态 |
   | **Administration** | 读取仓库管理信息 |
   | **Checks** | 读取检查运行状态 |
   | **Commit statuses** | 读取提交状态 |
   | **Contents** | 读取/创建/更新/删除文件 |
   | **Dependabot alerts** | 读取安全警报 |
   | **Deployments** | 读取部署信息 |
   | **Discussions** | 读取/创建讨论（如需要） |
   | **Environments** | 读取环境信息 |
   | **Issues** | 读取/创建/更新/关闭 Issues |
   | **Metadata** | 读取基础仓库信息（必需）|
   | **Packages** | 读取包信息 |
   | **Pages** | 读取 GitHub Pages 信息 |
   | **Pull requests** | 读取/合并/审查 PR |
   | **Repository security advisories** | 读取安全公告 |
   | **Secret scanning alerts** | 读取密钥扫描警报 |
   | **Workflows** | 读取工作流 |

   **Account permissions（账户权限）：**
   - 保持默认即可

4. **选择仓库访问范围**
   - **All repositories** - 访问所有仓库（推荐）
   - **Only select repositories** - 仅访问指定仓库

5. **生成并保存 Token**
   - 点击 "Generate token"
   - **⚠️ 立即复制 Token**（页面关闭后无法再次查看）
   - 运行 `python3 github_login.py token <TOKEN>`
   - 验证成功后 Token 会被安全存储到本地

---

**选项 2：Classic Personal Access Token**

传统的 Token 类型，使用 scopes 权限模型。

1. **打开设置页面**
   - 访问 https://github.com/settings/tokens
   - 或 GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)

2. **生成新 Token**
   - 点击 "Generate new token (classic)"
   - 输入 Token 名称（如：GitHub-Assistant-Skill）
   - 设置过期时间（建议 90 天或更长）

3. **选择 Scopes（权限范围）**

   **必需 Scopes：**
   
   | Scope | 用途 |
   |-------|------|
   | `repo` | 完全控制私有仓库（包含所有仓库操作）|
   | `public_repo` | 访问公共仓库 |
   
   **推荐 Scopes（根据需要使用）：**
   
   | Scope | 用途 |
   |-------|------|
   | `workflow` | 更新 GitHub Actions 工作流文件 |
   | `read:org` | 读取组织成员信息 |
   | `read:user` | 读取用户资料信息 |
   | `read:discussion` | 读取团队讨论 |

4. **生成并保存 Token**
   - 点击 "Generate token"
   - **⚠️ 立即复制 Token**（页面关闭后无法再次查看）
   - 运行 `python3 github_login.py token <TOKEN>`
   - 验证成功后 Token 会被安全存储到本地

---

**Token 类型对比：**

| 特性 | Fine-grained PAT | Classic PAT |
|------|-----------------|-------------|
| 权限粒度 | 按仓库、按权限细粒度控制 | 全局 scopes |
| 安全性 | 更高，可限制访问范围 | 较低，全局权限 |
| 组织仓库 | 需要组织管理员批准 | 直接可用 |
| 推荐度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 适用场景 | 生产环境、团队协作 | 个人使用、快速测试 |

### 验证登录状态

运行 `python3 github_login.py check` 查看当前登录状态。

---

## 功能指令映射

### 1. 查看 Trending（核心功能）

**触发词**: trending、热门、排行榜、最火

| 参数 | 值 |
|------|-----|
| since | daily（默认）/ weekly / monthly |
| language | python / javascript / go / rust 等（可选）|

**Agent 执行流程**：

> ⚠️ **必须使用浏览器模式** 以获取完整数据（含贡献者和期间Star数）。
> API 模式仅作为 fallback，不包含 `built_by` 和 `period_stars`。

```bash
# 浏览器模式（推荐，自动滚动获取所有项目）
python3 github_trending.py daily "" browser       # 今日所有Trending项目
python3 github_trending.py weekly python browser   # 本周Python所有Trending项目
python3 github_trending.py monthly "" browser      # 本月所有Trending项目
```

> 💡 **自动加载所有项目**：脚本会自动滚动页面，加载 **当日/当周/当月的所有 Trending 项目**（不仅仅是首页显示的），直到没有新项目加载为止。

#### ⭐ Trending 输出格式规范（⚠️ 必须严格遵守）

> 🔴 **重要**：所有 Trending 输出**必须严格遵循以下格式模板**，不得自行创造其他格式。
> 这是本 Skill 的标准输出规范，确保一致性和可读性。
>
> **默认行为**：Agent 在输出 Trending 项目时，**必须严格按照下方「标准输出模板」的格式输出**，包括：
> - 标题格式和日期
> - 热榜概览结构
> - 每个仓库的详解格式（含深度解读）
> - 今日洞察部分
>
> **除非用户明确提出了额外的格式要求或特殊指令**，否则必须完全按照模板输出，不得：
> - 省略任何部分
> - 更改输出格式
> - 使用 Markdown 表格（IM 聊天平台禁止使用）
> - 简化或合并内容

**新模板结构：**
1. **标题** — 带日期和表情符号
2. **热榜概览** — 统计数据和亮点总结
3. **仓库详解** — 每个仓库的详细分析（含深度解读）
4. **今日洞察** — 核心主题、趋势信号、实用推荐

**标准输出模板**（IM聊天平台，不使用Markdown表格）：

```
🔥 GitHub 今日 Trending (2026-04-02)

📊 今日热榜概览
• 总上榜仓库数：8个
• 最大热点：anthropics/claude-code 正式发布，单日 +8,764 ⭐ 爆棚！
• AI 编程 Agent 双雄：Claude Code + OpenAI Codex 同日霸榜
• 热门语言：Python 领跑（5/8），Shell/Rust/JavaScript 跟进
• 数据来源：GitHub Trending 页面（browser 模式）

━━━━━━━━━━━━━━━━━━━━━━━━━
🏆 Trending 仓库详解
━━━━━━━━━━━━━━━━━━━━━━━━━

1. anthropics/claude-code ⭐ 105,566
⭐ Stars: 105,566 | 🍴 Forks: 16,781 | 💻 语言: Shell | 📅 今日上榜
🔗 项目链接: https://github.com/anthropics/claude-code
📝 项目简介：
一款运行在终端中的智能编程工具，能理解你的代码库，通过自然语言命令帮你更快写代码——执行常规任务、解释复杂代码、处理 Git 工作流。
🔍 深度解读：
• 项目定位：Anthropic 官方推出的 AI 编程 Agent 终端工具，Claude Code 正式开源仓库
• 核心功能：终端内 AI 编程助手，代码理解、自动修改、Git 操作全自然语言驱动
• 为何火爆：Claude Code 此前为闭源工具，社区高度关注。今日 +8,764 星标创近期绝对记录，表明开发者对官方开源的热情极高
• 适用场景：所有日常编程开发工作，尤其是需要频繁操作 Git 和代码审查的场景
• 推荐指数：⭐⭐⭐⭐⭐（今日无可争议的第一名）

━━━━━━━━━━━━━━━━━━━━━━━━━

2. openai/codex ⭐ 72,448
⭐ Stars: 72,448 | 🍴 Forks: 10,140 | 💻 语言: Rust | 📅 今日上榜
🔗 项目链接: https://github.com/openai/codex
📝 项目简介：
一款运行在终端中的轻量级编程 Agent。
🔍 深度解读：
• 项目定位：OpenAI 官方的终端编程 Agent，Claude Code 的直接竞争对手
• 核心功能：用 Rust 编写的高性能终端 AI 助手，聚焦轻量和速度
• 为何火爆：与 Claude Code 同日上榜，AI 编程 Agent 赛道竞争白热化的标志
• 适用场景：偏好 OpenAI 生态、追求极致性能的终端编程开发者
• 推荐指数：⭐⭐⭐⭐⭐

━━━━━━━━━━━━━━━━━━━━━━━━━

3. microsoft/VibeVoice ⭐ 34,994
⭐ Stars: 34,994 | 🍴 Forks: 3,977 | 💻 语言: Python | 📅 今日上榜
🔗 项目链接: https://github.com/microsoft/VibeVoice
📝 项目简介：
微软开源的前沿语音 AI 项目。
🔍 深度解读：
• 项目定位：微软出品的开源语音 AI 框架，持续霸榜多日
• 核心功能：前沿语音合成、语音识别能力，面向研究者和开发者
• 为何火爆：微软品牌背书 + 语音 AI 赛道持续升温，连续多日上榜说明热度不减
• 适用场景：语音助手开发、语音 AI 研究、多模态应用
• 推荐指数：⭐⭐⭐⭐

━━━━━━━━━━━━━━━━━━━━━━━━━
💡 今日洞察
🎯 核心主题：AI 编程 Agent 正式进入「双雄时代」
今日 Trending 最大看点是 anthropics/claude-code 和 openai/codex 首次同日上榜：
• Anthropic Claude Code 今日 +8,764 ⭐，创近期单日最高纪录，官方开源引爆社区
• OpenAI Codex 以 +1,416 ⭐ 紧随其后，Rust 实现主打轻量高性能
• 两家 AI 巨头在同一赛道正面交锋，标志着 AI 编程工具从萌芽期进入全面竞争阶段

📈 三大趋势信号：
1️⃣ AI 编程工具全面开源化：Claude Code 官方仓库今日上榜，加上此前社区的逆向工程和 Python 重写版本，整个生态正在从闭源走向开放
2️⃣ AI 基础模型领域扩展加速：google-research/timesfm 将基础模型从 NLP/CV 扩展到时间序列，预示更多垂直领域基础模型将涌现
3️⃣ 语音 AI 持续火热：microsoft/VibeVoice 连续多日上榜，语音作为 AI 交互的重要入口正在被各大厂商押注

🔧 实用推荐：
• 如果你在用 Claude Code → claude-howto 配套教程值得收藏
• 如果你在做时间序列 → google-research/timesfm 是官方优选
• 如果你在做 OCR → zai-org/GLM-OCR 新晋选手值得关注

📡 数据来源：GitHub Trending (browser) | 下次推送：2026-04-03 22:00 CST
```

**关键规则（⚠️ 必须严格遵守）**：
> 🔴 **所有输出必须严格遵循上述模板格式，不得使用Markdown表格或其他格式。**
> 这是本 Skill 的唯一标准输出规范。

- 每个项目之间用 `━━━━━━━━━━━━━━━━━━━━━━━━━` 分隔，提升可读性
- 仓库信息必须包含：名称、链接、描述、语言、Star/Fork、贡献者、新增 Star
- 每个仓库必须有 **🔍 深度解读** 部分，包含：
  - 项目定位（一句话说明这是什么）
  - 核心功能（技术亮点）
  - 为何火爆（上榜原因分析）
  - 适用场景（谁应该用）
  - 推荐指数（1-5星）
- 输出末尾必须有 **💡 今日洞察** 部分，包含：
  - 🎯 核心主题（今日最大看点）
  - 📈 趋势信号（2-3个行业趋势）
  - 🔧 实用推荐（针对不同用户的建议）
  - 📡 数据来源和下次推送时间
- 所有标签使用中文
- since 参数映射：每日→daily、每周→weekly、每月→monthly
- 输出标题使用中文并带日期

### 2. 搜索项目

**触发词**: 搜索、查找、search

```bash
python3 github_search.py repos "机器学习" 10    # 搜索仓库
python3 github_search.py repos "stars:>10000 language:python"
python3 github_search.py users "octocat"         # 搜索用户
python3 github_search.py info microsoft vscode   # 查看仓库详情
```

**输出格式**：

```
🔍 搜索结果：「关键词」（共 xxx 个）

1. owner/repo
   🔗 https://github.com/owner/repo
   📝 项目描述...
   🔤 Python | ⭐ 12,345 | 🍴 1,234 | Updated: 2024-xx-xx
```

### 3. 仓库操作

**触发词**: star、fork、watch、unwatch、取消关注

> ⚠️ 需要 Token 登录 或 浏览器模式登录

```bash
python3 github_operations.py star microsoft/vscode
python3 github_operations.py unstar owner/repo
python3 github_operations.py fork owner/repo
python3 github_operations.py watch owner/repo
python3 github_operations.py unwatch owner/repo
python3 github_operations.py info owner/repo      # 获取仓库信息
python3 github_operations.py starred              # 列出已star的仓库
```

**操作反馈**：

```
⭐ 已收藏: microsoft/vscode
🍴 已克隆: owner/repo → your-username/repo
👁️ 已关注: owner/repo
```

### 4. Issues 管理

**触发词**: issue、问题、缺陷、bug

> ⚠️ 需要 Token 登录，权限：Issues (Read and Write)

```bash
# 列出 Issues
python3 github_operations.py issues microsoft/vscode open      # open/closed/all
python3 github_operations.py issue microsoft/vscode 1234       # 获取指定 Issue

# 创建 Issue
python3 github_operations.py create-issue owner/repo "Bug标题" "详细描述"

# 关闭/重新打开 Issue
python3 github_operations.py close-issue owner/repo 1234
python3 github_operations.py reopen-issue owner/repo 1234
```

### 5. Pull Requests 操作

**触发词**: pr、pull request、合并请求

> ⚠️ 需要 Token 登录，权限：Pull requests (Read and Write)

```bash
# 列出 PRs
python3 github_operations.py prs microsoft/vscode open         # open/closed/all
python3 github_operations.py pr microsoft/vscode 1234          # 获取指定 PR

# 创建 PR
python3 github_operations.py create-pr owner/repo "PR标题" feature-branch main ["描述"]

# 关闭/重新打开 PR
python3 github_operations.py close-pr owner/repo 1234
python3 github_operations.py reopen-pr owner/repo 1234

# 合并 PR
python3 github_operations.py merge-pr owner/repo 1234 "合并标题"

# 审查 PR
python3 github_operations.py approve-pr owner/repo 1234 "LGTM!"

# PR 详情
python3 github_operations.py pr-files owner/repo 1234      # 列出修改的文件
python3 github_operations.py pr-commits owner/repo 1234    # 列出提交记录
python3 github_operations.py pr-reviews owner/repo 1234    # 列出审查记录
```

### 6. 代码内容获取

**触发词**: 代码、文件、内容、readme

> ⚠️ 需要 Token 登录，权限：Contents (Read)

```bash
# 获取文件内容
python3 github_operations.py file owner/repo path/to/file.py [分支/标签]

# 获取 README
python3 github_operations.py readme owner/repo [分支/标签]

# 列出目录
python3 github_operations.py ls owner/repo [path] [分支/标签]

# 创建/更新文件（需要 Contents Write 权限）
python3 github_operations.py create-file owner/repo "path/file.py" "提交信息" "文件内容"
```

### 7. 评论管理

**触发词**: 评论、comment

> ⚠️ 需要 Token 登录，权限：Issues (Write) 或 Pull requests (Write)

```bash
# Issue 评论
python3 github_operations.py comments owner/repo 1234          # 列出评论
python3 github_operations.py comment owner/repo 1234 "评论内容"
```

### 8. 用户操作

**触发词**: 用户、user、followers、关注

> ⚠️ 需要 Token 登录，部分操作需要 user 权限

```bash
# 获取用户信息
python3 github_operations.py user              # 当前登录用户
python3 github_operations.py user torvalds     # 指定用户

# 列出用户的仓库
python3 github_operations.py my-repos owner    # 当前用户的仓库
python3 github_operations.py user-repos torvalds  # 指定用户的仓库

# 粉丝和关注
python3 github_operations.py followers         # 当前用户的粉丝
python3 github_operations.py following         # 当前用户关注的人
python3 github_operations.py follow username   # 关注用户
python3 github_operations.py unfollow username # 取消关注
```

### 9. 仓库管理

**触发词**: 创建仓库、create repo

> ⚠️ 需要 Token 登录，权限：Contents (Write)

```bash
# 创建新仓库
python3 github_operations.py create-repo my-new-repo "仓库描述"

# 列出仓库的 Forks
python3 github_operations.py forks owner/repo

# 列出 Stargazers
python3 github_operations.py stargazers owner/repo
```

### 10. 分支管理

**触发词**: 分支、branch

> ⚠️ 需要 Token 登录，创建分支需要 Contents (Write)

```bash
# 列出分支
python3 github_operations.py branches owner/repo

# 获取分支信息
python3 github_operations.py branch owner/repo main

# 创建分支
python3 github_operations.py create-branch owner/repo new-branch main
```

### 11. Releases 管理

**触发词**: release、发布

> ⚠️ 需要 Token 登录，创建需要 Contents (Write)

```bash
# 列出 Releases
python3 github_operations.py releases owner/repo

# 获取指定 Release
python3 github_operations.py release owner/repo <release_id>

# 创建 Release
python3 github_operations.py create-release owner/repo v1.0.0 "Release名称" "发布说明"
```

### 12. Actions 操作

**触发词**: workflow、工作流、actions

> ⚠️ 需要 Token 登录，权限：Actions (Read)、Contents (Read/Write)

```bash
# 列出工作流运行
python3 github_operations.py workflows owner/repo

# 获取指定工作流
python3 github_operations.py workflow owner/repo <workflow_id>

# 触发工作流
python3 github_operations.py trigger-workflow owner/repo ci.yml main
```

### 13. Issue Labels 管理

**触发词**: label、标签

> ⚠️ 需要 Token 登录，权限：Issues (Write)

```bash
# 列出 Issue 标签
python3 github_operations.py labels owner/repo 1234

# 添加标签
python3 github_operations.py add-labels owner/repo 1234 bug priority

# 锁定/解锁 Issue
python3 github_operations.py lock-issue owner/repo 1234 "off-topic"
python3 github_operations.py unlock-issue owner/repo 1234
```

### 14. 通知管理

**触发词**: 通知、notification

> ⚠️ 需要 Token 登录，权限：Notifications

```bash
# 列出通知
python3 github_operations.py notifications          # 未读通知
python3 github_operations.py notifications --all    # 所有通知

# 仓库通知
python3 github_operations.py repo-notifications owner/repo

# 标记已读
python3 github_operations.py mark-read <thread_id>
```

### 15. 组织操作

**触发词**: 组织、org

```bash
# 列出当前用户的组织
python3 github_operations.py orgs

# 获取组织信息
python3 github_operations.py org github

# 列出组织仓库
python3 github_operations.py org-repos github

# 列出组织成员
python3 github_operations.py org-members github
```

### 16. 其他操作

```bash
# 查看提交历史
python3 github_operations.py commits owner/repo [文件路径]

# 检查登录状态
python3 github_operations.py check

# 查看 API 限流
python3 github_operations.py rate-limit
```

### 17. 浏览器自动化操作（API 不支持的功能）

**触发词**: 贡献图、insights、流量、网络图、blame、设置页面、探索、marketplace

> ⚠️ 这些功能 GitHub REST API 不支持，需要通过浏览器自动化实现
> 浏览器操作过程可见，操作结束后浏览器保持打开，用户可继续手动操作

```bash
# 用户相关（API 不支持）
python3 github_browser_ops.py contributions torvalds    # 查看贡献图
python3 github_browser_ops.py activity torvalds         # 查看活动时间线
python3 github_browser_ops.py stars torvalds            # 查看 Star 列表页面
python3 github_browser_ops.py followers torvalds        # 查看粉丝列表页面
python3 github_browser_ops.py sponsors torvalds         # 查看赞助页面

# 仓库 Insights（需要 push 权限）
python3 github_browser_ops.py insights owner/repo       # Pulse 概览
python3 github_browser_ops.py traffic owner/repo        # 流量统计
python3 github_browser_ops.py network owner/repo        # Fork 网络图
python3 github_browser_ops.py dependents owner/repo     # 依赖者列表

# 代码相关
python3 github_browser_ops.py blame owner/repo path/file.py    # Git Blame
python3 github_browser_ops.py history owner/repo path/file.py  # 文件提交历史
python3 github_browser_ops.py compare owner/repo main dev      # 分支比较
python3 github_browser_ops.py codesearch owner/repo "keyword"  # 仓库内代码搜索

# 设置页面
python3 github_browser_ops.py settings                  # 用户设置
python3 github_browser_ops.py settings owner/repo       # 仓库设置

# 导航
python3 github_browser_ops.py notifications             # 通知页面
python3 github_browser_ops.py explore                   # Explore 页面
python3 github_browser_ops.py marketplace               # Marketplace
python3 github_browser_ops.py search "query"            # GitHub 搜索
python3 github_browser_ops.py goto "https://..."        # 导航到指定 URL

# 浏览器控制
python3 github_browser_ops.py close                     # 关闭浏览器
```

**操作反馈**：

```
🌐 正在导航到: https://github.com/torvalds
   📋 查看用户 @torvalds 的个人资料
✅ 页面加载完成: https://github.com/torvalds

💡 浏览器保持打开，您可以继续手动操作。
   浏览器将保持打开状态，您可以继续手动操作。
   如需关闭浏览器，请运行: python3 github_browser_ops.py close
```

---

## 浏览器模式指南（Agent专用）

当需要使用 Playwright 浏览器（browser_* 工具）时，遵循以下流程：

### Trending 页面数据提取

**URL 格式**：
- 全语言：`https://github.com/trending?since={daily|weekly|monthly}`
- 按语言：`https://github.com/trending/{language}?since={daily|weekly|monthly}`

**页面 CSS 选择器映射**：

| 数据项 | 选择器 / 提取方式 |
|--------|------------------|
| 仓库名 | `article h2 a` → `href` 去掉前导 `/` |
| 描述 | `article p` → innerText |
| 语言 | `article [itemprop="programmingLanguage"]` → innerText |
| 总Stars | `article a[href*="/stargazers"]` → innerText |
| Forks | `article a[href*="/forks"]` → innerText |
| 贡献者 | `article a` 中 textContent 以 `@` 开头的链接 |
| 期间Stars | 正则匹配 innerText: `(\d[\d,]*) stars (today\|this week\|this month)` |

### 浏览器执行 Star 操作（备选方案）
```
1. 导航到 https://github.com/{owner}/{repo}
2. 找到 "Star" 按钮（已登录状态）
3. 点击 Star
4. 确认按钮变为 "Starred"
```

### 浏览器执行 Watch 操作（备选方案）
```
1. 导航到 https://github.com/{owner}/{repo}
2. 找到 "Watch" 下拉按钮
3. 选择 "Custom" → "Issues, Pull Requests" 等
4. 确认已变为 "Watching"
```

---

## 权限速查表

| 操作 | 所需权限 | 权限级别 |
|------|---------|---------|
| Trending 查看 | 无需登录 | - |
| 项目搜索 | 无需登录 | - |
| Star/Unstar | Token | - |
| Fork | Token | - |
| Watch/Unwatch | Token | Metadata (Read) |
| 查看仓库信息 | Token | Metadata (Read) |
| **创建仓库** | Token | Contents (Write) |
| **列出 Issues** | Token | Issues (Read) |
| **创建/关闭 Issue** | Token | Issues (Write) |
| **Issue Labels** | Token | Issues (Write) |
| **锁定 Issue** | Token | Issues (Write) |
| **列出 PRs** | Token | Pull requests (Read) |
| **创建/关闭 PR** | Token | Pull requests (Write) |
| **合并 PR** | Token | Pull requests (Write) |
| **PR 审查** | Token | Pull requests (Write) |
| **获取文件内容** | Token | Contents (Read) |
| **创建/更新文件** | Token | Contents (Write) |
| **分支管理** | Token | Contents (Write) |
| **Release 管理** | Token | Contents (Write) |
| **查看 Actions** | Token | Actions (Read) |
| **触发工作流** | Token | Contents (Write) |
| **用户信息** | Token | - |
| **关注用户** | Token | user:follow |
| **通知** | Token | Notifications |
| **组织信息** | Token | read:org |

---

## 文件结构

```
github-assistant/
├── SKILL.md                    ← 你正在读的文件
├── README.md                   ← GitHub项目介绍
├── LICENSE                     ← MIT 许可证
├── scripts/
│   ├── github_trending.py      ← Trending抓取（浏览器模式）
│   ├── github_search.py        ← 项目搜索
│   ├── github_operations.py    ← 完整操作（Star/Fork/Issues/PR/代码/评论）
│   ├── github_browser_ops.py   ← 浏览器自动化操作（API不支持的功能）
│   ├── github_login.py         ← 登录管理
│   ├── install_browser.py      ← 浏览器安装脚本
│   ├── config.py               ← 集中配置管理
│   └── requirements.txt        ← Python依赖
├── references/
│   └── github_api_endpoints.md ← API参考
└── assets/

~/.github-assistant/            ← 用户数据目录（不在skill文件夹内）
├── github_token.txt            ← Token存储
├── github_auth.json            ← 浏览器session
└── browser_data/               ← 浏览器持久化数据
```

> ⚠️ **安全说明**：敏感数据（Token、浏览器会话）存储在用户目录 `~/.github-assistant/`，不会出现在 skill 文件夹中，可安全上传到公开仓库。

## 注意事项

- Token 存储在本地文件 `github_token.txt`，请勿上传到公开仓库
- GitHub API 限流：未认证 60次/小时，认证后 5000次/小时
- 浏览器模式首次需安装 Chromium：`playwright install chromium`
- Trending 查询优先使用浏览器模式以获取完整数据（含贡献者和期间Star数）
- IM 聊天平台**禁止使用 Markdown 表格**，使用 emoji + 列表格式
- Fine-grained PAT 权限需要仔细配置，权限不足会导致操作失败
