# How to Harness

<p align="left">
  <a href="./README.md"><b>简体中文</b></a> ·
  <a href="./README-en.md">English</a>
</p>

<p align="left">
  <a href="https://github.com/dimayip/how-to-harness/stargazers"><img src="https://img.shields.io/github/stars/dimayip/how-to-harness?style=flat-square" alt="Stars"></a>
  <a href="https://github.com/dimayip/how-to-harness/network/members"><img src="https://img.shields.io/github/forks/dimayip/how-to-harness?style=flat-square" alt="Forks"></a>
  <a href="https://github.com/dimayip/how-to-harness/issues"><img src="https://img.shields.io/github/issues/dimayip/how-to-harness?style=flat-square" alt="Issues"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/github/license/dimayip/how-to-harness?style=flat-square" alt="License"></a>
</p>

> **一个专门用来设计 Harness-style 闭环 / 自优化 / 人类掌舵-Agent 执行系统的 facilitation skill——把"我想做一个 AI 闭环"变成对齐 7 条 Harness 原则的可落地方案。**

`how-to-harness` 把 OpenAI 的 [Harness Engineering](https://openai.com/index/harness-engineering/) 方法论——**"Humans steer, agents execute"**——落实为一套**可以在真实对话里跑起来**的引导规则集。它在常规的 Socratic facilitation 之上额外叠加一层**硬性领域约束**（Layer 0 · 7 条 Harness Principles），确保每一个锁定的决策都对齐 Harness 方法论的核心原则。

无论你想做的是 Agent loop、Ralph loop、CI 式评测循环，还是一套需要分级自动化与人类闸门的治理系统，本 skill 都帮你**先把约束摆好**，再开始问。

---

## 它解决什么问题

Harness-style 系统的设计失败，**绝大多数不是"问得不够多"，而是"问得没问在点子上"**——决策往往在违反 Harness 原则的位置就被仓促锁死，等三个月后跑起来才发现拐点根本不在那里。常见塌方：

| 用户原话 | 几个月后的代价 | 违反原则 |
|---|---|---|
| "我们这个闭环暂时没评测集，先上线再说" | 改了一堆，但没人能说清是好是坏 | HP-1 |
| "管理者会亲自下场改 Prompt" | 管理者成了瓶颈，系统越大越慢 | HP-2 |
| "每次跑结果不一样也行" | 不可复现 / 不可调试 / 不可回滚 | HP-3 |
| "改进了就直接上线，没观察期" | 一次失败炸掉整条产线 | HP-4 |
| "要么全自动要么全人工" | 没有分级、没有升级路径 | HP-5 |
| "资产存在个人电脑上" | 三个月后没人知道是谁改了什么 | HP-6 |
| "人不够就加班" | 隐性成本炸锅，团队耗散 | HP-7 |

直接让 AI"帮我设计一个自优化系统"通常踩中这套失败模式：方案听起来漂亮，但真正能拦住塌方的硬约束被 AI 客气地放过去了。

`how-to-harness` 的设计只围绕一个视角转换：

> **设计者掌舵（拥有所有决策），Agent 执行（只问、只对照、只组织）——并且 Agent 必须以 7 条 Harness 原则为尺子，拒绝违反领域硬约束的决策。**

这一行不是口号，是 skill 里所有规则的根。

---

## 核心理念：Layer 0 是这个 skill 的灵魂

普通的设计引导 skill 只做"让你问得清楚"。`how-to-harness` 在它之上加了一层**领域硬约束**——Layer 0 的 7 条 Harness Principles。

```
Layer 0: Harness Principles（领域硬约束，不可协商）  ← 这个 skill 的灵魂
   ↓
Layer 1: Capture Context —— 锚点 + 业务现状 + 产物消费者
   ↓
Layer 2: Brainstorming 纪律（已内化）—— 6 条硬纪律约束节奏
   ↓
Layer 3: Socratic 追问 —— A/B/C/D 候选 + 依赖拓扑 + 4 项一致性校验
   ↓
Layer 4: 产物组织 —— 按消费者选 schema，把锁定的决策摆进去
```

**只有 Layer 1–4 = 普通 brainstorming**，问得很顺但容易锁错地方。
**只有 Layer 0 = 一堆教条**，没有问答节奏没法落地。
**5 层叠加 = 把"问得好"和"以领域为尺子"结合起来。**

---

## 7 条 Harness Principles（Layer 0 硬约束）

| # | 原则 | 一句话理解 | 为什么这是硬约束 |
|---|------|-----------|---------------|
| **HP-1** | Eval is foundation | 任何改进循环先建 Gold Set，没评测不能自动改 | 没有评测的循环只是"以为在改进"——好坏分不出，方向感全靠错觉 |
| **HP-2** | Humans steer via gates, not via code | 人类定义/审批/调整闸门，不亲自下场改代码 | 让人下场写代码，人就成了瓶颈；人定义闸门，系统才能扩 |
| **HP-3** | Loops must be idempotent & resumable | 每一步重跑结果一致，中途中断可从断点恢复 | 不幂等的循环 = 不可复现 = 不可调试 = 不可回滚 |
| **HP-4** | Small, reversible steps | 改动小 · 有观察期 · 失败可自动回滚 | 大爆炸式上线在自优化系统里是双倍危险——你都不知道是哪一步出问题 |
| **HP-5** | Automation tiers with clear escalation | 自动化分 L1/L2/L3 档，每档有清晰边界和升级条件 | 0/1 开关式自动化必然会被滥用——要么过度依赖，要么彻底关掉 |
| **HP-6** | Asset versioning | 演化资产必须版本化，任一版本可单独回滚 | 演化资产没版本化 = 三个月后没人能回答"是谁改的、为什么改" |
| **HP-7** | Human time budget is a first-class constraint | 人类投入时间是预先设定的预算，不是事后算账 | 默认"人不够就加班"等于把成本藏到了团队疲劳里——直到团队耗散 |

每条规则的执行细节、必问问题、红线信号见 [`SKILL.md`](./SKILL.md) 和 [`references/decision-checklists.md`](./references/decision-checklists.md)。

---

## 它和普通 AI 设计引导的差别

| 普通 AI 设计引导（默认动作） | `how-to-harness` 引导下的对话 |
|----------------|-----------------|
| 一上来就开始画架构图 | 第 1 轮**完全不画**，先做 Layer 0 验收 7 问 |
| 问"你需要 Gold Set 吗？" | "Gold Set 必须有（HP-1）。它从哪来——A. 人工标注 / B. 规则提名 / C. 历史样本？我建议..." |
| 接受"管理者会自己改 Prompt" | 当场指出违反 HP-2，建议改为"管理者只调闸门" |
| 接受"改完直接上线就行" | 当场指出违反 HP-4，要求定观察期 + 回滚条件 |
| 默认产物是 PRD | 先问消费者是谁，再决定 PRD / Design Doc / RFC / Kickoff / ADR / One-Pager |
| 一轮问 5 个维度 | 每轮只问 1 个维度，按依赖拓扑严格排序 |
| 用开放式问题"你希望怎么设计？" | 用 A/B/C/D 候选 + 推荐 + 理由 |
| 接受用户决策后立即写文档 | 每轮做 4 项一致性校验，特别是对 HP-1~HP-7 的检查 |
| "OK 我帮你写好了！" 一次性甩方案 | 分节呈现，逐节 Approve；每 3 轮做一次决策锁定回顾 |
| 系统名 / 仓库名 AI 自己起 | 给 2-3 个候选让用户选 |

如果你之前用 AI 设计过自优化 / Agent loop 系统，最后跑起来发现"评测一直没补上"、"管理者陷在 Prompt 调优里"、"自动改进不可回滚"——多半就是踩中了左列的默认模式。

---

## 设计依据（为什么这样设计有效）

7 条原则不是凭空发明，是把多源工程经验压成可执行的硬约束：

- **OpenAI Harness Engineering 方法论**——"humans steer, agents execute" 的核心思想，HP-2 / HP-5 / HP-7 都直接源自它。
- **CI / CD 与 Site Reliability 工程实践**——可观察性、灰度、可回滚、断点续传是大型系统能扩的根本。HP-3 / HP-4 / HP-6 的来源。
- **机器学习评测工程**——没有 Gold Set 的"持续改进"在 ML 领域早就被反复证明是错觉。HP-1 的来源。
- **Socratic facilitation + 认知负荷管理**——A/B/C/D 候选、依赖拓扑、每轮一维、分节 Approve 这些纪律来自 brainstorming 领域的成熟实践，避免"问太多太散"导致用户随便选。Layer 2 / Layer 3 的来源。

换句话说：`how-to-harness` 不是"另一种设计引导风格"，而是把闭环 / 自优化系统在工程实践中已经被反复验证的硬约束，**强制还给设计者**——因为只有设计者本人能在闸门、预算、粒度这些维度上做最终决定，但 Agent 必须先把这些约束摆到桌面上。

---

## 何时使用

✅ **适合触发本 skill 的场景**：

- 系统存在**闭环 / 自优化**结构（Agent loop / Ralph loop / CI 式评测循环 / 周期性自改进）
- 系统存在明确的**人机协作闸门**（分级自动化 L1/L2/L3、谁审批什么、什么情况升级到人）
- 系统以**评测驱动**（Gold Set、回归测试、LLM-as-judge、硬门禁 / 软评估）
- 用户明确提到 Harness Engineering / Ralph loop / LLM-as-judge / gatekeeper / 闭环 / 自治 / agent autonomy / 熔断升级路径

**判定钥匙**：问一个关键问题——"这个系统会不会**自己执行自己改进自己**？" 答案不是"会"，本 skill 不适用。

❌ **不适合的场景**（应该路由到其他 skill 或直接动笔）：

- 普通产品功能 / 内部工具 / 平台改造 / API / 数据模型 / 工作流
- 一次性的对话 / 问答功能
- 已经想清楚的纯 CRUD 需求文档

---

## 最终产物不是"PRD"一种

本 skill 的输出**按真实消费者选择**，不是固定格式：

| 场景 | 建议产物 | 主要消费者 |
|------|----------|-----------|
| 从 0 到 1 设计新系统（工程为主） | **Design Doc + Kickoff 清单** | 开发者 + AI coding agent |
| 产品立项 / 对上汇报 | **PRD + One-Pager** | 产品评审 + 管理层 |
| 内部技术改造 / 跨团队协作 | **RFC / 技术方案** | 工程团队 + 架构评审 |
| 需求仍在探索 / 决策未完全锁定 | **ADR + 待办问题清单** | 自己 + 后续推进 |
| 已有方案需落地 | **里程碑计划 + 分工表** | 执行团队 |

多种产物可以**并行交付**（例如 PRD + One-Pager + Kickoff 三件套，给不同受众看）。详细模板与选择决策树见 [`references/deliverables.md`](./references/deliverables.md)。

---

## 标准工作流

```
Step 0    识别是否需要本 skill（30 秒：系统会不会自己改自己？）
   │
   ▼
Step 0.5  Layer 0 硬约束验收（HP-1~HP-7 共 7 问，不过先扣住）
   │
   ▼
Step 1    Capture Context（第 1 轮：现状 + 锚点 + 产物形态 + 消费者，复述校验）
   │
   ▼
Step 2    Socratic 追问（N 轮，按依赖拓扑，每 3 轮决策锁定回顾，每轮 4 项一致性校验）
   │
   ▼
Step 3    方案分节呈现（2–5 节，每节结束问 "approve 还是调整？"）
   │
   ▼
Step 4    按选定 schema 组织产物（多产物并行交付 + 说明各自消费者）
   │
   ▼
Step 5    复盘（可选，强烈推荐）—— 诚实回答"用了什么框架、哪些 HP 扣住了用户"
```

完整执行细节（每一步的硬约束、必问问题、禁令）见 [`SKILL.md`](./SKILL.md)。

---

## 仓库结构

```
how-to-harness/
├── SKILL.md                               # AI 执行手册——5 层框架 + HP-1~HP-7 + 工作流 + 禁令
├── README.md                              # （本文件）面向人类的中文总览
├── README-en.md                           # 面向人类的英文总览
└── references/
    ├── decision-checklists.md             # Harness 类系统的硬性决策清单（每节对齐一条 HP）
    ├── deliverables.md                    # 6 类产物（PRD / Design Doc / RFC / Kickoff / ADR / One-Pager）模板与决策树
    └── ralph-case-study.md                # 真实案例：从"想做个 AI 循环"到 Ralph Harness 方案的 9 轮推导
```

文件职责互不重叠：执行步骤只在 SKILL 中、决策清单只在 decision-checklists 中、产物模板只在 deliverables 中、案例叙事只在 ralph-case-study 中。

- **[`SKILL.md`](./SKILL.md)** — AI agent 真正加载执行的规范文件。想用或想移植本 skill 从这里入手。
- **[`references/decision-checklists.md`](./references/decision-checklists.md)** — Socratic 追问阶段的硬性决策清单，每一节都对齐一条 HP（HP-1 评测 / HP-2 闸门 / HP-3 幂等 / HP-4 粒度 / HP-5 分档 / HP-6 版本 / HP-7 预算）。
- **[`references/deliverables.md`](./references/deliverables.md)** — 6 类产物的完整模板 + Capture 阶段的产物选择决策树。
- **[`references/ralph-case-study.md`](./references/ralph-case-study.md)** — 端到端案例：从用户一句"基于 Harness Engineering 给我的排障 AI Agent 做个自优化循环"开始，9 轮对话推出完整 Ralph Harness 方案。**最好的学习材料。**

---

## 自给自足原则

`how-to-harness` 内化了 Socratic brainstorming 纪律 + 6 类主流文档的 schema 知识 + 全部 7 条 Harness 硬约束，**不依赖其他 skill**。原因：

1. **完整方法论在一个 skill 内**便于传授、演化、复盘——你不需要先去学另一个 brainstorming skill 才能用这个。
2. **避免调度失败风险**——依赖的外部 skill 未命中触发条件，整条链就断了；`how-to-harness` 自包含意味着无论 agent 平台调度多么粗糙，核心方法论都不会丢。
3. **允许跨阶段引用**——Capture 阶段锁定的决策，Layer 4 书写阶段能直接使用，不丢上下文。

---

## 安装

通过 [skills.sh](https://skills.sh) 一键安装（支持 Claude Code / Cursor / Codex / CodeBuddy / OpenCode 等 50+ agent）：

```bash
# 全局安装（所有项目可用）
npx skills add dimayip/how-to-harness -g -a claude-code

# 项目级安装（跟随项目提交）
npx skills add dimayip/how-to-harness -a codebuddy
```

或手动把整个目录放到你的 agent skills 目录下，例如
`~/.claude/skills/how-to-harness/` 或 `.codebuddy/skills/how-to-harness/`。

兼容 [Agent Skills Specification](https://agentskills.io)。

---

## 如何使用

**作为 AI agent 用户：**

1. 用 `npx skills add dimayip/how-to-harness` 一键安装（见上），或手动把整个目录放到平台的 skills 文件夹下；
2. 当用户的请求明确涉及闭环 / 自优化 / Agent-loop / 评测驱动（提到 Harness Engineering / Ralph / LLM-as-judge / gatekeeper 等），agent 会加载本 skill 的 `SKILL.md`；
3. `references/` 下的文件**按需加载**——agent 只在当前对话真正需要决策清单、产物模板或参考案例时才读，让 `SKILL.md` 本身保持精简。

**作为人类引导者：** 完整读一遍 `SKILL.md` 把 Layer 0 的 HP-1~HP-7 内化为直觉，把三份 reference 文件在对话时开在旁边随时查。强烈建议先读 `references/ralph-case-study.md`——9 轮对话演示这套方法论怎么真的跑起来。

---

## 给想 fork 或改造本 skill 的人

- **领域硬约束优先。** Layer 0 的 7 条 HP 是这个 skill 的灵魂，改的时候**只增不减**。如果你要适配其他领域（比如安全审计、合规治理），新增对应的 HP 而不是稀释现有的。
- **规则优于建议。** HP-1~HP-7 是"硬约束"，不是"软建议"。软建议会在压力下被忽略；硬约束会幸存。措辞上保持"必须 / 不能 / 立即指出"这类不留余地的语言。
- **Reference 按需加载。** `SKILL.md` 保持精简，让 agent 能便宜地持有；更深的材料（决策清单、产物模板、案例）按轮次 opt-in。
- **决策的所有权永远归用户。** Agent 的职责是**问得对 + 以 HP 为尺子 + 在用户违反时诚实指出**——但永远不替用户决定。哪怕用户选择"我知道这违反 HP-3，但我接受"，那也是用户的知情决定，agent 要记录而不是反复劝阻。

---

## 元原则

> **本 skill 最重要的不是让 Agent 更会"问"，而是让 Agent 在问得好的基础上再多一层——以 Harness 原则为尺子，拒绝违反领域硬约束的决策。**
>
> "好问题 + 领域判据 = 好决策 = 好产物"（无论最后产出的是 PRD、RFC、Design Doc 还是别的）。
> 用户永远是决策的所有者，Agent 只是帮助用户把决策表达出来——并**在用户违反 Harness 原则时诚实指出**。

---

## ⭐ Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=dimayip/how-to-harness&type=Date)](https://star-history.com/#dimayip/how-to-harness&Date)

---

## License

除非单独文件另有说明，本仓库内容遵循 MIT License。详见 [`LICENSE`](./LICENSE)。

---

## Credits

由 [@dimayip](https://github.com/dimayip) 设计并维护。核心思想来自 OpenAI 的 [Harness Engineering](https://openai.com/index/harness-engineering/)，融合 CI/SRE 工程实践、ML 评测工程与 Socratic facilitation——压缩成一套**在真实对话里跑得动**的硬规则集，以 Layer 0 的 HP-1~HP-7 作为领域尺子，引导设计者锁定 Harness-style 闭环系统的每一个关键决策。
