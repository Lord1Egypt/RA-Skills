<div align="center">

# 🤖 Omnibot

### AI Agent 的浏览器基础设施

[![Version](https://img.shields.io/badge/version-2.4.0-blue?style=flat-square)](./SKILL.md)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)]()

[![SkillHub](https://img.shields.io/badge/SkillHub-omnibot-00A8E0?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNOCAwTDAgNFYxMkw4IDE2TDE2IDEyVjRMOCAwWiIgZmlsbD0id2hpdGUiLz48L3N2Zz4=)](https://skillhub.cn/skills/omnibot)
[![ClawHub](https://img.shields.io/badge/ClawHub-omnibot--skills-FF6B35?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJNOCAxQzQuMTMgMSAxIDQuMTMgMSA4QzEgMTEuODcgNC4xMyAxNSA4IDE1QzExLjg3IDE1IDE1IDExLjg3IDE1IDhDMTUgNC4xMyAxMS44NyAxIDggMVpNOCAzQzkuNjYgMyAxMSA0LjM0IDExIDZDMTEgNy42NiA5LjY2IDkgOCA5QzYuMzQgOSA1IDcuNjYgNSA2QzUgNC4zNCA2LjM0IDMgOCAzWiIgZmlsbD0id2hpdGUiLz48L3N2Zz4=)](https://clawhub.ai/dennisjcy/skills/omnibot-skills)

[![Chrome 应用商店](https://img.shields.io/badge/Chrome%20应用商店-浏览器扩展-4285F4?style=flat-square&logo=google-chrome&logoColor=white)](https://chromewebstore.google.com/detail/fojlpefamkmjbboafmjkkaejohagbdgn)

**将 AI agent 连接到真实的 Chromium 浏览器。**<br>
读取页面。点击按钮。填充表单。导航。提取内容。收集证据。<br>
通过本地守护进程和 CLI 完成一切——无头浏览器？不需要。脆弱的选择器？不需要。

[快速开始](#-快速开始) · [工作原理](#-工作原理) · [核心功能](#-核心功能) · [文档](#-文档)

🌐 **[English](./README.md)** · **[日本語](./README_ja.md)** · **[한국어](./README_ko.md)** · **[Español](./README_es.md)** · **[Français](./README_fr.md)** · **[Deutsch](./README_de.md)**

</div>

---

## 🚀 Omnibot 是什么？

Omnibot 是 AI Agent 的浏览器基础设施。它让 **Hermes**、**Claude Code**、**Codex**、**OpenCode** 等 AI agent 能够连接到一个真实的 Chromium 浏览器——就像人类一样操作。

```
┌──────────────┐         ┌──────────────┐         ┌──────────────────┐
│   AI Agent   │ ──CLI──▶│  Omnibot     │ ──WS──▶ │  Chromium        │
│  (Hermes,    │         │  守护进程     │         │  扩展             │
│   Claude...) │         │  :18765      │         │  (真实浏览器)     │
└──────────────┘         └──────────────┘         └──────────────────┘
```

**不是 Puppeteer。不是 Playwright。不是无头浏览器。**<br>
**是真实的浏览器。真实的 Cookie。真实的扩展。真实的用户会话。**

## 🎬 实际演示

<table>
<tr>
<td width="50%" align="center" valign="top">

### 公众号后台数据自动分析
**Hermes 分析微信公众号数据及趋势**

[![公众号数据分析](https://img.youtube.com/vi/xZ-_0TInCRE/maxresdefault.jpg)](https://youtu.be/xZ-_0TInCRE)

*Hermes 智能体自动登录微信公众号后台，提取用户增长、文章阅读、用户画像等数据，生成完整的数据分析报告。*

</td>
<td width="50%" align="center" valign="top">

### X 自动化获取前沿 AI 信息
**Hermes 速览 X 总结最新 AI 资讯**

[![X AI 资讯](https://img.youtube.com/vi/PknnOhAE6bI/maxresdefault.jpg)](https://youtu.be/PknnOhAE6bI)

*Hermes 智能体自动浏览 X（Twitter），搜索和筛选最新 AI 资讯，自动整理成结构化的资讯速览。*

</td>
</tr>
<tr>
<td width="50%" align="center" valign="top">

### 裁决文书分析
**Hermes 检索凶杀案裁决文书并分析共性特征**

[![裁决文书分析](https://img.youtube.com/vi/PQQNDbzgXgQ/maxresdefault.jpg)](https://youtu.be/PQQNDbzgXgQ)

*Hermes 智能体自动在裁判文书网检索凶杀案，精读8份案件全文，生成包含犯罪人画像、动机分析、作案特征的完整共性分析报告。*

</td>
<td width="50%" align="center" valign="top">

### 头条号文章自动发布
**Hermes 将工作区文章发布到头条号**

[![头条号发布](https://img.youtube.com/vi/elUxHLp1C4Q/maxresdefault.jpg)](https://youtu.be/elUxHLp1C4Q)

*Hermes 智能体自动登录头条号，填写标题、正文并插入配图，设置封面和广告收益，预览后一键发布文章。*

</td>
</tr>
</table>

<div align="center">

**更多应用场景等你探索！**

</div>

## ✨ 核心功能

<table>
<tr>
<td width="50%" valign="top">

### 🔍 观察
- 将渲染后的页面内容读取为干净的文本/Markdown
- 快照完整的无障碍树，带交互式引用
- 截取整页或特定视觉区域的截图
- 检查控制台日志、网络流量和 DOM 状态

</td>
<td width="50%" valign="top">

### 🎯 操作
- 通过语义角色、占位符或无障碍引用点击元素
- 填充表单、选择选项、勾选复选框——带事件派发
- 在页面间导航、管理标签页和标签组
- 拖拽、滚动、输入、按键——类人交互

</td>
</tr>
<tr>
<td width="50%" valign="top">

### ✅ 验证
- 等待条件：URL 变化、元素可见、文本出现
- 断言元素状态：启用、可见、已勾选、值
- 捕获网络日志和 API 证据
- 多步验证，带观察 → 操作 → 验证循环

</td>
<td width="50%" valign="top">

### 🛡️ 可靠
- 会话令牌工作流隔离
- 标签页定向命令——无意外跨标签页变更
- 7 层回退链，从语义到原始 CDP
- 内置反模式防护和安全规则

</td>
</tr>
</table>

## ⚡ 快速开始

### 1. 安装 CLI

通过 npm 全局安装 Omnibot CLI（推荐）：

```bash
npm install -g @omniaibot/omnibot
```

自动检测平台并安装对应的二进制文件。安装后运行 `omnibot doctor` 验证安装。

### 2. 加载浏览器扩展

- 打开 [Chrome Web Store 中的 Omnibot 扩展页面](https://chromewebstore.google.com/detail/fojlpefamkmjbboafmjkkaejohagbdgn)
- 点击「添加至 Chrome」并完成安装
- 安装后点击浏览器右上角的 Omnibot 扩展图标
- 确认扩展显示**已连接**，或复制弹窗中的机器码用于购买激活码

默认情况下，扩展会连接本地 WebSocket 服务 `127.0.0.1:18765`。

扩展弹窗配置：
- **WebSocket 地址**：`ws://127.0.0.1:18765`
- 连接状态会自动刷新
- 如果连接失败，先运行 `omnibot doctor` 检查守护进程状态

### 3. 检查连接

不需要手动启动守护进程。直接运行任意浏览器命令时，omnibot CLI 会自动启动本地守护进程，浏览器扩展会通过 WebSocket 连接到 `127.0.0.1:18765`。

```bash
omnibot doctor
omnibot tabs
```

`doctor` 检查守护进程和扩展状态。`tabs` 列出可用的浏览器标签页。

如果 `doctor` 显示扩展未连接，请打开 Chrome/Edge，加载或重新加载浏览器扩展，并保持至少一个 HTTP/HTTPS 标签页打开。

### 4. 安装 Agent 技能

Omnibot v2 通过技能替代 MCP 提示词注入：

```bash
omnibot skills install --agent hermes --profile nuwa
omnibot skills install --agent opencode
omnibot skills install --agent claude
omnibot skills install --agent codex
```

查看内置技能路径：

```bash
omnibot skills path
```

Omnibot 内置了流行 AI Agent 的技能配置。从快速开始页面选择你的 Agent 即可获取安装命令。

## 🔄 工作原理

每个浏览器操作都遵循严格的循环：

```
  ┌──────────┐      ┌──────────┐      ┌──────────┐
  │  观察    │ ───▶ │  操作    │ ───▶ │  验证    │──┐
  │          │      │ (一次)   │      │          │  │
  └──────────┘      └──────────┘      └──────────┘  │
       ▲                                              │
       └──────────── 失败则回退重试 ──────────────────┘
```

1. **观察** — 快照页面、读取内容、检查当前状态
2. **操作** — 使用最佳可用模式执行一次操作
3. **验证** — 用证据确认预期的状态变化

如果验证失败，agent 重新观察并尝试下一层回退。不盲目重试。不猜测。

## 🧩 原生命令路由

Omnibot 总是为任务选择最窄的原生命令：

| 意图 | 原生命令 | 不要用 |
|------|---------|--------|
| 读取页面内容 | `read`, `get text` | ~~`execute-js`~~ |
| 点击按钮 | `find --action click`, `click @eN` | ~~`querySelector().click()`~~ |
| 填充表单 | `fill`, `type` | ~~`element.value = "..."`~~ |
| 等待状态 | `wait` | ~~`sleep 3`~~ |
| 滚动 | `scroll`, `scrollintoview` | ~~`window.scrollTo()`~~ |

**原生优先。JavaScript 是回退，不是捷径。**

## 🏗️ 架构

```
Agent Skill (SKILL.md)
    │
    ▼
omnibot CLI  ──────────────────────────────┐
    │                                       │
    ▼                                       ▼
本地守护进程 (:18765)                Chromium 扩展
    │                                       │
    ├── 会话管理                            ├── DOM 访问
    ├── 命令路由                            ├── 无障碍树
    ├── 标签页追踪                          ├── 网络拦截
    └── 工作流隔离                          └── 视觉区域检测
```

**核心设计原则：**
- **可靠性 > 便利性** — 每个操作都被验证
- **显式状态 > 隐式状态** — 无隐藏假设
- **模式 > 命令** — 从任务出发，而非 API
- **允许回退，但不优先**

## 📚 文档

| 资源 | 描述 |
|------|------|
| [SKILL.md](./SKILL.md) | 完整的 agent 执行规范 |
| [命令参考](./references/command-reference.md) | 完整的 CLI 命令查询 |
| [操作模式](./references/operation-patterns.md) | 读取、点击、填充、滚动、导航、等待、提取、批处理 |
| [反模式](./references/anti-patterns.md) | 常见错误及如何避免 |
| [调试与证据](./references/debugging-and-evidence.md) | 截图、网络日志、追踪、录制/回放 |
| [会话与标签页](./references/session-and-tabs.md) | 工作流隔离和标签页定向 |
| [回退操作](./references/fallback-operations.md) | 7 层回退链详解 |

## 🤝 兼容的 Agent

Omnibot 适用于任何可以执行 CLI 命令的 agent 系统：

- 🧠 **Hermes** — 原生集成
- 🟠 **Claude Code** — 通过 skill 文件
- 📦 **Codex** — 通过 skill 文件
- 🔓 **OpenCode** — 通过 skill 文件
- 🔧 **任何支持 CLI 的 agent** — 通过 `omnibot` 命令

## 📋 示例工作流

```bash
# 设置工作流上下文
export OMNIBOT_SESSION_TOKEN=research

# 打开新标签页
omnibot open "https://github.com"

# 快照页面，带交互式引用
omnibot snapshot -i --tab-id $TAB_ID

# 点击搜索框并输入
omnibot find placeholder "Search GitHub" --action type \
  --action-value "omnibot" --tab-id $TAB_ID

# 按回车
omnibot press Enter --tab-id $TAB_ID

# 等待结果
omnibot wait --text "repositories" --tab-id $TAB_ID

# 读取结果
omnibot read --tab-id $TAB_ID
```

## 📄 许可证

专有许可证。详见 LICENSE 文件。

---

<div align="center">

**为需要"看到"网页的 agent 而生——而非仅仅抓取。**

[⭐ 在 GitHub 上 Star](https://github.com/DennisJcy/Omnibot-skills) · [📖 阅读 Skill 规范](./SKILL.md)

</div>
