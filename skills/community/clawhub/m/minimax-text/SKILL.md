---
name: minimax-text
description: MiniMax 文本生成模型，支持 M2.7/M2.5/M2.1/M2 等大语言模型。使用 MINIMAX_API_KEY 环境变量。
metadata: {"openclaw":{"emoji":"💬","requires":{"bins":["python3"]}}}
---

# MiniMax 文本生成

使用 MiniMax 大语言模型进行文本生成、对话、代码编写等任务。

## 支持的模型

| 模型 | 说明 |
|------|------|
| `MiniMax-M2.7` | 旗舰模型，2048K context，支持多语言编程和复杂推理 |
| `MiniMax-M2.5` | 高性能模型，2048K context，优化代码生成 |
| `MiniMax-M2.1` | 强力多语言编程能力 |
| `MiniMax-M2` | Agent 能力，高级推理 |
| `MiniMax-M2.5-highspeed` | M2.5 高速版，~100 tps |

## 前置要求

- Python 3
- `pip3 install requests`
- 设置环境变量 `MINIMAX_API_KEY`

```bash
export MINIMAX_API_KEY="你的API Key"
```

## 使用方法

### 直接调用

```bash
python3 {baseDir}/scripts/text.py --model MiniMax-M2.7 --prompt "你好，介绍一下自己"
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--model` | 模型名 | `MiniMax-M2.7` |
| `--prompt` | 输入提示 | - |
| `--system` | 系统提示 | 可选 |
| `--messages` | JSON 格式的历史消息 | 可选 |
| `--think` | 启用思考模型（0/1）| 0 |
| `--output` | 输出文件 | stdout |

### 示例

```bash
# 基本对话
python3 {baseDir}/scripts/text.py --model MiniMax-M2.7 --prompt "用Python写一个快速排序"

# 带系统提示
python3 {baseDir}/scripts/text.py --model MiniMax-M2.5 --system "你是一个专业的Python程序员" --prompt "解释一下什么是装饰器"
```
