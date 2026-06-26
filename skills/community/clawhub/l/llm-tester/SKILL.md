---
name: llm-tester
description: LLM 模型对比测试工具。支持多模型批量对比测试，自动记录耗时、Token 消耗、成功率，生成 JSON 格式对比报告。当需要评估不同 LLM 模型在特定任务上的表现时使用。
---

# LLM Tester - 模型对比测试工具

## Overview

自动化对比测试多个 LLM 模型在相同任务上的表现，记录速度、Token 消耗、成功率等指标，生成标准化 JSON 报告。适用于模型选型、Prompt 优化、成本评估等场景。

**使用场景**：
- 需要对比不同 LLM 模型的性能
- 需要评估模型在特定任务上的质量
- 需要批量测试多个样本
- 需要标准化测试报告

## 核心功能

| 功能 | 说明 |
|------|------|
| **多模型对比** | 同时测试多个模型，自动对比结果 |
| **批量测试** | 支持多个样本文件和 Prompt 模板 |
| **性能记录** | 自动记录耗时、Token 消耗、成功率 |
| **超时控制** | 单个模型超时自动跳过，不阻塞其他模型 |
| **JSON 报告** | 标准化输出，易于集成 CI/CD |

## CLI 使用

```bash
# 基本用法
python3 scripts/llm_benchmark.py --samples samples/ --prompts prompts/ --models qwen3.6-plus qwen3-max

# 指定超时和输出路径
python3 scripts/llm_benchmark.py \
  --samples samples/ \
  --prompts prompts/ \
  --models qwen3.6-plus qwen3-max-2026-01-23 \
  --timeout 90 \
  --output reports/report.json

# 简写
python3 scripts/llm_benchmark.py -s samples/ -p prompts/ -m qwen3.6-plus qwen3-max -t 90 -o report.json
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--samples` / `-s` | ✅ | 测试样本目录（包含 .txt 文件） |
| `--prompts` / `-p` | ✅ | Prompt 模板目录（包含 .txt 文件） |
| `--models` / `-m` | ❌ | 要测试的模型列表（默认：qwen3.6-plus qwen3-max） |
| `--timeout` / `-t` | ❌ | 单个模型超时时间（秒，默认 60） |
| `--output` / `-o` | ❌ | 报告输出路径（默认：reports/benchmark-report.json） |

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DASHSCOPE_API_KEY` | API Key | 无（必须设置） |
| `LLM_API_BASE` | API 地址 | `https://coding.dashscope.aliyuncs.com/v1/chat/completions` |

## 测试数据格式

### 样本文件（samples/*.txt）

纯文本文件，每个文件一个测试样本。

### Prompt 模板（prompts/*.txt）

使用 `{text}` 占位符，运行时替换为样本内容。

```txt
分析以下文本的写作风格，输出 JSON：
{"complexity": "简洁或复杂", "pace": "快速/舒缓/紧凑", "labels": ["标签1", "标签2", "标签3"]}

文本：
{text}
```

## 报告格式

```json
{
  "timestamp": "2026-04-14 13:30:00",
  "config": {
    "samples_dir": "samples/",
    "prompts_dir": "prompts/",
    "models": ["qwen3.6-plus", "qwen3-max-2026-01-23"],
    "timeout": 60
  },
  "summary": {
    "qwen3.6-plus": {
      "success_rate": "16/16 (100%)",
      "avg_time": "43.8s",
      "avg_tokens": "2952",
      "total_time": "701.4s",
      "total_tokens": 47230
    },
    "qwen3-max-2026-01-23": {
      "success_rate": "16/16 (100%)",
      "avg_time": "6.1s",
      "avg_tokens": "735",
      "total_time": "97.7s",
      "total_tokens": 11762
    }
  },
  "results": {
    "chapter_1_style-analysis": {
      "qwen3.6-plus": {"status": "success", "time": 36.13, "tokens": 2496, "result": {...}},
      "qwen3-max-2026-01-23": {"status": "success", "time": 13.12, "tokens": 707, "result": {...}}
    }
  }
}
```

## 依赖

- Python 3.10+
- requests >= 2.31

安装依赖：
```bash
pip install -r scripts/requirements.txt
```

## 与其他技能集成

### 与 style-analyzer 集成

```bash
# 测试风格分析能力
python3 scripts/llm_benchmark.py \
  --samples samples/novel-chapters/ \
  --prompts prompts/style-analysis.txt \
  --models qwen3.6-plus qwen3-max \
  --output reports/style-benchmark.json
```

### 与 foreshadowing-tracker 集成

```bash
# 测试伏笔识别能力
python3 scripts/llm_benchmark.py \
  --samples samples/novel-chapters/ \
  --prompts prompts/foreshadowing.txt \
  --models qwen3.6-plus qwen3-max \
  --output reports/foreshadowing-benchmark.json
```

## 注意事项

- 必须设置 `DASHSCOPE_API_KEY` 环境变量
- Prompt 模板必须包含 `{text}` 占位符
- 样本文件必须是 `.txt` 格式
- 超时时间建议 60-90 秒
