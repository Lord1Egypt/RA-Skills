# learn-x

<p align="left">
  <a href="./README.md"><b>简体中文</b></a> ·
  <a href="./README-en.md">English</a>
</p>

<p align="left">
  <a href="https://github.com/dimayip/learn-x/stargazers"><img src="https://img.shields.io/github/stars/dimayip/learn-x?style=flat-square" alt="Stars"></a>
  <a href="https://github.com/dimayip/learn-x/network/members"><img src="https://img.shields.io/github/forks/dimayip/learn-x?style=flat-square" alt="Forks"></a>
  <a href="https://github.com/dimayip/learn-x/issues"><img src="https://img.shields.io/github/issues/dimayip/learn-x?style=flat-square" alt="Issues"></a>
  <a href="./LICENSE"><img src="https://img.shields.io/github/license/dimayip/learn-x?style=flat-square" alt="License"></a>
</p>

> **一个 Socratic 式的学习引导 skill——把"我想学 X"变成可操作的理解，并且每次会话都留下一个你可以带走的成果物。**

`learn-x` 是一套**领域无关**的教练框架，让 AI 助手不再"讲课"，而是先诊断你的真实起点，再一次只引入一个概念，用结构化选择题代替开放提问，并以**你自己产出的东西**结束每一次会话。

无论 X 是一门编程语言、一个数学概念、一个设计模式、一个工具、一个框架、一个领域，还是一项软技能，都适用。

---

## 它解决什么问题

绝大多数学习失败，**不是因为讲得不够，而是因为讲得太多、太快**。在你的大脑还没把新概念接入已有心智模型之前，下一段解释已经压上来了——你一边点头一边遗忘，48 小时内几乎完全失效。

直接让 AI"教我 X"通常踩中这套失败模式：一段话把所有重点说完，听起来很懂，但一合上窗口什么都不剩。

`learn-x` 用一个视角转换来应对：

> **学习者掌舵（负责把事情想明白）。教练执行（只问，不讲）。**

这一行不是口号，是 skill 里所有规则的根。每条提问模板、每个工作流步骤，都是为了让你的大脑**保持主动**而不是被动接收。

---

## 核心理念：每轮对话同时激活 4 层

这是 `learn-x` 区别于"普通 AI 教学"最关键的一点：**任何一轮对话，AI 都必须同时激活下面 4 层**。只问问题（L3）却不锚定目标（L1）、不产出任何东西（L4）的对话，会让会话逐渐漂移成闲聊。

| 层 | 作用 | 当轮示例 |
|----|------|--------|
| **L1 · 锚点（Anchor）** | 把当前动作连回学习者声明的目标 | *"别忘了你说下个月要做出 X，这个概念就是为这件事服务的。"* |
| **L2 · 纪律（Discipline）** | 控制节奏：诊断先行、单概念、lock-in、魔鬼代言人 | *"先别急着看我解释——你**以为**它是干嘛的？"* |
| **L3 · 战术（Tactics）** | Socratic 动作：prime / hypothesize / verify / apply / reflect / challenge | *"A / B / C 选一个——哪个更符合你的直觉？"* |
| **L4 · 产物（Artifact）** | 每几轮就要产出一件具体的东西 | *"用你自己的话写一个 5 行版本。"* |

只有 L3 = 漂移；只有 L1+L4 = 灌输。**4 项缺一不可。**

---

## 5 条硬纪律

| # | 规则 | 一句话理由 |
|---|------|----------|
| 1 | **先诊断，再教学。** 第 1 轮只问目的、先前印象、相邻知识。 | 不知道学习者站在哪里就开讲，是切线方向的高质量教学——越认真越离题。 |
| 2 | **每轮只引入一个新概念。** 多出来的进队列。 | 工作记忆一次只能消化少量新条目；堆叠会让前一个还没生根就被冲走。 |
| 3 | **结构化选择优先于开放提问。** 用 A/B/C/D 替代"你会怎么做"。 | 让学习者先猜，大脑会进入预测状态；正确答案揭示时，"咬合感"远超直接被告知。 |
| 4 | **每 ~3 轮做一次 lock-in 回顾。** 显式复盘已锁住的 + 下一步。 | 复述本身就是检索练习，是最便宜的留存放大器。 |
| 5 | **答对之后必魔鬼代言人。** 翻转一个假设、推一个边界。 | 答对很便宜，深度才贵。停在"答对了"会留下脆弱的表层认知。 |

每条规则的执行细节见 [`SKILL.md`](./SKILL.md)。

---

## 它和普通 AI 教学的差别

| 普通 AI 教学（默认动作） | `learn-x` 引导下的对话 |
|----------------|-----------------|
| 一上来就解释概念，整段输出 | 第 1 轮**完全不教**，先问 4 个诊断问题 |
| "你会怎么做？" 等开放问题 | "A / B / C 选一个，为什么？" + 永远留一个 D（自己的答案） |
| "你好聪明！棒极了！" 空洞表扬 | 只给具体反馈："对了，而且你还捕捉到了 X，我没提示" |
| 一轮塞 3–5 个新名词 | 一轮 ≤ 1 个新概念，其余排队 |
| 学习者求"直接告诉我就好" 就照办 | "先猜一秒钟，deal？"——不让步 |
| 结尾"我们今天覆盖了很多！" | 结尾必须有一个**学习者自己产出的东西**：demo / cheat sheet / mindmap / flashcards / teach-back |

如果你以前用 AI 学东西总觉得"听懂了但记不住"，多半是踩中了左列的默认模式。

---

## 教学法依据（为什么这样设计有效）

skill 里的硬规则不是拍脑袋写的，是把三条认知科学根因压成可执行规则：

- **认知负荷理论**——工作记忆容量很小，新概念必须**单个进入并扎根**才能搬入长期记忆。规则 2 的根。
- **Retrieval practice / 主动回想**——你说出来、写下来、预测一次，比你听 10 遍更能形成留存。规则 3、4、L4 的根。
- **Productive failure**——让大脑先尝试并失败一次，再揭示答案，比直接给答案产生更深的理解。规则 3 的"先猜再揭示"和规则 5 的根。

换句话说：`learn-x` 不是"另一种讲法"，而是把学习的认知工作**强制还给学习者**——因为只有你的大脑才能完成它。

---

## 何时使用

✅ **适合触发本 skill 的请求：**

- "教我 X" / "帮我学 Y" / "我想搞懂 Z" / "带我入门 ..."
- "help me learn / understand / get good at ..."
- "能不能带我过一遍 ...?"
- "我一直没搞清楚 ..."

尤其有效：

- 主题复杂、多层次
- 学习者起点不清楚
- 之前"看看文档就懂了"没能奏效

❌ **不适合的场景**（应该路由到其他 skill）：

- 纯事实查询（"Python 是哪年发布的？"）
- 让 Agent 直接代劳（写代码、修 bug、生成文档）

---

## 4 阶段工作流

```
阶段 1 — Onboarding           阶段 2 — 路径提案
（先诊断，不教）       ──►   （3–7 个里程碑，学习者确认）
                                         │
                                         ▼
阶段 4 — 产物            阶段 3 — 里程碑循环
（demo / cheat sheet /  ◄──  （prime → hypothesize → reveal → verify
 mindmap / flashcards ...）    → challenge；每 3 轮 lock-in）
```

- **阶段 1 — Onboarding。** 用 [`references/diagnose-playbook.md`](./references/diagnose-playbook.md) 的 4 个诊断问题起手（一次只问一个）。**此时不教任何东西**，即使学习者的先前认知是错的——记下，留待后续在语境中处理。
- **阶段 2 — 路径提案。** 基于诊断给出 3–7 个有序里程碑，让学习者确认或替换。这一步的目的是让学习者**和你共同拥有计划**。
- **阶段 3 — 里程碑循环。** 每个里程碑走 6 步微循环：*prime → hypothesize → reveal + 微任务 → verify → challenge*，每 ~3 轮做一次 lock-in。
- **阶段 4 — 产物。** 每次会话以学习者产出的有形东西作为结束。**没有产物的会话几乎等于没学。**

---

## 校准旋钮

框架是去适配学习者的，不是反过来：

| 情况 | 调整 |
|------|------|
| 完全零基础 | 更多 prime、更小粒度、更多复述、更早产物 |
| 有相邻领域经验 | 跳过基础，加大 challenge，节奏放快 |
| 学习者说"直接告诉我就好" | 讨价还价："先猜一秒钟，deal？" |
| 学习者沉默 | 抽象度降一级，或者举一个具体例子 |
| 学习者跟你的答案争论 | 鼓励它——认真对待，他可能是对的 |
| 时间盒 ≤ 30 分钟 | 压到 1 个里程碑；最后 10% 时间永远留给产物 |

---

## 仓库结构

```
learn-x/
├── SKILL.md                               # AI 执行手册——角色、4 层、5 条硬纪律、4 阶段工作流
├── README.md                              # （本文件）面向人类的中文总览
├── README-en.md                           # 面向人类的英文总览
└── references/
    ├── diagnose-playbook.md               # 阶段 1 开场：4 问脚本 + 听答→做动作判定表
    ├── question-templates.md              # 6 类 Socratic 模板（prime / hypothesize / verify / apply / reflect / challenge）
    └── session-patterns.md                # 5 种学习类型（概念 / 工具 / 技能 / 判断 / 思维习惯）的会话形状
```

文件职责互不重叠：开场脚本只在 diagnose 中、提问措辞只在 templates 中、会话形状只在 patterns 中。

- **[`SKILL.md`](./SKILL.md)** — AI agent 真正加载执行的规范文件。想用或想移植本 skill 从这里入手。
- **[`references/diagnose-playbook.md`](./references/diagnose-playbook.md)** — 会话前 3–10 分钟的脚本化开场 + 需要倾听的信号。
- **[`references/question-templates.md`](./references/question-templates.md)** — 每个 Socratic 动作的可复用措辞库。
- **[`references/session-patterns.md`](./references/session-patterns.md)** — 概念学习 vs. 工具上手 vs. 技能构建 vs. 判断训练 vs. 思维习惯，分别该怎么排会话。

---

## 安装

通过 [skills.sh](https://skills.sh) 安装（支持 Claude Code / Cursor / Codex / CodeBuddy / OpenCode 等 [50+ 种 agent](https://github.com/vercel-labs/skills#supported-agents)）：

```bash
# 全局安装 — 所有项目共享
npx skills add dimayip/learn-x -g -a claude-code

# 项目级安装 — 随仓库提交
npx skills add dimayip/learn-x -a codebuddy

# 其他 agent：-a 后面换成 cursor / codex / opencode 等
```

或手动 clone 到 agent 的 skills 目录：

```bash
# Claude Code（全局）
git clone https://github.com/dimayip/learn-x ~/.claude/skills/learn-x

# CodeBuddy（项目级）
git clone https://github.com/dimayip/learn-x .codebuddy/skills/learn-x
```

兼容 [Agent Skills Specification](https://agentskills.io)。

---

## 如何使用

**作为 AI agent 用户：**

1. 把整个目录放到平台的 skills 文件夹下（例如 `.codebuddy/skills/learn-x/`）；
2. 当你的请求匹配 skill 描述（学习、教练、"教我 X" 等）时，agent 会自动加载 `SKILL.md`；
3. `references/` 下的文件**按需加载**——agent 只在当前对话真正需要详细脚本、问题措辞或特定场景指引时才读。

**作为人类引导者：** 完整读一遍 `SKILL.md` 把 5 条硬纪律内化，会话时把三份 reference 文件开在旁边随时查。

---

## 给想 fork 或改造本 skill 的人

- **领域无关优先。** 核心规范里的每一条都必须能对任何 X 适用。主题相关的微调只能放在 `references/session-patterns.md` 里，不能污染主规则。
- **规则优于建议。** 5 条硬纪律是**难以绕过**的硬规则。软建议会在压力下被忽略；硬规则会幸存。
- **Reference 按需加载。** `SKILL.md` 保持精简，让 agent 能便宜地持有；更深的材料按轮次 opt-in。
- **没有产物 = 没学。** 整套框架以**留存**为优化目标，而留存最高杠杆的一招是**产出可带走的东西**。

---

## License

除非单独文件另有说明，本仓库内容遵循 MIT License。详见 [`LICENSE`](./LICENSE)。

---

## Credits

由 [@dimayip](https://github.com/dimayip) 设计并维护。融合了 Socratic 教学、认知负荷理论、retrieval practice 以及 "harness engineering" 中"掌舵/执行分离"的思路——压缩成一套**在真实会话里跑得动**的硬规则集。
