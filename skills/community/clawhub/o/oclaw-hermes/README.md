# oclaw-hermes

**OpenClaw × Hermes × DeerFlow 三位一体智能体桥接方案**

> Agent 的边界，就是世界的边界。

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/ruiyongwang/oclaw-hermes)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-OpenClaw-orange.svg)](https://openclawmp.stepfun.com)

## 一句话简介

**oclaw-hermes** 是专为 OpenClaw 平台打造的智能体桥接方案，将 Hermes 的自进化记忆、DeerFlow 的多智能体协作与 OpenClaw 的 58+ Skills 深度融合，实现三位一体、无缝协作的 AI 智能体集群。

## 核心能力

| 能力 | 说明 |
|------|------|
| **mflow 记忆流** | 独创五层记忆架构，实现 OpenClaw/Hermes/DeerFlow 三端记忆无缝同步 |
| **智能体集群** | 7 大智能体协同：Lead/Research/Code/Browser/Skill/Memory/Expert |
| **深度研究链** | 一键深度研究：问题分解 → 多源搜索 → 信息验证 → 综合分析 → 报告生成 |
| **专家蒸馏器** | 集成度量衡专家系统，六路并行采集 + 三重验证提炼 |
| **58+ Skills** | 完整接入 OpenClaw 工程咨询、大师系列等专业 Skills |

## 快速开始

### 1. 安装

```bash
# 通过 OpenClaw 安装
openclawmp install oclaw-hermes

# 或手动安装
git clone https://github.com/ruiyongwang/oclaw-hermes.git
cd oclaw-hermes
pip install -e .
```

### 2. 配置

```bash
cp .env.example .env
# 编辑 .env 填入 API Keys
```

### 3. 启动

```bash
# Docker 一键启动（推荐）
docker-compose up -d

# 或手动启动
oclaw-hermes start
```

### 4. 验证

```bash
oclaw-hermes status
```

## 使用示例

### 命令行

```bash
# 交互式对话
oclaw-hermes chat

# 深度研究
oclaw-hermes research "中国装配式建筑发展现状"

# 蒸馏专家
oclaw-hermes distill "曹德旺"

# 同步记忆
oclaw-hermes sync
```

### Python API

```python
from oclaw_hermes import OclawHermes

client = OclawHermes()

# 智能对话
response = client.chat("帮我写一个 Python 爬虫")

# 深度研究
report = client.research("新能源汽车电池技术")

# 蒸馏专家
skill_path = client.distill("段永平")
```

### 在 OpenClaw 中使用

```bash
> 启动 hermes 桥接
> 用 deerflow 研究一下量子计算
> 蒸馏一个马斯克视角
> 同步所有记忆
```

## 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                      oclaw-hermes                           │
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

## 文档

- [SKILL.md](SKILL.md) - 完整技能定义与配置详解
- [docs/INSTALL.md](docs/INSTALL.md) - 详细安装指南
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - 架构设计文档
- [docs/API.md](docs/API.md) - API 参考手册

## 系统要求

- Docker & Docker Compose
- Python 3.10+
- Node.js 18+
- 4GB+ RAM
- 10GB+ 磁盘空间

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
