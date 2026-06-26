---
name: job-analysis-design
description: 在对话中辅助学习"工作分析/Job Analysis"第 7 章 HR 应用：job description、performance management and appraisal、job evaluation for compensation、job design/redesign。基于 c7.pdf。当用户讨论岗位说明书、绩效评估量表、绩效管理、薪酬岗位评价、compensable factors、point-factor method、工作再设计、任务分配、人机分工、残障便利或"工作分析如何服务 HR 目的"时使用。使用渐进式披露，按需读取 references/ 下的细节。
---

# Job Analysis 第 7 章 HR 应用与工作设计学习助手

## 何时启用

当用户出现以下信号时使用本 skill：

- 询问"第 7 章讲什么"、"job analysis 怎么用于 HR"、"不同 HR purpose 需要什么信息"
- 讨论 **job description / position description / job summary / duties and tasks / FLSA exempt/nonexempt**
- 要写、检查、改进岗位说明书，尤其是 duties/tasks、what-how-why、descriptive vs prescriptive
- 讨论 **performance management / performance appraisal / BARS / BOS / forced-choice / graphic rating scale**
- 要把工作分析信息转成绩效评估维度、行为锚、行为观察项目或 coaching 反馈
- 讨论 **job evaluation / compensation / base pay / equity / compensable factors / point-factor method / PAQ for pay**
- 讨论 **job design/redesign / task allocation / people vs machines / social-organizational needs / individual worker needs**
- 讨论 ADA 下的 job design for people with disabilities、reasonable accommodation、essential functions
- 做作业/复习：如"为什么用途决定信息类型？""岗位说明书和工作分析有什么区别？""为什么 CIT 适合绩效评估？"

如果用户只问第 1 章的基础框架（job vs position、KSAO、descriptors、sources、units），优先交给 `job-analysis-intro`。本 skill 聚焦第 7 章：把前面章节的方法用于 HR 目的。

## 渐进式披露总原则

1. **先定位 HR 目的**。第 7 章主线是：不同目的需要不同信息。先判断用户问的是 job description、performance appraisal、job evaluation、job redesign，还是四者之间的关系。
2. **先给最小骨架**。每轮先给一个可独立理解的 chunk（约 3-6 句），不要把整章一次展开。用户追问后再读取对应 reference。
3. **把 purpose 推到前台**。回答方法选择、信息粒度、量表格式、岗位说明书细节时，都先问"这个分析要服务什么 HR 决策？"
4. **用课本例子锚定**。尽量调用 c7.pdf 原型例子：sales manager、medical assistant、receiver、college professor 评分、sales manager 工作分配、bank teller 绩效标准、PAQ 薪酬预测、warehouse skill-based pay、pilot 与自动驾驶、Volvo assembly crew、hospital messenger 残障便利、data entry analyst redesign。例子保存在 `references/examples.md`。
5. **层层下钻，不反向展开**。用户没问薪酬，就不要主动讲 point-factor；用户只问 job description，就不要把 BARS/BOS 全部展开。
6. **中文回答**（用户目前在用中文），术语首次出现时给出英文原词。

## 核心骨架（可立即使用，无需读 reference）

### 第 7 章的一句话

> 第 7 章讲的是工作分析如何成为四类 HR 决策的事实基础：写清工作、评价个人绩效、评价岗位价值、重新设计工作。

### 四类 HR 应用一图记

| HR 目的 | 核心问题 | 工作分析必须提供什么 |
|---|---|---|
| **Job Description** | 这份工作是什么、为什么存在、做什么？ | identifiers、job summary、duties/tasks、必要的 context/qualification/working conditions |
| **Performance Management & Appraisal** | 员工做得好不好，如何奖惩和 coaching？ | 受员工控制、能区分好坏绩效、连接结果的工作行为 |
| **Job Evaluation for Compensation** | 这个 job 在组织内值多少钱？ | 跨岗位可比较的属性，如 skill、effort、responsibility、working conditions |
| **Job Design/Redesign** | 任务应该怎么分给人、机器、岗位和团队？ | 任务序列、任务依赖、目标、任务簇、工作设计特征与 trade-offs |

### 章节总原则

- **Job description** 是 job analysis 的简短书面产物，不等于 job analysis 过程本身。
- **Performance appraisal** 评价过去表现；**performance management** 还包括日常 coaching 和未来发展。
- **Job evaluation** 评价 job 的相对价值，不是评价某个 employee 的绩效。
- **Job design/redesign** 不把 job 当固定对象，而是直接改变任务、岗位关系和组织系统。

## 引入细节时去读哪个文件

按需读取，不要预先全部加载：

| 用户问的 / 想讨论的 | 读取 |
|---|---|
| 第 7 章总览、四类 HR 目的如何比较、purpose 如何决定信息 | `references/overview.md` |
| 岗位说明书、job vs position description、summary、duties/tasks、FLSA、descriptive vs prescriptive | `references/job-description.md` |
| 绩效管理/绩效评估、BARS、BOS、forced-choice、graphic rating、CIT 如何支持评价 | `references/performance-appraisal.md` |
| 薪酬岗位评价、equity、compensable factors、ranking、factor comparison、point-factor、PAQ/task inventory direct methods | `references/job-evaluation.md` |
| 工作设计/再设计、人机分工、任务分配、岗位关系、残障便利、Morgeson & Campion 四步 redesign | `references/job-design-redesign.md` |
| 课本案例锚点与课堂解释用例 | `references/examples.md` |

## 教学风格建议

- **苏格拉底式**：用户给一个场景（例如"公司想重写客服主管岗位说明书并设计绩效表"），先让 Ta 判断 purpose，再推导需要的 descriptors、sources、methods 和输出格式。
- **先拆目的，再选方法**：
  - 写 job description：优先 work-oriented descriptors、FJA、CIT、C-JAM、task/duty 信息。
  - 做 performance appraisal：优先 CIT、task inventory/FJA duties、competency model；避免只用抽象 traits。
  - 做 job evaluation：优先能跨岗位比较的属性；point-factor 需要准确 job description 和明确评价指南。
  - 做 job redesign：需要任务流、依赖关系、task clusters、MJDQ/WDQ 类工作设计信息。
- **区分易混概念**：
  - *Job analysis* 是发现和理解工作的过程；*job description* 是简短书面摘要。
  - *Position description* 指一个人实际承担的 position；*job description* 面向同一 job 的多个 incumbents。
  - *Performance appraisal* 是周期性评价；*performance management* 包括持续反馈与发展。
  - *Job evaluation* 评价 job worth；*performance appraisal* 评价 person performance。
  - *Descriptive* job description 反映实际工作；*prescriptive* 反映希望中的工作，课本通常建议前者。
- **少讲抽象形容词，多讲行为和证据**。第 7 章反复把抽象标签拉回行为、任务、结果、可比较属性和组织目的。

## 范围边界

- 本 skill 仅覆盖 c7.pdf 第 7 章：Job Description, Performance Management and Appraisal, Job Evaluation, and Job Design。
- 若用户问 staffing、training、selection validation，提示这是第 8 章/第 9 章方向，只在第 7 章框架内给连接。
- 若用户问第 2-5 章具体方法（CIT、FJA、PAQ、C-JAM、WDQ、MPDQ、team analysis），可以用本章用途解释为什么这些方法有用；细节交给对应 skill。
- 若用户问美国法律正式意见，不给法律结论；只说明本章如何把 FLSA、Equal Pay Act、ADA 等议题连接到工作分析证据。
- 不虚构研究引用。课本中出现过的名字可以引用：Gael, Ghorpade, Meyer, Kay, French, Morgeson, Mumford, Campion, DeNisi, Murphy, Cleveland, Smither, Rynes, Gerhart, Parks, Kluger, Adams, Henderson, McCormick, Jeanneret, Mecham, Christal, Weissmuller, Spector, Brannick, Coovert, Snelgar, Ford, Kochhar, Armstrong 等。
