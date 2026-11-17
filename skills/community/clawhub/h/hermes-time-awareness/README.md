# hermes-time-awareness

**Languages:** English (primary) · [简体中文](#中文说明-chinese)

**Time awareness for [Hermes Agent](https://github.com/NousResearch/hermes-agent).** Injects current time and idle detection into every LLM turn — so the model always knows *what time it is* and *how long you've been away*.

> Based on the `pre_llm_call` hook mechanism. Zero core changes, prompt-cache safe, ~30 tokens per turn.

## What It Does

Every turn, the model sees a compact time block appended to the user message:

```
[time: 2026-08-29 18:00 AEST +10:00 Sat]
```

When you come back after a break:

```
[time: 2026-08-29 18:47 AEST +10:00 Sat | idle: 47m]
```

**What the model can now do:**
- Know the current time without calling `date`
- Detect when you've been away and re-anchor context
- Make time-aware decisions ("it's 11pm, defer this to tomorrow")
- Pace work within time constraints ("30 min left, prioritize P0")

## How It Works

Uses Hermes's official `pre_llm_call` plugin hook:

1. Before each LLM call, the hook fires
2. Returns `{"context": "[time: ...]"}` 
3. Hermes appends this to the **API copy** of the user message
4. The stored transcript stays clean (never persisted)
5. The system prompt is untouched (prompt cache stays warm)

### Idle Detection

The plugin tracks when each user message arrives:
- **Primary source:** `conversation_history[-2].timestamp` — cross-process accurate from the session DB
- **Fallback:** in-process per-session timestamp record
- **Threshold:** idle hint only appears after ≥60 seconds gap (avoids noise)

### Timezone Resolution

Priority chain:
1. `hermes_time` module (Hermes's own resolver)
2. `HERMES_TIMEZONE` environment variable
3. `timezone` field in `~/.hermes/config.yaml`
4. System local timezone

## Quick Start

```bash
git clone https://github.com/mfang0126/hermes-time-awareness.git /tmp/hermes-time-awareness
cd /tmp/hermes-time-awareness && bash scripts/install.sh
```

Or see **[SETUP_PROMPT.md](SETUP_PROMPT.md)** — paste one prompt to your AI agent and it does everything.

## Install (manual)

```bash
git clone https://github.com/mfang0126/hermes-time-awareness \
  ~/.hermes/plugins/hermes-time-awareness
hermes plugins enable hermes-time-awareness
hermes gateway restart
```

## Uninstall

```bash
hermes plugins disable hermes-time-awareness
rm -rf ~/.hermes/plugins/hermes-time-awareness
```

## Configuration

No configuration required — works out of the box.

Optional: set timezone explicitly if auto-detection is wrong:
```bash
# In ~/.hermes/.env
HERMES_TIMEZONE=Australia/Sydney
```

Or in `~/.hermes/config.yaml`:
```yaml
timezone: Asia/Shanghai
```

## Token Cost

| Mode | Tokens per turn |
|------|----------------|
| Time only | ~20-30 |
| Time + idle | ~35-45 |

This is a fraction of a typical tool call. The tradeoff is worth it — the model stops guessing time and starts reasoning about it.

## Tests

```bash
cd ~/.hermes/plugins/hermes-time-awareness
python3 -m pytest tests/ -v
```

## Structure

```
hermes-time-awareness/
├── plugin.yaml              # Hermes plugin manifest
├── __init__.py              # Entry point (register → hooks)
├── hooks.py                 # pre_llm_call hook
├── time_awareness/
│   ├── __init__.py
│   └── time_context.py      # Core: timezone, idle detection, formatting
├── tests/
│   └── test_time_context.py # 13 unit tests
├── scripts/
│   ├── install.sh           # Automated installer
│   └── doctor.sh            # Health check
├── SETUP_PROMPT.md          # One-shot agent setup prompt
├── README.md
├── LICENSE                  # MIT
└── .gitignore
```

## Design Principles

- **Ephemeral:** injected into API copy only, never persisted to session DB
- **Cache-safe:** does not touch the system prompt, so prompt-cache prefix stays byte-stable
- **Zero dependencies:** stdlib only (`datetime`, `threading`, `zoneinfo`)
- **Never throws:** any error returns empty string, the hook degrades gracefully
- **Minimal footprint:** ~150 lines of code total

---

## Version

v1.0.0 — current time + idle detection via pre_llm_call hook.

---

## Credits & Inspiration

This plugin would not exist without the work of these people:

### Hermes Community

- **[gejifeng](https://github.com/gejifeng)** — Author of [hermes-time-perception-extension](https://github.com/gejifeng/hermes-time_perception-extension), the original `pre_llm_call` time injection plugin for Hermes. Our code is built on top of his foundation. He also authored [PR #32942](https://github.com/NousResearch/hermes-agent/pull/32942) to upstream this into Hermes core.

- **[PR #15872](https://github.com/NousResearch/hermes-agent/pull/15872)** by quinnmacro — The maintainer-endorsed canonical approach for time injection in Hermes core. Maintainer **markojak** called it the "preferred salvage path" in [issue #17476](https://github.com/NousResearch/hermes-agent/issues/17476). This PR established the architectural pattern we follow: `pre_llm_call` hook → ephemeral user-message injection → prompt-cache safe.

- **[PR #92237](https://github.com/NousResearch/hermes-agent/pull/92237)** — The "turn-clock" plugin PR that introduced elapsed-since-last-message awareness to Hermes. Inspired our idle detection feature.

- **[Randool](https://github.com/Randool)** — Author of [time-gap](https://github.com/Randool/time-gap), a complementary Hermes plugin that injects coarse elapsed-time hints after large gaps (2h+). His approach of reading timestamps from `state.db` (restart-safe) influenced our cross-process idle detection design.

- **Hermes maintainers** (markojak, teknium1) — For clearly defining the architectural constraints in [issue #10421](https://github.com/NousResearch/hermes-agent/issues/10421): no system prompt mutation, ephemeral injection only, prompt-cache stability. These constraints made the design straightforward.

### Claude Code Community

- **[pleasedodisturb](https://github.com/pleasedodisturb)** — Author of [ChronoClaude](https://github.com/pleasedodisturb/chronoclaude), the comprehensive time awareness plugin for Claude Code. ChronoClaude's seven-layer approach (message timestamps, idle notes, passive timing blocks, MCP time tools, statusline, `/timestamps` command) was the original inspiration — it showed us what "time awareness" should look like for an AI agent.

- **[clankercode](https://github.com/clankercode)** — Author of [claude-inject-idle-time](https://github.com/clankercode/claude-inject-idle-time), the first Claude Code plugin to inject a hidden `[timing]` block on every user message via hooks. ChronoClaude merged this as its core passive timing layer.

- **[s-a-s-k-i-a](https://github.com/s-a-s-k-i-a)** — Author of [claude-code-timestamps](https://github.com/s-a-s-s-k-i-a/claude-code-timestamps) (MIT), the retrospective `/timestamps` transcript timeline for Claude Code.

### How These Pieces Fit Together

```
ChronoClaude (Claude Code)
    ↓ inspired
gejifeng/time-perception (Hermes plugin)
    ↓ established the pre_llm_call pattern
PR #15872 (maintainer-endorsed direction)
    ↓ set the architectural constraints
PR #92237 (turn-clock, elapsed awareness)
    ↓ inspired idle detection
hermes-time-awareness (this plugin)
    = time-perception + idle detection + proper attribution
```

We stand on the shoulders of all these contributors. If you find this useful, consider starring their repos too.

---

## License

MIT

---

# 中文说明 (Chinese)

**为 [Hermes Agent](https://github.com/NousResearch/hermes-agent) 提供时间感知能力。** 通过 `pre_llm_call` 钩子在每次 LLM 调用时注入当前时间与空闲检测信息，让模型始终知道 *现在几点*、*你离开多久了*。

> 基于 `pre_llm_call` 钩子机制。零核心改动、提示缓存友好（prompt-cache safe）、每轮仅约 30 tokens。

## 功能

每轮对话，模型都会在用户消息后看到一段紧凑的时间信息：

```
[time: 2026-08-29 18:00 AEST +10:00 Sat]
```

离开一段时间后回来：

```
[time: 2026-08-29 18:47 AEST +10:00 Sat | idle: 47m]
```

**模型现在可以：**
- 无需调用 `date` 即可知道当前时间
- 检测到你离开过，重新锚定上下文
- 做出时间感知的决策（"现在晚上 11 点了，这件事推迟到明天"）
- 在时间约束内安排工作节奏（"还剩 30 分钟，优先处理 P0"）

## 工作原理

使用 Hermes 官方的 `pre_llm_call` 插件钩子：

1. 每次 LLM 调用前，钩子触发
2. 返回 `{"context": "[time: ...]"}`
3. Hermes 将其追加到用户消息的 **API 副本** 中
4. 存储的对话记录保持干净（永不持久化）
5. 系统提示词不被修改（提示缓存保持热状态）

### 空闲检测

插件记录每条用户消息到达的时间：
- **主要来源：** `conversation_history[-2].timestamp` —— 从会话数据库读取，跨进程准确
- **兜底方案：** 进程内按会话记录的时间戳
- **阈值：** 间隔 ≥60 秒才显示空闲提示（避免噪音）

### 时区解析

优先级：
1. `hermes_time` 模块（Hermes 自带的解析器）
2. `HERMES_TIMEZONE` 环境变量
3. `~/.hermes/config.yaml` 中的 `timezone` 字段
4. 系统本地时区

## 快速开始

```bash
git clone https://github.com/mfang0126/hermes-time-awareness.git /tmp/hermes-time-awareness
cd /tmp/hermes-time-awareness && bash scripts/install.sh
```

或参考 **[SETUP_PROMPT.md](SETUP_PROMPT.md)** —— 把一段提示词粘贴给你的 AI 智能体，即可自动完成全部安装。

## 手动安装

```bash
git clone https://github.com/mfang0126/hermes-time-awareness \
  ~/.hermes/plugins/hermes-time-awareness
hermes plugins enable hermes-time-awareness
hermes gateway restart
```

## 卸载

```bash
hermes plugins disable hermes-time-awareness
rm -rf ~/.hermes/plugins/hermes-time-awareness
```

## 配置

无需配置，开箱即用。

可选：如果自动检测的时区不正确，可以显式设置：
```bash
# 在 ~/.hermes/.env 中
HERMES_TIMEZONE=Australia/Sydney
```

或在 `~/.hermes/config.yaml` 中：
```yaml
timezone: Asia/Shanghai
```

## Token 成本

| 模式 | 每轮 tokens |
|------|------------|
| 仅时间 | ~20-30 |
| 时间 + 空闲 | ~35-45 |

这只是一次工具调用的零头。这个代价是值得的——模型不再猜测时间，而是直接基于时间进行推理。

## 测试

```bash
cd ~/.hermes/plugins/hermes-time-awareness
python3 -m pytest tests/ -v
```

## 设计原则

- **临时性：** 只注入到 API 副本，永不写入会话数据库
- **缓存友好：** 不修改系统提示词，提示缓存前缀保持字节级稳定
- **零依赖：** 仅使用标准库（`datetime`、`threading`、`zoneinfo`）
- **永不抛错：** 任何错误都返回空字符串，钩子优雅降级
- **极简体积：** 全部代码约 150 行

## 项目结构

```
hermes-time-awareness/
├── plugin.yaml              # Hermes 插件清单
├── __init__.py              # 入口（注册 → 钩子）
├── hooks.py                 # pre_llm_call 钩子
├── time_awareness/
│   ├── __init__.py
│   └── time_context.py      # 核心：时区、空闲检测、格式化
├── tests/
│   └── test_time_context.py # 13 个单元测试
├── scripts/
│   ├── install.sh           # 自动安装脚本
│   └── doctor.sh            # 健康检查
├── SETUP_PROMPT.md          # 一次性智能体安装提示词
├── README.md
├── LICENSE                  # MIT
└── .gitignore
```

## 版本

v1.0.0 —— 通过 `pre_llm_call` 钩子实现当前时间 + 空闲检测。

## 致谢与灵感

本项目站在以下贡献者的肩膀上（详见上方英文版 Credits & Inspiration 章节）：

- **[gejifeng](https://github.com/gejifeng)** — [hermes-time-perception-extension](https://github.com/gejifeng/hermes-time_perception-extension) 的作者，Hermes 上最早的 `pre_llm_call` 时间注入插件，我们的代码建立在他的基础上
- **[PR #15872](https://github.com/NousResearch/hermes-agent/pull/15872)** — 维护者认可的 Hermes 时间注入规范方案，确立了本项目遵循的架构模式
- **[PR #92237](https://github.com/NousResearch/hermes-agent/pull/92237)** — "回合时钟"插件，引入距上条消息的间隔感知，启发了我们的空闲检测功能
- **[Randool](https://github.com/Randool)** — [time-gap](https://github.com/Randool/time-gap) 的作者，其从 `state.db` 读取时间戳的做法影响了我们的跨进程空闲检测设计
- **Hermes 维护者**（markojak、teknium1）— 明确了架构约束：不修改系统提示词、只做临时注入、保持提示缓存稳定
- **[pleasedodisturb](https://github.com/pleasedodisturb)** — [ChronoClaude](https://github.com/pleasedodisturb/chronoclaude) 的作者，本项目最初的整体灵感来源
- **[clankercode](https://github.com/clankercode)** — [claude-inject-idle-time](https://github.com/clankercode/claude-inject-idle-time) 的作者，首个在每条用户消息中注入隐藏 `[timing]` 块的 Claude Code 插件
- **[s-a-s-k-i-a](https://github.com/s-a-s-k-i-a)** — [claude-code-timestamps](https://github.com/s-a-s-s-k-i-a/claude-code-timestamps) 的作者

如果你觉得本项目有用，也请去给他们的仓库点个 Star。

## 许可证

MIT
