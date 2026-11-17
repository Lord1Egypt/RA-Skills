---
name: opensource-llm-models
description: "开源大模型综合技能 - 覆盖国内外主流开源LLM的选型、部署、调优、API调用。国产: DeepSeek/Qwen/ChatGLM/Yi/MiniMax/Baichuan/Kimi。国际: Llama/Mistral/Gemma/Phi/Falcon/Granite/DBRX"
metadata:
  version: 1.0.0
  date: "2026-07-29"
  author: "曙光"
  tags:
    - opensource
    - llm
    - deepseek
    - qwen
    - chatglm
    - yi
    - llama
    - mistral
    - gemma
    - phi
    - model-selection
    - model-deployment
    - model-comparison
---

# 开源大模型综合技能

## 一、模型全景

### 国内开源 (China)

| 模型 | 公司 | 架构 | 参数量 | 上下文 | 核心优势 | 许可证 |
|------|------|------|--------|--------|----------|--------|
| **DeepSeek V3/R1** | 深度求索 | MoE (671B, 37B激活) | 671B | 128K | 推理天花板, 数学/代码极强, 成本极低 | MIT |
| **Qwen3** | 阿里巴巴 | Dense | 0.5B-236B | 128K-1M | 多模态全覆盖, 中文最优, 工具调用强 | Apache 2.0 |
| **ChatGLM-4** | 智谱AI | Dense | 9B-130B | 128K | 中文理解深, 工具调用原生, 企业级 | Apache 2.0 |
| **Yi-1.5/34B** | 零一万物 | Dense | 6B-34B | 200K | 长上下文, 推理精准, 数学好 | Apache 2.0 |
| **MiniMax-Text-01** | MiniMax | MoE (456B, 45.9B激活) | 456B | 1M | 超长上下文, 线性注意力, 成本低 | MIT |
| **Baichuan-4** | 百川智能 | Dense | 7B-13B | 128K | 医疗/法律垂直领域, 安全过滤 | Apache 2.0 |
| **Kimi (K2/K3)** | 月之暗面 | MoE (1T+, 稀疏激活) | 1T+ | 128K | Agent/子Agent架构, 长上下文, 多模态 | MIT |

### 国际开源 (Global)

| 模型 | 公司 | 架构 | 参数量 | 上下文 | 核心优势 | 许可证 |
|------|------|------|--------|--------|----------|--------|
| **Llama 4** | Meta | MoE (17B-2T) | 17B-2T | 128K-1M | 生态最完善, 社区最强, 微调资源最多 | Llama 4 Community |
| **Mistral/Mixtral** | Mistral AI | MoE (8x7B-8x22B) | 7B-141B | 32K-128K | 效率极高, 代码强, 部署友好 | Apache 2.0 |
| **Gemma 3/4** | Google | Dense | 2B-27B | 8K-128K | 轻量级, 单GPU可跑, 安全对齐好 | Gemma |
| **Phi-3/4** | Microsoft | Dense | 3.8B-14B | 128K | 小模型推理天花板, 端侧部署 | MIT |
| **Falcon 2** | TII | Dense | 11B-180B | 8K-128K | 多语言, 阿拉伯语, 企业级 | Apache 2.0 |
| **Granite 3** | IBM | Dense | 3B-34B | 128K | 企业级代码, RAG, 安全合规 | Apache 2.0 |
| **DBRX** | Databricks | MoE (132B, 36B激活) | 132B | 32K | MoE架构, 推理快, 代码好 | Databricks |

## 二、选型指南

### 按场景推荐

| 场景 | 推荐模型 | 理由 |
|------|----------|------|
| **推理/数学/逻辑** | DeepSeek R1 > Llama 4 > Qwen3 | DeepSeek推理专用, 数学SOTA |
| **中文对话/创作** | Qwen3 > ChatGLM-4 > DeepSeek V3 | Qwen中文最优, ChatGLM理解深 |
| **代码生成** | DeepSeek V3 > Qwen3-Coder > Mistral-Codestral | DeepSeek代码评测第一 |
| **多模态(图/视频)** | Qwen3-VL > Llama 4 > Gemma 3 | Qwen多模态覆盖面最广 |
| **长文档分析** | MiniMax-Text-01 > Yi-1.5 > Kimi | MiniMax 1M上下文, 线性注意力 |
| **Agent/工具调用** | Kimi K3 > Qwen3 > ChatGLM-4 | Kimi原生子Agent架构 |
| **端侧部署** | Phi-4 > Gemma 3 > Qwen3-0.5B | 小模型推理天花板的Phi |
| **企业级安全** | Granite 3 > Falcon 2 > ChatGLM-4 | IBM安全合规, 智谱企业级 |
| **成本敏感** | DeepSeek V3 > MiniMax > Mixtral | DeepSeek推理成本极低 |

### 按部署方式

```
本地部署 (单GPU):
  Phi-4 (14B) → Gemma 3 (12B) → Qwen3 (7B) → Mistral (7B)

本地部署 (多GPU/显存):
  DeepSeek R1 (671B quant) → Llama 4 (70B) → Mixtral (8x22B) → Qwen3 (72B)

API调用:
  DeepSeek (最便宜) → Qwen (阿里云) → ChatGLM (智谱) → Yi (零一)
```

## 三、API 调用模板

### DeepSeek

```python
import openai
client = openai.OpenAI(
    api_key="sk-xxx",
    base_url="https://api.deepseek.com/v1",
)
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "你好"}],
    temperature=0.7,
)
```

### Qwen (阿里云)

```python
from openai import OpenAI
client = OpenAI(
    api_key="sk-xxx",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
response = client.chat.completions.create(
    model="qwen3-72b-instruct",
    messages=[{"role": "user", "content": "你好"}],
)
```

### ChatGLM (智谱)

```python
from zhipuai import ZhipuAI
client = ZhipuAI(api_key="xxx")
response = client.chat.completions.create(
    model="glm-4-plus",
    messages=[{"role": "user", "content": "你好"}],
)
```

### 统一路由 (多模型切换)

```python
# 使用 openclaw-aisa-llm-router 或 asia-llm-router-skills
# 一个API Key 切换70+模型
ROUTER_BASE = "https://api.aisa.com/v1"

client = OpenAI(
    api_key="sk-xxx",
    base_url=ROUTER_BASE,
)

# 根据任务切换模型
def pick_model(task_type: str) -> str:
    models = {
        "reasoning": "deepseek-r1",
        "chat": "qwen3-72b-instruct",
        "code": "deepseek-chat",
        "vision": "qwen3-vl",
        "agent": "kimi-k3",
        "cheap": "deepseek-chat",
    }
    return models.get(task_type, "qwen3-72b-instruct")
```

## 四、本地部署

### Ollama (推荐)

```bash
# 安装
ollama pull deepseek-r1
ollama pull qwen3:72b
ollama pull llama4
ollama pull mistral
ollama pull phi-4
ollama pull gemma3

# 运行
ollama run deepseek-r1
```

### LM Studio (Windows)

```bash
# 下载GGUF模型
# 支持: DeepSeek R1, Qwen3, Llama 4, Mistral, Phi-4, Gemma 3
# 本地API: http://localhost:1234/v1
```

### llama.cpp

```bash
# 编译
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && cmake -B build && cmake --build build --config Release

# 运行
./build/bin/llama-cli -m model.gguf -p "你好" -n 512
```

## 五、模型路由策略

### 成本优先

```python
# 简单任务 → 便宜模型
# 复杂任务 → 强模型
# 推理任务 → DeepSeek R1
# 多模态任务 → Qwen3-VL
```

### 质量优先

```python
# 中文 → Qwen3-72B
# 英文 → Llama 4-70B
# 代码 → DeepSeek V3
# 推理 → DeepSeek R1
# Agent → Kimi K3
```

### 速度优先

```python
# DeepSeek V3 (Flash) → 极快
# Qwen3-7B → 本地快
# Phi-4 → 端侧快
# Mistral 7B → 轻量快
```

## 六、最佳实践

### 1. 模型选择四步法
1. 确定任务类型（推理/代码/创作/分析/Agent）
2. 确定部署约束（API/本地/端侧）
3. 确定成本预算（免费/低成本/高成本）
4. 匹配最优模型

### 2. 降本策略
- 简单任务用便宜模型（DeepSeek Chat）
- 批量任务用路由缓存
- 本地部署长尾任务
- 使用量化模型（GGUF q4/q8）

### 3. 质量提升
- 推理用 DeepSeek R1（思维链）
- 中文用 Qwen3（中文理解最好）
- 代码用 DeepSeek Coder（代码评测第一）
- Agent用 Kimi K3（原生子Agent架构）

### 4. 模型切换时机
- 普通问答 → DeepSeek Chat / Qwen3
- 复杂推理 → DeepSeek R1
- 代码生成 → DeepSeek Coder / Mistral Codestral
- 多模态 → Qwen3-VL / Llama 4
- 长文档 → MiniMax / Yi
- Agent任务 → Kimi K3 / Qwen3

## 七、参考资源

### 国内模型
- DeepSeek: https://platform.deepseek.com
- Qwen: https://help.aliyun.com/zh/model-studio
- ChatGLM: https://open.bigmodel.cn
- Yi: https://platform.lingyiwanwu.com
- MiniMax: https://platform.minimaxi.com
- Baichuan: https://platform.baichuan-ai.com
- Kimi: https://platform.moonshot.cn

### 国际模型
- Llama: https://llama.meta.com
- Mistral: https://console.mistral.ai
- Gemma: https://ai.google.dev/gemma
- Phi: https://azure.microsoft.com/en-us/products/phi
- Falcon: https://huggingface.co/tiiuae
- Granite: https://huggingface.co/ibm-granite
- DBRX: https://www.databricks.com/blog/introducing-dbrx

### 部署资源
- Ollama: https://ollama.com
- LM Studio: https://lmstudio.ai
- llama.cpp: https://github.com/ggerganov/llama.cpp
- Hugging Face: https://huggingface.co/models
- OpenRouter: https://openrouter.ai
