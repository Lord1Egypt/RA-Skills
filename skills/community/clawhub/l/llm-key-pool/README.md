# LLM Key Pool

分层轮询多平台 LLM API Key 管理工具，支持故障转移与自动切换。

## 兼容运行平台

本工具/skill 可安装运行于以下AI编程客户端：

| 平台 | 安装方式 | 支持 |
|------|---------|------|
| **Claude Code** | Skill 直接安装 | ✅ 原生支持 |
| **OpenClaw** | 作为Python依赖库集成 | ✅ 原生支持 |
| **OpenCode** | 作为Python依赖库集成 | ✅ 原生支持 |
| **通义千问 (Qwen)** | 命令行调用 / Python集成 | ✅ 支持 |
| **Any editor/IDE** | Python脚本调用 | ✅ 支持 |
| **独立使用** | 命令行直接调用 | ✅ 支持 |

## 功能

- **三层 Key 池**：主力层 (primary) → 每日回血层 (daily) → 兜底层 (fallback)
- **智能故障转移**：429 自动冷却、401 永久禁用、500/503 重试
- **OpenAI 兼容接口**：统一 `/chat/completions` 格式，同时支持 Anthropic Messages API
- **多平台支持**：主流大模型厂商全兼容（见下方完整列表）
- **线程安全**：内置锁机制，支持并发调用

## 支持的AI模型平台

所有支持OpenAI兼容接口的大模型平台均可接入，当前已验证支持：

### 主力层 (primary) - 高额度推荐
- **阿里云百炼** - qwen-max, qwen-plus, qwen-turbo
- **智谱AI** - glm-4, glm-3-turbo, glm-4-air
- **小龙虾** - xiaolongxia-72b, xiaolongxia-34b

### 每日回血层 (daily) - 额度每日刷新
- **火山引擎** - doubao-pro-256k, doubao-pro-32k
- **Google AI Studio** - gemini-1.5-pro, gemini-1.5-flash

### 兜底层 (fallback) - 开源/聚合平台保证可用性
- **硅基流动** - Qwen2.5, Llama 3.1, GLM-4 等开源模型
- **OpenRouter** - 聚合上百种大模型，免费模型可用
- **GitHub Models** - GitHub官方模型服务
- **Groq** - 极速推理，免费额度
- **OpenCode** - 专注代码生成
- **Qwen独立API** - 通义千问独立API服务
- **ClaudeCode (Anthropic)** - claude-3-5-sonnet, claude-3-opus
- **腾讯混元** - hunyuan-lite, hunyuan-standard

> 详细配置说明见：[references/supported_providers.md](references/supported_providers.md)

## 安装

### 方式一：作为 Claude Code Skill 安装（推荐）

Claude Code 用户可以安装为 Skill：

```bash
# 创建 skills 目录（如果不存在）
mkdir -p ~/.claude/skills

# 克隆或复制项目到 skills 目录
git clone https://github.com/OpenClaw/llm-key-pool.git ~/.claude/skills/llm-key-pool

# 安装依赖
pip install -r ~/.claude/skills/llm-key-pool/requirements.txt
```

Windows 路径：
```
C:\Users\用户名\.claude\skills\llm-key-pool\
```

安装后，Claude Code 需要调用大模型时会自动触发该 Skill。

### 方式二：作为独立 Python 包安装

```bash
pip install .
```

或可编辑模式（开发）：

```bash
pip install -e .
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
# 或者如果已经 pip 安装了包，可以跳过这一步
```

### 2. 创建配置文件（填入你的 API Key）

项目中已经提供了配置模板，只需要复制并填写你的 API Key：

```bash
# 复制模板文件到当前目录
cp assets/llm_config.yaml.example ./llm_config.yaml

# 编辑文件，替换占位符为你的真实 API Key
notepad llm_config.yaml  # Windows
# 或者
vim llm_config.yaml     # Linux/macOS
```

**模板位置**: `assets/llm_config.yaml.example` 已经预填了各大平台的配置，你只需要：
- 去掉不需要平台的注释（或保留，删掉占位符 `sk-...` 换成你的 Key）
- 将 `"sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"` 替换成你真实的 API Key
- `.gitignore` 已经默认忽略 `llm_config.yaml`，不用担心密钥泄露

### 3. 调用 LLM

```bash
python -m llm_key_pool.llm_client \
  --config ./llm_config.yaml \
  --prompt "你好，请介绍一下自己"
```

### 4. 在 Python 代码中使用

```python
from llm_key_pool import TieredLLMClient

client = TieredLLMClient('./llm_config.yaml')
result, usage_info = client.call_llm(prompt="你好")
print(result)
```

## 分层架构

| 层级 | 说明 | 推荐平台 |
|------|------|---------|
| `primary` | 主力层，高额度 | 阿里云百炼、智谱 AI |
| `daily` | 每日回血层，额度每日刷新 | 火山引擎、Google AI Studio |
| `fallback` | 兜底层，开源/聚合平台 | 硅基流动、OpenRouter、Groq |

系统自动从主力层开始轮询，不可用时自动切换到下一层，无需手动干预。

## 命令行参数

| 参数 | 说明 |
|------|------|
| `--config` | 配置文件路径（默认：`./llm_config.yaml`） |
| `--prompt` | 用户提示词 |
| `--system-prompt` | 系统提示词（可选） |
| `--temperature` | 温度参数（默认：0.7） |
| `--max-tokens` | 最大 Token 数（默认：2000） |
| `--test` | 测试配置 |
| `--status` | 查看 Key 池状态 |

## 配置示例

```yaml
providers:
  alibaba_bailian:
    tier: primary
    model: "qwen-max"
    api_keys:
      - "sk-your-api-key"
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"

  siliconflow:
    tier: fallback
    model: "Qwen/Qwen2.5-7B-Instruct"
    api_keys:
      - "sk-your-api-key"
    base_url: "https://api.siliconflow.cn/v1"

global:
  max_retries: 3
  cooldown_seconds: 300
  error_threshold: 5
```

## 项目结构

```
llm-key-pool/
├── llm_key_pool/            # 核心包
│   ├── __init__.py
│   ├── config_loader.py     # 配置加载与验证
│   ├── key_pool.py          # Key 池管理与轮询
│   └── llm_client.py        # LLM 调用客户端
├── assets/                  # 模板与示例
├── references/              # 参考文档
├── pyproject.toml
├── requirements.txt
├── LICENSE
└── README.md
```

## 许可证

Apache License 2.0
