# 产品评审团 / Product Review Panel

> 召唤多位产品大师组成评审团，对你的 PRD 给出严格的 GO / NO-GO / CONDITIONAL GO 结论，并完整保留反对意见。
>
> Convene a multi-expert panel that delivers a definitive verdict on your PRD — with dissenting opinions preserved as first-class output.

一个用于 Claude Code / Cowork mode 的 skill。
A skill for Claude Code / Cowork mode.

---

## 📖 这是什么 / What this is

**中文**

当产品经理需要严肃评审自己的 PRD 时，这个 skill 会召唤一个由真实产品大师（Marty Cagan、俞军、Clayton Christensen 等）+ 虚构角色（大厂 P9 产品总监 + 魔鬼裁判 The Closer）组成的评审团，按结构化流程跑完一轮评审，并**强制给出可执行的最终结论**。

**English**

When a Product Manager needs critical review of a PRD, this skill convenes a panel of real product thinkers (Marty Cagan, Clayton Christensen, Reid Hoffman, etc.) plus fictional archetypes (Senior PM Director + The Closer). It runs a structured review process and **forces a definitive, actionable verdict** — no "it depends," no "think more about it."

---

## 🎯 为什么不一样 / What makes it different

Most "expert panel" prompts are theater — famous names saying generic things. This skill is built around three structural choices that make it actually useful:

| Design choice | Why it matters |
|---|---|
| **Frameworks over personas / 框架重于人物** | Each expert is anchored to their *actual* public framework (Cagan's 4 risks, JTBD, 俞军的用户价值公式), not their writing voice. The output is grounded in real decision tools, not impressions. |
| **Verdict-or-die / 必须出结论** | The Closer (魔鬼裁判) is a strict moderator who forces every review to end with one of three answers: GO / NO-GO / CONDITIONAL GO. Reality is messy, but verdicts cannot be. |
| **Dissent as a first-class output / 反对意见独立成章** | Like a Supreme Court ruling, dissents are preserved with author, strongest argument, and **observable failure signals**. Six months later, if the project starts failing, the PM can check whether the dissenters were right. |

---

## 🎤 评审团成员 / Panel members

The panel automatically switches based on the user's conversation language.

### 🇨🇳 中文面板 / Chinese panel

| 角色 / Role | 类型 / Type | 框架 / Framework |
|---|---|---|
| **Marty Cagan** | 核心 | 产品四大风险（价值/可用/可行/商业可行） |
| **俞军** | 核心 | 用户价值 = 新体验 - 旧体验 - 替换成本 |
| **大厂 P9 产品总监** | 核心（虚构） | 经验性反对 / 历史失败案例匹配 |
| **张小龙** | 情境（C 端 / 体验重构） | 克制设计 / 用完即走 |
| **Steve Jobs** | 情境（消费品 / 产品身份） | 聚焦即说不 / 一句话测试 |
| **张一鸣** | 情境（内容 / 推荐 / 出海） | 底层投影 / 数据飞轮 |
| **马斯克** | 情境（成本 / 基建 / 流程） | 白痴指数 / 五步算法 |
| **The Closer 魔鬼裁判** | 终审（虚构） | 强制收敛 + 翻车前兆信号 |

### 🌐 International panel

| Expert | Type | Framework |
|---|---|---|
| **Marty Cagan** | Core | The Four Big Risks |
| **Clayton Christensen** | Core | Jobs to Be Done |
| **Senior PM Director** | Core (fictional) | Experiential opposition |
| **Don Norman** | Situational (UX redesign) | Affordances, mental models |
| **Steve Jobs** | Situational (consumer / simplification) | Focus = saying no, one-liner test |
| **Reid Hoffman** | Situational (pricing / business model) | Network effects, blitzscaling |
| **Teresa Torres** | Situational (iteration) | Opportunity-solution tree |
| **Elon Musk** | Situational (platform / cost / infra) | Idiot index, five-step algorithm |
| **The Closer** | Final arbiter (fictional) | Forced convergence + failure signals |

---

## 🔁 评审流程 / Review flow

```
0. Disclaimer                         (always shown — non-negotiable)
1. P9 intake interrogation            — pushes PM for missing info, max 5 turns
2. PRD classification                 — determines situational expert(s)
3. Panel intro card                   — credentials + frameworks + signature questions
4. Round 1: parallel reviews          — each expert: tendency + ≤80-word rationale + 追问
5. Tendency direction check           — split → Round 2 / unanimous → skip to 7
6. Round 2: pointed debate            — strongest GO vs strongest NO-GO, one exchange
7. The Closer: final verdict          — GO / NO-GO / CONDITIONAL GO + conditions + failure signals
8. Dissent section                    — minority view + observable failure signals
```

---

## 📋 一个真实输出片段 / Sample output excerpt

Snippet from the Chinese feature-review example (full version in `references/examples/example-cn-feature-review.md`):

```
P9: 你写"提升用户活跃度"。哪个活跃度？DAU？下单频次？给一个数字。

PM: 主要看周下单频次。当前 2.3 次/周，目标 2.8 次/周。

P9: 好。下一个。
[...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【The Closer · 终审】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

我数了一下：0 票 GO，3 票 NO-GO，1 票 CONDITIONAL。

俞军算了用户价值公式 — 净值接近零。P9 总监指出"美团 2020 年
做过类似的，留存数据并不好看"。张小龙提出"用户没说他需要被
推荐，是产品需要 KPI"。三个独立角度，同一个结论。

P9 的审讯记录显示，PM 跳过了 kill criteria 这一项。

结论：NO-GO

如果以下信号出现，可以重启评估：
  • 至少 5 次目标用户访谈，≥ 3 人主动提到"每天选择午餐很
    痛苦，希望有人帮我选"
  • A/B 实验中"每周推荐"模块的 CTR ≥ "历史订单"模块的 1.5 倍
  • 美团/饿了么近期推出了类似功能且 D30 留存高于基线

完。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

完整示例见 `references/examples/` 目录。
Full examples are in the `references/examples/` directory.

---

## 📂 文件结构 / File structure

```
product-review-panel-skill/                  ← Git repo root (this folder)
├── README.md                                # 本文件 / This file
├── LICENSE                                  # MIT
├── .gitignore
└── product-review-panel/                    ← the skill itself
    ├── SKILL.md                             # 主入口 / Main orchestration
    └── references/                          # 按需加载文档 / On-demand docs
        ├── personas/                        # 角色定义 / Character definitions
        │   ├── p9-director.md               # 大厂 P9 / Senior PM Director
        │   ├── closer.md                    # The Closer / 魔鬼裁判
        │   ├── experts-cn.md                # 中文专家面板
        │   └── experts-intl.md              # International expert panel
        ├── templates/                       # 输出模板 / Output templates
        │   ├── disclaimer.md                # 免责声明 / Disclaimer
        │   ├── panel-intro-card.md          # 出场卡 / Panel intro card
        │   ├── intake-dialogue.md           # 审讯对话 / Intake dialogue
        │   └── output-structure.md          # 完整输出骨架 / Output skeleton
        ├── workflows/                       # 流程逻辑 / Decision logic
        │   ├── prd-classification.md        # PRD 分类
        │   ├── information-gap-check.md     # 信息缺口
        │   └── verdict-logic.md             # 终审决策树
        └── examples/                        # 端到端示例 / End-to-end examples
            ├── example-cn-feature-review.md
            └── example-intl-pricing-review.md
```

---

## 🚀 安装 / Installation

### Cowork mode

1. Copy this entire `product-review-panel/` folder into your skills directory
2. The skill will automatically be discovered the next time Claude starts a Cowork session
3. Trigger it by asking "评审我的 PRD" / "review my PRD" / "panel review my proposal" — the description in `SKILL.md` will route the request

### Claude Code

1. Copy `product-review-panel/` into `~/.claude/skills/` (per-user) or your project's `.claude/skills/` (per-project)
2. Invoke from Claude Code by mentioning the skill or letting Claude auto-route

### As a `.skill` bundle

To package and share:

```bash
cd product-review-panel
zip -r ../product-review-panel.skill .
```

Then `product-review-panel.skill` can be installed via Cowork's plugin / skill install flow.

---

## 🎨 使用建议 / Usage tips

**中文**

- **直接给 skill 一份完整 PRD**，让它把整个流程跑完。中途不要打断 P9 的审讯，让他问完。
- 如果 P9 问到你跳过了的字段，**老实跳过**——这本身就是数据，会被 The Closer 记录并影响最终置信度。
- **特别关注"翻车前兆信号"那一段**——它是整个 skill 的最高价值输出，比结论本身更值得保存。
- 同一份 PRD 可以多次跑评审。每次 PRD 完善一些（比如补了用户访谈数据），结论会变得更锐利。

**English**

- **Hand the skill your full PRD** and let the process run end-to-end. Don't interrupt P9 / Senior PM Director's interrogation.
- If asked about a field you haven't thought through, **honestly skip it** — that's data too, and The Closer will use it to weight the final verdict.
- **Pay special attention to the "failure signals" section** — it's the single highest-value output of the skill, more important than the verdict itself.
- Re-run the review as the PRD evolves. Each iteration sharpens the verdict.

---

## 🛠 自定义 / Customization

想加入你自己崇拜或害怕的产品大师？想替换 P9 的语气？想增加新的 PRD 类型？

Want to add a product thinker you admire? Want to change P9's voice? Want to support a new PRD type?

| 想做什么 / What to change | 改哪个文件 / Which file |
|---|---|
| 加 / 减 / 替换专家 | `references/personas/experts-cn.md` 或 `references/personas/experts-intl.md` |
| 调整 P9 或 The Closer 的语气 | `references/personas/p9-director.md` 或 `references/personas/closer.md` |
| 改变最终输出格式 | `references/templates/output-structure.md` |
| 增加 PRD 类型 | `references/workflows/prd-classification.md` |
| 改变信息缺口检测规则 | `references/workflows/information-gap-check.md` |
| 改变终审决策逻辑 | `references/workflows/verdict-logic.md` |

Each file is self-contained — you can edit one without touching others.

---

## 🗺 路线图 / Roadmap

- [x] **v1**: PRD review (the case where a PM already has a written PRD)
- [ ] **v2**: Early-stage exploration (the case where the PM has only an idea, no PRD yet) — different panel composition, different discussion depth, more JTBD-heavy
- [ ] **v2+**: 中文面板的商业模式 / 定价情境专家 — 目前是 gap
- [ ] **v2+**: Sub-agent parallelization for Round 1 (currently single-threaded; parallel would improve opinion diversity)

---

## ⚠️ 免责声明 / Disclaimer

**中文**

本 skill 中所有"专家观点"均为基于其公开方法论和决策框架的演绎应用，**不代表本人对您具体方案的真实意见**。其中"大厂 P9 产品总监"和"The Closer 魔鬼裁判"为完全虚构角色，与任何真实人物无关。

请将专家视角作为思维工具，而非权威背书。如果您计划在公开场合引用本 skill 的输出，请明确标注其为 AI 推演结果。

**English**

The expert perspectives produced by this skill are interpretive applications of public frameworks — **not the individuals' actual opinions** on any specific proposal. "Senior PM Director" and "The Closer" are fully fictional archetypes with no real-life counterpart.

Treat these perspectives as thinking tools, not authoritative endorsements. If you plan to cite this skill's output publicly, please clearly mark it as AI-generated interpretation.

---

## 📄 License

MIT License — see [LICENSE](./LICENSE) for full text.

简言之：你可以自由使用、修改、分发、商用本 skill。唯一要求是保留原始版权声明。
TL;DR: free to use, modify, distribute, including commercially. Just keep the copyright notice.

---

<sub>Built as a Claude skill. Designed to be edited.</sub>
<sub>用 Claude skill 构建。欢迎根据你的实际需要修改。</sub>
