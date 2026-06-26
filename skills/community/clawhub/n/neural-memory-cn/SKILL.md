---
name: neural-memory
description: "神经网络启发的记忆系统，支持激活扩散和联想检索。安装后即可使用本地模式，配置 LLM 后可启用智能意图分析。/ Neural network-inspired memory with activation spreading. Works out-of-box in local mode; configure LLM for smart intent analysis."
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python"] },
        "install":
          [
            {
              "id": "python",
              "kind": "python",
              "label": "Python 3.10+ required / 需要 Python 3.10+",
            },
          ],
      },
  }
---

# Neural Memory / 神经记忆系统

**Works out of the box! / 开箱即用！**

No configuration required for basic usage. Install and start using immediately.
基础使用无需配置，安装后即可立即使用。

---

## Quick Start / 快速开始

### 1. Install / 安装

```bash
npx clawhub install neural-memory-cn
```

### 2. Initialize / 初始化

```python
import sys
sys.path.insert(0, "~/.openclaw/skills/neural-memory-cn/scripts")

from thinking import ThinkingModule

# Auto-detects and creates storage / 自动检测并创建存储
memory = ThinkingModule()

# Start using! / 开始使用！
result = memory.think("民航安全")
print(result)
```

### 3. Learn New Knowledge / 学习新知识

```python
memory.learn_and_think(
    content="深度学习是机器学习的一个分支...",
    concept_name="深度学习",
    concept_type="concept",
    tags=["AI", "机器学习"]
)
memory.save()
```

---

## Usage Modes / 使用模式

| Mode | Description | LLM Required |
|------|-------------|--------------|
| `smart` | Intent analysis + activation spreading / 意图分析 + 激活扩散 | Optional |
| `exact` | Direct neuron lookup / 直接神经元查找 | No |
| `associative` | Hybrid mode / 混合模式 | Optional |

```python
# Local mode (no LLM needed) / 本地模式（无需 LLM）
result = memory.think("民航安全怎么样", mode="smart")

# Exact lookup / 精确查找
result = memory.think("中医", mode="exact")
```

---

## Optional: Enable LLM for Better Analysis / 可选：启用 LLM 获得更好分析

**English**: For enhanced intent understanding, configure an LLM provider.

**中文**: 要增强意图理解能力，可配置 LLM 提供商。

### Method 1: Environment Variables / 方式1：环境变量

```bash
export NEURAL_MEMORY_LLM_API_KEY="your-api-key"
export NEURAL_MEMORY_LLM_BASE_URL="https://openrouter.ai/api/v1"
export NEURAL_MEMORY_LLM_MODEL="openai/gpt-3.5-turbo"
```

### Method 2: Setup Script / 方式2：安装脚本

```bash
python ~/.openclaw/skills/neural-memory-cn/scripts/setup.py \
    --api-key "your-key" \
    --base-url "https://openrouter.ai/api/v1" \
    --model "openai/gpt-3.5-turbo"
```

### Method 3: Edit Config / 方式3：编辑配置文件

Edit `~/.openclaw/neural-memory/config.yaml`:

```yaml
thinking:
  intent:
    use_llm: true
    llm_api_key: "your-key"
    llm_base_url: "https://openrouter.ai/api/v1"
    llm_model: "openai/gpt-3.5-turbo"
```

---

## Core Concepts / 核心概念

| Concept | Description (EN) | Description (CN) |
|---------|------------------|------------------|
| Neuron | Knowledge unit (concept, fact, experience) | 知识单元（概念、事实、经验） |
| Synapse | Connection between neurons with weight | 神经元间的连接，带权重 |
| Activation Spreading | Memory retrieval through association | 通过联想进行记忆检索 |
| Intent Layer | Query understanding (optional LLM) | 查询理解（可选 LLM） |

---

## Define Knowledge Domains / 定义知识领域

Edit `domain_hints.json` for accurate spreading:

```json
{
  "民航": ["民航安全", "人为因素", "SMS"],
  "中医": ["中医诊断", "中药"],
  "系统思维": ["AnyLogic", "系统动力学"]
}
```

---

## API Summary / API 摘要

```python
# Query / 查询
result = memory.think("query", mode="smart")

# Learn / 学习
memory.learn_and_think(content, name, type, tags)

# Get stats / 获取统计
stats = memory.get_thinking_stats()

# Save / 保存
memory.save()
```

---

## File Structure / 文件结构

```
~/.openclaw/neural-memory/
├── config.yaml              # Configuration / 配置文件
└── memory_long_term/
    ├── neurons.json         # All neurons / 所有神经元
    ├── synapses/            # Connections / 连接
    └── domain_hints.json    # Domain definitions / 领域定义
```

---

## Documentation / 文档

- **API Reference**: `references/api.md`
- **Architecture**: `references/architecture.md`

---

## Troubleshooting / 故障排除

| Issue | Solution |
|-------|----------|
| Module not found | Check sys.path points to scripts/ |
| Empty results | Add neurons with learn_and_think() |
| LLM not working | Check API key and base URL in config |
| Slow queries | Increase hot_cache_size in config |