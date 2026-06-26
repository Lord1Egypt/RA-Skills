# 输出格式规范（Output Format Specification）

完整生成 Introduction 时，默认产出**两个文件**：一份英文版、一份中文注释版。两者都是 Markdown 格式，保存在用户当前工作目录下。

如果用户只要求 inline 草稿、只要英文/中文、只要段落提纲、只要修改建议、或只要功能诊断，则按用户请求输出，不强制生成或保存双文件。

## 文件命名

- `introduction_en.md`  — 英文版（纯引言文本，可直接投稿）
- `introduction_zh.md`  — 中文版（含逐句、逐段功能注释，用于学习/审阅）

如果用户希望文件名带上论文标题，使用短横线连接的 slug 形式，如：
- `introduction_chitin-pla_en.md`
- `introduction_chitin-pla_zh.md`

若目标文件已存在且不是本次任务刚创建的文件，优先使用带标题 slug 或日期的文件名，避免覆盖用户已有稿件。

## 英文版格式（introduction_en.md）

```markdown
# Introduction — [Paper Title]

> **Field**: [Field / Discipline]
> **Template used**: [Template name, e.g., "Template 1: Materials Science"]
> **Generated**: [YYYY-MM-DD]
> **TL;DR**: [1-2 sentence summary of the paper's contribution]

---

## 1. Introduction

[Paragraph 1 — typically Component 1: importance + background + general problem area. 3-5 sentences.]

[Paragraph 2 — typically Component 2: literature and contributions review. 4-6 sentences. Use linking phrases from language-toolkit.md.]

[Paragraph 3 — typically Component 3: gap / problem / motivation. 2-4 sentences. Lead with However / Although / Despite.]

[Paragraph 4 — typically Component 4: describe present paper (aim, method, main result). 3-5 sentences. Include evidence-calibrated contribution markers.]

[(Optional) Paragraph 5 — extended result preview or paper organization, if appropriate for the field.]

---

## References (placeholders)

[REF: background fact]
[REF: prior approach]
[REF: closest competing method]
```

未提供真实引用时，使用语义化占位符（如 `[REF: biodegradable PLA review]`），不要生成看似真实的作者年份或期刊信息，除非用户明确说明这是允许虚构引用的课程练习。

## 中文注释版格式（introduction_zh.md）

```markdown
# 引言 — [论文题目中文]

> **领域**：[学科名]
> **所用模板**：[模板名称]
> **生成日期**：[YYYY-MM-DD]
> **一句话贡献**：[paper 的核心贡献]

> ⚠️ **阅读说明**：本文件供学习与审阅使用。每一段开头有【段落功能】行，说明该段在引言中所起的整体性作用；每一句后面紧跟 *（本句功能：...）* 的斜体注释，说明该句在引言结构中的**功能性角色**（function），而不是句子内容的翻译或概括。这种设计遵循 Glasman-Deal 《Science Research Writing》第 1 单元逆向工程方法论。

---

## 第一段

【段落功能】对应组件 [N]，段落在引言中的作用是 [建立重要性 / 综述研究地图 / 锁定 gap / 介绍本文] ...。本段共 [X] 句，整体构成引言"漏斗"的 [宽端 / 中部 / 窄端] 部分。

[句子 1 的中文]。*（本句功能：[S1 — 建立主题重要性 / S2 — 提供背景事实 / ...] — 具体说明此句如何运作，对应时态与信号词。）*

[句子 2 的中文]。*（本句功能：...）*

[句子 3 的中文]。*（本句功能：...）*

...

## 第二段

【段落功能】对应组件 [N] ...

[句子 1 的中文]。*（本句功能：...）*

...

## 第三段

【段落功能】对应组件 [N] — 锁定研究空白 ...

...

## 第四段

【段落功能】对应组件 [N] — 介绍本研究 ...

...

---

## 写作要点回顾（给读者的学习提示）

- 本引言遵循 **漏斗结构**（funnel shape）：从宽（组件 1）逐步收窄到本研究（组件 4）。
- 关键过渡词：**However / Although / Despite** 用于引出 gap。
- 贡献标记词（如 new, systematic, robust, significant, first demonstration）出现在 [段落 N] 的 [第 X 句]；强断言需有用户材料或真实引用支撑。
- 动词时态关键：
  - 重要性背景用 [Present Perfect]
  - 事实背景用 [Present Simple]
  - 前人研究用 [Past Simple]
  - 本文描述用 [Present Simple]

## 需要用户核查的事项

- [ ] 所有引用占位符需替换为真实引用
- [ ] 关键术语的中文译名是否与目标期刊一致
- [ ] 是否需要增加某个具体数据点（如效能提升的百分比）
- [ ] 是否符合目标期刊的段落数与字数规范
```

---

## 注释写作要点

### 【段落功能】的写法

- 必须明确对应到**四组件模型中的哪一个（或多个）**。
- 说明该段对整个引言的**贡献**，而不是内容概括。
- 1-2 句即可。示例：

> 【段落功能】对应组件 1 — 建立研究主题的重要性，提供必要的事实背景，并引出领域一般性问题。此段位于引言"漏斗"的最宽端，目的是让不同背景的读者能共同进入论文讨论。

### *（本句功能：...）* 的写法

- 描述"句子在做什么（what the sentence is DOING）"，不是"句子在说什么（what the sentence SAYS）"。
- 简洁明了，通常 1 句 20-60 字。
- 尽可能包含**时态说明**或**信号词说明**。
- 示例对比：

❌ **错误写法**（内容概括）：
> *（本句功能：介绍 PLA 是什么以及它的来源。）*

✅ **正确写法**（功能解释）：
> *（本句功能：S2 — 为读者提供 PLA 的基本事实背景；用一般现在时陈述已广泛接受的事实，避免跨学科读者被后续细节甩开。）*

❌ **错误写法**（翻译式）：
> *（本句功能：作者说这个研究很重要。）*

✅ **正确写法**：
> *（本句功能：S1 — 建立研究主题的重要性；用 "has received much attention in recent years" 的现在完成时结构把主题锚定为"当前热点"，为整个漏斗的宽端奠基。）*

### 句尾功能注释的风格

统一使用 Markdown 斜体 + 括号，整行附在句子后（同一段内），格式如下：

```markdown
[中文句子]。*（本句功能：...）*

[下一句中文]。*（本句功能：...）*
```

或者，若句子较长，可以换行：

```markdown
[中文句子]。
*（本句功能：...）*

[下一句中文]。
*（本句功能：...）*
```

---

## 特殊情况的处理

### 1. 用户没有指定目标期刊

- 默认用 "general science" 风格：可读性优先，术语解释充分。
- 在 zh 版末尾提示用户"若目标期刊风格更细分，请进一步调整术语密度与段落结构"。

### 2. 用户材料只有标题和一句话

- **不要强行生成完整稿**。先收集最小可生成输入（Topic / Title、Field、Gap / problem、Aim / approach、Main finding / contribution）。
- 若用户坚持，可生成一份**带更多 `[TO BE FILLED: ...]` 占位符**的版本，并在 zh 版开头清晰标注"此版为骨架稿，需要您补充细节"。

### 3. 用户希望生成简短版本（如 abstract-style intro）

- 采用**方案 B（3 段式）**。
- 仍然包含四组件，但每组件压缩为 1-2 句。
- 长度控制在 8-12 句。

### 4. 用户要求 §1.6 / Exercise 5 / 250-350 words 练习

- 采用 `templates.md` 的"模板 4B：工程 / 交通 / 设计短引言"或同等三段式结构。
- 若是 SPPPV / bicycle cover 题目，读取 `writing-practice.md` 和 `examples.md` 的样例 7。
- 如果练习题明确允许 fake references，可以创造 plausible references；但应在输出或汇报中说明它们是练习用占位，不是真实文献。
- 若用户要真实投稿稿件，则不要虚构引用，改用用户提供的引用或语义化占位符（如 `[REF: prior aerodynamic design]`）。

### 5. 用户提供多个候选标题

- 选择最具体的一个作为主标题，其他在文件开头 TL;DR 下列出作为 alternative titles。

### 6. 生成中英文的优先顺序

- 如果用户要求完整双语输出，**先生成英文版**，然后据此生成中文注释版。
- 中文注释版的结构必须与英文版**一一对应**：同样的段数、每段同样的句数。
- 中文不是对英文的直译——允许中文在句式上更符合中文阅读习惯，但**每个英文句子必须对应一个中文句子 + 一条功能注释**。
- 如果用户只要求单语版本、提纲、诊断或修改建议，不要为了满足默认格式而额外生成未请求的文件。

---

## 保存后的用户汇报

保存文件后，向用户以**简短总结**汇报，不要复述全文：

示例：
> 已完成。根据您的信息（[领域]、[主题]），使用[模板名]模板生成了引言：
>
> - `introduction_en.md`（英文版，[X] 段、[Y] 句）
> - `introduction_zh.md`（中文注释版，含逐句功能解释）
>
> 两个文件的四组件结构完整，gap 用 "[具体信号词]" 明确标出，贡献标记词使用在 [位置]。请核查引用占位符，并根据目标期刊风格微调。
