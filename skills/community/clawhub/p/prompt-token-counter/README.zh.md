# prompt-token-counter

[English](README.md)

一个 **OpenClaw skill**，用于统计 token 数量并估算 API 成本。

## 实现原理

本项目提供**本地 token 计数**，无需调用 API：

| 方式 | OpenAI | 其他模型 |
|------|--------|----------|
| **方法** | tiktoken（精确） | 公式近似 |
| **精度** | 精确 | 约 85–95% |

对非 OpenAI 模型，使用**按 provider 校准的公式**。当文本包含 CJK（中/日/韩）时，会根据 CJK 字符占比**混合比例**，使中文为主的文本获得更低的 chars/token（每字符更多 token）。

### 基准测试：主力模型（8927 字符，英文/混合）

| 模型 | 字符数 | Token 数 | 1 token ≈ 多少字符 | 状态 |
|------|--------|----------|-------------------|------|
| anthropic/claude-sonnet-4-6 | 8927 | 2763 | 3.23 | ✓ |
| anthropic/claude-sonnet-4-5 | 8927 | 2763 | 3.23 | ✓ |
| anthropic/claude-opus-4.6 | 8927 | 2763 | 3.23 | ✓ |
| openai/gpt-5.2-codex | 8927 | 2459 | 3.63 | ✓ |
| google/gemini-3.1-pro-preview | 8927 | 2627 | 3.40 | ✓ |
| z-ai/glm-5 | 8927 | 2457 | 3.63 | ✓ |
| volcengine/doubao-seed-2-0-pro | 8927 | 2702 | 3.30 | ✓ |
| moonshot/kimi-k2.5 | 8927 | 2402 | 3.72 | ✓ |
| minimax/MiniMax-M2.5 | 8927 | 2428 | 3.68 | ✓ |
| deepseek-v3.2 | 8927 | 2578 | 3.46 | ✓ |

### 基准测试：主力模型（3050 字符，混杂中文）

| 模型 | 字符数 | Token 数 | 1 token ≈ 多少字符 | 状态 |
|------|--------|----------|-------------------|------|
| anthropic/claude-sonnet-4-6 | 3050 | 1913 | 1.59 | ✓ |
| anthropic/claude-sonnet-4-5 | 3050 | 1913 | 1.59 | ✓ |
| anthropic/claude-opus-4.6 | 3050 | 1913 | 1.59 | ✓ |
| openai/gpt-5.2-codex | 3050 | 1564 | 1.95 | ✓ |
| google/gemini-3.1-pro-preview | 3050 | 1473 | 2.07 | ✓ |
| z-ai/glm-5 | 3050 | 1318 | 2.31 | ✓ |
| volcengine/doubao-seed-2-0-pro | 3050 | 1494 | 2.04 | ✓ |
| moonshot/kimi-k2.5 | 3050 | 1257 | 2.43 | ✓ |
| minimax/MiniMax-M2.5 | 3050 | 1289 | 2.37 | ✓ |
| deepseek-v3.2 | 3050 | 1361 | 2.24 | ✓ |

*基准数据来自 `scripts/examples/benchmark_token_ratio.py`（API 模式）。*

## 这个 Skill 能做什么

加载后，Agent 可以：

| 能力 | 使用场景 |
|------|----------|
| **统计 token** | 「这段 prompt 有多少 token？」、「X 的 token 长度」 |
| **估算成本** | 「这段文字用 GPT-4 要多少钱？」、「Claude 的 API 成本」 |
| **审计 OpenClaw 工作区** | 「我的工作区用了多少 token？」、「哪些 memory/persona/skills 消耗 token？」 |
| **对比模型** | 「对比不同模型的 token 成本」、「哪个模型更便宜？」 |

### OpenClaw Token 审计

该 skill 帮助识别工作区各组件的 token 消耗：

- **Memory 与 persona**：AGENTS.md、SOUL.md、IDENTITY.md、USER.md、MEMORY.md、TOOLS.md 等
- **Skills**：`~/.openclaw/skills/` 或 `workspace/skills/` 下的每个 SKILL.md

审计示例（批量多文件）：
```bash
python -m scripts.cli -m gpt-4o -c AGENTS.md SOUL.md MEMORY.md
```

## 何时触发

- 用户询问 token 数量、prompt 长度、API 成本
- 用户提到 OpenClaw 上下文大小或工作区 token 使用
- Agent 需要在变更前后审计 token 消耗

## 复制发送给 OpenClaw

**ClawHub（推荐，国际）**
```text
Please run clawhub install prompt-token-counter to install this skill, and help me count tokens and estimate API costs.
```

**npm**
```text
Please run npm i prompt-token-counter to install this skill, and help me count tokens and estimate API costs.
```

## 快速参考

```bash
python -m scripts.cli -m gpt-4 "Hello, world!"
python -m scripts.cli -f input.txt -m claude-3-opus -c
python -m scripts.cli -l   # 列出 300+ 模型
```

## 基准测试脚本

运行 `scripts/examples/benchmark_token_ratio.py` 可批量测试各模型的 token 比例：

- **API 模式**（默认）：调用模型 API 获取精确 `prompt_tokens`。需在脚本中设置 `API_KEY` 和 `BASE_URL`。
- **本地模式**（`--local`）：使用本项目的 TokenCounter 近似计算，无需 API。

```bash
python scripts/examples/benchmark_token_ratio.py           # API 模式
python scripts/examples/benchmark_token_ratio.py --local   # 本地近似
```

MIT
