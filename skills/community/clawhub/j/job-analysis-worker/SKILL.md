---
name: job-analysis-worker
description: 在对话中辅助学习"工作分析/Job Analysis"第 3 章"Worker-Oriented Methods"。基于 Brannick/Levine/Morgeson 等人教材。当用户讨论、提问、或应用 worker-oriented 方法（JEM、PAQ、TTAS、ARS、ORP、AET、JCI、cognitive task analysis、personality-oriented job analysis、Big Five/PPRF 等）及相关概念（KSAO、work behaviors、traits、B/S/T/P 四量表、TV/IT/TR、OCEAN、declarative/procedural knowledge、novice vs expert）时使用。使用渐进式披露，按需读取 references/ 下的细节。
---

# Job Analysis 第 3 章 "Worker-Oriented Methods" 学习助手

## 何时启用

当用户出现以下信号时使用本 skill：

- 询问 "worker-oriented method"、"worker-oriented vs work-oriented"、"第 3 章讲了什么"
- 要求解释 **Job Element Method / JEM / Primoff / element / subelement / Barely Acceptable (B) / Superior (S) / Trouble Likely If Not Considered (T) / Practical (P) / Total Value (TV) / Item Index (IT) / Training Value (TR) / J-coefficient** 任一术语
- 讨论 **Position Analysis Questionnaire / PAQ / McCormick / S-O-R / 194 / 300 items / information input / mediation / work output / interpersonal / work situation / miscellaneous / DNA items / common knowledge effects / Smith & Hakel** 任一内容
- 讨论 **Threshold Traits Analysis System / TTAS / Lopez / "can do" / "will do" / 33 traits**、**Ability Requirements Scales / ARS / Fleishman**、**Occupational Reinforcer Pattern / ORP / Borgen**
- 讨论 **AET (Arbeitswissenschaftliches Erhebungsverfahren zur Tätigkeitsanalyse) / ergonomics / Rohmert**、**Job Components Inventory / JCI / Banks**
- 讨论 **cognitive task analysis / CTA / Seamster / declarative / procedural / generative / self-knowledge / automated skill / representational skill / decision-making skill / novice vs expert / think aloud / airport screener**
- 讨论 **personality-oriented job analysis / Big Five / OCEAN / Barrick & Mount / Tett / PPRF / Raymark / Hogan / failed leaders**
- 让你帮忙判断某个岗位的 KSAO、设计 PPRF 题、跑一次 JEM 的四量表评分、对比某两种方法
- 做作业 / 复习：如"这个描述属于哪一种 worker-oriented 方法？"、"PAQ 的六大类是什么？"

不要一启动就把全部课本内容倒出来。**先诊断用户当前处于哪一层认知**，再按需读取下方 reference 文件。

如果用户问第 1 章基础概念（job vs. position、KSAO 定义、12 种用途、4 大构件），先交给 `job-analysis-intro`；第 2 章四大 work-oriented 方法（time-motion、FJA、task inventory、CIT），交给 `job-analysis-work`。本 skill 聚焦"worker-oriented"方法的细节。

## 渐进式披露总原则

1. **先问后讲**。除非用户明确要求"全盘讲解"，先用 1–2 句话确认 Ta：
   - 想要概念定义 / 想要方法流程 / 想要案例套用 / 想要方法之间对比选型？
   - 是完全新手、已读过章节、还是做具体题目 / 评估某个岗位？
2. **最小必要信息**。每轮先给一个可独立理解的 chunk（~3–6 句），然后停下来问是否继续深入或换方向。
3. **用课本例子锚定**。尽量调用原书例子（police officer JEM 表 3.2、electrician JEM、office manager JEM、auto mechanic J-coefficient、airport screener CTA、pilot CTA、firefighter 团队沟通、surgeon CTA 训练、taste tester / math professor DNA items、figure skater / guitar / astronomer 引入例）。例子保存在 `references/examples.md`。
4. **层层下钻，不反向展开**。用户追问细节时，把相关 reference 文件读进来；用户没问就不要主动铺开。
5. **把 "purpose" 推到前台**。Chapter 3 延续课本教诲："Know your purpose!" —— JEM 最适合选拔（尤其 work-sample-like tests）；PAQ 擅长 job evaluation、薪酬比较、disability；TTAS/ARS 把 KSAO 对接到测验；ORP 面向 vocational guidance；AET/JCI 以设备/人体工学或 tools 为抓手；CTA 面向 expert training、error reduction；PPRF 面向 personality-based selection。
6. **中文回答**（用户目前在用中文），术语首次出现时给出英文原词加斜体或括号。

## 核心骨架（可立即使用，无需读 reference）

### 第 3 章的"一句话"

> 第 3 章讲的是 **worker-oriented** 方法 —— 聚焦"**做好这份工作的人需要具备什么**（KSAOs、traits、能力、人格）"而非"做了什么（tasks）"的方法。核心术语是 **KSAOs (knowledge, skills, abilities, and other personal characteristics)**。

### KSAOs 四件套（Levine, 1983 定义）

- **K**nowledge：记忆中可检索的技术事实、概念、语言、程序（与岗位直接相关）。
- **S**kill：通过训练获得的、使用工具 / 设备 / 机器完成任务的能力。
- **A**bility：相对稳定的天赋，支持获取 K/S、或在不需工具的情境下完成任务。
- **O**ther personal characteristics：兴趣、偏好、性格、气质等"适不适合"这份日常。

### 七大（组）方法一图记

| 方法 | 核心思想 | 代表 descriptor | 最典型用途 |
|---|---|---|---|
| **Job Element Method (JEM)** | SME 提 elements + 四量表打分 | work behaviors & 结果 | 选拔、work sample tests |
| **Position Analysis Questionnaire (PAQ)** | 所有岗位套同一张 300 项问卷 | 标准 element（信息输入/心理加工/输出/人际/情境/杂项） | 薪酬、job evaluation、disability |
| **Threshold Traits (TTAS)** | 33 traits, "can do" + "will do" | abilities + attitudes | 选拔、培训、job description |
| **Ability Requirements Scales (ARS)** | Fleishman 的通用人类能力清单 | 认知 / 心理动作 / 生理 / 感知 | 选拔、聚 job families |
| **Occupational Reinforcer Pattern (ORP)** | 岗位能满足哪些"需要" | 10 种 reinforcers | vocational guidance |
| **AET / JCI** | 从 ergonomics / 工具出发 | 工作设备、操作 220 件工具 | 工作再设计、培训 |
| **Cognitive Task Analysis (CTA)** | 专家怎么思考 | declarative / procedural / automated / representational / decision-making | 培训、减少人为差错 |
| **Personality-Oriented (PPRF)** | Big Five 对应到岗位行为 | OCEAN 5 维 + 12 sub | personality-based selection |

### JEM 的"高浓度"记忆锚

- 开发者：**Ernest Primoff**，1950s，U.S. Civil Service Commission（现 OPM）；JEM 是最早的 worker-oriented 方法。
- 工作流：6 个 SME × 2 次 3–5 小时会议，先 brainstorm elements（"怎样的人拿奖金？怎样会被开？"），再评 4 量表，最后把结果用于构建测验 / 培训。
- 4 量表（三档：0 / ✓ / +）：
  - **B**arely Acceptable：最差的合格者也要具备吗？
  - **S**uperior：此项能否把优秀与普通拉开？
  - **T**rouble Likely If Not Considered：如果不测，麻烦大吗？
  - **P**ractical：招得到满足这一项的人吗？
- 3 个导出量表：
  - **TV** (Total Value) = (S − B − P) + (SP + T)，用于选拔。>100 就算"显著 element"。
  - **IT** (Item Index) = SP + T，>50 可以给应聘者排序。
  - **TR** (Training Value) = S + T + SP′ − B（P′ = P 取反），>75 进入培训。
- 5 种元素类别：E（element, TV ≥ 100）、S（significant subelement, IT ≥ 50）、TS（training subelement, TR ≥ 75）、SC（screenout, B 与 P ≥ 75 且 T ≥ 50）、RS（rankable screenout, 同时满足 S 与 SC）。
- "警察身高" vs "能换车胎"案例——screenout 虽然数学上成立，但可能引发 disparate impact（对女性）。
- **J-coefficient**：Primoff 的"用判断估验证系数"的想法，需要 element–performance、test–element、element–element 三种相关；Hamilton & Dickinson (1987) 表明可与 empirical validity 一致。
- JEM "循环": "Tests are *not* inferred from the job analysis, but *incorporate* the work example definitions of the subelements"（Primoff & Eyde, 1988, p. 815）。

### PAQ 的"高浓度"记忆锚

- 开发者：**Ernest McCormick** 1960s，Purdue；理论基础是行为主义 **S-O-R**。
- 2004 年前 194 items（187 element + 7 compensation），2004 年后扩到 **300** items。
- 6 大类（major divisions）：
  1. **Information input**
  2. **Mediation (mental processes)**
  3. **Work output**
  4. **Interpersonal activities**
  5. **Work situation and job context**
  6. **Miscellaneous aspects**
- 6 种 rating scales：Extent of Use (U), Importance to the Job (I), Special Codes (S), Amount of Time (T), Possibility of Occurrence (P), Applicability (A) —— 每题只配一种。
- 用法：分析师**先观察**再访谈 incumbents；一般**不**让 incumbents 自填（阅读水平高 + 太抽象 + 薪酬用途更容易被拉高）。
- 信效度：同岗位跨 item 一致性高；跨岗位跨 item 较弱；.70–.80 再测稳定性。PAQ 能预测薪酬、GATB 分数。
- **Common knowledge effects**（Smith & Hakel, 1979）：只给学生一个 *job title*，他们的 PAQ 剖面与专家相关 .90+。原因至少一部分是 **DNA (does not apply)** items 很容易判断——人人都知道 taste tester 不用长柄工具。关键 item（applies）上，业余和专家仍有明显差距。
- 现在：2004 年 PAQ Services 易主，2018 起归 ERI（www.erieri.com/paq），主要场景之一是**长期残疾保险**。

### TTAS / ARS / ORP 一分钟版本

- **TTAS (Lopez, 1970)**：33 traits 分 "can do"（体力、心智、学得会的能力）和 "will do"（动机 / 社会）。典型 trait："strength"、"stamina"、"comprehension"、"adaptability"、"tolerance"。
- **ARS (Fleishman)**：给每种通用人类能力一套 scale + 对应心理测验。4 大类：Cognitive、Psychomotor、Physical、Sensory/Perceptual（Table 3.6 例：oral comprehension、control precision、static strength、night vision）。适合建 **job families**。缺点：能力名字只有心理学家听得懂。
- **ORP (Borgen)**：10 种"reinforcers"（ability utilization、activity、authority、compensation、creativity、moral values、security、social status、variety、autonomy）—— 描述岗位能满足什么需求，用于 vocational guidance。

### AET / JCI 一分钟版本

- **AET**：德语缩写 *Arbeitswissenschaftliches Erhebungsverfahren zur Tätigkeitsanalyse* = "ergonomic task analysis data collection procedure"。从人体工学看"这份活能不能改得更不累"。例：把轮子从地面抬到车轴→设计坡道减背伤。
- **JCI (Banks, 1988, 英国)**：为青少年职业指导设计，最突出的部分是涵盖 **220 件工具 / 设备**（标记、测量、夹持等），所以也能为培训所用。

### CTA 的"高浓度"记忆锚

- 出现于 1990s，"eliciting, analyzing, and representing the knowledge and cognitive processes involved in task performance"。聚焦 **novice vs. expert** 差异。
- 通常先做 work-oriented task analysis（第 2 章），从 tasks 里挑子集再 CTA。
- 4 种 knowledge：**declarative**（what）、**procedural**（how）、**generative**（新情境下的推导）、**self-knowledge**（知道自己能不能）。
- 3 种 skill（Seamster 等 1997）：**automated**（自动化，如熟练开车）、**representational**（心智模型，车为啥启动不了）、**decision-making**（启发式，黄灯是刹还是冲）。
- 5 类数据收集方法：**interviewing / team communication / diagramming / verbal report (think aloud) / psychological scaling**（如卡片分类）。
- 建议：至少 **两种方法交叉验证**，且 SME 必须是真专家（用两个指标挑人）。
- 经典案例：**airport screener**——专家有"图像库"，能瞬间辨认 X 光图像（automated skill）；新手 search 更多行李但速度更慢。
- 对比 Table 3.8：work-oriented 重 behavior、描述"唯一做法"；CTA 重 cognition、允许个体差异、专攻 expertise & learning。

### Personality-oriented 的"高浓度"记忆锚

- 起点：Barrick & Mount (1991)、Tett, Jackson & Rothstein (1991) 的 meta-analysis 复兴了"人格 → 绩效"的研究。
- **Big Five (OCEAN)**：Openness、Conscientiousness、Extraversion、Agreeableness、Neuroticism。
- **PPRF (Personality-Related Position Requirements Form, Raymark, Schmit & Guion, 1997)**：107 items、5 dim、12 subdim。5 dim 标签 = Surgency（Extraversion）、Agreeableness、Conscientiousness、Emotional Stability（Neuroticism）、Intellectance（Openness）。
- PPRF 三档：1 = not a requirement；2 = helps；3 = essential。
- 问题：多数 personality descriptor **太 social desirable**（integrity、dependability），每份工作都会被打满分，反而失去区分度。
- **Hogan**（Aamodt 2016 总结）：失败领导者的 personality 更值得看—— paranoid/passive-aggressive（背后捅刀）、high likability floater（讨好型但不挑战人）、narcissist（抢功爱曝光）。
- O\*NET 里也有 **work styles**，实质上就是人格维度。

## 引入细节时去读哪个文件

按需读取（Read tool），不要预先全部加载：

| 用户问的 / 想讨论的 | 读取 |
|---|---|
| 各种 worker-oriented 方法对比、如何选、purpose ↔ method 匹配、work-oriented vs worker-oriented 辨析 | `references/overview.md` |
| JEM 全部内容（Primoff、elements、subelements、4 量表、3 导出量表、5 类别、J-coefficient、circularity、legal issues） | `references/jem.md` |
| PAQ 全部内容（McCormick、194/300 items、6 大类、6 量表、reliability/validity、Common Knowledge Effects、ERI、disability 用法） | `references/paq.md` |
| TTAS、ARS、ORP 三种基于人类特质列表的方法 | `references/trait-methods.md` |
| AET（ergonomics、人体工学）、JCI（220 工具） | `references/equipment-methods.md` |
| Cognitive task analysis 全部内容（4 类 knowledge、3 类 skill、5 类方法、airport screener、reliability/validity、surgical training） | `references/cta.md` |
| Personality-oriented job analysis、Big Five、OCEAN、PPRF、Hogan 失败领导者、O\*NET work styles | `references/personality.md` |
| 课本案例库（police officer JEM、electrician、office manager、auto mechanic、airport screener、pilot、firefighter、surgeon、taste tester / professors DNA、figure skater/guitar/astronomer 等） | `references/examples.md` |

## 教学风格建议

- **苏格拉底式**：给一个情境（例如"某医院要给护士岗开发在线选拔题库"），让用户自己判断 purpose → 推导应该用 JEM 还是 PAQ 还是 PPRF，再对照课本补充。
- **把 purpose 推到前台**。课本原话："We would not recommend …" "We recommend …" —— 这些"推荐 / 不推荐"都是 purpose-driven 的，务必先问用途。
- **区分易混概念**：
  - *Work-oriented element*（第 2 章：tasks / behaviors）≠ *JEM element*（worker-oriented: 行为 + evidence）≠ *PAQ element*（standardized item to respond to）。**三种 "element" 含义完全不同。**
  - *JEM* 强调 work *behaviors*，刻意不往抽象 ability 上推（behaviorist 传统）；*PAQ* 反而用 300 项标准抽象描述。
  - *Knowledge* ≠ *Skill*（Seamster: knowledge = info，skill = 用 info 的过程，所以说 "procedural skill" 而非 "procedural knowledge"）。
  - *Big Five 5 维* ≠ *PPRF 5 维 + 12 sub*（标签也不同：Surgency、Intellectance）。
  - *ability* vs *trait* vs *reinforcer*：ARS 给 ability、TTAS 给 trait、ORP 给 reinforcer——三套框架。
  - *Screenout (SC)* 只是"最低要求"；*Rankable Screenout (RS)* 是"最低要求之上还能排序"。
- **黄金提醒**：
  - **JEM 量表是三档响应**（0 / ✓ / +），但最后换算成百分比（6 SME 满分 12 → 6 分 = 50%）；TV 重新 scaling 到 max 150。
  - **PAQ 不要让 incumbents 自填**（阅读水平高 + 很多项 DNA 他们不接受 + 用于薪酬时会虚报）。
  - **cognitive task analysis 先得做 task analysis**——CTA 不替代 work-oriented 方法，而是"在其基础上深入"。
  - **personality descriptor 容易全部打高分**——社会赞许偏差；frame-of-reference training 可能有帮助（Aguinis et al., 2009）。

## 范围边界

- 本 skill 仅覆盖第 3 章（worker-oriented methods）。
- 若用户问 **competency modeling**，提示："课本把 competency modeling 放到第 5 章（管理者/团队情境）"；给钩子不展开。
- 若问到 **O\*NET 的完整结构**、work styles 之外的细节，提示"第 4 章详讲 O\*NET，本章只作为 reference 的占位出现"。
- 若问到 **PAQ 衍生物** 如 CMQ、或 **threshold traits 之外** 的 trait-based 工具，可说"课本只略提，细节见原始参考文献"。
- 若问 **法律 / ADA / disparate impact**（如 police officer height requirement 是否违法），点到第 8 章；但 JEM 里那个身高例子可以在本章解释 disparate impact 的直觉。
- 不虚构研究引用。课本中出现过的名字可以引用：Primoff, Eyde, Hamilton, Dickinson, Trattner, McCormick, Jeanneret, Mecham, Smith, Hakel, Jones, Cornelius, DeNisi, Blencoe, Harvey, Hayes, Friedman, Surrette, Aamodt, Johnson, Lopez, Fleishman, Mumford, Quaintance, Reilly, Borgen, Rohmert, Banks, Miller, Seamster, Redding, Kaempf, Rosen, Salas, Lazzara, Lyons, Chao, Salvendy, Clark, Estes, Sullivan, Yates, Inaba, Lam, Wingfield, DuBois, Shalin, Levi, Borman, Barrick, Mount, Tett, Jackson, Rothstein, Raymark, Schmit, Guion, Cucina, Vasilopoulos, Sehgal, Morgeson, Campion, Aguinis, Mazurkiewicz, Heggestad, Hogan, Raskin, Fazzini, Arneson, Rolland, Mogenet, Foster, Gaddis 等。

## 与 job-analysis-intro / job-analysis-work 的分工

- `job-analysis-intro`（Ch.1）：job analysis 是什么、KSAO 基本定义、purpose 总框架、4 大构件。若用户还没搞清"worker-oriented vs work-oriented 的分野"或"KSAO 是什么"，先打这个底。
- `job-analysis-work`（Ch.2）：time-and-motion study、FJA、task inventory、CIT 四种 **work-oriented** 方法。若用户把 CIT / FJA 与 JEM / PAQ 混了，切到那个 skill 做对比。
- 本 skill（Ch.3）：以 **worker** 为焦点的方法 —— 覆盖 JEM / PAQ / TTAS / ARS / ORP / AET / JCI / CTA / PPRF。
- 跨章节案例可互相引用：如 police officer 既在 Ch.2（task inventory、critical incident）也在 Ch.3（JEM 表 3.2、CTA interview prompt）出现；pilot 在 Ch.3（CTA、PAQ DNA）和第 4 章（O\*NET）都有。
