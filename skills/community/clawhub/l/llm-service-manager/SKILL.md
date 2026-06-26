# LLM Service Manager

Manage local LLM services (Ollama/vLLM/OpenAI-compatible API endpoints) through a unified command interface.

## Usage

```python
from llm_service_manager import run

# Check all service statuses
print(run("status"))

# Start Ollama
print(run("start"))

# Pull a model
print(run("pull gemma3:2b"))

# Query via Ollama
print(run("ollama:什么是ReAct模式?"))

# Query via API
print(run("api:用Python写一个快速排序"))
```

## Commands

| Command | Description |
|---------|-------------|
| `status` | Check all LLM services (Ollama/vLLM/API) |
| `start` | Start Ollama service (Windows) |
| `pull <model>` | Download a model via Ollama |
| `ollama:<query>` | Query Ollama with a model |
| `api:<query>` | Query OpenAI-compatible API |
| (any text) | Auto-detect and query available service |

## Trigger
- User says "LLM", "模型服务", "Ollama", "本地模型"
- Needs to check/start/manage local LLM services

Base directory: file:///C:/Users/pc/.config/opencode/skills/llm_service_manager


## B站学习
> 学习时间: 2026-06-01 20:57

- **小小的人来自火星**: 学习review manager操作啦！
  - 关键词: 学习review, manager操作啦
- **老吴聊技术**: 怎么用Antigravity-Manager实现Token自由？
  - 关键词: 怎么用Antigravity, Manager实现Token自由

## B站学习
> 学习时间: 2026-06-01 21:02

- **小小的人来自火星**: 学习review manager操作啦！
- **老吴聊技术**: 怎么用Antigravity-Manager实现Token自由？
- **盐之微积分**: Obsidian数学使用方法-用callout manager打造清爽笔记

## B站学习 (第1轮)
> 学习时间: 2026-06-02 09:21

- **小小的人来自火星**: 学习review manager操作啦！
  https://www.bilibili.com/video/BV1Rb4y1v78j
- **krrrris**: 基于STAR CCM+的参数优化分析（design manager）
  https://www.bilibili.com/video/BV1L5411w78A
- **老吴聊技术**: 怎么用Antigravity-Manager实现Token自由？
  https://www.bilibili.com/video/BV1RY9xBPESu

## B站学习 (第2轮)
> 学习时间: 2026-06-02 09:34

- **小小的人来自火星**: 学习review manager操作啦！
  https://www.bilibili.com/video/BV1Rb4y1v78j
- **krrrris**: 基于STAR CCM+的参数优化分析（design manager）
  https://www.bilibili.com/video/BV1L5411w78A
- **老吴聊技术**: 怎么用Antigravity-Manager实现Token自由？
  https://www.bilibili.com/video/BV1RY9xBPESu
