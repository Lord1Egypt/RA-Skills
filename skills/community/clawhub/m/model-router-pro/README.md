# Smart Model Router

12-dimension task scorer with 98 pre-configured models across 20 providers.
Automatically routes every substantive user request to the optimal LLM model.

## Installation

```bash
clawhub install model-router-pro
```

OpenClaw's skills watcher loads SKILL.md automatically after installation.
However, the agent must be configured to use installed skills — check your
OpenClaw `skills` settings to ensure the watcher is enabled for your agent.

> **Tip**: Add a note to your agent's AGENTS.md (e.g. `Always follow smart-model-router SKILL.md instructions`) to reinforce compliance, especially when using less capable models that may ignore skill instructions.

### Post-Install Setup

```bash
python3 <skill_path>/scripts/router.py --setup
```

This reads your `~/.openclaw/openclaw.json`, matches models against the 98 built-in
defaults, and generates a `models.json` with pre-filled capability scores.
Edit the generated `models.json` to customize scores based on your experience.

> **Without `--setup`, the router returns `fallback/default` and will NOT switch models.**

## Quick Start

```bash
# Route a task (after --setup)
python3 <skill_path>/scripts/router.py --task "Write a Python web scraper"

# Debug the scoring
python3 <skill_path>/scripts/router.py --task "Explain quantum entanglement" --debug
```

---

## Architecture

```
User Message
    │
    ▼
┌─────────────────────────────────────────┐
│           12-Dimension Scorer           │
│                                         │
│  tokenCount    codePresence             │
│  reasoning     technicalTerms           │
│  creative      simpleIndicators         │
│  multiStep     questionComplexity       │
│  imperative    constraintCount          │
│  outputFormat  agenticTask              │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│        Sigmoid Confidence Calibrator     │
│                                         │
│  Weighted Score → Tier + Confidence     │
│  SIMPLE / MEDIUM / COMPLEX / REASONING  │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│         Capability Matcher               │
│                                         │
│  Rank by task-relevant dimension        │
│  Ties broken by cost (ascending)        │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│         Availability Filter              │
│                                         │
│  Exclude models not in openclaw.json    │
│  All-default → fallback (no switch)     │
└──────────────────┬──────────────────────┘
                   │
                   ▼
              Recommended Model
```

### Execution Flow

When installed as an OpenClaw skill, the agent executes this on every substantive request:

1. **Score** the user's message across 12 dimensions
2. **Parse** the JSON output (`full_id`, `tier`, `confidence`)
3. **Switch** to the recommended model via `session_status(model=<full_id>)`
4. **Answer** the user's request with the optimal model

### Key Features

- **12-Dimension Scoring**: Analyzes task complexity from token count, code presence, reasoning markers, technical terms, creative markers, simple indicators, multi-step patterns, question complexity, imperative verbs, constraints, output format, and agentic task signals.

- **Sigmoid Confidence Calibration**: Maps weighted dimension scores to a tier (SIMPLE/MEDIUM/COMPLEX/REASONING) with a confidence value between 0.5 and 1.0. Smooth transitions between tiers, no hard cutoffs.

- **Reasoning Override**: Tasks with 2+ reasoning keywords (analyze, prove, derive, explain why) are directly upgraded to REASONING tier, bypassing the sigmoid.

- **Capability Matching**: Models are ranked by their score in the task-relevant dimension. Code tasks prioritize the `code` capability; reasoning tasks prioritize `reasoning`. Ties are broken by cost (cheapest first).

- **98 Pre-Configured Models**: Built-in capability defaults for 98 models across 20 providers. `--setup` auto-matches models from your openclaw.json against the defaults database.

- **Unconfigured Guard**: If all models have default (5.0) capabilities, the router returns `fallback/default` instead of picking randomly. The agent is instructed not to switch models in this case.

- **Availability Filter**: Models listed in `models.json` but not present in `~/.openclaw/openclaw.json` are automatically excluded.

- **Profile Strategies** (optional): `auto` (default), `eco` (prefer cheaper), `premium` (prefer stronger), `coding` (1.5× code task boost).

- **Zero Dependencies**: Python stdlib only, works everywhere.

---

## Model Database

### Coverage

| Provider | Models | Highlights |
|----------|:------:|-----------|
| OpenAI | 11 | GPT-5.4, GPT-5.5, O3, O4-Mini |
| Anthropic | 8 | Claude Opus 4.7, Sonnet 4.6, Haiku 4.5 |
| Google | 8 | Gemini 3.1 Pro/Flash, Gemma 4 |
| xAI | 5 | Grok-4.20, Grok-4, Grok-3 |
| Zhipu AI | 13 | GLM-5.1, GLM-5, GLM-4.7 |
| Alibaba | 9 | Qwen 3.6 Plus, Qwen3-Coder-Plus |
| Moonshot | 3 | Kimi K2.6, K2.5, K2 |
| MiniMax | 5 | M2.7, M2.5 |
| DeepSeek | 8 | V4-Pro, V4, V3.2, R1 |
| Xiaomi | 5 | MiMo V2.5-Pro, V2-Pro |
| Meta | 2 | Llama 4 Maverick, Scout |
| Mistral | 7 | Large, Medium 3.1, Codestral |
| Amazon | 3 | Nova Premier, Pro |
| NVIDIA | 2 | Nemotron 3 Super |
| ByteDance | 3 | Seed 2.0 |
| Baidu | 1 | ERNIE 4.5 |
| Perplexity | 2 | Sonar Pro, Deep Research |
| StepFun | 1 | Step 3.5 Flash |
| Microsoft | 1 | Phi-4 |
| Elephant | 1 | Elephant Alpha |

### Score System

Scores are **unbounded floats** (no ceiling) to accommodate future models:

- `code`: Programming ability
- `reasoning`: Logic, math, analysis
- `agentic`: Multi-step tool use
- `cost`: Relative cost (lower = cheaper)

Current range: 0.3 – 11.0. As models improve, scores can exceed 10.

---

## Strengths

1. **Largest pre-configured model database** — 98 models across 20 providers, vs competitors' 5-15 models

2. **Zero-config setup** — `--setup` pre-fills all scores, no manual editing required

3. **Comprehensive scoring** — 12 dimensions vs competitors' 2-3

4. **Safe by default** — unconfigured = no switch, unavailable = auto-filtered

5. **Fully debuggable** — `--debug` shows every dimension score and signal

6. **Zero dependencies** — Python stdlib only, works everywhere

## Limitations

1. **Estimated capability scores** — Scores are derived from general model knowledge, not from standardized benchmarks (SWE-bench, GPQA, etc.). We chose breadth (98 models) over precision (benchmark-derived scores for 10 models). Adjust based on your experience.

2. **Agent compliance dependency** — Automatic model switching relies on the agent following SKILL.md instructions. Strong models (Claude, GPT, Qwen) reliably comply. Weaker models may ignore the switch command.

3. **Estimated cost** — Cost scores are derived from model tier, not actual API pricing. Users on discounted plans should adjust manually.

4. **String-based model matching** — Models with unusual suffixes (e.g., `-preview`, `-exp`) may not match the defaults database. Check `models.json` after running `--setup`.

## Comparison

| Feature | model-router-premium | auto-model-router | smart-model-router |
|---------|:---:|:---:|:---:|
| Scoring dimensions | 2 | Agent LLM judgment | **12** |
| Confidence calibration | None | None | **Sigmoid** |
| Pre-configured models | ~5 | ~5 | **98** |
| Profile strategies | None | None | **4** |
| Auto model switching | No | Yes (agent) | **Yes (agent)** |
| Zero-config setup | No | Partial | **`--setup`** |
| Debug output | No | No | **12 dimensions** |
| Availability filter | No | No | **Yes** |

## File Structure

```
smart-model-router/
├── README.md                    # This file
├── SKILL.md                     # Agent execution instructions
├── capabilities_defaults.json   # 98 model defaults
├── scripts/
│   ├── router.py                # Core: scorer + CLI
│   └── config.py                # Config loading
└── examples/
    ├── models.json              # Example model config
    └── config.json              # Example router config
```

## License

MIT

---

# 智能模型路由器

12 维度任务评分器，预配置 98 个模型，覆盖 20 家厂商。自动将每条实质性用户请求路由到最优模型。

**中文用户友好**：支持中文关键词检测（分析、推导、写、翻译等），预配置国内主流模型（GLM、Qwen、Kimi、MiniMax、DeepSeek、MiMo、ERNIE、Seed 等）。

## 安装

```bash
clawhub install model-router-pro
```

OpenClaw 的 skills watcher 安装后会自动加载 SKILL.md。但需要确保你的 agent 配置中启用了 skills watcher。

> **提示**：在 AGENTS.md 中添加一条提醒（如 `Always follow smart-model-router SKILL.md instructions`），特别是使用较弱模型时，可以增强 agent 对路由指令的遵循度。

### 安装后配置

```bash
python3 <skill_path>/scripts/router.py --setup
```

> **不运行 `--setup`，路由器将返回 `fallback/default`，不会切换模型。**

## 快速开始
python3 scripts/router.py --task "帮我写一个Python爬虫"

# 4. 查看评分详情
python3 scripts/router.py --task "分析一下AI模型的趋势" --debug
```

## 架构设计

```
用户消息
    │
    ▼
┌─────────────────────────────────────────┐
│              12 维度评分器                 │
│                                         │
│  tokenCount    codePresence             │
│  reasoning     technicalTerms           │
│  creative      simpleIndicators         │
│  multiStep     questionComplexity       │
│  imperative    constraintCount          │
│  outputFormat  agenticTask              │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│           Sigmoid 置信度校准              │
│                                         │
│  加权分数 → 等级 + 置信度 [0.5, 1.0]     │
│  SIMPLE / MEDIUM / COMPLEX / REASONING  │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│              能力匹配器                   │
│                                         │
│  按任务相关维度排序                      │
│  同分按成本升序                          │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│              可用性过滤器                  │
│                                         │
│  排除 openclaw.json 中不存在的模型        │
│  全默认 → 返回 fallback（不切换）         │
└──────────────────┬──────────────────────┘
                   │
                   ▼
              推荐模型
```

### 执行流程

安装为 OpenClaw 技能后，agent 在每条实质性请求上执行：

1. **评分**：对用户消息进行 12 维度评分
2. **解析**：从 JSON 提取 `full_id`、`tier`、`confidence`
3. **切换**：通过 `session_status(model=<full_id>)` 切换到推荐模型
4. **回答**：用最优模型回答用户

### 核心特性

- **12 维度评分**：从 token 数量、代码特征、推理标记、技术术语、创意标记、简单指示、多步模式、问题复杂度、祈使动词、约束数量、输出格式、智能体任务等维度分析任务复杂度

- **Sigmoid 置信度**：加权分数映射到等级 + 置信度 [0.5, 1.0]，平滑过渡

- **推理快速通道**：2+ 推理关键词（分析、证明、推导）直接升级为 REASONING 等级

- **能力匹配**：代码任务优先 code 分数，推理任务优先 reasoning 分数

- **98 个预配置模型**：内置 98 个模型的能力默认值，`--setup` 自动匹配

- **未配置保护**：全默认分数 → 返回 fallback，永不降级体验

- **可用性过滤**：自动排除 openclaw.json 中不存在的模型

## 模型数据库

### 覆盖范围

| 厂商 | 模型数 | 代表模型 |
|------|:------:|---------|
| 智谱 Zhipu | 13 | GLM-5.1, GLM-5, GLM-4.7 |
| 阿里 Alibaba | 9 | Qwen 3.6 Plus, Qwen3-Coder-Plus |
| 月之暗面 Moonshot | 3 | Kimi K2.6, K2.5, K2 |
| MiniMax | 5 | M2.7, M2.5 |
| DeepSeek | 8 | V4-Pro, V4, V3.2, R1 |
| 小米 Xiaomi | 5 | MiMo V2.5-Pro, V2-Pro |
| 字节跳动 ByteDance | 3 | Seed 2.0 |
| 百度 Baidu | 1 | ERNIE 4.5 |
| OpenAI | 11 | GPT-5.4, GPT-5.5, O3, O4-Mini |
| Anthropic | 8 | Claude Opus 4.7, Sonnet 4.6, Haiku 4.5 |
| Google | 8 | Gemini 3.1 Pro/Flash, Gemma 4 |
| xAI | 5 | Grok-4.20, Grok-4, Grok-3 |
| Meta | 2 | Llama 4 Maverick, Scout |
| Mistral | 7 | Large, Medium 3.1, Codestral |
| Amazon | 3 | Nova Premier, Pro |
| NVIDIA | 2 | Nemotron 3 Super |
| Perplexity | 2 | Sonar Pro, Deep Research |
| StepFun | 1 | Step 3.5 Flash |
| Microsoft | 1 | Phi-4 |
| Elephant | 1 | Elephant Alpha |

## 优势

1. **最大的预配置模型库** — 98 个模型覆盖 20 家厂商，竞品仅 5-15 个

2. **零配置开箱即用** — `--setup` 一键生成，无需手动编辑

3. **全面评分** — 12 个维度，竞品仅 2-3 个

4. **默认安全** — 未配置不切换，不可用自动过滤

5. **完全可调试** — `--debug` 显示每个维度的评分和信号

6. **零依赖** — 纯 Python 标准库，随处可用

7. **中文友好** — 原生中文关键词检测，预配置国内主流模型

## 局限性

1. **估算能力分数** — 分数基于模型的一般认知，非标准化 benchmark 数据（SWE-bench、GPQA 等）。我们选择了覆盖广度（98 个模型）而非精度。建议根据实际使用体验调整分数。

2. **依赖 agent 遵循指令** — 自动模型切换依赖 agent 遵循 SKILL.md 指令。强模型（Claude、GPT、Qwen）能可靠执行。弱模型可能忽略切换命令。

3. **估算成本** — 成本分数基于模型层级，非实际 API 定价。有折扣方案的用户请手动调整。

4. **基于字符串的模型匹配** — 带有特殊后缀的模型（如 `-preview`、`-exp`）可能无法匹配默认数据库。运行 `--setup` 后请检查生成的 `models.json`。

## 竞品对比

| 特性 | model-router-premium | auto-model-router | smart-model-router |
|------|:---:|:---:|:---:|
| 评分维度 | 2 | Agent 判断 | **12** |
| 置信度校准 | 无 | 无 | **Sigmoid** |
| 预配置模型 | ~5 | ~5 | **98** |
| Profile 策略 | 无 | 无 | **4** |
| 中文支持 | 否 | 部分 | **原生双语** |
| 自动切换 | 否 | 是 (agent) | **是 (agent)** |
| 零配置 | 否 | 部分 | **`--setup`** |
| 调试输出 | 否 | 否 | **12 维度** |
| 可用性过滤 | 否 | 否 | **是** |
