# oclaw-hermes v3.0

**OpenClaw × Hermes × DeerFlow 深度融合智能体架构**

> Agent 的边界，就是世界的边界。

## 简介

`oclaw-hermes` 是专为 OpenClaw 平台打造的 **下一代智能体架构**，深度融合三大核心系统：

- **Hermes 五层自进化记忆** (mflow v2.0)
- **DeerFlow 六大智能体协作** (LangGraph编排)
- **OpenClaw 58+ Skills 生态**

实现记忆驱动的智能体路由、Skill-记忆双向增强、跨平台状态同步的完整闭环。

### v3.0 核心创新

| 特性 | 说明 |
|------|------|
| **统一核心** | UnifiedCore 深度融合三大系统 |
| **记忆驱动路由** | 基于记忆上下文智能选择智能体 |
| **Skill-记忆双向增强** | Skill调用自动沉淀为记忆，记忆指导Skill选择 |
| **六智能体协作** | Lead/Research/Code/Browser/Memory/Skill |
| **自动记忆提取** | 会话内容实时提取事实，自动分层存储 |
| **图记忆推理** | 实体关系网络支持复杂推理查询 |
| **跨平台同步** | OpenClaw/Hermes/DeerFlow 三端记忆实时同步 |

### 核心能力矩阵

| 维度 | OpenClaw | Hermes | DeerFlow | oclaw-hermes |
|------|----------|--------|----------|--------------|
| **技能生态** | ✅ 58+ Skills | ✅ 技能自动创建 | ✅ 技能管理 API | ✅ 三端同步 |
| **记忆系统** | ❌ 会话隔离 | ✅ 三层记忆 | ✅ 线程持久化 | ✅ mflow 记忆流 |
| **多智能体** | ❌ 单 Agent | ⚠️ 子 Agent 委托 | ✅ LangGraph 编排 | ✅ 智能体集群 |
| **研究能力** | ❌ 无 | ⚠️ 基础搜索 | ✅ 深度研究链 | ✅ 一键研究 |
| **代码执行** | ✅ 本地执行 | ✅ 多后端 | ✅ 沙箱执行 | ✅ 安全隔离 |
| **浏览器** | ❌ 无 | ✅ 浏览器工具 | ✅ 自动化浏览 | ✅ 视觉感知 |
| **部署方式** | 云端 | 本地/Docker | Docker/本地 | **全场景覆盖** |

## 核心特性

### 1. 三位一体架构

```
┌─────────────────────────────────────────────────────────────┐
│                      oclaw-hermes                           │
│              (OpenClaw × Hermes × DeerFlow)                 │
├───────────────┬───────────────────┬─────────────────────────┤
│   OpenClaw    │      Hermes       │       DeerFlow          │
│   技能生态    │    自进化记忆     │    多智能体协作         │
├───────────────┼───────────────────┼─────────────────────────┤
│ • 58+ Skills  │ • 三层记忆体系    │ • LangGraph 编排        │
│ • 工程咨询    │ • 技能自动创建    │ • 子智能体集群          │
│ • 大师系列    │ • 长期记忆        │ • 深度研究链            │
│ • 专业工具    │ • 多平台网关      │ • 代码沙箱              │
└───────────────┴───────────────────┴─────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   mflow 记忆流   │
                    │  (记忆同步中枢)  │
                    └─────────────────┘
```

### 2. mflow 记忆流系统

独创的 **记忆流 (Memory Flow)** 架构，实现三端记忆无缝同步：

```yaml
mflow:
  layers:
    - layer_1: 即时记忆      # 当前会话上下文
    - layer_2: 短期记忆      # 最近 7 天会话
    - layer_3: 长期记忆      # 持久化知识库
    - layer_4: 技能记忆      # Skill 使用经验
    - layer_5: 专家记忆      # 蒸馏的专家思维
  
  sync:
    openclaw: 实时同步 Skill 调用记录
    hermes:   双向同步记忆状态
    deerflow: 线程级记忆持久化
  
  bridge:
    - 会话状态桥接
    - 技能调用桥接
    - 记忆检索桥接
    - 专家思维桥接
```

### 3. 智能体集群

基于 DeerFlow 的 **LangGraph 多智能体编排**：

| 智能体 | 职责 | 触发条件 |
|--------|------|----------|
| **Lead Agent** | 意图识别、任务分发 | 所有请求 |
| **Research Agent** | 深度研究、信息收集 | 研究类任务 |
| **Code Agent** | 代码生成、执行、调试 | 编程类任务 |
| **Browser Agent** | 网页浏览、数据提取 | 需要外部信息 |
| **Skill Agent** | Skill 调用、管理 | 需要专业技能 |
| **Memory Agent** | 记忆检索、更新 | 需要上下文 |
| **Expert Agent** | 专家思维蒸馏 | 需要专家视角 |

### 4. 深度研究链

继承 DeerFlow 的研究能力，实现 **一键深度研究**：

```
用户请求
    │
    ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  问题分解   │───▶│  多源搜索   │───▶│  信息验证   │
└─────────────┘    └─────────────┘    └─────────────┘
                                              │
    ┌─────────────────────────────────────────┘
    ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  综合分析   │───▶│  报告生成   │───▶│  技能沉淀   │
└─────────────┘    └─────────────┘    └─────────────┘
```

## 部署指南

### 前置要求

- Docker & Docker Compose
- Python 3.10+
- Node.js 18+
- OpenClaw CLI (`openclawmp`)

### 快速部署

```bash
# 1. 克隆仓库
git clone https://github.com/ruiyongwang/oclaw-hermes.git
cd oclaw-hermes

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 填入 API Keys

# 3. Docker 启动三件套
docker-compose up -d

# 4. 验证部署
python scripts/verify.py
```

### 手动部署

```bash
# 1. 安装 Hermes Agent
pip install hermes-agent

# 2. 安装 DeerFlow
git clone https://github.com/bytedance/deerflow.git
cd deerflow && docker-compose up -d

# 3. 配置 OpenClaw Bridge
openclawmp login --token YOUR_TOKEN

# 4. 启动桥接服务
python scripts/bridge.py --mode full
```

## 配置详解

### 主配置 (config.yaml)

```yaml
# oclaw-hermes 核心配置
version: "2.0.0"

# 平台连接
platforms:
  openclaw:
    endpoint: "https://openclawmp.stepfun.com"
    token: "${OPENCLAW_TOKEN}"
    skills_path: "~/.openclaw/skills"
  
  hermes:
    endpoint: "http://localhost:8080"
    memory_path: "~/.hermes/memories"
    config_path: "~/.hermes/config.yaml"
  
  deerflow:
    endpoint: "http://localhost:2026"
    gateway_url: "${DEERFLOW_GATEWAY_URL}"
    langgraph_url: "${DEERFLOW_LANGGRAPH_URL}"

# mflow 记忆流
mflow:
  enabled: true
  sync_interval: 300  # 秒
  layers:
    - name: "instant"
      ttl: 3600        # 1小时
    - name: "short"
      ttl: 604800      # 7天
    - name: "long"
      persistent: true
    - name: "skill"
      persistent: true
    - name: "expert"
      persistent: true

# 智能体集群
agents:
  lead:
    model: "anthropic/claude-3.7-sonnet"
    mode: "ultra"  # flash/standard/pro/ultra
  
  research:
    enabled: true
    max_depth: 5
  
  code:
    enabled: true
    sandbox: "docker"
  
  browser:
    enabled: true
    headless: true
  
  skill:
    enabled: true
    auto_register: true
  
  memory:
    enabled: true
    fts_index: true
  
  expert:
    enabled: true
    sources: 6        # 六路采集
    validation: 3     # 三重验证

# 技能创造者
skill_creator:
  enabled: true
  expert_system: "~/.workbuddy/skills/dlh365-expert-system"
  output_path: "~/.hermes/skills"
  auto_publish: false  # 自动发布到 OpenClaw
```

### 环境变量 (.env)

```bash
# OpenClaw
OPENCLAW_TOKEN=sk_xxxxxxxx

# Hermes
HERMES_MODEL_PROVIDER=openrouter
HERMES_MODEL=anthropic/claude-3.7-sonnet

# DeerFlow
DEERFLOW_URL=http://localhost:2026
DEERFLOW_GATEWAY_URL=http://localhost:2026
DEERFLOW_LANGGRAPH_URL=http://localhost:2026/api/langgraph

# LLM API Keys
OPENROUTER_API_KEY=sk-or-xxx
ANTHROPIC_API_KEY=sk-ant-xxx
OPENAI_API_KEY=sk-xxx

# 可选：其他配置
LOG_LEVEL=INFO
DEBUG=false
```

## 使用方式

### 命令行

```bash
# 启动完整服务
oclaw-hermes start

# 发送消息
oclaw-hermes chat "分析当前建筑行业趋势"

# 深度研究
oclaw-hermes research "中国装配式建筑发展现状"

# 蒸馏专家
oclaw-hermes distill "曹德旺"

# 同步记忆
oclaw-hermes sync --full

# 查看状态
oclaw-hermes status
```

### Python API

```python
from oclaw_hermes import OclawHermes

# 初始化
client = OclawHermes()

# 发送消息（自动路由到最优智能体）
response = client.chat(
    message="帮我写一个 Python 爬虫",
    mode="ultra",  # flash/standard/pro/ultra
    context={
        "skills": ["regex-generator", "excel-formula"],
        "experts": ["elon-musk", "buffett"]
    }
)

# 深度研究
report = client.research(
    topic="新能源汽车电池技术",
    depth=5,
    output_format="markdown"
)

# 蒸馏专家
skill_path = client.distill(
    expert_name="段永平",
    sources=["books", "interviews", "social"],
    output_dir="~/my-skills/"
)

# 记忆同步
client.sync_memories(direction="bidirectional")
```

### 在 OpenClaw 中使用

```bash
# 安装 oclaw-hermes Skill
openclawmp install oclaw-hermes

# 使用
> 启动 hermes 桥接
> 用 deerflow 研究一下量子计算
> 蒸馏一个马斯克视角
> 同步所有记忆
```

## 核心脚本

| 脚本 | 功能 |
|------|------|
| `bridge.py` | 三平台桥接服务 |
| `mflow.py` | 记忆流同步引擎 |
| `distill.py` | 专家蒸馏器 |
| `research.py` | 深度研究链 |
| `verify.py` | 部署验证 |
| `chat.py` | 交互式对话 |

## 架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                         用户交互层                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │  命令行 CLI  │  │  Python API │  │ OpenClaw   │  │  Web UI     │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘ │
└─────────┼────────────────┼────────────────┼────────────────┼────────┘
          │                │                │                │
          └────────────────┴────────────────┴────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      oclaw-hermes 核心层                            │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    智能体路由器                              │   │
│  │         (意图识别 → 智能体选择 → 任务分发)                   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│  ┌─────────────┬─────────────┼─────────────┬─────────────┐         │
│  │  Lead Agent │Research Agent│  Code Agent │Browser Agent│         │
│  └──────┬──────┴──────┬──────┴──────┬──────┴──────┬──────┘         │
│         │             │             │             │                │
│  ┌──────┴──────┐ ┌────┴────┐  ┌────┴────┐  ┌────┴────┐            │
│  │  Skill Agent │ │Memory Agent│ │Expert Agent│                    │
│  └──────┬──────┘ └────┬────┘  └────┬────┘  └────┬────┘            │
│         │             │             │             │                │
│         └─────────────┴─────────────┴─────────────┘                │
│                              │                                      │
│  ┌───────────────────────────┴───────────────────────────┐         │
│  │                    mflow 记忆流                        │         │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐     │         │
│  │  │ 即时记忆 │ │短期记忆 │ │长期记忆 │ │技能记忆 │     │         │
│  │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘     │         │
│  │       └───────────┴───────────┴───────────┘          │         │
│  │                         │                            │         │
│  │                    ┌────┴────┐                       │         │
│  │                    │专家记忆 │                       │         │
│  │                    └─────────┘                       │         │
│  └──────────────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────────────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
          ▼                        ▼                        ▼
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│    OpenClaw     │      │     Hermes      │      │    DeerFlow     │
│   技能生态系统   │      │   自进化记忆    │      │  多智能体协作   │
│                 │      │                 │      │                 │
│ • 58+ Skills    │      │ • 三层记忆      │      │ • LangGraph     │
│ • 工程咨询      │      │ • 技能创建      │      │ • 研究链        │
│ • 大师系列      │      │ • 多平台网关    │      │ • 代码沙箱      │
│ • 专业工具      │      │ • 40+ 工具      │      │ • 浏览器自动化  │
└─────────────────┘      └─────────────────┘      └─────────────────┘
```

## 与原版 Hermes 的差异

| 特性 | Hermes | oclaw-hermes |
|------|--------|--------------|
| **目标平台** | 通用 | OpenClaw 专属优化 |
| **记忆同步** | 单端 | 三端同步 (mflow) |
| **多智能体** | 子 Agent 委托 | DeerFlow 集群 |
| **研究能力** | 基础 | 深度研究链 |
| **技能生态** | 自建 | OpenClaw 58+ Skills |
| **专家蒸馏** | 无 | 集成度量衡专家系统 |
| **部署方式** | 多种 | Docker Compose 一键 |

## 贡献

欢迎提交 Issue 和 PR！

## 许可

MIT License

## 致谢

- [Hermes Agent](https://github.com/NousResearch/hermes) - 自进化 Agent 框架
- [DeerFlow](https://github.com/bytedance/deerflow) - 多智能体协作平台
- [OpenClaw](https://openclawmp.stepfun.com) - Skill 生态系统

---

> **Agent 的边界，就是世界的边界。**
> 
> 让 OpenClaw、Hermes、DeerFlow 的边界，成为你能力的延伸。
