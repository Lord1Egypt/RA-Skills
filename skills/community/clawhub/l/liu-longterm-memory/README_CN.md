# Liu Longterm Memory 🧠

**AI 智能体终极记忆系统。** 再也不会丢失上下文。

[![npm version](https://img.shields.io/npm/v/liu-longterm-memory.svg?style=flat-square)](https://www.npmjs.com/package/liu-longterm-memory)
[![npm downloads](https://img.shields.io/npm/dm/liu-longterm-memory.svg?style=flat-square)](https://www.npmjs.com/package/liu-longterm-memory)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

---

## 兼容平台

<p align="center">
  <img src="https://img.shields.io/badge/Claude-AI-orange?style=for-the-badge&logo=anthropic" alt="Claude AI" />
  <img src="https://img.shields.io/badge/GPT-OpenAI-412991?style=for-the-badge&logo=openai" alt="GPT" />
  <img src="https://img.shields.io/badge/ZhipuAI-智谱-blue?style=for-the-badge" alt="ZhipuAI" />
  <img src="https://img.shields.io/badge/Cursor-IDE-000000?style=for-the-badge" alt="Cursor" />
  <img src="https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=for-the-badge" alt="LangChain" />
</p>

<p align="center">
  <strong>适用于：</strong> Clawdbot · Moltbot · Claude Code · 任何 AI 智能体
</p>

---

6 层记忆架构，打造坚不可摧的 AI 记忆：

- ✅ **WAL 预写日志协议** — 先写后答，对抗压缩和崩溃
- ✅ **LanceDB 向量搜索** — 语义召回相关记忆（可选）
- ✅ **Git-Notes 知识图谱** — 结构化决策，分支感知
- ✅ **文件归档** — 人类可读的 MEMORY.md + 每日日志
- ✅ **备份** — zip 打包或 Git 远程仓库（GitHub/Gitee）同步
- ✅ **记忆卫生** — 保持向量精简，防止 token 浪费
- ✅ **自动提取** — LLM 驱动的事实提取（智谱免费模型或零依赖）

## 快速开始

```bash
# 国内用户推荐使用镜像加速
npx --registry https://registry.npmmirror.com liu-longterm-memory init

# 或直接使用
npx liu-longterm-memory init

# 检查状态
npx liu-longterm-memory status

# 创建今日日志
npx liu-longterm-memory today

# 备份记忆（zip 打包）
npx liu-longterm-memory backup

# 备份记忆（Git 提交 + 推送）
npx liu-longterm-memory backup --git

# 从备份恢复
npx liu-longterm-memory restore memory-backup-20260404.zip
```

## 架构

```
┌─────────────────────────────────────────────────────┐
│              ELITE LONGTERM MEMORY                  │
├─────────────────────────────────────────────────────┤
│  热内存            温存储            冷存储          │
│  SESSION-STATE.md → LanceDB      → Git-Notes       │
│  (对抗压缩)        (语义搜索)      (永久决策)       │
│         │              │                │          │
│         └──────────────┼────────────────┘          │
│                        ▼                           │
│                   MEMORY.md                        │
│                 (精选长期记忆)                       │
└─────────────────────────────────────────────────────┘
```

## 6 层记忆体系

| 层级 | 文件/系统 | 用途 | 持久性 |
|------|----------|------|--------|
| 1. 热内存 | SESSION-STATE.md | 当前任务上下文 | 对抗压缩/重启 |
| 2. 温存储 | LanceDB | 语义搜索 | 自动召回（可选） |
| 3. 冷存储 | Git-Notes | 结构化决策 | 永久 |
| 4. 归档 | MEMORY.md + daily/ | 人类可读 | 精选 |
| 5. 备份 | zip / Git 远程 | 跨设备同步 | 可选 |
| 6. 自动提取 | Agent 规则 / GLM-4-Flash | 事实提取 | 内置 |

## WAL 预写日志协议

**核心思想：** 先写状态，再回复用户。

```
用户: "这个项目用 Tailwind，不用 vanilla CSS"

Agent（内部流程）:
1. 写入 SESSION-STATE.md → "决策：使用 Tailwind"
2. 然后回复 → "好的，就用 Tailwind..."
```

如果先回复再保存，一旦崩溃或压缩，上下文就丢了。WAL 确保持久性。

## 记忆为什么会失败（以及如何修复）

| 问题 | 原因 | 修复 |
|------|------|------|
| 什么都忘了 | memory_search 未启用 | 启用 memorySearch + 配置 embedding 服务 |
| 重复犯错 | 没有记录教训 | 写入 memory/lessons.md |
| 子 Agent 隔离 | 没有继承上下文 | 在任务提示中传递关键上下文 |
| 事实未被捕获 | 未启用自动提取 | Agent 默认自动提取；或使用 LLM 批量提取 |

## 自动事实提取（LLM 驱动）

Agent 会自动从每次对话中提取偏好、决策、截止日期和纠正信息。两种模式：

1. **Agent 规则驱动**（零依赖）— Agent 遵循提取规则，无需 API
2. **LLM 批量提取**（推荐）— 使用智谱 GLM-4-Flash 免费模型进行结构化提取

详见 [SKILL.md](./SKILL.md) Layer 6。

## Embedding 服务配置

在配置文件（`~/.openclaw/openclaw.json` 或 `~/.clawdbot/clawdbot.json`）中配置。

> **核心记忆无需 API Key。** 向量搜索是可选增强功能。

### 智谱AI（推荐，免费注册送 2500 万 tokens）

```json
{
  "memorySearch": {
    "enabled": true,
    "provider": "openai-compatible",
    "baseURL": "https://open.bigmodel.cn/api/paas/v4",
    "model": "embedding-3",
    "apiKeyEnv": "ZHIPUAI_API_KEY",
    "sources": ["memory"]
  }
}
```

```bash
# 在 https://bigmodel.cn/ 免费注册获取 Key
export ZHIPUAI_API_KEY="your-key"
```

### 更多 Embedding 服务

| 服务商 | baseURL | 模型 | 免费额度 |
|--------|---------|------|----------|
| **智谱AI** | `https://open.bigmodel.cn/api/paas/v4` | `embedding-3` | 2500 万 tokens 免费 |
| **Ollama（本地）** | `http://localhost:11434/v1` | `nomic-embed-text` | 完全免费离线 |
| **DeepSeek** | `https://api.deepseek.com/v1` | `deepseek-embedding` | 有免费额度 |
| **通义千问** | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `text-embedding-v3` | 有免费额度 |
| **OpenAI** | `https://api.openai.com/v1` | `text-embedding-3-small` | 付费 |

详见 [SKILL.md](./SKILL.md) 完整配置指南。

## 生成的文件

```
workspace/
├── SESSION-STATE.md    # 热内存（当前上下文）
├── MEMORY.md           # 精选长期记忆
└── memory/
    ├── 2026-04-04.md   # 每日日志
    └── ...
```

## 命令

```bash
elite-memory init          # 初始化记忆系统
elite-memory status        # 检查健康状态
elite-memory today         # 创建今日日志
elite-memory backup        # zip 备份记忆文件
elite-memory backup --git  # Git 提交 + 推送备份
elite-memory restore <f>   # 从备份文件恢复
elite-memory help      # 显示帮助
```

## 国内用户指南

### 安装加速

```bash
# 使用 npmmirror 镜像加速
npx --registry https://registry.npmmirror.com liu-longterm-memory init

# 或全局设置镜像
npm config set registry https://registry.npmmirror.com
```

### 服务可用性

| 服务 | 国内可用性 | 说明 |
|------|-----------|------|
| **核心记忆**（SESSION-STATE.md, MEMORY.md, 每日日志） | ✅ 完全可用 | 纯本地文件，无网络依赖 |
| **LanceDB + 智谱AI** | ✅ 完全可用 | 智谱 API 国内直连，免费注册送 2500 万 tokens |
| **LanceDB + Ollama** | ✅ 完全可用 | 本地运行，无需网络 |
| **LanceDB + DeepSeek** | ✅ 完全可用 | DeepSeek API 国内直连 |
| **Git-Notes** | ✅ 完全可用 | 本地 git 操作 |
| **LLM 事实提取（GLM-4-Flash）** | ✅ 完全可用 | 智谱免费模型，国内直连 |
| **备份（zip / Gitee）** | ✅ 完全可用 | zip 本地备份 或 Gitee 远程同步 |
| **ClawdHub** | ✅ 有国内镜像 | 使用 `mirror-cn.clawhub.com` |

### 推荐配置

1. 使用**智谱AI**或**Ollama**作为 embedding 服务
2. 使用**内置自动提取** + **GLM-4-Flash**（免费，国内直连）
3. 使用 **zip** 或 **Gitee** 远程仓库备份记忆文件
4. 通过国内镜像安装 npm 包

## 链接

- [完整文档 (SKILL.md)](./SKILL.md)
- [ClawdHub](https://clawdhub.com/skills/liu-longterm-memory)
- [ClawdHub 国内镜像](https://mirror-cn.clawhub.com)
- [GitHub](https://github.com/louiseliu/liu-longterm-memory)

---

> **项目来源：** 本项目基于 [elite-longterm-memory](https://github.com/NextFrontierBuilds/elite-longterm-memory)（作者 [@NextXFrontier](https://x.com/NextXFrontier)）改进。主要改动：适配国内用户、集成智谱AI、支持多 embedding 服务商、中文文档。
