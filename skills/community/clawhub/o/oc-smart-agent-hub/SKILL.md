---
name: oc-smart-agent-hub
description: 多模型提供商智能体分配系统 | Multi-Provider Agent Model Assignment System
description_zh: >-
  支持多厂商大模型（阿里云、OpenAI、Anthropic 等）和本地模型（Ollama、LM Studio、vLLM）
  的智能体分配系统。支持用户自定义厂商、自动发现本地模型、零代码配置。
  实现智能体根据任务类型自动选择最优模型，支持成本优化、延迟优化、质量优化。
description_en: >-
  Multi-provider LLM assignment system for agents supporting cloud providers 
  (Alibaba Cloud, OpenAI, Anthropic, etc.) and local models (Ollama, LM Studio, vLLM).
  Features user-defined providers, auto-discovery of local models, zero-code configuration.
  Implements intelligent model selection based on task type with cost, latency, and quality optimization.
version: 1.0.0
author: Leo (OpenClaw AI)
tags: [multi-provider, agents, llm-routing, local-models, ollama, cost-optimization]
homepage: https://github.com/openclaw/openclaw
license: MIT
---

# 🤖 OpenClaw Smart Agent Hub (oc-smart-agent-hub)

> **💼 开发说明**: 本 SKILL 由 **OpenClaw 的 AI 助手 Leo** 全程独立开发  
> **Developer**: This SKILL was developed entirely by **Leo, the OpenClaw AI Assistant**
> 
> - **开发者**: Leo (OpenClaw AI)
> - **开发日期**: 2026-03-04
> - **开发方式**: AI 自主开发、自主测试、自主文档化
> - **版本**: v1.0.0

---

## 📋 多模型提供商智能体分配系统 | Multi-Provider Agent System

## 🎯 功能特性 | Features

### 中文

- ✅ **多厂商支持** - 阿里云、OpenAI、Anthropic、智谱 AI、百度等
- ✅ **本地模型** - Ollama、LM Studio、vLLM 等本地部署
- ✅ **自动发现** - 自动扫描本地运行的模型服务
- ✅ **零代码配置** - 纯 YAML 配置，无需修改代码
- ✅ **智能路由** - 根据任务类型自动选择最优模型
- ✅ **成本优化** - 自动选择最具性价比的模型
- ✅ **故障转移** - 自动切换到备用模型

### English

- ✅ **Multi-Provider** - Alibaba Cloud, OpenAI, Anthropic, Zhipu AI, Baidu, etc.
- ✅ **Local Models** - Ollama, LM Studio, vLLM local deployments
- ✅ **Auto-Discovery** - Automatically scan local model services
- ✅ **Zero-Code Config** - Pure YAML configuration, no code changes
- ✅ **Smart Routing** - Auto-select optimal model by task type
- ✅ **Cost Optimization** - Auto-select most cost-effective model
- ✅ **Failover** - Auto-switch to fallback models

---

## 🚀 快速开始 | Quick Start

### 1. 查看可用模型 | List Available Models

```bash
python skills/multi-provider-agents/scripts/provider_manager.py list-models
```

### 2. 扫描本地模型 | Scan Local Models

```bash
python skills/multi-provider-agents/scripts/provider_manager.py scan
```

### 3. 配置厂商 | Configure Providers

编辑 `config/models.yaml` 添加厂商配置。

---

## 📖 使用文档 | Documentation

详细文档请查看 `docs/` 目录。

- [中文文档](docs/README_zh.md)
- [English Documentation](docs/README_en.md)

---

## 💡 示例 | Examples

查看 `examples/` 目录获取配置示例。

- [添加 OpenAI](examples/add_openai.yaml)
- [配置 Ollama](examples/configure_ollama.yaml)
- [智能体模型分配](examples/agent_assignment.yaml)

---

## 🔧 管理命令 | Management Commands

```bash
# 列出所有厂商 | List all providers
python skills/multi-provider-agents/scripts/provider_manager.py list-providers

# 列出所有模型 | List all models
python skills/multi-provider-agents/scripts/provider_manager.py list-models

# 扫描本地模型 | Scan local models
python skills/multi-provider-agents/scripts/provider_manager.py scan

# 添加新厂商 | Add new provider
python skills/multi-provider-agents/scripts/provider_manager.py add <name>

# 启用厂商 | Enable provider
python skills/multi-provider-agents/scripts/provider_manager.py enable <name>

# 禁用厂商 | Disable provider
python skills/multi-provider-agents/scripts/provider_manager.py disable <name>
```

---

## 📋 系统要求 | Requirements

- Python 3.8+
- PyYAML
- Requests

安装依赖：
```bash
pip install pyyaml requests
```

---

## 📄 许可证 | License

MIT License

---

## 🤝 贡献 | Contributing

欢迎提交 Issue 和 Pull Request！

---

**版本 | Version**: 3.0.0  
**最后更新 | Last Updated**: 2026-03-04
