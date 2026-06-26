# llmfit-advisor - OpenClaw Agent 技能

> 基于 LLMfit 的本地 LLM 模型推荐技能
> **版本**: 0.9.8
> **类型**: Experience/Skill

## 🎯 功能概述

这个技能让 OpenClaw Agent 能够：
- **智能推荐** - 根据系统硬件配置推荐最适合的 LLM 模型
- **场景优化** - 支持通用、编码、推理、聊天等多种使用场景
- **量化建议** - 推荐最佳量化方案（Q8_0, Q2_K, FP8 等）
- **硬件感知** - 自动检测 CPU、RAM、GPU 配置
- **多运行时** - 支持 Ollama、llama.cpp、MLX、Docker Model Runner、LM Studio

## 🚀 快速开始

### 使用 llmfit 推荐模型

Agent 可以调用 llmfit 命令获取模型推荐：

```
llmfit recommend --json --use-case coding --limit 5
llmfit recommend --json --use-case chat --limit 5
llmfit recommend --json --use-case general --limit 5
```

### 获取最佳匹配

```
llmfit fit --perfect -n 5              # 完美匹配的 5 个模型
llmfit fit --good -n 10                # 良好匹配的 10 个模型
```

### 系统信息

```
llmfit --json system                   # 系统硬件信息
```

## 💡 使用场景

### 场景 1: 用户询问适合的设备
**用户**: "我有什么设备可以运行什么模型？"
**Agent 回答**: 
```
让我检查一下你的系统配置...
llmfit recommend --json --limit 3
```

### 场景 2: 编码助手推荐
**用户**: "我想找一个适合写代码的大模型"
**Agent 回答**:
```
让我为你推荐一个适合编码场景的模型...
llmfit recommend --json --use-case coding --limit 5
```

### 场景 3: 根据硬件配置优化
**用户**: "我只有 16GB 内存，有什么推荐吗？"
**Agent 回答**:
```
根据你的硬件配置，我推荐以下模型...
llmfit --ram=16G recommend --json --limit 5
```

## 🔧 命令参数详解

### `llmfit recommend --json`

**基本用法:**
```powershell
llmfit recommend --json [选项]
```

**选项:**
- `--use-case <type>` - 使用场景：`general` | `coding` | `reasoning` | `chat` | `multimodal` | `embedding`
- `--limit <n>` - 返回数量（默认 5）
- `--force-runtime <type>` - 强制运行时：`llamacpp` | `mlx` | `vllm`
- `--context <n>` - 上下文长度：`2048` | `4096` | `8192` | `16384` | `32768` | `65536` | `131072`
- `--json` - JSON 格式输出

### `llmfit fit`

**基本用法:**
```powershell
llmfit fit --perfect -n 5
llmfit fit --good -n 10
```

**选项:**
- `--perfect` - 只返回完美匹配的模型
- `--good` - 返回良好匹配的模型
- `--marginal` - 返回勉强可用的模型
- `-n <n>` - 返回数量

### `llmfit system --json`

**基本用法:**
```powershell
llmfit system --json
```

## 📊 返回数据格式

### 推荐模型数据结构

```json
{
  "models": [
    {
      "name": "Qwen/Qwen3-Coder-30B-A3B-Instruct",
      "parameter_count": "30.5B",
      "best_quant": "Q8_0",
      "estimated_tps": 18.4,
      "fit_level": "Marginal",
      "score": 86.5,
      "use_case": "Code generation and completion",
      "run_mode": "CPU",
      "runtime": "llama.cpp"
    }
  ]
}
```

### 评分成分

- **quality** - 模型质量评分 (0-100)
- **fit** - 硬件匹配度 (0-100)
- **speed** - 预期速度评分 (0-100)
- **context** - 上下文长度评分 (0-100)

## 🎨 使用技巧

### 1. 根据场景选择

| 场景 | 参数 | 说明 |
|------|------|------|
| **通用** | `--use-case general` | 适合日常使用 |
| **编码** | `--use-case coding` | 适合代码生成和补全 |
| **推理** | `--use-case reasoning` | 适合逻辑推理任务 |
| **聊天** | `--use-case chat` | 适合对话交互 |

### 2. 硬件优化

```powershell
# 指定 RAM 容量
llmfit --ram=16G recommend --json

# 指定 GPU VRAM
llmfit --memory=24G recommend --json

# 指定 CPU 核心数
llmfit --cpu-cores=16 recommend --json
```

### 3. 上下文长度

```powershell
# 长上下文推荐
llmfit --context=131072 recommend --json

# 特定模型定制
llmfit plan "Qwen/Qwen2.5-Coder-14B-Instruct" --context=8192
```

## 🔍 常见问题

### Q: 为什么推荐都是 CPU-only？
**A**: 你的系统 GPU VRAM 无法被自动检测。如果 GPU 正常，可以尝试手动指定：
```powershell
llmfit --memory=16G --json system
```

### Q: 如何获取已安装的模型？
**A**: 使用 `llmfit list` 命令列出已安装模型

### Q: 如何刷新模型数据库？
**A**: 运行更新脚本：
```powershell
cd C:/Users/admin/.openclaw/workspace/llmfit
./scripts/update_models.sh
```

### Q: 如何在 Docker 中使用？
**A**: 使用官方 Docker 镜像：
```powershell
docker run ghcr.io/alexsjones/llmfit --version
```

## 📚 更多资源

- **官方文档**: https://github.com/AlexsJones/llmfit
- **模型库**: https://huggingface.co
- **量化说明**: Q8_0, Q4_K_M, Q2_K, FP8 等

---

**作者**: AlexsJones (llmfit 原作者)  
**OpenClaw 集成**: 基于官方 skill 包  
**许可证**: MIT
