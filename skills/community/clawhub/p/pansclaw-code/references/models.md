# 模型支持

## 本地 Ollama 模型（推荐）

| 模型 | 说明 | API 密钥 |
|------|------|----------|
| `mistral-small:24b` | 默认本地模型，速度快 | ❌ 无需 |
| `qwen3` | 中文优化 | ❌ 无需 |
| `llama3` | 通用模型 | ❌ 无需 |
| `codellama` | 代码专用 | ❌ 无需 |

## 云端模型

| 提供商 | 模型 | API 密钥 |
|--------|------|----------|
| minimax | MiniMax-Text-01 | MINIMAX_API_KEY |
| anthropic | claude-opus-4-6 | ANTHROPIC_API_KEY |
| openai | gpt-4o | OPENAI_API_KEY |

## 模型别名

| 别名 | 实际模型 |
|------|----------|
| `opus` | claude-opus-4-6 |
| `sonnet` | claude-sonnet-4-6 |
| `haiku` | claude-haiku-4-5-20251213 |

## 使用示例

### 本地 Ollama

```bash
~/.local/bin/claw --provider ollama --model mistral-small:24b --dangerously-skip-permissions "解释这段代码"
```

### 云端 Anthropic

```bash
~/.local/bin/claw --provider anthropic --model opus --dangerously-skip-permissions "重构这个模块"
```

### 云端 MiniMax

```bash
~/.local/bin/claw --provider minimax --model MiniMax-Text-01 --dangerously-skip-permissions "写一个排序算法"
```

## 权限模式

| 模式 | 说明 |
|------|------|
| `read-only` | 只读访问 |
| `workspace-write` | 允许写入工作区 |
| `danger-full-access` | 完全访问（危险） |

```bash
~/.local/bin/claw --permission-mode workspace-write --provider ollama --model mistral-small:24b "修改 README.md"
```
