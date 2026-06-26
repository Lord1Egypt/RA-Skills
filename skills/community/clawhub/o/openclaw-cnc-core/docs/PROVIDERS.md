# 多平台适配指南

OpenClaw CNC Core 支持多种LLM服务提供商，你可以根据自己的需求选择。

---

## 支持的服务商

| 提供商 | 标识符 | 需要API Key | 说明 |
|--------|--------|-------------|------|
| DashScope (阿里云) | `dashscope` | ✅ | 国内推荐 |
| OpenAI | `openai` | ✅ | 国际推荐 |
| DeepSeek | `deepseek` | ✅ | 国产，性价比高 |
| 智谱AI | `zhipu` | ✅ | 国产，GLM系列 |
| Moonshot | `moonshot` | ✅ | 国产，Kimi |
| Ollama (本地) | `local` | ❌ | 完全本地，无需联网 |

---

## 使用方法

### 方式1：环境变量

```bash
# DashScope (阿里云)
export DASHSCOPE_API_KEY="your-key"

# OpenAI
export OPENAI_API_KEY="your-key"

# DeepSeek
export DEEPSEEK_API_KEY="your-key"
```

### 方式2：代码配置

```python
from core import HybridRetriever, APIAdapter

# 使用 DashScope
retriever = HybridRetriever(provider="dashscope")

# 使用 OpenAI
retriever = HybridRetriever(provider="openai")

# 使用本地模型（无需API Key）
retriever = HybridRetriever(provider="local")

# 自定义 API Key
adapter = APIAdapter("openai", api_key="your-key")
```

---

## 配置示例

```python
# config.py
CNC_QUOTE_CONFIG = {
    "llm_provider": "dashscope",  # 或 "openai", "deepseek", "local"
    "embedding_provider": "local",  # 使用本地nomic-embed-text
    "api_keys": {
        "dashscope": os.environ.get("DASHSCOPE_API_KEY"),
        "openai": os.environ.get("OPENAI_API_KEY"),
    }
}
```

---

## 本地模型推荐

如果你不想使用云服务，可以使用 Ollama 部署本地模型：

```bash
# 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 拉取模型
ollama pull qwen2.5:0.5b  # 小模型，快
ollama pull nomic-embed-text  # 嵌入模型

# 配置使用本地模型
retriever = HybridRetriever(provider="local")
```

---

## 成本对比

| 提供商 | 1M tokens成本 | 优势 |
|--------|---------------|------|
| 本地Ollama | ¥0 | 免费，隐私 |
| DeepSeek | ¥1 | 便宜 |
| DashScope | ¥2 | 国内稳定 |
| OpenAI | ¥10 | 效果好 |

---

## 切换服务商

```python
# 一键切换
def get_retriever(provider="dashscope"):
    return HybridRetriever(provider=provider)

# 测试不同服务商
for provider in ["dashscope", "openai", "deepseek", "local"]:
    try:
        r = get_retriever(provider)
        print(f"✅ {provider} 可用")
    except Exception as e:
        print(f"❌ {provider} 不可用: {e}")
```