# 任务类别与模型匹配

> 给你（AI Agent）读的决策规则。为任务选择 category 和 model 时查阅本文件。

---

## 核心洞察：模型是不同性格的开发者

把 AI 模型想象成团队里性格不同的开发者。**模型不是"更聪明"或"更笨"，而是思考方式不同。** 把同一条指令给 Claude 和 GPT，他们的理解和执行方式截然不同。

这不是 bug，而是系统设计的基础。每个 Agent 使用与其工作风格匹配的模型——就像组建团队时把合适的人放在合适的位置。

---

## 模型性格分类

### Claude / Kimi / GLM — 沟通型，机制驱动

这类模型像团队里那个什么都懂、靠沟通协调推动事情的人。给他一份详细操作手册，他会逐条执行。

擅长：
- 遵循复杂的多层级指令（SOUL.md + AGENTS.md 的详细规范正是为它们写的）
- 在大量工具调用中保持对话连贯
- 生成结构化、有条理的输出
- 理解细微的委派和编排模式

**Fallback Chain 内安全替换：** Claude Opus → Claude Sonnet → Kimi → GLM（同家族内替换，行为一致）

### GPT — 自主型，原则驱动

这类模型像团队里整天埋头钻研的技术专家。你说目标，他自己找方法；你给太多规则反而让他困惑。

擅长：
- 深度自主探索，无需手把手引导
- 跨多文件推理复杂代码库
- 原则驱动执行（给目标，不给步骤）
- 长时间独立工作而不偏离

**注意：** 把 GPT 换成 Claude 不是"降级"，而是换了脑子——同样的指令会被完全不同地理解。

### Gemini — 视觉型 + 速度优先

在视觉/前端任务上有独特优势，速度快、成本低。适合视觉推理或高频轻量任务。

**不要**把轻量任务"升级"到 Claude Opus——那是雇一个高级工程师来写会议纪要，浪费能力和成本。

---

## Agent 画像：谁用什么模型，为什么

### 沟通型 Agent → Claude / Kimi / GLM 优先

这些 Agent 的 SOUL.md 和 AGENTS.md 是机制驱动风格（详细清单、分步流程、明确原则），需要能忠实执行复杂指令的模型。

| Agent | 角色 | Fallback Chain | 说明 |
|-------|------|----------------|------|
| **芒格** | 战略规划 | Claude Opus → Kimi → GLM → GPT x.x | Claude 首选。同家族内可自由替换。 |
| **德明** | 质量把关 | Claude Opus → Kimi → GLM | 审查任务需要严格遵循清单，Claude 家族最合适。 |
| **德鲁克** | 项目管理 | Claude Sonnet → Kimi → GLM | Sonnet 足够，不需要 Opus 级别。 |

### 自主型 Agent → GPT 优先

费曼的 SOUL.md 是原则驱动风格（"追根究底"、"What I cannot create, I do not understand"）。这类 Agent 假设模型会自主探索，给目标而非步骤。

| Agent | 角色 | Fallback Chain | 说明 |
|-------|------|----------------|------|
| **费曼** | 深度开发 | GPT x.x Codex → Claude Opus → Gemini x.x Pro | GPT Codex 优先。**降级到 Claude 时需补偿**（见下文）。 |

**降级补偿：** 当费曼用 Claude Opus 时，`sessions_send` 的 message 里要写明详细步骤，而不只是说目标。Claude 需要"地图"，GPT 只需要"目的地"。

### 速度型任务 → Gemini Flash / MiniMax / Claude Haiku

轻量、高频、不需要深度推理的任务。**不要"升级"到 Opus**。

| 场景 | Fallback Chain | 说明 |
|------|----------------|------|
| 视觉/前端任务 | Gemini x.x Pro → GLM → Claude Opus | Gemini 在视觉推理上有独特优势 |
| 快速简单任务 | Claude Haiku → Gemini x.x Flash → GPT x.x Nano | 速度优先，成本最低 |

---

## 模型家族详解

> 帮你（和用户）理解每个模型适合干什么，以及在 `openclaw.json` 里怎么填写。

### Claude 家族 — 沟通型，适合编排和审查

| 模型 | 特点 | 最适合的场景 | openclaw.json 填法 |
|------|------|------------|-------------------|
| **Claude Opus** | 最强的指令遵循能力，最高合规度 | 芒格（复杂规划）、德明（严格审查）、高难度通用任务 | `anthropic/claude-opus-4.6` |
| **Claude Sonnet** | 速度和能力的平衡点 | 德鲁克（项目协调）、日常中等难度任务 | `anthropic/claude-sonnet-4.6` |
| **Claude Haiku** | 最快、最便宜的 Claude | 快速简单任务、高频轻量调用 | `anthropic/claude-haiku-4.5` |
| **Kimi** | 行为非常接近 Claude，性价比高 | Claude 的平替，适合所有 Claude 适合的场景 | `moonshotai/kimi-k2.5` |
| **GLM** | Claude-like 行为，中文能力强 | 中文场景的编排和协调任务 | `z-ai/glm-5` 或 `openrouter/z-ai/glm-4.x` |

**家族内安全替换顺序：** Claude Opus → Claude Sonnet → Kimi → GLM

---

### GPT 家族 — 自主型，适合深度技术工作

| 模型 | 特点 | 最适合的场景 | openclaw.json 填法 |
|------|------|------------|-------------------|
| **GPT x.x Codex** | 深度代码能力，自主探索，原则驱动 | 费曼（深度开发）——这是费曼的**首选**，不要轻易替换 | `openai/codex-...`（按当前可用版本） |
| **GPT x.x** | 高智能，战略推理 | 需要最高推理能力的任务（ultrabrain 的首选）| `openai/gpt-...`（按当前可用版本） |
| **GPT x.x Nano** | 超快、极低成本 | 简单工具性任务，快速任务的最后兜底 | `openai/gpt-...-nano`（按当前可用版本） |

> **提示：** GPT 模型的具体版本号会随时更新。用 `openclaw models` 查看当前可用的模型列表，选 GPT 系列里最新的 Codex 版本给费曼，最新的旗舰版给 ultrabrain 任务。

---

### Gemini 家族 — 视觉型 + 速度优先

| 模型 | 特点 | 最适合的场景 | openclaw.json 填法 |
|------|------|------------|-------------------|
| **Gemini x.x Pro** | 视觉推理出色，不同的思维风格 | 视觉/前端任务（visual-engineering）、创意任务（artistry）的首选 | `google/gemini-pro-...`（按当前可用版本） |
| **Gemini x.x Flash** | 快速，适合文档和轻量任务 | writing 任务首选、quick 任务备选 | `google/gemini-flash-...`（按当前可用版本） |

---

### Grok Code Fast — 代码搜索专用，极速

| 模型 | 特点 | 最适合的场景 | openclaw.json 填法 |
|------|------|------------|-------------------|
| **Grok Code Fast** | 闪电速度，专为代码检索优化 | `quick` 类任务的**首选**，尤其适合高频并行的代码搜索。可以同时并发 10 个调用。 | `openrouter/x-ai/grok-...`（按当前可用版本） |

> Speed is everything. Fire 10 in parallel.（速度就是一切，可以同时开 10 个并行。）

---

### MiniMax — 速度型，极低成本

| 模型 | 特点 | 最适合的场景 | openclaw.json 填法 |
|------|------|------------|-------------------|
| **MiniMax** | 快且便宜，适合工具性任务 | `quick` 任务次选，Grok Code Fast 不可用时的兜底 | `minimax/minimax-m2.5` |

---

### 如何查看当前可用模型

```bash
# 查看 OpenClaw 当前配置的可用模型
openclaw models

# 或查看 openclaw.json 里配置的模型
cat ~/.openclaw/openclaw.json | grep model
```

模型名称的格式通常是 `<provider>/<model-id>`，如 `anthropic/claude-opus-4-6`。通过 OpenRouter 访问时前缀是 `openrouter/`，如 `openrouter/openai/gpt-4o`。

---

## 任务类别（Category）完整匹配表

按 category 选模型时，参考以下 Fallback Chain（基于 oh-my-openagent 原始设计）：

| Category | 适用场景 | Fallback Chain |
|----------|---------|----------------|
| `visual-engineering` | Frontend、UI/UX、CSS、动画 | Gemini x.x Pro → GLM → Claude Opus |
| `ultrabrain` | 战略规划、架构决策、PRD 设计 | GPT x.x → Gemini x.x Pro → Claude Opus |
| `deep` | 复杂实现、多文件重构、深度调试 | GPT x.x Codex → Claude Opus → Gemini x.x Pro |
| `artistry` | 营销文案、品牌故事、创意方案 | Gemini x.x Pro → Claude Opus → GPT x.x |
| `quick` | 单行修改、配置值、拼写修复 | Grok Code Fast → MiniMax → Claude Haiku → Gemini x.x Flash → GPT x.x Nano |
| `unspecified-high` | 代码审查、多步骤复杂分析 | Claude Opus → GPT x.x → GLM → Kimi |
| `unspecified-low` | 进度跟踪、文档整理、日常协调 | Claude Sonnet → GPT x.x Codex → Gemini x.x Flash |
| `writing` | README、技术文档、说明文章 | Gemini x.x Flash → Claude Sonnet |

---

## 模型配置方式（openclaw.json）

**关键：Fallback 是全局配置，写在 `agents.defaults.model.fallbacks`，不是每个 Agent 单独写。**

`agents.list[]` 里每个子 Agent 只配 `model`（单个字符串，主模型）。当主模型不可用时，OpenClaw 自动按 `agents.defaults.model.fallbacks` 的顺序降级。

```json5
{
  agents: {
    defaults: {
      model: {
        // 全局主模型（未单独配置 model 的 Agent 都走这个）
        primary: "anthropic/claude-opus-4-6",
        // 全局 Fallback Chain：主模型失败时依次尝试
        fallbacks: [
          "openrouter/moonshotai/kimi-k2",
          "openrouter/z-ai/glm-5",
          "anthropic/claude-sonnet-4-6",
          "minimax/minimax-m2.5",           // 速度型任务兜底，快且便宜
        ],
      },
    },
    list: [
      {
        id: "munger",
        workspace: "~/.openclaw/workspace-munger",
        model: "anthropic/claude-opus-4-6",   // 沟通型 → Claude Opus
      },
      {
        id: "feynman",
        workspace: "~/.openclaw/workspace-feynman",
        model: "openai/gpt-5.3-codex",        // 自主型 → GPT Codex（单独覆盖）
      },
      {
        id: "deming",
        workspace: "~/.openclaw/workspace-deming",
        model: "anthropic/claude-opus-4-6",   // 审查 → Claude Opus
      },
      {
        id: "drucker",
        workspace: "~/.openclaw/workspace-drucker",
        model: "anthropic/claude-sonnet-4-6", // 协调 → Sonnet 足够
      },
    ],
  },
}
```

> ⚠️ `agents.list[]` 里**没有** `fallback` 字段——写了会报 `Unrecognized key: "fallback"` 错误。Fallback 只能写在 `agents.defaults.model.fallbacks`（全局生效）。

---

## Fallback Chain 执行逻辑

```
Step 1: 读取 ~/.openclaw/openclaw.json，找可用模型列表
         如果无法读取 → 询问用户

Step 2: 按任务 category 找对应 Fallback Chain

Step 3: 遍历 Chain，选第一个在可用列表中的模型
         （模糊匹配：用户配了 "gemini-2.0-flash" → 匹配 Gemini x.x Flash）

Step 4: 全部不可用 → 使用 defaultModel

Step 5: 连 defaultModel 也不确定 → 询问用户
```

---

## 安全 vs 危险的模型替换

**安全**（同性格家族内替换）：
- 芒格 / 德明 / 德鲁克：Claude Opus → Claude Sonnet → Kimi → GLM
- 费曼降级到 Claude：可以，但需要补偿（message 里写更详细的步骤）

**危险**（跨性格家族，会导致行为偏移）：
- 费曼 → Claude Haiku：Haiku 太轻量，无法胜任复杂多文件推理
- 快速任务 → Claude Opus：大材小用，速度慢、成本高、没有额外收益
- 主 Agent（编排者）→ 早期 GPT 版本：编排者需要沟通型模型，旧版 GPT 不适合

---

## 只有一个模型时

直接用，不需要 Fallback Chain 逻辑。告知用户但不阻塞工作：

```
当前只有 [model] 可用，我会用它处理所有任务。
建议后续配置多模型以获得更好的效果。
```

---

**版本：** 5.0.0  
**参考：** [oh-my-openagent agent-model-matching](https://github.com/code-yeongyu/oh-my-openagent/blob/dev/docs/guide/agent-model-matching.md)  
**最后更新：** 2026-03-17
