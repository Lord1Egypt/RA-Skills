# OpenClaw CNC Core

> CNC加工报价引擎核心模块 | Core engine for CNC machining quotes

[English](#english) | [中文](#中文)

---

## 中文

### 项目简介

OpenClaw CNC Core 是面向CNC加工行业的报价计算引擎，提供材料库管理、工时算法、风险控制等核心能力。

**社区版**（本项目）包含：
- 报价引擎框架
- STEP图纸解析
- 风险控制模块
- 混合检索器

**商业版**包含：
- 1200+ 预训练报价数据
- 行业价格数据库
- 定制开发服务

### 🌐 在线演示

**演示地址**: http://47.253.101.130/

> 🔒 **安全防护已启用**: Nginx限流 (20次/分钟/IP) + 安全头 + 50MB上传限制

**功能体验**：
- 📁 上传 STEP/STL 图纸
- 🎨 选择表面处理工艺
- 🔩 选择材料类型
- 📏 设置公差等级
- 🚀 获取即时报价

### 快速开始

```bash
# 克隆仓库
git clone https://github.com/Timo2026/openclaw-cnc-core.git

# 安装依赖
pip install -r requirements.txt

# 配置API（支持多平台）
export DASHSCOPE_API_KEY="your-key"  # 阿里云
# 或 export OPENAI_API_KEY="your-key"  # OpenAI
# 或使用本地模型，无需API Key

# 运行示例
python examples/quick_start.py
```

### 支持的LLM平台

| 平台 | 标识符 | 需要API Key | 说明 |
|------|--------|-------------|------|
| DashScope | `dashscope` | ✅ | 国内推荐 |
| OpenAI | `openai` | ✅ | 国际推荐 |
| DeepSeek | `deepseek` | ✅ | 国产，性价比高 |
| 智谱AI | `zhipu` | ✅ | 国产，GLM系列 |
| Ollama (本地) | `local` | ❌ | 完全本地，免费 |

详见 [多平台适配指南](docs/PROVIDERS.md)

### 核心模块

| 模块 | 说明 |
|------|------|
| `quote_engine.py` | 报价计算引擎 |
| `risk_control.py` | 报价风险控制 |
| `step_2d_validator.py` | STEP图纸解析 |
| `hybrid_retriever.py` | 混合检索器 |
| `case_retriever.py` | 案例检索 |

### 应用场景

- CNC加工厂快速报价
- 制造企业成本核算
- 报价系统二次开发

### 开源协议

MIT License - 可自由使用、修改、商业化

---

## English

### Overview

OpenClaw CNC Core is a quote calculation engine designed for the CNC machining industry, providing material database management, time algorithms, and risk control capabilities.

**Community Edition** (this project) includes:
- Quote engine framework
- STEP file parsing
- Risk control module
- Hybrid retriever

**Commercial Edition** includes:
- 1200+ pre-trained quote records
- Industry price database
- Custom development services

### Quick Start

```bash
# Clone repository
git clone https://github.com/Timo2026/openclaw-cnc-core.git

# Install dependencies
pip install -r requirements.txt

# Run example
python examples/quick_start.py
```

### Core Modules

| Module | Description |
|--------|-------------|
| `quote_engine.py` | Quote calculation engine |
| `risk_control.py` | Quote risk control |
| `step_2d_validator.py` | STEP file parser |
| `hybrid_retriever.py` | Hybrid retriever |
| `case_retriever.py` | Case retriever |

### Use Cases

- Quick quoting for CNC workshops
- Cost calculation for manufacturers
- Secondary development of quoting systems

### License

MIT License - Free to use, modify, and commercialize

---

## 联系方式 | Contact

- 🌐 官网 | Website: https://openclaw.ai/cnc
- 📧 邮箱 | Email: miscdd@163.com
- 💬 QQ: 849355070
- GitHub: https://github.com/Timo2026/openclaw-cnc-core
- Gitee: https://gitee.com/timo2026/openclaw-cnc-core
- ClawHub: https://clawhub.ai/skills/openclaw-cnc-core

---

**开源日期 | Release Date**: 2026-03-26

**版本 | Version**: v1.0.0