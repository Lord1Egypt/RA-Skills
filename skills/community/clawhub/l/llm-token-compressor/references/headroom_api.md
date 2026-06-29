# Headroom API 详细参考

## Python SDK

### compress()

```python
from headroom import compress

# 基本用法
compressed = compress(messages)

# 完整参数
compressed = compress(
    messages,           # list[dict] — OpenAI/Anthropic 格式的消息列表
    model="claude-sonnet-4-20250514",  # str — 目标模型名
    target_ratio=0.4,   # float | None — 压缩保留比例
)
```

**参数说明**：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `messages` | `list[dict]` | 必填 | OpenAI/Anthropic 格式消息列表 |
| `model` | `str` | None | 目标模型名，影响 tokenizer 选择 |
| `target_ratio` | `float` | None | 保留比例（0.2-0.6），None 为自动 |

**返回值**：`list[dict]` — 压缩后的消息列表

### SDK 集成

#### Anthropic SDK

```python
from anthropic import Anthropic
from headroom import withHeadroom

client = withHeadroom(Anthropic())
response = client.messages.create(...)
```

#### OpenAI SDK

```python
from openai import OpenAI
from headroom import withHeadroom

client = withHeadroom(OpenAI())
response = client.chat.completions.create(...)
```

#### LiteLLM

```python
import litellm
from headroom import HeadroomCallback

litellm.callbacks = [HeadroomCallback()]
response = litellm.completion(...)
```

#### LangChain

```python
from headroom import HeadroomChatModel

model = HeadroomChatModel(your_llm)
```

### TypeScript SDK

```typescript
import { compress, withHeadroom } from 'headroom-ai';

// 基本压缩
const compressed = await compress(messages, { model: 'claude-sonnet-4-20250514' });

// 包装 SDK
const client = withHeadroom(new Anthropic());
```

## CLI 完整命令

### 代理模式

```bash
headroom proxy [OPTIONS]

Options:
  --port INT          代理端口（默认 8787）
  --target-ratio FLOAT  压缩保留比例
  --backend STRING    Vertex AI 后端
  --region STRING     Vertex AI 区域
```

### 包装模式

```bash
headroom wrap claude    # 包装 Claude Code
headroom wrap codex     # 包装 Codex
headroom wrap aider     # 包装 Aider
headroom wrap cursor    # 包装 Cursor（打印配置）
headroom wrap copilot   # 包装 Copilot CLI
headroom wrap openclaw  # 安装为 OpenClaw 插件
```

### 性能监控

```bash
headroom perf              # 压缩节省统计
headroom output-savings    # 输出 token 节省
headroom audit-reads       # Read 操作审计
headroom audit-reads --simulate-maturation  # 模拟 Read Maturation 效果
```

### 学习模式

```bash
headroom learn                           # 挖掘失败会话
headroom learn --verbosity               # 预览输出简洁度学习
headroom learn --verbosity --apply       # 应用学习结果
headroom learn --verbosity --llm-judge   # 使用 LLM 评判
```

### MCP

```bash
headroom mcp install    # 安装 MCP 工具
```

### Copilot 认证

```bash
headroom copilot-auth login
headroom wrap copilot --subscription -- --model gpt-4o
```

## 环境变量完整列表

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `HEADROOM_TARGET_RATIO` | None | 压缩保留比例 |
| `HEADROOM_OUTPUT_SHAPER` | 0 | 输出压缩开关 |
| `HEADROOM_READ_MATURATION` | 0 | Read Maturation 开关 |
| `HEADROOM_CCR_BACKEND` | sqlite | 缓存后端 |
| `HEADROOM_OUTPUT_HOLDOUT` | 0 | A/B 对照组比例 |
| `HEADROOM_EMBEDDER_RUNTIME` | default | 嵌入器运行时 |
| `HEADROOM_CONTEXT_TOOL` | None | CLI 上下文工具 |
| `CLAUDE_CODE_USE_VERTEX` | 0 | Vertex AI 模式 |
| `REQUESTS_CA_BUNDLE` | None | 自定义 CA 证书 |
| `SSL_CERT_FILE` | None | SSL 证书文件 |
| `HF_HUB_OFFLINE` | 0 | HuggingFace 离线模式 |
| `HF_ENDPOINT` | None | HuggingFace 镜像 |

## 安装选项

```bash
# 完整安装
pip install "headroom-ai[all]"

# 按需安装
pip install "headroom-ai[proxy]"     # 代理模式
pip install "headroom-ai[mcp]"       # MCP Server
pip install "headroom-ai[ml]"        # Kompress-base 模型
pip install "headroom-ai[code]"      # 代码压缩
pip install "headroom-ai[memory]"    # 内存压缩
pip install "headroom-ai[relevance]" # 相关性压缩
pip install "headroom-ai[image]"     # 图像压缩
pip install "headroom-ai[langchain]" # LangChain 集成
pip install "headroom-ai[evals]"     # 评估工具
pip install "headroom-ai[pytorch-mps]"  # Apple GPU 加速
```

## 压缩算法详解

### CacheAligner
稳定消息前缀，确保 Anthropic/OpenAI 的 KV 缓存命中。压缩不会破坏缓存。

### ContentRouter
自动检测内容类型（JSON、代码、自然语言、混合），路由到对应压缩器。

### SmartCrusher
通用 JSON 压缩器，处理数组、嵌套对象、混合类型。支持 `lossless_min_savings_ratio` 配置。

### CodeCompressor
AST 感知压缩，支持 Python/JS/Go/Rust/Java/C++。保留语法结构，移除冗余。

### Kompress-base
HuggingFace 模型（`chopratejas/kompress-v2-base`），基于 agent 轨迹训练。语义级压缩。

### CCR (Compress-Cache-Retrieve)
可逆压缩，原始内容缓存到 SQLite（`~/.headroom/ccr_store.db`），可通过 `headroom_retrieve` 按需检索。
