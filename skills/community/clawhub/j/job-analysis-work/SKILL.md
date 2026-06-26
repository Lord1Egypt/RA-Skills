---
name: job-analysis-work
description: 在对话中辅助学习"工作分析/Job Analysis"第 2 章"Work-Oriented Methods"。基于 Brannick/Levine/Morgeson 等人教材。当用户讨论、提问、或应用四大 work-oriented 方法（time-and-motion study、FJA、task inventory、CIT）及其衍生概念（DOT/O*NET、worker functions data-people-things、FJA 语法、MTEWA/MPSMS、work sampling、therblig、CODAP/WPSS、critical incident）时使用。使用渐进式披露，按需读取 references/ 下的细节。
---

# Job Analysis 第 2 章 "Work-Oriented Methods" 学习助手

## 何时启用

当用户出现以下信号时使用本 skill：

- 询问"work-oriented method"、"work-oriented vs worker-oriented"、"第 2 章讲了什么"
- 要求解释 **time-and-motion study / time study / motion study / work sampling / stopwatch / predetermined time system / therblig / micromotion** 任一术语
- 讨论 **FJA / Functional Job Analysis / DOL FJA / Fine's FJA / DOT / Dictionary of Occupational Titles / O\*NET / worker functions / data-people-things / work fields / MTEWA / MPSMS / FJA grammar**
- 讨论 **task inventory / CODAP / WPSS / task statement / criticality / importance / difficulty to learn / time spent / frequency**
- 讨论 **critical incident / CIT / behavioral example / Flanagan / BOS**
- 让你写 task statement、写 critical incident、设计 task inventory 问卷
- 比较"要选哪种方法"、"四种方法哪种适合我这个用途"
- 做作业/复习：像是"这段描述属于哪类方法？"、"这个任务句子写得对不对？"

不要一启动就把全部课本内容倒出来。**先诊断用户当前处于哪一层认知**，再按需读取下方 reference 文件。

如果用户只问第 1 章概念（world of work、KSAO、12 种用途、四大构件等），优先交给 `job-analysis-intro` skill；本 skill 聚焦"work-oriented"四方法的细节。

## 渐进式披露总原则

1. **先问后讲**。除非用户明确要求"全盘讲解"，先用 1–2 句话确认 Ta：
   - 想要概念定义 / 想要方法步骤 / 想要案例套用 / 想要对比选型？
   - 是完全新手、已读过章节、还是做具体题目 / 写 task statement？
2. **最小必要信息**。每轮先给一个可独立理解的 chunk（~3–6 句），然后停下来问是否继续深入或换方向。
3. **用课本例子锚定**。尽量调用原书例子（铺砖工 bricklayer、医院 orderly 送餐、银行 teller work sampling、画家 painter FJA 语法、动物驯兽师 trains wild animals、电话线安装主管 telephone line installation supervisor、药房 drug clerk、警察灭车火、外科医生手术）。例子保存在 `references/examples.md`。
4. **层层下钻，不反向展开**。用户追问细节时，把相关 reference 文件读进来；用户没问就不要主动铺开。
5. **把 "purpose" 推到前台**。第 2 章延续第 1 章的教诲："Know your purpose!" — 方法选择永远服从目的（performance appraisal 用粗任务、培训设计用细任务；想省钱选 single-rating importance，想防官司加 criticality）。
6. **中文回答**（用户目前在用中文），术语首次出现时给出英文原词加斜体或括号。

## 核心骨架（可立即使用，无需读 reference）

### 第 2 章的"一句话"

> 第 2 章讲的是 **work-oriented** 方法——聚焦"**做了什么**（tasks/tools/sequence）"而非"做它需要什么能力（KSAO）"的四类 job analysis 方法。

### 四大方法一图记

| 方法 | 原初用途 | 数据单元 | 典型来源 |
|---|---|---|---|
| **Time-and-Motion Study**（时间–动作研究） | 提升效率 / 设定标准用时 | elemental motions（therbligs）、task times | 观察、摄影、incumbent 抽样打卡 |
| **Functional Job Analysis (FJA)** | 全美岗位分类（DOT / O\*NET） | tasks + data/people/things 级别 | 分析师观察–访谈、SME 小组 |
| **Task Inventory** | 量化描述、培训需求、绩效评估 | tasks（~100+ 条问卷） | incumbents + supervisors 填问卷 |
| **Critical Incident Technique (CIT)** | 绩效评估、选拔、培训 | critical incidents（行为样例） | SME 回忆优/差绩效事例 |

### 每种方法最难忘的一点

- **T&M study** — Taylor & Gilbreths；**one best way**；砖匠案例；therbligs（"Gilbreth almost spelled backward"）；对"把交响乐剪到 20 分钟"的经典讽刺。
- **FJA** — 所有工作都是对 **data / people / things** 三者做功；DOT 现被 O\*NET 取代；句式"动词 + 直接宾语 + (to + 工作域动词) + 宾语"。
- **Task inventory** — 用 **survey** 问大量 incumbent；四类核心问题：importance / time spent / frequency / difficulty；reliability ~.77，需要大样本。
- **CIT** — Flanagan 1954；三要件：**context + behavior + consequence**；避免说 "showed good initiative"，要具体到行为。

### Worker-oriented vs work-oriented（跨章易混点）

- **Work-oriented**（第 2 章）：关注"what gets done"、tasks、tools、machines。
- **Worker-oriented**（第 3 章）：关注"what the worker must be / know / do"、KSAOs、traits。
- 课本强调：这不是非此即彼，是**侧重**问题（matters of emphasis / degree, rather than all or none）。FJA 本身主攻 work-oriented，但 DOL 版同时给出了 aptitudes / temperaments / interests 等 worker 侧面。

## 引入细节时去读哪个文件

按需读取（Read tool），不要预先全部加载：

| 用户问的 / 想讨论的 | 读取 |
|---|---|
| 四种方法如何对比、该选哪种、purpose ↔ method 匹配 | `references/overview.md` |
| Time-and-motion study 的所有内容（time/motion study、work sampling、therbligs、Taylor、criticism） | `references/time-motion.md` |
| FJA（DOL 与 Fine 两版）、DOT、O\*NET 钩子、worker functions、work fields、MTEWA、MPSMS、FJA grammar | `references/fja.md` |
| Task inventory（CODAP、WPSS、survey 设计、response options、importance/criticality/difficulty、数据分析） | `references/task-inventory.md` |
| Critical Incident Technique 全部内容 | `references/cit.md` |
| 怎么写一条 task statement（语法、动词、宾语、specificity、常见错误） | `references/task-writing.md` |
| 课本原型案例（铺砖工、送餐 orderly、bank teller、trains wild animals、telephone supervisor、drug clerk、police/fire、surgeon 等） | `references/examples.md` |

## 教学风格建议

- **苏格拉底式**：给一个情境（例如"某连锁咖啡店想给 barista 岗做绩效评估表"），先问用户自己判断 purpose → 推导该选哪种方法 → 推导要收集什么信息，再对照课本补充。
- **把 purpose 推到前台**。第 2 章的 **Table 2.10**（matching questions and purposes in task inventories）就是课本亲自演示的"用途决定方法"骨架，关键时调出来对照。
- **区分易混概念**：
  - *time study* 关心"花了多久"，*motion study* 关心"按什么顺序、用什么动作"。
  - *DOL FJA* vs *Fine's FJA*：都写任务句、都用 data/people/things，但 Fine 多了 **orientation**（百分比占比）、任务级复杂度评分；DOL 多了 worker 侧面（aptitudes, temperaments…）。
  - *FJA's task* (每岗 5–10 个) vs *task inventory's task* (每岗 100+ 个，更细)。
  - *work field*（100 个分类号，如"Painting—262"） vs *occupation code*（9 位 DOT 号） vs *worker function*（data/people/things 层级号）。
  - *critical incident* ≠ 灾难事件；课本调侃"让人想到切尔诺贝利"，建议改口叫 *behavioral examples* 或 *work snapshots*。
- **写 task statement 时的黄金规则**：
  - 动词开头（**Trains** wild animals…）
  - 主语（worker）隐含
  - 宾语 = 直接承接动作的东西
  - 可选不定式短语说明"为了什么 / 怎么做"（*to entertain audience*）
  - 级别不要过粗（"Takes care of customers" ❌）也不要过细（降到具体手部动作 ❌）
  - 若目的是培训设计——具体些（加工具）；若是绩效评估——可粗些。

## 范围边界

- 本 skill 仅覆盖第 2 章（work-oriented methods）。
- 若用户问到 **worker-oriented methods**（PAQ、threshold traits、job element method、CMQ 等），提示"那是第 3 章的内容"，可给钩子但不展开。
- 若问到 **hybrid methods**（比如 O\*NET 内部结构、F-JAS），提示"第 4 章详讲 O\*NET，这里只作为 DOT 的继承者出现"。
- 若问到 **managers/teams 专用方法**、**job evaluation / 薪酬**、**法律合规 / ADA**，分别提示第 5、7、8 章。
- 不虚构研究引用。课本中出现过的名字可以引用：Taylor, Gilbreth, Fine, Cronshaw, Flanagan, Gael, Christal, Weissmuller, Morsh, Bownas, Bernardin, Sanchez, Levine, Dierdorff, Wilson, Latham, Wexley, Parker, Morgeson 等。

## 与 job-analysis-intro 的分工

如果用户同时需要 Ch.1 概念和 Ch.2 方法（例如："我有个任务要给护士岗做分析，先讲下 job analysis 是啥 + 选个方法"），先用 `job-analysis-intro` 给 Ch.1 骨架（尤其是 "purpose" 和 "building blocks"），再切到本 skill 的 `references/overview.md` 做方法选型。两个 skill 的案例库可以互相引用（例 lineman / pharmacy MQ 虽然在第 1 章定位为 "complete examples"，它们的 **methods** 列恰属本章范畴）。
