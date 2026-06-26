#  GitHub Assistant Skill

**[中文](#中文文档) | [English](#english-documentation)**

---

<a id="中文文档"></a>

## 中文文档

> 一个为 AI Agent（Claude Code / OpenClaw / AstrBot 等）设计的全能 GitHub 助手技能包。
> 支持 Trending 查看、项目搜索、Star/Fork/Watch 操作、Issues/PR 管理、代码内容获取等完整功能。
> **默认输出语言：中文**


GitHub 操作全能助手技能，支持 Trending 查看、仓库搜索、Star/Fork/Watch 操作、Issues/PR 管理、代码内容获取、分支管理、Releases、Actions 操作等。通过 REST API + Playwright 浏览器双模式，覆盖 GitHub 官方 API 及网页操作专属功能（Insights、Traffic、Security 等）。适用于查看热门项目、搜索仓库、管理代码协作。

### ✨ 功能特性

- 🔥 **GitHub Trending** — 查看每日/每周/每月热门项目，支持按语言筛选
- 🔍 **项目搜索** — 支持搜索仓库、用户、查看项目详情
- ⭐ **仓库操作** — Star / Unstar / Fork / Watch / Unwatch / 创建仓库 / 列出 Forks & Stargazers
- 🐛 **Issues 管理** — 创建、列出、关闭、重新打开、评论、标签管理、锁定
- 🔀 **Pull Requests** — 创建、列出、关闭、合并、审查、评论、请求审查者
- 📄 **代码内容** — 获取文件、目录、README、创建/更新文件
- 🌿 **分支管理** — 列出、创建、删除分支
- 🚀 **Releases 管理** — 列出、创建、更新、删除 Release
- ⚡ **Actions 操作** — 列出工作流、触发/取消/重新运行工作流
- 👤 **用户操作** — 获取用户信息、列出仓库、关注/取消关注
- 🔔 **通知管理** — 列出通知、标记已读
- 🏢 **组织操作** — 列出组织、获取组织信息、列出成员
- 💬 **评论管理** — Issue/PR 评论
- 🌐 **浏览器自动化** — 支持 API 不支持的操作（贡献图、Insights、流量统计、网络图、Blame 等）
- 🔐 **双模式登录** — 浏览器手动登录 + Token 自动登录
- 🤖 **双引擎** — GitHub REST API + Playwright 浏览器自动化
- 📊 **完整数据** — Trending 信息包含仓库名、描述、语言、Star、Fork、贡献者、期间新增Star

### 📦 快速安装

**1. 安装依赖**

```bash
cd github-assistant/scripts
pip install -r requirements.txt
```

**2. 安装浏览器引擎（可选，浏览器模式需要）**

> ⚠️ **重要提示**：AI Agent/服务器环境请优先查看 **方案3-Docker** 或 **方案4-API模式**

#### 安装优先级说明

| 优先级 | 方案 | 适用场景 | 说明 |
|--------|------|----------|------|
| 1 | pip 安装 | **中国大陆用户推荐** | 使用 PyPI 镜像安装 Playwright 包，不受网络限制 |
| 2 | 官方 CDN + 代理 | 网络正常/有代理环境 | 从 cdn.playwright.dev 下载浏览器二进制 |
| 3 | 国内镜像源 | CDN 无法访问时 | 自动切换到淘宝/清华镜像 |
| 4 | Docker | AI Agent/服务器 | 预装浏览器，无需下载 |
| 5 | 纯 API 模式 | 无需 Trending 功能 | 跳过浏览器安装 |

#### 方式A — 智能安装脚本（推荐）

使用智能安装脚本，自动使用 PyPI 镜像安装 Playwright，然后下载浏览器：

**Mac/Linux:**
```bash
cd github-assistant/scripts
python3 install_browser.py
```

**Windows:**
```powershell
cd github-assistant\scripts
python install_browser.py
```

**脚本功能：**
- ✅ **首选 pip 安装 Playwright 包**（使用阿里云 PyPI 镜像，中国大陆可正常访问）
- ✅ 自动检测系统代理设置
- ✅ 自动检测 DNS 解析状态
- ✅ 自动检测前10秒下载进度
- ✅ 下载停滞时自动切换国内镜像源
- ✅ 自动处理镜像版本兼容性
- ✅ 自动验证浏览器安装状态

**命令行参数：**
```bash
# 检查 DNS 解析状态
python3 install_browser.py --check-dns

# 直接使用指定镜像源
python3 install_browser.py --mirror 1    # 淘宝镜像
python3 install_browser.py --mirror 2    # 清华镜像

# 跳过官方源，直接使用镜像
python3 install_browser.py --skip-official
```

#### 方式B — 手动安装

**Mac/Linux:**
```bash
python3 -m playwright install chromium
```

**Windows:**
```powershell
# 使用PowerShell
python -m playwright install chromium

# 或使用cmd
python.exe -m playwright install chromium
```

> 💡 **中国用户提示**：如果下载缓慢或失败，请使用下方的 **方式C：国内镜像源**。

> 🔄 **代理自动检测**：安装脚本会自动检测并使用系统代理设置（`HTTP_PROXY`/`HTTPS_PROXY`/`ALL_PROXY`）。

#### 方式C — 备用安装方案（默认方式下载失败时使用）

**方案0：使用系统代理（自动检测）**

安装脚本会自动检测以下环境变量中的代理设置：

| 环境变量 | 说明 |
|---------|------|
| `HTTPS_PROXY` / `https_proxy` | HTTPS 代理 |
| `HTTP_PROXY` / `http_proxy` | HTTP 代理 |
| `ALL_PROXY` / `all_proxy` | 通用代理 |
| `NO_PROXY` / `no_proxy` | 不走代理的地址 |

**设置代理示例：**

```bash
# Mac/Linux (临时)
export HTTPS_PROXY="http://127.0.0.1:7890"
export HTTP_PROXY="http://127.0.0.1:7890"

# 然后运行安装脚本
python3 install_browser.py

# 或直接一行
HTTPS_PROXY="http://127.0.0.1:7890" python3 install_browser.py
```

```powershell
# Windows PowerShell (临时)
$env:HTTPS_PROXY = "http://127.0.0.1:7890"
$env:HTTP_PROXY = "http://127.0.0.1:7890"
python install_browser.py
```

**方案1：DNS 解析失败解决方案**

如果遇到 `cdn.playwright.dev` DNS 解析失败，可尝试以下解决方案：

**方案1.1：更换 DNS 服务器（推荐）**

| DNS 服务器 | IP 地址 | 说明 |
|------------|---------|------|
| Google DNS | 8.8.8.8, 8.8.4.4 | 全球通用 |
| Cloudflare | 1.1.1.1, 1.0.0.1 | 速度快 |
| 阿里 DNS | 223.5.5.5, 223.6.6.6 | 国内推荐 |
| 腾讯 DNS | 119.29.29.29 | 国内推荐 |

**方案1.2：添加 hosts 映射**

**Mac/Linux:**
```bash
# 查询 IP（使用备用 DNS）
nslookup cdn.playwright.dev 8.8.8.8

# 添加到 hosts 文件（需要管理员权限）
echo "13.107.253.39 cdn.playwright.dev" | sudo tee -a /etc/hosts
```

**Windows (PowerShell 管理员):**
```powershell
# 添加到 hosts 文件
Add-Content -Path "$env:SystemRoot\System32\drivers\etc\hosts" -Value "13.107.253.39 cdn.playwright.dev"
```

**方案1.3：使用代理**
```bash
# 设置代理环境变量
export HTTPS_PROXY="http://your-proxy:port"
export HTTP_PROXY="http://your-proxy:port"

# 然后执行安装
python3 -m playwright install chromium
```

**方案2：使用国内镜像源（⭐推荐中国用户）**

> ⚠️ **注意**：镜像源版本可能滞后于官方版本。如果镜像源没有所需版本，请使用 Docker 方案或代理。

Playwright 支持通过环境变量 `PLAYWRIGHT_DOWNLOAD_HOST` 设置浏览器下载镜像源。

**Mac/Linux (bash/zsh):**
```bash
# 使用淘宝镜像（推荐）
PLAYWRIGHT_DOWNLOAD_HOST=https://registry.npmmirror.com/-/binary/playwright python3 -m playwright install chromium

# 或使用清华大学镜像
PLAYWRIGHT_DOWNLOAD_HOST=https://mirrors.tuna.tsinghua.edu.cn/playwright python3 -m playwright install chromium
```

**Mac/Linux (永久设置):**
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export PLAYWRIGHT_DOWNLOAD_HOST=https://registry.npmmirror.com/-/binary/playwright

# 然后执行
python3 -m playwright install chromium
```

**Windows (PowerShell):**
```powershell
# 使用淘宝镜像
$env:PLAYWRIGHT_DOWNLOAD_HOST="https://registry.npmmirror.com/-/binary/playwright"
python -m playwright install chromium

# 或使用清华大学镜像
$env:PLAYWRIGHT_DOWNLOAD_HOST="https://mirrors.tuna.tsinghua.edu.cn/playwright"
python -m playwright install chromium
```

**Windows (CMD):**
```cmd
set PLAYWRIGHT_DOWNLOAD_HOST=https://registry.npmmirror.com/-/binary/playwright
python -m playwright install chromium
```

**Windows (永久设置):**
```powershell
# 以管理员身份运行 PowerShell，设置系统环境变量
[Environment]::SetEnvironmentVariable("PLAYWRIGHT_DOWNLOAD_HOST", "https://registry.npmmirror.com/-/binary/playwright", "User")

# 重新打开终端后执行
python -m playwright install chromium
```

**常用镜像源列表：**

| 镜像源 | 地址 | 说明 |
|--------|------|------|
| npmmirror（淘宝） | `https://registry.npmmirror.com/-/binary/playwright` | 推荐，同步及时 |
| 清华大学 | `https://mirrors.tuna.tsinghua.edu.cn/playwright` | 教育网速度优秀 |

**镜像版本滞后解决方案：**

> ⚠️ 镜像源可能没有最新版本的浏览器。例如：Playwright 1.58.0 需要 chromium v1208，但镜像可能只有 v1200。

**方案2.1：智能安装脚本自动降级（推荐）**

智能安装脚本会自动检测镜像版本并降级 Playwright 到兼容版本：

```bash
# 脚本会自动：
# 1. 检测镜像源可用的 chromium 版本
# 2. 查找兼容的 Playwright 版本
# 3. 自动降级安装兼容版本
python3 install_browser.py --mirror 1
```

**方案2.2：手动降级 Playwright 版本**

如果镜像安装失败，可以手动降级 Playwright：

```bash
# 查看当前 Playwright 版本
python3 -m playwright --version

# 安装与镜像兼容的 Playwright 版本
pip install playwright==1.57.1

# 然后使用镜像安装浏览器
PLAYWRIGHT_DOWNLOAD_HOST=https://registry.npmmirror.com/-/binary/playwright python3 -m playwright install chromium
```

**Playwright 与 Chromium 版本对照表：**

| Playwright 版本 | Chromium 构建 | 说明 |
|----------------|--------------|------|
| 1.58.0 | v1208 | 最新版 |
| 1.57.1 | v1200 | 镜像常用 |
| 1.57.0 | v1199 | |
| 1.56.0 | v1194 | |
| 1.55.0 | v1181 | |
| 1.54.0 | v1179 | |
| 1.53.0 | v1169 | |

**方案3：使用Docker（⭐推荐AI Agent/服务器环境）**

AI Agent通常运行在headless/无图形界面环境，Docker是最佳方案：

**Mac/Linux:**
```bash
docker run -it --rm \
  --ipc=host \
  -v "$(pwd):/workspace" \
  -w /workspace \
  mcr.microsoft.com/playwright/python:v1.40.0-jammy \
  bash -c "pip install -r scripts/requirements.txt && python3 scripts/github_trending.py daily"
```

**Windows (PowerShell):**
```powershell
docker run -it --rm `
  --ipc=host `
  -v "${PWD}:/workspace" `
  -w /workspace `
  mcr.microsoft.com/playwright/python:v1.40.0-jammy `
  bash -c "pip install -r scripts/requirements.txt && python3 scripts/github_trending.py daily"
```

**Windows (CMD):**
```cmd
docker run -it --rm --ipc=host -v "%CD%:/workspace" -w /workspace mcr.microsoft.com/playwright/python:v1.40.0-jammy bash -c "pip install -r scripts/requirements.txt && python3 scripts/github_trending.py daily"
```

**Docker方案优势：**
- ✅ 预装Chromium浏览器，无需下载等待
- ✅ 自动headless模式，完美适配Agent环境
- ✅ 环境隔离，避免依赖冲突
- ✅ 跨平台一致（Mac/Linux/Windows/服务器）

**方案4：跳过浏览器安装（纯API模式）**

如果仅需基础功能，可跳过浏览器安装：

| 功能 | 是否需要浏览器 | 说明 |
|------|--------------|------|
| 🔥 Trending | ✅ 需要 | GitHub无官方Trending API，必须浏览器抓取 |
| 🔍 搜索 | ❌ 不需要 | 使用GitHub Search API |
| ⭐ Star/Fork | ❌ 不需要 | 使用GitHub REST API |
| 🐛 Issues/PR | ❌ 不需要 | 使用GitHub REST API |
| 📄 代码内容 | ❌ 不需要 | 使用GitHub REST API |

**纯API模式使用方法：**
```bash
# 仅需安装Python依赖，无需浏览器
pip install -r requirements.txt

# 使用API功能（搜索、Star、Issues等）
python3 scripts/github_search.py repos "machine learning"
python3 scripts/github_operations.py star owner/repo
```

**3. 登录 GitHub（二选一）**

#### 方式A — 浏览器手动登录（推荐新手）

```bash
python3 scripts/github_login.py browser
```

弹出浏览器窗口，手动输入 GitHub 账号密码完成登录。

#### 方式B — Token 登录（支持全部操作）

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
   | **Discussions** | 读取/创建讨论 |
   | **Environments** | 读取环境信息 |
   | **Issues** | 读取/创建/更新/关闭 Issues |
   | **Metadata** | 读取基础仓库信息（必需）|
   | **Packages** | 读取包信息 |
   | **Pages** | 读取 GitHub Pages 信息 |
   | **Pull requests** | 读取/合并/审查 PR |
   | **Repository security advisories** | 读取安全公告 |
   | **Secret scanning alerts** | 读取密钥扫描警报 |
   | **Workflows** | 读取工作流 |

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

**4. 验证登录**

```bash
python3 github_login.py check
```

### 🚀 使用示例

#### 查看 GitHub Trending

每条 Trending 项目包含完整 7 项信息：仓库名、链接、描述、语言、Star/Fork 数、贡献者、期间新增Star。

> 💡 **自动加载所有项目**：脚本会自动滚动页面，获取 **当日/当周/当月的所有 Trending 项目**（不仅仅是首页显示的），直到没有新项目加载为止。

```bash
python3 scripts/github_trending.py daily "" browser       # 今日所有Trending项目（全语言）
python3 scripts/github_trending.py weekly python browser   # 本周Python所有Trending项目
python3 scripts/github_trending.py monthly "" browser      # 本月所有Trending项目（全语言）
```

**输出示例：**

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
🔗 GitHub - anthropics/claude-code: Claude Code is an agentic coding tool that lives in your terminal
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
🔗 GitHub - openai/codex: Lightweight coding agent that runs in your terminal
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
🔗 GitHub - microsoft/VibeVoice: Open-Source Frontier Voice AI
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

📡 数据来源：GitHub Trending (browser) | 
```

#### 搜索项目

```bash
python3 scripts/github_search.py repos "LLM agent"          # 搜索仓库
python3 scripts/github_search.py repos "stars:>10000 language:python"
python3 scripts/github_search.py info facebook react        # 仓库详情
python3 scripts/github_search.py users "torvalds"           # 搜索用户
```

#### 用户操作

```bash
python3 scripts/github_operations.py user                    # 当前登录用户信息
python3 scripts/github_operations.py user torvalds           # 指定用户信息
python3 scripts/github_operations.py my-repos                # 当前用户的仓库
python3 scripts/github_operations.py user-repos torvalds     # 指定用户的仓库
python3 scripts/github_operations.py followers               # 当前用户粉丝
python3 scripts/github_operations.py following               # 当前用户关注的人
python3 scripts/github_operations.py follow username         # 关注用户
python3 scripts/github_operations.py unfollow username       # 取消关注
```

#### 仓库操作

```bash
python3 scripts/github_operations.py star microsoft/vscode   # Star
python3 scripts/github_operations.py unstar owner/repo       # 取消 Star
python3 scripts/github_operations.py fork owner/repo         # Fork
python3 scripts/github_operations.py watch owner/repo        # Watch
python3 scripts/github_operations.py unwatch owner/repo      # 取消 Watch
python3 scripts/github_operations.py info owner/repo         # 仓库信息
python3 scripts/github_operations.py starred                 # 列出已 Star 仓库
python3 scripts/github_operations.py create-repo my-repo "描述"  # 创建新仓库
python3 scripts/github_operations.py forks owner/repo        # 列出 Forks
python3 scripts/github_operations.py stargazers owner/repo   # 列出 Stargazers
```

#### Issues 管理

```bash
python3 scripts/github_operations.py issues microsoft/vscode open      # 列出 Issues
python3 scripts/github_operations.py issue microsoft/vscode 1234       # 获取指定 Issue
python3 scripts/github_operations.py create-issue owner/repo "Bug标题" "描述"  # 创建
python3 scripts/github_operations.py close-issue owner/repo 1234       # 关闭
python3 scripts/github_operations.py reopen-issue owner/repo 1234      # 重新打开
python3 scripts/github_operations.py labels owner/repo 1234            # 列出 Issue 标签
python3 scripts/github_operations.py add-labels owner/repo 1234 bug enhancement  # 添加标签
python3 scripts/github_operations.py lock-issue owner/repo 1234 "reason"  # 锁定 Issue
python3 scripts/github_operations.py unlock-issue owner/repo 1234      # 解锁 Issue
```

#### Pull Requests 操作

```bash
python3 scripts/github_operations.py prs microsoft/vscode open         # 列出 PRs
python3 scripts/github_operations.py pr microsoft/vscode 1234          # 获取指定 PR
python3 scripts/github_operations.py create-pr owner/repo "PR标题" feature-branch main  # 创建 PR
python3 scripts/github_operations.py close-pr owner/repo 1234          # 关闭 PR
python3 scripts/github_operations.py reopen-pr owner/repo 1234         # 重新打开 PR
python3 scripts/github_operations.py merge-pr owner/repo 1234 "标题"   # 合并 PR
python3 scripts/github_operations.py approve-pr owner/repo 1234 "LGTM" # 批准 PR
python3 scripts/github_operations.py pr-files owner/repo 1234          # PR 修改的文件
python3 scripts/github_operations.py pr-commits owner/repo 1234        # PR 的提交
python3 scripts/github_operations.py pr-reviews owner/repo 1234        # PR 审查记录
```

#### 分支管理

```bash
python3 scripts/github_operations.py branches owner/repo               # 列出分支
python3 scripts/github_operations.py branch owner/repo main            # 获取分支信息
python3 scripts/github_operations.py create-branch owner/repo new-branch main  # 创建分支
```

#### Releases 管理

```bash
python3 scripts/github_operations.py releases owner/repo               # 列出 Releases
python3 scripts/github_operations.py release owner/repo 123456         # 获取指定 Release
python3 scripts/github_operations.py create-release owner/repo v1.0.0 "Release名称" "描述"  # 创建 Release
```

#### Actions 操作

```bash
python3 scripts/github_operations.py workflows owner/repo              # 列出工作流运行
python3 scripts/github_operations.py workflow owner/repo workflow.yml  # 获取指定工作流
python3 scripts/github_operations.py trigger-workflow owner/repo workflow.yml main  # 触发工作流
```

#### 代码内容获取

```bash
python3 scripts/github_operations.py file owner/repo path/to/file.py   # 获取文件
python3 scripts/github_operations.py readme owner/repo                 # 获取 README
python3 scripts/github_operations.py ls owner/repo src                 # 列出目录
python3 scripts/github_operations.py create-file owner/repo "test.py" "提交信息" "内容"  # 创建文件
```

#### 评论操作

```bash
python3 scripts/github_operations.py comments owner/repo 1234          # 列出评论
python3 scripts/github_operations.py comment owner/repo 1234 "评论内容" # 创建评论
```

#### 通知操作

```bash
python3 scripts/github_operations.py notifications          # 列出未读通知
python3 scripts/github_operations.py notifications --all    # 列出所有通知
python3 scripts/github_operations.py repo-notifications owner/repo  # 仓库通知
python3 scripts/github_operations.py mark-read thread_id    # 标记已读
```

#### 组织操作

```bash
python3 scripts/github_operations.py orgs                   # 列出当前用户的组织
python3 scripts/github_operations.py org org_name           # 获取组织信息
python3 scripts/github_operations.py org-repos org_name     # 列出组织仓库
python3 scripts/github_operations.py org-members org_name   # 列出组织成员
```

#### 其他操作

```bash
python3 scripts/github_operations.py commits owner/repo                # 提交历史
python3 scripts/github_operations.py check                             # 登录状态
python3 scripts/github_operations.py rate-limit                        # API 限流
```

#### 浏览器自动化操作（API 不支持的功能）

> ⚠️ 这些功能 GitHub REST API 不支持，需要通过浏览器自动化实现
> 浏览器操作过程可见，操作结束后浏览器保持打开，用户可继续手动操作

**用户相关（API 不支持）：**

```bash
python3 scripts/github_browser_ops.py contributions torvalds    # 查看贡献图
python3 scripts/github_browser_ops.py activity torvalds         # 查看活动时间线
python3 scripts/github_browser_ops.py stars torvalds            # 查看 Star 列表页面
python3 scripts/github_browser_ops.py followers torvalds        # 查看粉丝列表页面
python3 scripts/github_browser_ops.py sponsors torvalds         # 查看赞助页面
```

**仓库 Insights（需要 push 权限）：**

```bash
python3 scripts/github_browser_ops.py insights owner/repo       # Pulse 概览
python3 scripts/github_browser_ops.py traffic owner/repo        # 流量统计
python3 scripts/github_browser_ops.py network owner/repo        # Fork 网络图
python3 scripts/github_browser_ops.py dependents owner/repo     # 依赖者列表
```

**代码相关：**

```bash
python3 scripts/github_browser_ops.py blame owner/repo path/file.py    # Git Blame
python3 scripts/github_browser_ops.py history owner/repo path/file.py  # 文件提交历史
python3 scripts/github_browser_ops.py compare owner/repo main dev      # 分支比较
python3 scripts/github_browser_ops.py codesearch owner/repo "keyword"  # 仓库内代码搜索
```

**设置页面：**

```bash
python3 scripts/github_browser_ops.py settings                  # 用户设置
python3 scripts/github_browser_ops.py settings owner/repo       # 仓库设置
```

**导航：**

```bash
python3 scripts/github_browser_ops.py notifications             # 通知页面
python3 scripts/github_browser_ops.py explore                   # Explore 页面
python3 scripts/github_browser_ops.py marketplace               # Marketplace
python3 scripts/github_browser_ops.py search "query"            # GitHub 搜索
python3 scripts/github_browser_ops.py goto "https://..."        # 导航到指定 URL
```

**浏览器控制：**

```bash
python3 scripts/github_browser_ops.py close                     # 关闭浏览器
```

### 🤖 Agent 指令示例

| 用户指令 | Agent 执行 |
|---------|-----------|
| "看看今天GitHub有什么热门项目" | 今日 Trending（完整7项信息） |
| "本周 Python 最火的项目" | `weekly python browser` |
| "本月 GitHub 排行榜" | `monthly "" browser` |
| "帮我搜一下 OCR 相关的项目" | 搜索仓库 |
| "帮我 Star microsoft/vscode" | Star 操作 |
| "Fork 一下 facebook/react" | Fork 操作 |
| "查看这个项目的 Issues" | 列出 Issues |
| "合并 PR #123" | 合并 Pull Request |
| "获取 README 内容" | 获取代码文件 |
| "GitHub 登录" | 启动浏览器登录 |
| "查看 GitHub 登录状态" | 登录状态检查 |

### 权限速查表

| 操作 | 所需权限 | 权限级别 |
|------|---------|---------|
| Trending 查看 | 无需登录 | - |
| 项目搜索 | 无需登录 | - |
| Star/Unstar | 无需权限 / Token | - |
| Fork | 无需权限 / Token | - |
| Watch/Unwatch | Token | Metadata (Read) |
| 查看仓库信息 | Token | Metadata (Read) |
| **列出 Issues** | Token | Issues (Read) |
| **创建/关闭 Issue** | Token | Issues (Write) |
| **列出 PRs** | Token | Pull requests (Read) |
| **合并 PR** | Token | Pull requests (Write) |
| **获取文件内容** | Token | Contents (Read) |
| **创建/更新文件** | Token | Contents (Write) |
| **查看 Actions** | Token | Actions (Read) |

---

---

<a id="english-documentation"></a>

## English Documentation

> A comprehensive GitHub assistant skill pack designed for AI Agents (Claude Code / OpenClaw / AstrBot etc.).
> Supports Trending browsing, project search, Star/Fork/Watch operations, Issues/PR management, code content access, and more.
> **Default output language: Chinese** (unless user specifies otherwise)


An all-in-one GitHub assistant skill supporting Trending browsing, repository search, Star/Fork/Watch operations, Issues/PR management, code content access, branch management, Releases, Actions operations, and more. Through REST API + Playwright browser dual mode, it covers GitHub official API and web-exclusive features (Insights, Traffic, Security, etc.). Suitable for viewing trending projects, searching repositories, and managing code collaboration.

### ✨ Features

- 🔥 **GitHub Trending** — View daily/weekly/monthly trending repos, filter by language
- 🔍 **Project Search** — Search repositories, users, view repo details
- ⭐ **Repo Operations** — Star / Unstar / Fork / Watch / Unwatch / Create Repo / List Forks & Stargazers
- 🐛 **Issues Management** — Create, list, close, reopen, comment, labels, lock
- 🔀 **Pull Requests** — Create, list, close, merge, review, comment, request reviewers
- 📄 **Code Content** — Get files, directories, README, create/update files
- 🌿 **Branch Management** — List, create, delete branches
- 🚀 **Releases Management** — List, create, update, delete releases
- ⚡ **Actions Operations** — List workflows, trigger/cancel/rerun workflows
- 👤 **User Operations** — Get user info, list repos, follow/unfollow
- 🔔 **Notifications** — List notifications, mark as read
- 🏢 **Organization Operations** — List orgs, get org info, list members
- 💬 **Comments** — Issue/PR comments
- 🌐 **Browser Automation** — Support API-unsupported operations (contributions, insights, traffic, network graph, blame, etc.)
- 🔐 **Dual Login** — Interactive browser login + Token login
- 🤖 **Dual Engine** — GitHub REST API + Playwright browser automation
- 📊 **Full Data** — Trending info includes repo name, description, language, stars, forks, contributors, period star growth

### 📦 Quick Start

**1. Install Dependencies**

```bash
cd github-assistant/scripts
pip install -r requirements.txt
```

**2. Install Browser Engine (optional, for browser mode)**

```bash
playwright install chromium
```

**3. Login to GitHub (choose one)**

#### Option A — Interactive Browser Login (recommended for beginners)

```bash
python3 scripts/github_login.py browser
```

A browser window opens. Manually enter your GitHub credentials.

#### Option B — Token Login (supports all operations)

Supports two token types: **Fine-grained PAT** (recommended) or **Classic PAT**

---

**Option 1: Fine-grained Personal Access Token (Recommended)**

More secure permission control with per-repository configuration.

1. **Open Settings**
   - Visit https://github.com/settings/tokens?type=beta
   - Or GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens

2. **Generate New Token**
   - Click "Generate new token"
   - Enter token name (e.g., GitHub-Assistant-Skill)
   - Set expiration (recommend 90 days or longer)

3. **Configure Permissions (Important!)**

   **Repository permissions — Set to Read and Write:**
   
   | Permission | Purpose |
   |------------|---------|
   | **Actions** | Read workflow runs |
   | **Administration** | Read repository management info |
   | **Checks** | Read check runs |
   | **Commit statuses** | Read commit statuses |
   | **Contents** | Read/create/update/delete files |
   | **Dependabot alerts** | Read security alerts |
   | **Deployments** | Read deployment info |
   | **Discussions** | Read/create discussions |
   | **Environments** | Read environment info |
   | **Issues** | Read/create/update/close Issues |
   | **Metadata** | Read basic repository info (required) |
   | **Packages** | Read package info |
   | **Pages** | Read GitHub Pages info |
   | **Pull requests** | Read/merge/review PRs |
   | **Repository security advisories** | Read security advisories |
   | **Secret scanning alerts** | Read secret scanning alerts |
   | **Workflows** | Read workflows |

4. **Select Repository Access**
   - **All repositories** - Access all repositories (recommended)
   - **Only select repositories** - Access specific repositories only

5. **Generate and Save Token**
   - Click "Generate token"
   - **⚠️ Copy token immediately** (cannot be viewed again after closing)
   - Run `python3 github_login.py token <TOKEN>`
   - Token will be securely stored locally after verification

---

**Option 2: Classic Personal Access Token**

Traditional token type using scopes permission model.

1. **Open Settings**
   - Visit https://github.com/settings/tokens
   - Or GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)

2. **Generate New Token**
   - Click "Generate new token (classic)"
   - Enter token name (e.g., GitHub-Assistant-Skill)
   - Set expiration (recommend 90 days or longer)

3. **Select Scopes**

   **Required Scopes:**
   
   | Scope | Purpose |
   |-------|---------|
   | `repo` | Full control of private repositories |
   | `public_repo` | Access public repositories |
   
   **Recommended Scopes:**
   
   | Scope | Purpose |
   |-------|---------|
   | `workflow` | Update GitHub Actions workflow files |
   | `read:org` | Read organization membership |
   | `read:user` | Read user profile data |
   | `read:discussion` | Read team discussions |

4. **Generate and Save Token**
   - Click "Generate token"
   - **⚠️ Copy token immediately** (cannot be viewed again after closing)
   - Run `python3 github_login.py token <TOKEN>`
   - Token will be securely stored locally after verification

---

**Token Type Comparison:**

| Feature | Fine-grained PAT | Classic PAT |
|---------|-----------------|-------------|
| Permission granularity | Per-repository, per-permission | Global scopes |
| Security | Higher, limited access scope | Lower, global permissions |
| Organization repos | Requires org admin approval | Directly available |
| Recommendation | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Use case | Production, team collaboration | Personal use, quick testing |

**4. Verify Login**

```bash
python3 github_login.py check
```

### 🚀 Usage Examples

#### View GitHub Trending

Each trending item includes all 7 fields: repo name, link, description, language, stars, forks, contributors, period star growth.

> 💡 **Auto-load all projects**: The script automatically scrolls the page to fetch **ALL daily/weekly/monthly Trending projects** (not just the first page), loading until no new projects are found.

```bash
python3 scripts/github_trending.py daily "" browser       # All today's Trending (all languages)
python3 scripts/github_trending.py weekly python browser   # All this week's Python Trending
python3 scripts/github_trending.py monthly "" browser      # All this month's Trending (all languages)
```

**Output Format Requirements (⚠️ MUST follow strictly):**

> 🔴 **IMPORTANT**: All Trending output **MUST strictly follow the format template below**. Do not create other formats.
>
> **Default Behavior**: When outputting Trending projects, the Agent **MUST strictly follow the "Standard Output Template" format below**, including:
> - Title format with date
> - Overview statistics structure
> - Detailed repo analysis format (with deep insights)
> - Today's insights section
>
> **Unless the user explicitly provides additional format requirements or special instructions**, you must NOT:
> - Omit any section
> - Change the output format
> - Use Markdown tables (forbidden in IM chat platforms)
> - Simplify or merge content

**Output Example:**

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

#### Search Projects

```bash
python3 scripts/github_search.py repos "LLM agent"          # Search repos
python3 scripts/github_search.py repos "stars:>10000 language:python"
python3 scripts/github_search.py info facebook react        # Repo details
python3 scripts/github_search.py users "torvalds"           # Search users
```

#### Repo Operations

```bash
python3 scripts/github_operations.py star microsoft/vscode   # Star
python3 scripts/github_operations.py unstar owner/repo       # Unstar
python3 scripts/github_operations.py fork owner/repo         # Fork
python3 scripts/github_operations.py watch owner/repo        # Watch
python3 scripts/github_operations.py unwatch owner/repo      # Unwatch
python3 scripts/github_operations.py info owner/repo         # Repo info
python3 scripts/github_operations.py starred                 # List starred repos
```

#### Issues Management

```bash
python3 scripts/github_operations.py issues microsoft/vscode open      # List issues
python3 scripts/github_operations.py issue microsoft/vscode 1234       # Get issue
python3 scripts/github_operations.py create-issue owner/repo "Bug title" "Description"
python3 scripts/github_operations.py close-issue owner/repo 1234       # Close
python3 scripts/github_operations.py reopen-issue owner/repo 1234      # Reopen
```

#### Pull Requests

```bash
python3 scripts/github_operations.py prs microsoft/vscode open         # List PRs
python3 scripts/github_operations.py pr microsoft/vscode 1234          # Get PR
python3 scripts/github_operations.py merge-pr owner/repo 1234 "Title"  # Merge PR
python3 scripts/github_operations.py approve-pr owner/repo 1234 "LGTM" # Approve PR
```

#### Code Content

```bash
python3 scripts/github_operations.py file owner/repo path/to/file.py   # Get file
python3 scripts/github_operations.py readme owner/repo                 # Get README
python3 scripts/github_operations.py ls owner/repo src                 # List directory
python3 scripts/github_operations.py create-file owner/repo "test.py" "Commit msg" "Content"
```

#### Comments

```bash
python3 scripts/github_operations.py comments owner/repo 1234          # List comments
python3 scripts/github_operations.py comment owner/repo 1234 "Comment text"
```

#### Other Operations

```bash
python3 scripts/github_operations.py commits owner/repo                # Commit history
python3 scripts/github_operations.py branches owner/repo               # List branches
python3 scripts/github_operations.py releases owner/repo               # Releases
python3 scripts/github_operations.py workflows owner/repo              # Actions workflows
python3 scripts/github_operations.py check                             # Auth status
python3 scripts/github_operations.py rate-limit                        # API rate limit
```

### 🤖 Agent Command Examples

| User Command | Agent Action |
|---------|-----------|
| "看看今天GitHub有什么热门项目" | Today's Trending (full 7 fields) |
| "本周 Python 最火的项目" | `weekly python browser` |
| "本月 GitHub 排行榜" | `monthly "" browser` |
| "帮我搜一下 OCR 相关的项目" | Search repos |
| "帮我 Star microsoft/vscode" | Star operation |
| "Fork 一下 facebook/react" | Fork operation |
| "查看这个项目的 Issues" | List Issues |
| "合并 PR #123" | Merge Pull Request |
| "获取 README 内容" | Get code file |
| "GitHub 登录" | Launch browser login |
| "查看 GitHub 登录状态" | Check login status |

### Permission Quick Reference

| Operation | Required Permission | Level |
|-----------|---------------------|-------|
| Trending view | No login required | - |
| Project search | No login required | - |
| Star/Unstar | No permission / Token | - |
| Fork | No permission / Token | - |
| Watch/Unwatch | Token | Metadata (Read) |
| View repo info | Token | Metadata (Read) |
| **List Issues** | Token | Issues (Read) |
| **Create/Close Issue** | Token | Issues (Write) |
| **List PRs** | Token | Pull requests (Read) |
| **Merge PR** | Token | Pull requests (Write) |
| **Get file content** | Token | Contents (Read) |
| **Create/Update file** | Token | Contents (Write) |
| **View Actions** | Token | Actions (Read) |

---

### 📁 Project Structure

```
github-assistant/
├── SKILL.md                          # Skill definition (Agent reads this)
├── README.md                         # Documentation (Chinese + English)
├── scripts/
│   ├── github_trending.py            # Trending fetcher (browser only)
│   ├── github_search.py              # Search tool
│   ├── github_operations.py          # Full operations (Star/Fork/Issues/PR/Code/Comments)
│   ├── github_login.py               # Login manager
│   └── requirements.txt              # Python dependencies
├── references/
│   └── github_api_endpoints.md       # GitHub API endpoint reference
├── assets/                           # Static resources
├── github_token.txt                  # Token storage (auto-generated, gitignored)
└── github_auth.json                  # Browser session (auto-generated, gitignored)
```

### ⚙️ Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────┐
│  User Input  │────▶│  Agent (Claude)   │────▶│   Scripts    │
│ (Natural Lang)│    │ Intent + Route    │     │  (Python)    │
└─────────────┘     └──────────────────┘     └──────┬───────┘
                                                     │
                                            ┌────────┴────────┐
                                            ▼                 ▼
                                    ┌──────────────┐  ┌──────────────┐
                                    │  GitHub API  │  │  Playwright  │
                                    │  (REST)      │  │  (Browser)   │
                                    └──────────────┘  └──────────────┘
```

### 🔒 Security

- Token is stored locally in `~/.github-assistant/github_token.txt`
- Browser session stored in `~/.github-assistant/github_auth.json`
- **No sensitive data is stored in this skill folder** — safe to upload to public repos
- Fine-grained PAT allows precise permission control
- Clear error messages on token verification failures

### 📋 Dependencies

- Python 3.8+
- requests>=2.28.0
- playwright>=1.40.0 (optional, for browser mode / Trending)

> Note: `beautifulsoup4`, `lxml`, `pyyaml` have been removed. Trending scraping now uses Playwright browser mode only.

### 📄 License

MIT License
