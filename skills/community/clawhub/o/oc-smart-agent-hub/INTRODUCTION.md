# oc-smart-agent-hub 介绍

---

## 🇨🇳 中文介绍

**oc-smart-agent-hub** - 智能体多模型路由系统，由使用者 MSonline 提出需求，OpenClaw AI 助手 Leo 独立开发。

本 SKILL 以充分使用阿里云百炼 Coding Plane 提供的 8 种功能性大模型为核心目标，为分工不同的子智能体匹配最适合的大模型，从而提高运行效率和内容完成质量。

支持阿里云、OpenAI、Anthropic 等 5+ 厂商及 Ollama 本地模型，提供智能体专属模型分配、任务类型自动路由、成本优化等功能。纯 YAML 配置，零代码，企业级安全规范。

### 核心功能

- **🌐 多厂商支持** - 支持阿里云百炼 8 种功能性大模型 + OpenAI、Anthropic 等外部厂商
- **🎯 智能体匹配** - 为项目协调、前端开发、智能合约、数据库、测试、运营、安全、数值、美术等子智能体分配专属模型
- **⚡ 效率优化** - 根据任务类型自动选择最优模型，提高运行效率
- **✨ 质量提升** - 为不同子智能体匹配最适合的模型，提高内容完成质量
- **🏠 本地模型** - 支持 Ollama、LM Studio、vLLM 等本地部署，自动发现、完全免费
- **⚙️ 零代码配置** - 纯 YAML 配置，即改即用，无需修改代码
- **🔒 安全规范** - 企业级敏感信息保护，打包前自动检查

### 百炼 Coding Plane 8 种功能性大模型

| 模型 | 适用智能体 | 用途 |
|------|----------|------|
| qwen3.5-plus | 项目协调、数据库设计 | 均衡全能，日常任务 |
| qwen3-max | 测试审计、安全审计 | 最强推理，关键任务 |
| qwen3-coder-plus | 前端开发、智能合约 | 代码专家，编程任务 |
| qwen3-coder-next | 前端开发（快速） | 低延迟，快速响应 |
| glm-5 | 项目协调 | Agent 编排，任务调度 |
| kimi-k2.5 | 运营方案、美术设计 | 长文本，创意理解 |
| MiniMax-M2.5 | 运营方案 | Agent 原生，多语言 |
| glm-4.7 | 备用模型 | 备用，基础任务 |

### 适用场景

- 需要为不同子智能体分配不同的大模型
- 希望根据任务类型自动选择最优模型
- 关注运行效率和内容完成质量
- 想要部署本地模型降低成本
- 需要同时使用多个大模型厂商

### 快速开始

```bash
# 安装 SKILL
clawhub install oc-smart-agent-hub

# 配置模型
编辑 config/models.yaml

# 启动智能体
python scripts/provider_manager.py list-models
```

---

## 🇺🇸 English Description

**oc-smart-agent-hub** - Intelligent multi-model routing system for agents, developed by Leo (OpenClaw AI Assistant) based on requirements from user MSonline.

This SKILL is designed to fully utilize the 8 functional LLMs provided by Alibaba Cloud Bailian Coding Plane, matching the most suitable model for each sub-agent with different responsibilities, thereby improving operational efficiency and content completion quality.

Supports 5+ providers including Alibaba Cloud, OpenAI, Anthropic, and Ollama local models. Features agent-specific model assignment, task-based auto-routing, and cost optimization. Pure YAML configuration, zero-code, enterprise-grade security.

### Key Features

- **🌐 Multi-Provider** - Support 8 Bailian Coding Plane LLMs + external providers (OpenAI, Anthropic)
- **🎯 Agent Matching** - Assign dedicated models to sub-agents: coordinator, frontend, contract, database, testing, operations, security, planning, art
- **⚡ Efficiency** - Auto-select optimal model by task type to improve operational efficiency
- **✨ Quality** - Match most suitable model for each sub-agent to improve content quality
- **🏠 Local Models** - Support Ollama, LM Studio, vLLM with auto-discovery, completely free
- **⚙️ Zero-Code Config** - Pure YAML configuration, instant use, no code changes required
- **🔒 Security** - Enterprise-grade sensitive information protection with automated pre-publish checks

### Bailian Coding Plane 8 Functional LLMs

| Model | Suitable Agents | Purpose |
|-------|----------------|---------|
| qwen3.5-plus | Coordinator, Database | All-rounder, daily tasks |
| qwen3-max | Testing, Security | Strongest reasoning, critical tasks |
| qwen3-coder-plus | Frontend, Contract | Code expert, programming |
| qwen3-coder-next | Frontend (fast) | Low latency, quick response |
| glm-5 | Coordinator | Agent orchestration, task scheduling |
| kimi-k2.5 | Operations, Art | Long text, creative understanding |
| MiniMax-M2.5 | Operations | Agent native, multi-language |
| glm-4.7 | Fallback | Backup, basic tasks |

### Use Cases

- Need to assign different models to different sub-agents
- Want automatic model selection based on task type
- Concerned about operational efficiency and content quality
- Want to deploy local models to reduce costs
- Need to use multiple LLM providers simultaneously

### Quick Start

```bash
# Install SKILL
clawhub install oc-smart-agent-hub

# Configure models
Edit config/models.yaml

# Start agents
python scripts/provider_manager.py list-models
```

---

## 📊 技术规格 | Specifications

| 项目 | 详情 |
|------|------|
| **版本** | v1.0.0 |
| **开发者** | Leo (OpenClaw AI) |
| **开发日期** | 2026-03-04 |
| **文件大小** | ~50KB |
| **文件数** | 10 |
| **文档语言** | 中文 + English |
| **许可证** | MIT |

---

**最后更新**: 2026-03-04  
**状态**: ✅ 可发布到 ClawHub
