# openclaw-deploy

<p align="center">
  <strong>OpenClaw 本地能力交互式部署向导</strong><br>
  记忆栈 · 视频处理 · 微信集成 · 维护 Cron 任务
</p>

<p align="center">
  <a href="README.md">English</a> · <a href="README.zh-CN.md">中文</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/clawhub-openclaw--deploy-brightgreen?style=for-the-badge" alt="ClawHub">
  <img src="https://img.shields.io/badge/OpenClaw-skill-orange?style=for-the-badge" alt="OpenClaw">
  <img src="https://img.shields.io/badge/许可证-MIT-blue?style=for-the-badge" alt="License">
</p>

一个 [OpenClaw](https://github.com/openclaw/openclaw) skill，逐步引导你部署完整的本地能力栈 — 每个 Phase 之间有确认门控，不会跳过任何步骤。

告诉你的 agent 运行本 skill，它会检查依赖、安装每个组件、验证成功，并在进入下一 Phase 前暂停确认。可以全部部署，也可以只选需要的组件。

---

## 部署内容

| Phase | 组件 | 功能 |
|-------|------|------|
| **A** | [记忆栈](https://github.com/OttoPrua/openclaw-memory-manager) | qmd（语义搜索）+ LosslessClaw（上下文压缩） |
| **B** | [Memory Manager Skill](https://clawhub.ai/OttoPrua/agent-memory-protocol) | Agent 记忆写入/读取协议 |
| **C** | [vid2md](https://github.com/OttoPrua/vid2md) | 视频教程 → 结构化 Markdown |
| **D** | [微信插件](https://github.com/OttoPrua/openclaw-wechat-bot) | 微信群聊集成（仅 macOS） |
| **E** | Cron 任务 | 自动化记忆维护 |

每个 Phase 相互独立，可以全部部署或只选需要的。

---

## 使用方式

### 安装 skill

```bash
clawhub install openclaw-deploy
```

或直接克隆：
```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/OttoPrua/openclaw-deploy.git
```

### 运行

直接告诉你的 OpenClaw agent：

```
运行 openclaw-deploy skill
```

或

```
帮我部署 OpenClaw 本地能力
```

Agent 会：
1. 询问要部署哪些组件
2. 检查依赖并报告缺少的工具
3. 逐步执行每个选中 Phase 的安装和验证
4. Phase 之间暂停等待你的确认
5. 最后展示完整状态表

---

## Phase 详情

### Phase A — 记忆栈

- 安装 **qmd**（`@tobilu/qmd`）— 对 Markdown 文件做本地语义 + BM25 搜索
- 创建指向你工作区的 `memory-root` 和 `blackboard` collection
- 配置 `openclaw.json` 的 `qmd` 记忆后端
- 安装 **LosslessClaw**（`@martian-engineering/lossless-claw`）— DAG 分层上下文压缩
- 重启 gateway

→ 完整文档：[openclaw-memory-manager](https://github.com/OttoPrua/openclaw-memory-manager)

### Phase B — Memory Manager Skill

- 从 ClawHub 安装 `agent-memory-protocol` skill
- 如不存在则初始化 `memory/` 目录结构

→ 完整文档：[ClawHub: agent-memory-protocol](https://clawhub.ai/OttoPrua/agent-memory-protocol)

### Phase C — vid2md

- 克隆 vid2md 仓库
- 安装 Python 依赖（含平台适配的 ASR 模型）
- 可选下载 FunASR（中文）、mlx-whisper（英文/Apple Silicon）
- 可选拉取视觉模型用于 AI 帧描述
- 运行冒烟测试

→ 完整文档：[vid2md](https://github.com/OttoPrua/vid2md)

### Phase D — 微信插件

- 克隆微信插件仓库
- 配置 `openclaw.json` 的 channel 设置
- 引导完成微信通知和辅助功能权限设置

> 仅 macOS。

→ 完整文档：[openclaw-wechat-bot](https://github.com/OttoPrua/openclaw-wechat-bot)

### Phase E — Cron 任务

- 添加所选维护 cron 任务：
  - **Dream Cycle** — 每周记忆整合
  - **每日进度同步** — 项目状态同步到 Blackboard
  - **每月清理** — 归档旧 session 日志

→ 完整文档：[cron 参考配置](https://github.com/OttoPrua/openclaw-memory-manager/tree/main/cron)

---

## 依赖

Skill 会自动检查，以下是完整清单：

| 工具 | 用途 | 安装方式 |
|------|------|---------|
| git | 所有组件 | 系统包管理器 |
| python3 3.9+ | vid2md | 系统或 pyenv |
| brew | macOS 安装 | https://brew.sh |
| ffmpeg | vid2md | `brew install ffmpeg` |
| ollama | vid2md（AI 描述） | https://ollama.com |
| bun 或 node | qmd 安装 | https://bun.sh |
| openclaw | 所有组件 | `npm install -g openclaw` |

---

## 相关链接

- [OpenClaw](https://github.com/openclaw/openclaw)
- [OpenClaw 文档](https://docs.openclaw.ai)
- [ClawHub](https://clawhub.ai) — 社区 skills
- [Discord](https://discord.gg/clawd)

## 许可证

MIT
