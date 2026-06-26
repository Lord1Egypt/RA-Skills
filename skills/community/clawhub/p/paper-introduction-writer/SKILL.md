---
name: paper-introduction-writer
description: 根据论文主题、背景、前人研究、gap、方法和结果，按 Glasman-Deal《Science Research Writing》的四组件/十一句式模型生成、修改或注释研究论文 Introduction；支持英文稿、中文功能注释、段落提纲、已有引言修改和 §1.6 的 250-350 词短引言练习。
---

# Paper Introduction Writer 论文引言生成器

## 技能用途 / Purpose

本技能基于 Hilary Glasman-Deal *Science Research Writing: A Fresh Approach* (2nd ed., 2020) 第 1 单元 "How to Write the Introduction" 的**逆向工程（reverse-engineering）方法论**，从公开发表的高水平研究文章中提炼出引言的**结构化写作模型**，用于辅助用户为自己的研究论文生成、修改、注释或规划规范、丰富的 Introduction 部分。

## 何时启用本技能

满足以下任一条件即应启用：

- 用户要求"写引言 / 写 introduction / 写前言部分 / draft the introduction"。
- 用户要求"根据我的研究主题/论文题目，生成论文的 introduction"。
- 用户提供了研究的主题、背景、前人工作、gap、方法、结果等信息，并希望整合成一段学术规范的引言。
- 用户希望同时得到中英两个版本、或希望理解引言中每个句子/段落的**写作目的/功能**。
- 用户希望对照某个领域（材料、生命科学、CS、工程、化学、物理等）的典型引言模板进行写作。
- 用户提供已有 Introduction 草稿，希望润色、重构、检查 gap、补充文献综述、或添加逐句功能注释。
- 用户只要求段落级 outline、四组件诊断、或按目标期刊风格调整引言。

## 核心理论：四组件模型 + 十一句式

Glasman-Deal 从多个已发表论文中逆向归纳出 Introduction 的**通用四组件模型**（GENERIC INTRODUCTION MODEL），组件之间是**菜单式**的——不必全用，但必须覆盖主要功能：

1. **组件 1 — 建立背景（wide end）**：
   - 确立研究主题/领域的重要性（establish the importance of the topic）
   - 提供必要的事实背景（background factual information）
   - 引出该领域的一般性问题或当前研究焦点（general problem area / current research focus）

2. **组件 2 — 研究地图（literature & contributions review）**：
   - 综述前人/当前研究和贡献，构成"研究地图"，让读者看到本研究的坐标。
   - 可按三种模式组织：general-to-specific（最常见）/ different approaches / chronological。

3. **组件 3 — 锁定空白（locate a gap, narrow down）**：
   - 指出研究的空白、未解决的问题、矛盾、或前人方法的不足。
   - 通常用 However / Although 等信号词引出。
   - 陈述研究动机、假设、或研究机会。

4. **组件 4 — 介绍本研究（narrow end）**：
   - 描述本文/本研究是什么（目的、方法、结构、贡献、结果）
   - 使用与证据强度匹配的贡献标记词（contribution markers；传统上称为 "happy words"）显式标注本研究的贡献，如 *new, robust, lightweight, efficient, systematic* 等；只有在用户材料支持时才使用 *novel, first, significant, state-of-the-art* 等强断言。

Introduction 整体呈**漏斗形**：起笔宽泛（wide），逐步聚焦（narrow）到本研究。Discussion 则相反：从本研究出发回到宽泛。

在句子层面，可把四组件展开为**十一句式模板**（并非强制，是一把尺子）。详见 `references/model-structure.md`。

## §1.6 写作练习模式 / Short Practice Mode

当用户明确提到 "Exercise 5"、"1.6 Writing the Introduction"、"250-350 words"、"短引言练习"，或要求根据一个假想/已完成项目快速写一篇引言时，启用短引言练习模式：

- 先按段落规划整个 Introduction，再写句子；目标是把本单元的 model、language、writing skills 和 vocabulary 合在一次写作任务中使用。
- 使用 streamlined Introduction model：三段式通常足够，但仍必须覆盖四组件（C1 背景、C2 研究地图、C3 gap、C4 本文）。
- 句型应尽量贴近用户给定的 target articles；若用户没有提供目标文章，则参照 `references/examples.md` 与 `references/templates.md` 中相近领域的句型。
- 语言资源优先来自 `references/language-toolkit.md`，尤其是前人研究连接语、gap 信号词、本文引入句和贡献标记词。
- 若练习题明确允许虚构文献，可使用 Wang et al. (1999)、Martinez (2002)、Zhang et al. (2019) 这类 plausible references，并标注其为练习用占位；真实投稿稿件中不要虚构引用，只能使用用户提供的引用或语义化占位符（如 `[REF: prior safety-bar design]`）。
- 针对 SPPPV / bicycle cover 练习，读取 `references/writing-practice.md` 与 `references/examples.md` 的样例 7。

## 工作流 / Workflow

当启用本技能后，按以下步骤工作：

### 第 0 步 — 判断任务类型

先判断用户要的是哪一种任务，并让输出形式匹配任务，而不是机械生成完整双文件：

- **完整生成**：从用户笔记生成完整 Introduction。默认产出英文版和中文功能注释版，并保存文件。
- **修改已有稿**：用户提供 Introduction 草稿时，优先保留原意和已有引用，重构漏斗、gap、段落衔接和贡献表达；除非用户要求，不强制另存双文件。
- **功能注释 / 诊断**：只分析段落功能、句子功能、gap 与四组件完整性，不改写全文。
- **提纲模式**：只输出 paragraph-level outline 或四组件规划。
- **§1.6 短练习模式**：按 250-350 words、3 段、8-12 句左右生成练习型引言。

### 第 1 步 — 收集输入信息

如用户提供的信息不完整，**主动、礼貌地**询问以下核心要素（能一次问完就一次问完，不要多轮挤牙膏）：

| 字段 | 说明 | 示例 |
|---|---|---|
| **Topic / Title** | 论文题目或核心主题 | "A lightweight chitin-PLA composite for load-bearing biomedical applications" |
| **Field / Discipline** | 所属学科 | 材料科学 / 生物医学工程 |
| **Importance hook** | 该领域为何重要、为何有用 | PLA 可降解、可生物相容，广受关注 |
| **Background facts** | 读者需要了解的 1-3 条基础事实 | PLA 来自玉米、甘蔗等可再生原料；有优良的成型性 |
| **General problem / current focus** | 领域当前关注的一般性问题 | PLA 的抗冲击性弱；生物医学应用要求低毒性 |
| **Prior research / key studies** | 1-3 个相关前人工作（带作者或引用标号） | Penney et al. (2012) 在 PLA 基质中掺入角蛋白填料 |
| **Gap / problem** | 本文要解决的空白或问题 | 角蛋白显著增加复合材料重量，且很少有人关注替代生物相容材料 |
| **Aim / approach of this paper** | 本文的目的、方法 | 提出一套筛选标准；用壳聚糖替代角蛋白 |
| **Main finding / contribution** | 主要结果或贡献，贡献强度需有证据支撑 | 新型轻质共聚物，显著提高抗冲击性，同时保留生物相容性 |
| **Target journal style (optional)** | 目标期刊（用来匹配风格） | Biomaterials / Nature / PNAS 等 |

若用户信息已足够，**直接跳到第 2 步**，不要反复确认。

**最小可生成输入（minimum viable input）**：

- Topic / Title
- Field / Discipline
- Gap / problem
- Aim / approach of this paper
- Main finding / contribution（若尚无结果，可提供预期贡献或研究目的）

如果缺少上述 2 项或更多，先一次性询问补充信息。若用户只有标题和一句话但坚持生成，输出带 `[TO BE FILLED: ...]` 的骨架稿或提纲，并明确说明哪些位置需要用户补充。目标期刊、精确引用和详细结果是强烈建议项，但不是启动写作的硬性门槛。

### 第 2 步 — 选择模板

读取 `references/templates.md`，根据用户的学科匹配最接近的模板（材料 / 生命科学 / 计算机 / 工程 / 化学 / 物理 / 交叉学科）。若无完美匹配，使用通用模板（General Template）作为骨架。

若用户要求 §1.6 练习、250-350 词短引言、或 SPPPV / bicycle cover 题目，优先采用 `references/templates.md` 中的"模板 4B：工程 / 交通 / 设计短引言"，并读取 `references/writing-practice.md`。

### 第 2.5 步 — 形成段落级计划

在生成英文句子前，先形成 paragraph-level outline：每一段对应哪个组件、承担什么功能、如何连接上一段、最终如何通向本文贡献。默认可作为内部规划；若用户要求教学、审阅或确认结构，则把这个 outline 展示给用户。

### 第 3 步 — 生成英文版 Introduction

按照"四组件 + 十一句式"框架：

- 组件 1（约 2-4 句或 1 段）：importance hook → background facts → general problem area
- 组件 2（约 3-6 句或 1-2 段）：literature & contributions review（用 `references/language-toolkit.md` 中的 linking phrases）
- 组件 3（约 2-3 句）：gap / problem / motivation，通常以 *However / Although / Despite / Yet* 开头
- 组件 4（约 2-4 句或 1 段）：describe the present paper（aim + method + 可选结果 + 贡献标记词）

务必：
- 使用正确的动词时态（参见 `references/language-toolkit.md`）。
- 包含用户提供的引用；如果用户没给引用，使用语义化占位符（如 `[REF: biodegradable PLA review]`、`[REF: baseline method]`），不要伪造真实感作者年份，除非这是明确允许虚构引用的练习题。
- 使用与证据强度匹配的贡献标记词。没有结果数据时，优先使用稳健表达（*provides, examines, evaluates, proposes, offers*）；有充分证据时再使用强表达（*novel, first, significant, state-of-the-art*）。
- 常规投稿型引言要写得**充实、展开**：成熟引言通常 15-25 句，分 3-5 段。若用户明确要求 §1.6 / short practice / 250-350 words，则采用 8-12 句、3 段左右的紧凑版本，但四组件仍必须齐备。

### 第 4 步 — 生成中文版 Introduction（带功能注释）

中文版的结构与英文版一一对应，但**格式特殊**：

- 每一段开头先写一行 **"【段落功能】"** 注释，说明该段在整个引言中扮演什么角色（对应四组件的哪一部分）。
- 每一个句子后面，用 **斜体 + 括号** 形式紧跟一句功能注释，如 *（本句功能：确立研究主题的重要性）*。
- 这种注释**必须遵循 Glasman-Deal 的逆向工程原则**：描述"句子在做什么（function）"，不是"句子在说什么（content）"。参见 `references/model-structure.md` 的十一句式详表。

示例格式（片段）：

```markdown
## 第一段

【段落功能】组件 1 — 建立研究主题的重要性、提供必要的事实背景、引出一般性问题。此段是引言的"宽端"，让所有读者能共同进入论文。

近年来，来自生物质的聚乳酸（PLA）因其可降解性和生物相容性受到广泛关注。*（本句功能：确立研究主题的重要性——以"近年来"+ 现在完成时建立"该主题是热点"的基调，对应组件 1 的第一个功能。）*

生物质 PLA 可从玉米、甘蔗等可再生原料中制备。*（本句功能：提供读者理解本文所必需的基本事实背景；用一般现在时表达已被广泛接受的事实。）*

...
```

### 第 5 步 — 保存文件

完整生成任务默认在**用户当前工作目录**下保存两份 Markdown 文件：

- `introduction_en.md` — 英文版
- `introduction_zh.md` — 中文版（含逐句逐段功能注释）

但如果用户只要求 inline 草稿、只要英文/中文、只要提纲、只要修改建议、或只要求诊断，不要强制保存两份文件；按用户请求输出即可。若目标文件已存在且不是本次任务刚创建的文件，优先使用带标题 slug 或日期的文件名，避免覆盖用户已有稿件。

在两个文件开头分别添加一个 YAML 前言块或标题块，包含：
- Paper title
- Field
- Generation date
- Brief TL;DR of the paper's contribution

### 第 6 步 — 向用户汇报

简洁汇报：
- 文件路径（若保存了文件）
- 使用的模板名
- 英文版句数与段数
- 提醒用户检查引用占位符、替换为真实引用

## 渐进式披露策略

本 SKILL.md 只是入口。不要一次性读取所有 references——**按需读取**：

- 开始撰写前，**必读**：`references/model-structure.md`（核心模型）、`references/output-format.md`（格式规范）
- 确定字段/学科后，读取：`references/templates.md` 中对应的模板部分
- 修改已有 Introduction 时，读取：`references/model-structure.md`、`references/writing-tips.md`；需要重写格式或保存文件时再读取 `references/output-format.md`
- 用户要求 §1.6 练习、250-350 词短引言、SPPPV 或 bicycle cover 时，读取：`references/writing-practice.md`，并参考 `references/examples.md` 的样例 7
- 写 Component 2 前，读取：`references/language-toolkit.md`（linking phrases、verb tenses）
- 写 Component 3 前，读取：`references/gap-patterns.md`（gap 的多种表达方式）
- 用户需要参照完整示例时，读取：`references/examples.md`

## 输出质量标准

一份高质量引言应满足：

1. **漏斗结构清晰**：从宽到窄，不能从宽跳到宽或从窄跳到宽。
2. **四组件齐备**：至少组件 1、3、4 必须有；组件 2 依领域习惯，但绝大多数研究论文需要。
3. **时态正确**：参考 `references/language-toolkit.md`。
4. **引用到位**：每个前人贡献都有真实引用或语义化引用占位符；背景事实若已被广泛接受可不引。
5. **gap 明确**：用 However / Although / Despite 等显式信号引出，且 gap 与本文 aim 之间有逻辑衔接。
6. **贡献标记得体**：不过度自夸，但明确标识本研究的贡献；强断言必须有用户材料或真实引用支撑。
7. **长度匹配任务**：常规稿件通常 15 句、3 段以上；§1.6 练习或明确要求的短引言可为 8-12 句、250-350 词左右，但不能缺少四组件。
8. **中文注释贴合**：描述"句子的功能"，不重复内容；语言专业但简洁。

## 关键禁忌

- **不要**以研究的具体问题或方法开头——多数期刊期望从宏观重要性切入。
- **不要**在引言里铺陈过多的方法细节——属于 Methods。
- **不要**用问句陈述 gap——用 prediction / suggestion / hypothesis 形式。
- **不要**把 literature review 写成"shopping list"——必须有叙述主线，通往本文动机。
- **不要**忘记在中文版逐句标注功能；功能注释不等于中文翻译。
- **不要**无证据夸大贡献词——没有数据或用户确认时，不要写 first / breakthrough / state-of-the-art / significant 这类强断言。
- **不要**在真实投稿稿件中虚构参考文献；只有练习题明确允许时才可创造 fake references。
- **不要**在用户只要求提纲、诊断、单语版本或修改建议时强制生成并保存完整双文件。
