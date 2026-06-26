---
name: nvidia-agent-fleet
slug: nvidia-agent-fleet
version: 1.1.0
description: NVIDIA Agent Fleet — 19个模型Agent + 智能调度引擎 + 并行协作
author: openclaw
tags: [nvidia, multi-agent, dispatcher, llm, orchestration, parallel]
---

# 🚀 NVIDIA Agent Fleet

多 Agent 调度系统。每个 NVIDIA 模型拥有专属 Agent 身份，调度器自动分析任务类型并分配最佳 Agent 执行。

## 架构

```
任务输入 → 调度引擎 → 任务分类 → Agent 匹配 → 执行
                                            ├── DeepSeek V3.2 🧠
                                            ├── Qwen Coder 32B 💻
                                            ├── Kimi K2 🇨🇳
                                            ├── Llama 4 Maverick 🦙
                                            └── ... 19 个 Agent
```

## Agent 阵容 (19个)

| Agent | 模型 | 专长 |
|-------|------|------|
| 🧠 deepseek-v3-2 | DeepSeek V3.2 | 推理、逻辑、数学 |
| 🇨🇳 kimi-k2 | Kimi K2 | 中文、长文本、知识 |
| 🤔 kimi-k2-thinking | Kimi K2 Thinking | 深度思考、推理 |
| 🏆 mistral-large-3 | Mistral Large 3 (675B) | 通用智能、多语言 |
| ⚡ mistral-small | Mistral Small 4 | 快速响应 |
| 💻 qwen-coder-32b | Qwen2.5 Coder 32B | 代码生成、算法 |
| 🦾 qwen3-coder-480b | Qwen3 Coder 480B | 架构设计、审查 |
| 🔧 deepseek-coder | DeepSeek Coder 6.7B | 轻量代码、SQL |
| ⚙️ codestral | Codestral 22B | 代码补全、填空 |
| 🦙 llama-3-3-70b | Llama 3.3 70B | 通用对话 |
| 🦙🆕 llama-4-maverick | Llama 4 Maverick | 创意、分析 |
| 🔬 gemma-3-27b | Gemma 3 27B | 学术、科学 |
| 🏎️ phi-4-mini | Phi-4 Mini | 极速响应 |
| 💨 gemma-3-4b | Gemma 3 4B | 超轻量 |
| 🌏 yi-large | Yi Large | 中文优化 |
| 🏛️ glm-5-1 | GLM 5.1 | 中文问答 |
| 🐉 qwen-3-5-397b | Qwen 3.5 397B | 超大中文 |
| 👁️ llama-vision-90b | Llama Vision 90B | 视觉理解 |
| 📐 nv-embed | NV-EmbedQA | 文本嵌入 |

## 使用

### CLI

```bash
# 自动调度最佳 Agent
fleet "用Python写一个快速排序"

# 分析任务会匹配哪些 Agent
fleet analyze "解释一下量子纠缠"

# 指定 Agent 执行
fleet agent qwen-coder-32b "实现二分查找"

# 多 Agent 协同
fleet multi "如何看待人工智能的未来？"

# 列出所有 Agent
fleet list
```

### ⚡ 并行执行（v1.1.0 新增）

```bash
# 多 Agent 并行协同（同时调不同模型，互不等待）
fleet --multi --parallel "对比茅台和五粮液的财务状况"

# 指定 Agent 并行
fleet --multi --parallel --agent deepseek-v3-2,kimi-k2 "分析这个创业方案"

# 仍支持原有串行模式
fleet --multi "分析市场趋势"
```

**并行 vs 串行 速度对比**
```
串行: 任务A→任务B→任务C→任务D = 4个加起来
并行: 同时发4个请求 = 最慢那个决定总时间
加速比: x2~4 (取决于模型)
```

### 自动超时保护

每个模型有独立超时时间，快的先出结果，慢的到点自动跳过：

| 模型 | 超时 | 说明 |
|------|------|------|
| Llama 4 Maverick | 15s | 写作/报告类，极快 |
| Qwen Coder 32B | 20s | 代码/数据处理 |
| Kimi K2 | 25s | 中文分析 |
| DeepSeek V3.2 | 35s | 深度推理（最慢） |
| 其他 | 30s | 通用 |

### API Key 自动发现

支持多级检索，无需手动设置环境变量：
```
1. $NVIDIA_API_KEY (环境变量)
2. ~/.zshrc (常用 shell 配置)
3. openclaw.json (OpenClaw 配置)
```

### Python SDK

```python
from dispatcher.fleet import dispatch, select_agents, multi_dispatch

# 自动匹配
result = dispatch("实现一个Web服务器")
print(result["content"])

# 多Agent协同（串行）
results = multi_dispatch("哲学问题：意识是什么？")

# 多Agent协同（并行执行）🚀
results = multi_dispatch("分析市场", parallel=True)
for r in results:
    print(f"{r['emoji']} {r['name']}: {r['content'][:100]}...")
```

## v1.1.0 变更

### ✨ 新增
- **并行执行模式** (`--parallel` / `-p`): 多 Agent 同时调用，互不等待
- **逐模型超时保护**: 每个模型有独立超时，慢的不拖累快的
- **API Key 自动发现**: 环境变量 → .zshrc → openclaw.json 三级检索
- **线程安全**: ThreadPoolExecutor + Lock 确保日志不串

### 🔧 优化
- 执行失败时优雅降级，已完成结果不受影响
- 超时模型明确标记，不阻塞整体流程
