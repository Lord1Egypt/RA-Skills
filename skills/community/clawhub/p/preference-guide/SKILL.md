---
name: ask-to-remember
version: 1.0.5
description: Proactively capture reusable user preferences, habits, default ways of working, stable constraints, and recurring expectations likely worth remembering for future conversations. Trigger whenever the interaction exposes a plausible, non-sensitive reusable gap adjacent to the task that could help with future requests or interactions. Do not skip just because the task is already clear or completed, or because the signal already appears inside the task. Do not require certainty that the signal is permanent across all future situations; a plausible reusable default is enough. Do not treat a broad existing preference as a substitute for a newly surfaced, more specific signal. Ask at most one brief, low-friction, non-sensitive follow-up, preferably with concrete options, and append it naturally to the normal response. This skill is for non-blocking memory capture, not required clarification. Only trigger this skill in the user's direct main session, not in group chats or other shared contexts.
---

# Ask-to-Remember（ATR）—— 执行手册

如需具体的真实对话、多轮状态流转、以及 self-validation 样例，读取 `references/test-scenarios.md`。

路径约定：将 `<workspace>` 视为当前 Agent 的 workspace 根目录。不要假设所有宿主都固定使用 `~/.openclaw/workspace`。本文中的宿主文件统一指：`<workspace>/MEMORY.md`、`<workspace>/atr-state.json`、`<workspace>/atr-log.jsonl`。

## 0. 注册 ATR Prompt

首次触发时，检查 `<workspace>/AGENTS.md` 中是否已包含 `## Ask-to-Remember` 章节。如果已包含（无论是手动写入还是通过 Hook 自动注入），跳过本步骤。如果没有，将以下内容追加到 AGENTS.md 的 `## Memory` 章节末尾（如果没有 Memory 章节，追加到文件末尾）：

```markdown
## Ask-to-Remember

`ask-to-remember` skill proactively captures reusable user preferences. When the current interaction exposes a plausible, non-sensitive reusable preference gap, follow the execution steps in its `SKILL.md`. Only trigger in the human's direct main session.

### Pending Question Resolution

Check `atr-state.json` in your workspace root (if the file does not exist, skip — there is nothing to resolve). If `pendingQuestion` is not `null`, resolve it **before** doing anything else:

- **Answered** (user gave a clear preference) → extract the reusable fact, derive a short topic label from the question and reason (e.g. `周末行程风格`), append `## [ATR] <topic>` to MEMORY.md, clear `pendingQuestion`, append `{ "question": "...", "askedAt": "...", "outcome": "answered" }` to `askedQuestions`
- **Refused** (e.g. `别问了`, `别问这种`) → clear `pendingQuestion`, add a short normalized topic label to `refusedTopics`, append `{ "question": "...", "askedAt": "...", "outcome": "refused" }` to `askedQuestions`, do not write memory
- **Vague** (e.g. `都行`, `看情况`) → clear `pendingQuestion`; do not write memory; do not add to `askedQuestions`
- **Ignored** (completely unrelated to the question) → clear `pendingQuestion`; do not write memory; do not add to `askedQuestions`; increment `ignoredCount` for the topic (see Ignored cooldown below)

**Disambiguation priority:** If the user's wording can naturally be read as confirming one of the options, prefer **Answered**. If they are clearly just wrapping up the current task and bypassing the question, prefer **Ignored**. When uncertain, default to **Vague** (safest — no memory written, topic not locked).

**Ignored cooldown:** Track consecutive ignored count per topic. When the same topic has been ignored 2 times, automatically upgrade to **Refused** — add the topic to `refusedTopics` and log with `"event":"refused","note":"upgraded_from_ignored"`.

Every resolution writes one line to `atr-log.jsonl`:
`{"time":"ISO timestamp","phase":"B","event":"answered|vague|refused|ignored","question":"the original question","answer":"user's reply (if any)"}`

**Same-turn concurrency:** If Phase B resolves a pending question and Phase A is also triggered in the same turn, Phase A's precondition checks should treat `pendingQuestion` as already cleared by Phase B.

**Phase B confirmation style:** When confirming an Answered result in the same turn as a new task, keep the confirmation minimal (one short sentence) and weave it naturally into the response — do not front-load a lengthy acknowledgment before delivering the task result.
```

写入后，本次及后续会话 agent 启动时都会自动读到这段规则。

## 1. 读取状态 & 检查前置条件

读取 `<workspace>/atr-state.json`。若文件不存在，用以下默认值创建：

```json
{
  "pendingQuestion": null,
  "refusedTopics": [],
  "askedQuestions": []
}
```

**状态字段约定：**

| 字段 | 类型 | 约定 |
|------|------|------|
| `pendingQuestion` | `object \| null` | 非空时固定包含 `question`、`reason`、`askedAt` |
| `refusedTopics` | `string[]` | 存短的、归一化的话题标签，例如 `商务婉拒邮件风格`、`小段代码重构回复形式` |
| `askedQuestions` | `object[]` | 只记录已定稿的问题；条目结构固定为 `{ "question": string, "askedAt": string, "outcome": "answered" \| "refused" }` |

这里的 `topic` 是运行时概念，不要求单独存进 `pendingQuestion`。需要写 `MEMORY.md` 或 `refusedTopics` 时，从问题和 reason 中提炼一个稳定、可复用的短标签即可。

**前置条件检查表**——全部通过才继续，否则跳过并写 skipped 日志（见步骤 4）：

| 条件 | 不通过时 reason |
|------|----------------|
| `pendingQuestion` 为 `null`（Phase B 会在本轮优先收口，此处是同一个 gate 的 Phase A 侧） | `pending` |
| 目标话题不在 `refusedTopics` 中 | `refused` |
| `<workspace>/MEMORY.md` 中尚未记录该信息 | `already_known` |
| `askedQuestions` 中不存在语义重复的问题 | `duplicate` |

额外 skip reason：若 skill 被触发但评估后认为当前交互不存在值得长期复用的偏好 gap，直接跳过并以 `not_reusable` 写 skipped 日志。

注意：当前请求里已经露出了一个可复用偏好信号，不是跳过理由。只要仍存在一个值得长期复用的隐式 gap，就继续问。

## 2. 构造问题

唯一原则：**选择题 > 主观题**——尽量给 2-3 个具体选项，别让用户开放作答。

示例：
> “对了，你平时更习惯 X、Y、还是 Z？知道的话我以后直接按这个来。”

## 3. 嵌入回复 & 提问

把问题自然接在正常回复末尾。

禁止事项：
- 单独发一条消息来提问
- 提及 ATR、skill、状态机或任何内部机制
- 用分隔线、标题等特殊格式把问题和正常回复分开
- 同一轮提出多个 ATR 问题——如有多个候选话题，只选最有复用价值的一个

## 4. 更新状态 & 写日志

### 更新 atr-state.json

提问后仅更新相关字段，保留其他已有字段：

```json
{
  "pendingQuestion": {
    "question": "你问的问题",
    "reason": "为什么这个信息值得长期复用",
    "askedAt": "ISO 时间戳"
  }
}
```

### 写日志 atr-log.jsonl

向 `<workspace>/atr-log.jsonl` 追加一行。只在**提问**或**明确跳过**时写日志。

**成功提问：**
```json
{"time":"ISO时间戳","phase":"A","event":"asked","question":"你问的问题","reason":"复用价值说明"}
```

**跳过：**
```json
{"time":"ISO时间戳","phase":"A","event":"skipped","reason":"pending|refused|duplicate|already_known|not_reusable"}
```

---

## 可选：通过 Hook 自动注入（进阶）

如果你的宿主支持 OpenClaw Hooks，可以用 `agent:bootstrap` hook 替代上面的步骤 0，让 ATR prompt 在每次 agent 启动时自动注入，无需修改 AGENTS.md。

### 安装方式

将 `hooks/openclaw/` 目录下的文件复制到 managed hooks 目录：

```bash
mkdir -p ~/.openclaw/hooks/ask-to-remember
cp hooks/openclaw/HOOK.md hooks/openclaw/handler.js ~/.openclaw/hooks/ask-to-remember/
```

重启 Gateway 后验证：

```bash
openclaw hooks list
# 应看到 ask-to-remember 状态为 ✓ ready
```

安装成功后，ATR prompt 会通过 bootstrap 虚拟文件 `ASK_TO_REMEMBER.md` 自动注入，可以从 AGENTS.md 中移除手动写入的 `## Ask-to-Remember` 章节。
