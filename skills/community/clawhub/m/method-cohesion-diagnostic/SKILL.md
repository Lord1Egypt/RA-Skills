---
name: method-cohesion-diagnostic
version: 1.0.0
description: 诊断心理学论文Method部分的衔接与连贯问题，检查时序衔接、段落过渡、模块连贯性，输出评分与顶刊正例参考
metadata:
  domain: psychology-academic-writing
  dimension: cohesion
  source: Science_Research_Writing_2nd_edition_Unit_2_section_2.4.2
  companion_skills: [method-structure-diagnostic, method-logic-diagnostic, method-grammar-diagnostic, method-vocabulary-diagnostic]
user-invocable: true
---

# Method 部分「衔接与连贯」诊断 Skill

> 覆盖《Science Research Writing》(2nd ed.) **Unit 2**「How to Write about Methods」**§2.4.2** 关于**序列语言**（SEQUENCE LANGUAGE 的 8 组词汇 Group 1–8）、**因果—目的连接词**（CAUSE and RESULT connectors）、**对比连接词**（CONTRAST）、**JUSTIFY CHOICES**（in order to / with the aim of）、以及 Generic Methods Model 六模块叙事逻辑的全部规则，专用于心理学实证论文 Method 节的**衔接与连贯维度**诊断。
>
> **核心立场**：Method 节的衔接与连贯 = **时序衔接准确性 + 段落过渡自然性 + 模块间逻辑连贯性 + 指代与承接清晰性**四维联动。诊断目的：判断作者的**时序描述是否精确可复现**、**段落是否自然过渡**、**模块间跳转是否有承接**、**指代与引用是否清晰无歧义**。

---

## 一、诊断依据

本 Skill 的全部判定逻辑基于以下 **4 项不可拆分** 的依据，运行时按顺序加载：

| # | 依据 | 路径 | 用途 |
|---|------|------|------|
| 1 | **参考教材** | `D:\method-skill-project\01-reference\Science_Research_Writing_Methods.pdf` Unit 2（66 页） | §2.4.2 SEQUENCE LANGUAGE 八组词汇（Group 1–8）+ JUSTIFY CHOICES 词族 + CAUSE and RESULT 动词与连接词 + CONTRAST 连接词；§2.2.3 Generic Methods Model 六模块（OVERVIEW → DETAILS → FIGURE/TABLE → COMPARE → BACKGROUND → PROBLEMS）；§2.4.2 Option 1/2/3 比较框架 |
| 2 | **检查清单** | `references/checklist.md` | **4 大维度 / 29 子节 / 117 项** `- [ ]` 列表（时序衔接准确性 28 项 + 段落过渡自然性 24 项 + 模块间逻辑连贯性 36 项 + 指代与承接清晰性 29 项），作为违规定位与命中判定的对照表 |
| 3 | **评分细则** | `references/rubric.md` | 严重 / 中等 / 轻微三档扣分（**10–15 / 5–9 / 1–4 分/处**）+ A/B/C/D/F 五档等级（90/80/70/60/<60）+ 117 扣分点与 checklist 严格一一对应 |
| 4 | **顶刊正例** | `references/examples/positive/` | **37 个 `.md` 文件**，软链至 `D:\method-skill-project\02-positive_examples\cohesion\`，含 JPSP / JEP:G / Developmental Psychology / PSPB / OBHDP 等顶刊 Method 节衔接片段，按「**时序衔接样板**」「**段落过渡范式**」「**模块连贯示范**」「**指代承接样板**」四类诊断用途归组 |

> **教材原文摘录锚点**（用于本 Skill 内部一致性自检）：
> - §2.4.2 SEQUENCE LANGUAGE 八组定义：**Group 1（实验前）prior to / previously / beforehand / earlier；Group 2（起首）first / at the beginning / initially / to begin with；Group 3（步骤顺序）then / next / followed by / subsequently / afterwards；Group 4（短时距）shortly after / soon / quickly；Group 5（后段）eventually / later / towards the end；Group 6（同时性）simultaneously / meanwhile / at the same time / while / when；Group 7（收尾）finally / lastly / in the end；Group 8（后续延伸）afterwards / subsequently**（教材 p.105–106）
> - §2.4.2 序列词与 then/next 的区别：**"Words like then or next describe the order of events, but they don't provide information about how long each step took or how soon the next step occurred"**（教材 p.104）
> - §2.4.2 JUSTIFY CHOICES：**"in order to / with the aim of / thereby / which allowed / to take advantage of / for the sake of simplicity"**（教材 p.107）
> - §2.4.2 CONTRAST 连接词：**"however / whereas / by contrast / unlike / instead of"**（教材 p.110）
> - §2.2.3 Generic Methods Model：**OVERVIEW → DETAILS(±justify ±care) → FIGURE/TABLE → COMPARE → BACKGROUND(Present Simple) → PROBLEMS**（教材 p.88）

---

## 二、核心检查项（4 大维度，29 子节，117 项）

依据 `checklist.md` 提炼为以下 **4 个诊断维度**，运行时按此顺序扫描。每个维度下分若干子节，标注与 checklist 的对应关系。

### 维度 1：时序衔接准确性（对应 checklist §一，共 9 子节 / 28 项）

> **诊断核心问题**：实验步骤是否严格按时间顺序叙述？时序衔接词是否精确区分了短时距 / 长时距 / 同时性？动态材料（视频 / 音频 / 改编范式）的时序是否完整可复现？

| 子节 | 关键判定 |
|------|----------|
| 1.1 时间参照点（Group 1） | 描述实验前既有状态或预备条件时使用「先前」类词汇（prior to / previously / beforehand / earlier / formerly / originally）；引用同一研究系列前一实验时使用 prior study / earlier experiment / previous work 等回指；预备环节（知情同意、人口学、预筛问卷）作为时间锚点放在程序叙述的最前端 |
| 1.2 起首步骤（Group 2） | 程序总起句明确「第一步是什么」（first / firstly / at first / at the beginning / to begin with / initially）；系列实验的复用句式一致（"Materials and procedures were identical to Study X, with the following changes"）；程序段落开篇即给出时间锚点 |
| 1.3 步骤顺序（Group 3） | 步骤严格按实际执行的时间顺序排列，不预先讲述结论或后置步骤；多步骤程序显式编号（First / Second / Third / Fourth / Lastly）或分阶段命名（Phase 1 / Step 1 / Stage A）；步骤衔接使用精确序列词（then / next / followed by / subsequently / afterwards），而非仅靠「然后」类口语词；多步骤分析方案每步以目的状语起句 |
| 1.4 短时距（Group 4） | 描述快速衔接的事件时使用 shortly after / soon / quickly / immediately after；程序中相邻操作的时间窗（如 24 hr between sessions、48 hr–72 hr after）显式标注；短时距与长时距不混用同一时间副词 |
| 1.5 后段/长时距（Group 5） | 描述相对靠后的阶段使用 later / later on / eventually / towards the end；跨波次研究给出绝对天数与相对间隔（132 days after T0; 34 days after T1）；长期时间线在每个时点重申相对位置（Thielmann 样板） |
| 1.6 同时性/接口（Group 6） | 两操作并发或前后紧接时使用 simultaneously / at the same time / meanwhile / while / when；表达「A 紧接着 B」时使用 as soon as / immediately / directly / instantly / straight away / at that point；一事件结束恰好为另一事件开始时用 until / once 标识转换点；同时发生事件可附带因果暗示时显式标注 |
| 1.7 收尾步骤（Group 7） | 程序末尾步骤用 finally / lastly / in the end / at the end 显式收束；最终样本、最终数据集、最终得分在收尾处给出；多阶段流程结束时给总时长或总次数 |
| 1.8 后续延伸（Group 8） | 实验结束后追加动作（事后说明、再次测量、随访）使用 afterwards / subsequently；后续追加内容与主干程序明确区分（"beyond the scope of the current investigation" 式标注） |
| 1.9 刺激/材料时序的可复现性 | 视频/音频等动态刺激的每一拍标注精确秒数（Thiele 十一秒视频模板）；改编范式用 (a)/(b)/(c)/(d) 或子步骤嵌套呈现，每子步骤时长与衔接规则（If the toddler cried...）一并交代；程序性应急规则（If X happened, then Y）以条件句形式嵌入时序链 |

### 维度 2：段落过渡自然性（对应 checklist §二，共 6 子节 / 24 项）

> **诊断核心问题**：段落是否以段落入口句开场？跨段是否使用显式递进/对比/回指/结构提示连接词？段内是否避免「罗列式无连接」的多句堆砌？图/表/公式的衔接是否充分？

| 子节 | 关键判定 |
|------|----------|
| 2.1 段首句与总-分结构 | 每段以段落入口句（paragraph-entry sentence）开场，先立焦点再填充细节；段落入口句常用起首短语（First / Next / In addition / Beyond... / Building on the established measurement model / We then provided...）；段落入口句与前一段内容存在显式衔接（原因—结果、整体—局部、对照—补充）；大段开头给出主题句后，段内严格按 general → specific 顺序展开 |
| 2.2 跨段递进连接 | 跨段使用显式递进词（Next / Following this / Subsequently / Then / Building on...）；跨段使用对比/补充连接（In contrast / Conversely / Further / Additionally / Beyond...）；跨段使用回指总括（Hence / Therefore / In summary / Summarizing the major results）；跨段使用结构提示（As in Studies 1–3 / Comparable to Study X / Building on the established measurement model） |
| 2.3 段落间的逻辑承接（转折 / 因果 / 让步） | 转折关系显式标注（However / Nevertheless / Yet / Although / Whereas / By contrast），不靠读者脑补；让步-转折链完整（Although X → nevertheless Y → As such, we supplemented Z）；因果链显式（Because A → Therefore B / Hence B）；取舍论证显式（While X 提供 Y, Z was chosen for...）；假设-推导链完整（先重述假设 → 图示 → step-by-step 推导） |
| 2.4 段落内的衔接颗粒度 | 段内句间衔接不依赖读者脑补：每句都能从上一句或段落入口句推出；段内避免「罗列式无连接」的多句堆砌（连续 5 句以句号断开而无任何衔接词）；段内使用最小化承接词（Thus / Specifically / In all cases / Most of the tests / Moreover）；段内同一概念使用一致术语，无中途更换同义表达 |
| 2.5 跨段落主题切换 | 主题切换前显式过渡（Beyonds the facial stimuli that were used, two conversation topics were developed）；从方法描述切换到理论解释时显式标注（This procedure is based on research finding that...）；从结果描述切换到结果解释时显式标注（Accordingly / This means that / As a result） |
| 2.6 图/表/公式的衔接 | 图表/公式出现处使用引导短语（Figure 2 illustrates / Table 4 details / as shown in Figure 1, Panel A / Eq. (1)）；引导句包含「图/表内容概括 + 阅读指引」，避免仅写「(see Figure 1)」；图与表分工明确（路径系数归 Figure 2，假设检验汇总归 Table 4）；图/表编号与正文叙述顺序一致 |

### 维度 3：模块间逻辑连贯性（对应 checklist §三，共 7 子节 / 36 项）

> **诊断核心问题**：Methods 整体结构是否遵循六模块逻辑（OVERVIEW → DETAILS → FIGURE/TABLE → COMPARE → BACKGROUND → PROBLEMS）？子模块间过渡是否承接？分析方案内部衔接是否顺畅？排除漏斗是否完整？系列实验/多研究的模块间衔接是否标准化？控制变量与对照条件是否句法平行？

| 子节 | 关键判定 |
|------|----------|
| 3.1 Methods 整体结构的六模块逻辑 | Method 起首为研究概述句，重述研究目标/缺口；概述后给出材料的来源（were obtained from / were a kind gift from）；提供材料/方法的细节 + 理由 + 严谨性证据（in order to / with the aim of / tightly / precisely）；必要时描述图/表的内容与解读；与既有方法比较：完全相同（as described by）/ 相似（adapted from）/ 显著不同（unlike / instead of），并说明差异意义；必要时给出现有方法背景（一般现在时）+ 选择理由；局限/问题首次出现即提及 |
| 3.2 子模块间过渡 | Participants → Design/Measures：先介绍样本，再说明样本如何被分配到条件；Measures → Procedure：测量顺序与程序时间窗口匹配；Procedure → Analysis：分析方案与程序产出（变量类型、数据结构）一致；子模块标题命名符合目标期刊惯例 |
| 3.3 分析方案内部衔接 | 分析方案总览段以「We first / We then / We used / Lastly」四步或五步概括三步骤以上分析；每步分析以目的状语开头（to distinguish / to examine / to test / to control for / to scrutinize）；分析步骤与前言假设一一对应（Verhoef 五步 / Damian 五步样板）；括号内即时标注例外与口径；软件/包引用随分析步骤一并交代；总览段尾预留与详细段的对接 |
| 3.4 排除/筛选漏斗的衔接 | 排除流程按时间漏斗顺序：起始样本 → 逐条限制 → 每步人数与理由 → 最终样本；每步排除使用显式时序词（Initially → However → Afterward → Then → Finally → Hence）；每步排除理由具名（less than 18 years old / failed attention checks / < 80% survey completion / Mahalanobis & Cook's distances）；排除人数明确（50 / 116 / 69 / 5），与各步骤理由一一对应；选择效应自查：识别潜在偏差来源 → 推断后果 → 引出对照检验 → 量化比较 |
| 3.5 系列实验/多研究的模块间衔接 | 系列实验描述采用「基线 + 差异清单」结构；每条差异以 First / Second / Third 编号，并附改动动机；跨研究复用元素显式回指（on similar 11-point scales as in Experiments 1a–1c / as described above）；跨研究样本口径一致（As in Studies 1–c）；多研究间分析策略一致 |
| 3.6 控制变量与对照条件的衔接 | 每个控制变量的入选都附理由（To control for the possibility that / Although…does not predict…so we included it）；控制变量与可能混淆源一一对应（Landis 混淆源清单样板）；操纵检验与因变量的角色关系显式标注（As a manipulation check, we assessed...）；控制条件与实验条件在句法上平行呈现（whereas / a parallel question / similar procedure） |
| 3.7 测量决策链的衔接 | 测量工具介绍按「工具来源（含链接）→ 任务构成 → 效度证据 → 计分规则 → 信度」顺序推进；既有工具与改编工具的关系标注（adapted from / a (modified) version of / revised version of）；改编透明：改编后的条目原文/锚点/反向计分说明完整给出；单题/多题测量取舍论证完整（Although single-item → nevertheless reliance → As such, supplemented → Further, another gap → 再补充）；同一构念的多版本作为内部复制因素显式声明 |

### 维度 4：指代与承接清晰性（对应 checklist §四，共 7 子节 / 29 项）

> **诊断核心问题**：代词的先行项是否明确可定位？符号体系是否前后一致？引用位置是否紧跟所归属的方法/语句处？跨章节交叉引用是否清晰？跨实验指代是否衔接？句法层面的承接是否自然？

| 子节 | 关键判定 |
|------|----------|
| 4.1 代词的先行项明确 | 首次引入术语时即给缩写与全称（henceforth also referred to as the target person / hereafter referred to as X）；跨段落指代同一概念时使用一致术语，不中途切换近义表达；代词 it / they / this 的先行项在本句或上一句明确可定位；多义词在上下文中通过同位语/of-短语明确化 |
| 4.2 符号体系的一致性 | 路径分析/中介模型使用稳定的 X / M / Y 符号，三符号在叙述中前后一致（Haider 样板）；数学符号 λ / β / Δ 等与文字描述双向对应（March 细菌生长曲线样板）；缩写首次出现给全称，后续段落直接用缩写不重复展开；同一变量在不同模块使用同一名称 |
| 4.3 引用位置的承接 | 引用 reference 紧跟所归属的方法/语句处（X et al., 2010 直接接在 adapted from X et al. 之后），不全部堆放句末；引用格式符合目标期刊（作者-年份制 vs 编号制）；方法描述与既有文献关系明确三分：完全相同（as described by/in）/ 相似（adapted from）/ 显著不同（unlike, instead of）；改编/调整的具体差异点显式列出（with the following modifications / except for / with some changes）；引用既承担「定位出处」又承担「承认前人贡献」 |
| 4.4 跨章节交叉引用 | 测量用途指向具体分析章节（partners' responses... (see discriminant analyses section)）；程序中嵌入的指导语原文化呈现并清晰标注（adapted from Cikara et al., 2014）；Analysis 部分对 Measures / Procedure 的引用回到具体子模块名称，不使用「上述方法」的模糊指代；Supplemental Materials 在正文 Method 中显式引用 |
| 4.5 跨实验/跨研究的指代衔接 | 系列实验中复用材料/程序以回指短语承接（as in Experiments 1a–1c / as described above / using the same measures）；跨研究复用样本以回指短语承接（the final sample of Study 3 / as in Studies 1–c）；系列实验的变量命名、缩写、量表锚点完全一致 |
| 4.6 句法层面的承接 | 长句首部与前句尾部在指代上衔接；where / which / that 引导的定语从句的先行词在前句清晰可定位；介词短语 of / with / for 的链式嵌套不超过三层；数据呈现（n = / α = / M = SD =）与所修饰变量在同一句内直连；表格/图中的变量名与正文叙述使用同一全称或同一缩写 |
| 4.7 综述与决策的承接 | 综述既有方法时使用综述连接词（have shown / documented / previously reported / found that）；由综述衔接到本研究选择时显式标注（However / Nevertheless / As such / Therefore / Based on...）；决策取舍的两端都给出（A 的优势 → 但 A 的不足 → 因此选 B），不单向陈述；「本研究的目的」与「前人未解决的问题」显式绑定 |

---

## 三、执行步骤（6 步）

```
Step 1 读取规则 → Step 2 扫描文本 → Step 3 对照核验 → Step 4 计算得分 → Step 5 匹配正例 → Step 6 输出结果
```

### Step 1 — 读取规则

加载以下 4 份规则文件至内存：
- `references/checklist.md`（4 大维度 / 29 子节 / **117 项 `- [ ]`**）
- `references/rubric.md`（严重 / 中等 / 轻微扣分区间 + A/B/C/D/F 等级表 + 降档规则）
- `references/examples/positive/` 正例库（37 个 `.md` 文件，按文件名 `cohesion_<Author>_<Year>_<n>.md` 索引；n 为该文献片段序号）
- 教材 Unit 2 §2.4.2 核心论点锚点（见第一节表末）

构建内存映射表：`{checklist_id → (severity, score_range, positive_examples[])}`。

### Step 2 — 扫描文本

按 Method 节实际段落顺序（Participants / Design / Measures / Procedure / Analysis），逐段扫描。建议扫描粒度：
- **一段 = 一个聚合扫描单元**（用于检测段落入口句、总-分结构、模块间过渡、系列实验复用结构）
- **一句 = 一个细分扫描单元**（用于检测时序衔接词类型与搭配、对比/因果/让步连接词、引用位置、符号一致性、代词先行项）

扫描时同步记录：

| 扫描字段 | 用途 |
|---------|------|
| 时序衔接词类型（Group 1–8） | 维度 1（精确区分短时距 / 长时距 / 同时性 / 收尾） |
| 程序步骤链是否按时间顺序排列 | 维度 1.3 + 1.9（步骤顺序 + 刺激时序） |
| 跨段连接词（递进 / 对比 / 回指 / 结构） | 维度 2.2 + 2.3 |
| 段内是否连续多句无衔接词堆砌 | 维度 2.4 |
| 图/表/公式的引导句与编号顺序 | 维度 2.6 |
| 子模块标题命名与排列 | 维度 3.2 |
| 分析方案步骤与目的对应 | 维度 3.3 |
| 排除漏斗的时序与理由 | 维度 3.4 |
| 系列实验「基线 + 差异清单」结构 | 维度 3.5 |
| 控制变量的入选理由与句法平行性 | 维度 3.6 |
| 测量决策链的取舍论证 | 维度 3.7 |
| 代词的先行项定位 | 维度 4.1 |
| 符号体系（X/M/Y / λ）的一致性 | 维度 4.2 |
| 引用位置（紧跟所归属语句 vs 句末堆叠） | 维度 4.3 |
| 跨章节交叉引用与回指短语 | 维度 4.4 + 4.5 |
| 介词短语嵌套层数 | 维度 4.6 |
| 综述—决策的承接链 | 维度 4.7 |

### Step 3 — 对照核验

每发现一处违例，按以下逻辑归类：

```
1. 在 checklist 中找到对应的 `- [ ]` 项（按 checklist_id，如 1.3-a / 2.4-a / 3.4-a / 4.3-a）
2. 在 rubric 中确定 severity（严重 / 中等 / 轻微）
3. 在 rubric 扣分区间内取具体分数（按违例严重度在该区间内）
4. 同项多处违例按 N × 单项扣分累计，但单处封顶区间内高值
5. 一处违例触发多规则 → 按最严重等级判定一次，不重复扣分
```

**严重性判定核心问题清单**（按重要性排序）：

| 关键问题 | 严重等级触发 |
|---------|--------------|
| 步骤未按实际执行的时间顺序排列（前后颠倒） | **严重**（rubric §1.3-a，−15） |
| 视频/音频等动态刺激缺少精确秒数标注，时间轴不完整 | **严重**（rubric §1.9-a，−12） |
| 改编范式未用 (a)/(b)/(c)/(d) 或子步骤嵌套呈现，时长与衔接规则缺失 | **严重**（rubric §1.9-b，−11） |
| 排除流程未按时间漏斗顺序，最终样本缺少逐条理由 | **严重**（rubric §3.4-a，−12） |
| 段内连续多句以句号断开而无任何衔接词堆砌 | **严重**（rubric §2.4-b，−11） |
| 系列实验未采用「基线 + 差异清单」结构，差异条目缺失 | **严重**（rubric §3.5-a，−10） |
| 分析方案总览段未以「We first / We then / We used / Lastly」四步或五步概括三步骤以上分析 | **严重**（rubric §3.3-a，−10） |
| Method 起首未重述研究目标/缺口 | **严重**（rubric §3.1-a，−11） |
| 程序总起句未明确「第一步是什么」（first / firstly / at first / at the beginning） | **严重**（rubric §1.2-a，−10） |
| 最终样本、最终数据集、最终得分未在收尾处给出 | **严重**（rubric §1.7-b，−10） |
| 图/表编号与正文叙述顺序不一致（图 1 在图 2 之后被引用） | **严重**（rubric §2.6-d，−10） |

仅影响衔接词多样性或表述流畅性 → 中等；仅措辞优化、术语一致性细节 → 轻微。

### Step 4 — 计算得分

```
原始得分 = 100 − Σ(各处扣分)
最终等级 = A (90–100) / B (80–89) / C (70–79) / D (60–69) / F (<60)
强制 D = 严重违例 ≥ 3 处
强制 F = 总分 < 60
封底 = 0 分（扣分上限 100 分）
```

详见 `references/rubric.md` 第五节「评分档位说明」与第六节「评分使用提示」。

### Step 5 — 匹配正例

按本 Skill 第四节「正例调用规则」从 `references/examples/positive/` 中匹配正例。匹配成功后读取该正例文件，提取「原文片段 / 来源文献 / 适配诊断点」三段内容。

### Step 6 — 输出结果

按本 Skill 第五节「输出格式」的固定模板输出诊断报告。模板含 **4 个必备模块**：
1. 维度得分表
2. 整体评价
3. 核心问题（按严重度排序 + 修改建议 + 顶刊正例）
4. 优化建议

---

## 四、正例调用规则

### 4.1 触发条件

| 违例等级 | 是否调用正例 |
|----------|--------------|
| **严重** | **必须调用 1 个**（步骤时序混乱 / 不可复现 / 模块跳转突兀） |
| **中等** | **每个维度最多 2 个**（避免正例轰炸） |
| **轻微** | **不调用正例**（仅在「优化建议」中归类汇总） |
| 无违例 | 不调用正例 |
| **用户显式要求** | 不论等级均调用（如「请给顶刊参考」「需要范例」） |

### 4.2 匹配逻辑（按诊断用途四分类 → 文件名映射）

正例库按「**时序衔接样板 / 段落过渡范式 / 模块连贯示范 / 指代承接样板**」四类诊断用途归组，运行时按以下主路径匹配：

**主路径**（按 checklist 检查项编号匹配）：

| 违例所在子节 | 优先匹配正例（`examples/positive/` 下） | 诊断用途 |
|--------------|-----------------------------------------|----------|
| §1.1–1.2 时间参照点 / 起首步骤 | `cohesion_Buttner_2024_4.md`、`cohesion_Micheli_2023_5.md`、`cohesion_Werchan_2024_6.md` | "first...Then...Next" 时序链起首；"Upon consenting" 句式；"Prior to the task" 预备环节 |
| §1.3 步骤顺序 | `cohesion_Damian_2018_4.md`、`cohesion_Verhoef_2023_4.md`、`cohesion_Wang_2022_5.md`、`cohesion_Kardas_2021_4.md` | First/Second/Third/Fourth/Fifth 五步链；Purpose 从句起句；(a)(b)(c)(d) 分阶段；"After reading...were then..." 时序链 |
| §1.5 后段/长时距 | `cohesion_Thielmann_2025_5.md`、`cohesion_Carpenter_2019_5.md`、`cohesion_Vilanova_2022_6.md` | At T0/T1/T2/Finally 多波次回扣；Phase 1→2→3 → 时长 → 间隔；三步排除漏斗 |
| §1.6 同时性/接口 | `cohesion_Thiele_2025_4.md`、`cohesion_McLean_2019_4.md` | "Initially...before...resulting in...Then...again" 显式时间链；"trained...completed reliability...coded the remaining...met to resolve" |
| §1.9 刺激/材料时序 | `cohesion_Thiele_2025_4.md`、`cohesion_Wang_2022_5.md` | 十一秒视频模板（精确秒数 + 重复模式 + 中性规则）；(a)-(d) 分阶段 + 括号内时间点差异 + 哭闹应急规则 |
| §2.1 段首句与总-分 | `cohesion_McLean_2019_4.md`、`cohesion_Gaesser_2019_4.md`、`cohesion_Urban_2024_4.md` | 总-分结构（训练→信度→编码→分歧解决）；"We then provided...cover-story"；假设→图→step by step |
| §2.2 跨段递进连接 | `cohesion_Asaba_2025_4.md`、`cohesion_Rudert_2023_5.md`、`cohesion_Gao_2025_4.md` | First/Second 跨段编号；"identical to Study 3, with the following changes: First...Second..."；"Building on the established measurement model" |
| §2.3 段落间逻辑承接 | `cohesion_Phillips_2021_4.md`、`cohesion_Altgassen_2025_4.md`、`cohesion_Benitez-Agudelo_2025_4.md`、`cohesion_Urban_2024_4.md` | Although→nevertheless→As such→Further 让步转折链；Comparable to→However→Therefore 因果链；While→provide→chosen for 取舍论证；such a way that...→step by step 假设-推导链 |
| §2.4 段内衔接颗粒度 | `cohesion_Abramson_2024_4.md`、`cohesion_Damian_2018_4.md` | To assess→we first examined→assumes→In contrast→Accordingly→whereas 约束链；First...Second...Third...Fourth...Fifth 编号链 |
| §2.5 主题切换 | `cohesion_Petsko_2022_5.md`、`cohesion_Vail_2023_4.md` | "Beyond the facial stimuli...two conversation topics were developed" 平滑切换；"Next...This procedure is based on research finding that..." 理论解释衔接 |
| §2.6 图/表衔接 | `cohesion_Gao_2025_4.md` | Figure 2 illustrates 路径图 + Table 4 details 假设汇总 + "Summarizing the major results" 过渡 |
| §3.2 子模块间过渡 | `cohesion_Entringer_2026_4.md`、`cohesion_Park_2019_6.md` | 中介变量引入由研究问题驱动；partners' vs participants' 数据来源分流 + 指向具体分析章节 |
| §3.3 分析方案内部 | `cohesion_Verhoef_2023_4.md`、`cohesion_Damian_2018_4.md`、`cohesion_Diaz-Guerra_2026_4.md`、`cohesion_Olaru_2023_4.md` | First/Second/Third/Fourth/Lastly 五步 + 每步目的从句；First→Second→Third→Fourth→Fifth 编号链；data import→wrangling→effect sizes→meta-analyses→p-adjust 管线顺序；"We first tested...We then used..." 总览 + "We provide a more detailed description below" 铺垫 |
| §3.4 排除/筛选漏斗 | `cohesion_Vilanova_2022_6.md`、`cohesion_vanScheppingen_2020_5.md` | Initially/However/Afterward/Then/Finally/Hence 漏斗时序链；Because→may differ→Therefore→逐变量量化比较选择效应自查 |
| §3.5 系列实验模块间 | `cohesion_Rudert_2023_5.md`、`cohesion_Asaba_2025_4.md`、`cohesion_Zhou_2016_4.md` | "identical to Study 3, with the following changes: First...Second..." 复用 + 差异清单；"similar to Experiments 1a and 1b" 跨实验对照；2A/2B/3/4 一致句式 |
| §3.6 控制变量与对照条件 | `cohesion_Landis_2022_5.md`、`cohesion_Kteily_2016_5.md`、`cohesion_Zhou_2016_4.md` | "To control for the possibility that..." 入选理由 + "Although...so we included it" 论证；"As a manipulation check" 显式标注；whereas / a parallel question 句法平行 |
| §3.7 测量决策链 | `cohesion_Phillips_2021_4.md`、`cohesion_Petsko_2022_5.md`、`cohesion_Benitez-Agudelo_2025_4.md`、`cohesion_Le_2024_4.md` | 单题→多题→故意性多维补充 + α/.88/.71 + r = .45 交叉相关；"internal replication factor, much like..." 复用逻辑；While→provide→chosen for 取舍；工具→效度证据→计分规则→α 顺序 |
| §4.1 代词先行项 | `cohesion_Micheli_2023_5.md` | "henceforth also referred to as the target person" 缩写 + 全称首次引入 |
| §4.2 符号体系一致性 | `cohesion_Haider_2022_6.md`、`cohesion_March_2021_5.md` | X/M/Y 三角色 + Baron & Kenny (a)(b)(c)；λ 符号双向对应（细菌曲线 → TICC） |
| §4.3 引用位置 | `cohesion_Le_2024_4.md`、`cohesion_Wang_2022_5.md` | Fazio et al. (2021) 紧跟任务来源；Murray et al.'s (2008) 紧跟 adapted from |
| §4.4 跨章节交叉引用 | `cohesion_Park_2019_6.md`、`cohesion_Gaesser_2019_4.md`、`cohesion_Olaru_2023_4.md` | "(see discriminant analyses section) / (see alternative explanations section)"；"adapted from Cikara et al., 2014" 指导语原文化；"We provide a more detailed description below" 铺垫 |
| §4.5 跨实验指代 | `cohesion_Kardas_2021_4.md`、`cohesion_Asaba_2025_4.md`、`cohesion_Altgassen_2025_4.md`、`cohesion_Zhou_2016_4.md` | "on similar 11-point scales as in Experiments 1a–1c"；"in the previous experiments / In the current experiment"；"Comparable to Study 2"；跨实验 Qualtrics 模板一致句式 |
| §4.7 综述与决策承接 | `cohesion_Benitez-Agudelo_2025_4.md`、`cohesion_vanScheppingen_2020_5.md`、`cohesion_Landis_2022_5.md` | 测量方式→量表细节→金标准对比→选择理由；潜在偏差→后果→对照检验→量化比较；"Although...does not predict...so we included it" 决策论证 |

**回退路径**（主路径无匹配时）：

1. 扫描所有正例文件的「适配诊断点」段，匹配违例类型关键词：
   - 时序衔接：`prior to` / `subsequently` / `initially` / `finally` / `Meanwhile`
   - 段落过渡：`First` / `Next` / `Building on` / `However` / `Therefore` / `Hence`
   - 模块连贯：`identical to` / `adapted from` / `Building on` / `Compared to`
   - 指代承接：`henceforth` / `see` / `as described in` / `as in Studies`
2. 提取关键词出现 ≥ 2 次且与当前违例类型语义相关的正例 1 个。
3. 若仍无匹配，跳过正例引用，仅在「修改建议」中给出方法学改写模板。

**优先级冲突时**：
- 优先文件名较新者（年份大者）
- 同年优先编号靠后者（编号越大适配诊断点越细）
- 同年同号优先文件名较短者

### 4.3 展示要求

每条命中的正例在「核心问题」模块中按以下三行格式展示：

```
**顶刊正例**：[Author Year] [Brief title]. [Journal], [Vol/Issue], [Pages].
**原文片段**：[截取 50–150 字核心句段，含必要的上下文]
**适配诊断点**：[从正例「适配诊断点」段选 1–2 条最相关的]
```

引用要求：
- 作者名用「姓 + 年」格式（Damian 2018 / Verhoef 2023 / Phillips 2021 / Abramson 2024）
- 不省略期刊名（缩写或全称皆可，但需在第一次出现时给出全称）
- 片段前标注引用句首（如「Method 段 Design 子节第二段」「Studies 1a and 1b Method (Procedure)」）
- **不二次分发正例原文**：每份正例节选不超过 5 句；单报告引用正例不超过 3 份

### 4.4 正例目录维护

- **正例库**：37 个 `.md` 文件，软链至 `D:\method-skill-project\02-positive_examples\cohesion\`
- **文件名规范**：`cohesion_<Author>_<Year>_<n>.md`（n 为该文献片段序号，4/5/6 表明片段位于第几个子节）
- **正例结构**：四段式——① 片段类型（含衔接诊断用途）② 原文片段 ③ 来源文献 ④ 适配诊断点
- **典型正例**：
  - `cohesion_Damian_2018_4.md` — First / Second / Third / Fourth / Fifth 五步分析方案显式编号链（维度 1.3 + 2.4 + 3.3 样板）
  - `cohesion_Verhoef_2023_4.md` — First/Second/Third/Fourth/Lastly + 每步目的从句 to distinguish / to examine / to scrutinize（维度 1.3 + 3.3 样板）
  - `cohesion_Phillips_2021_4.md` — Although → nevertheless → As such → Further 单题→多题→故意性多维补充链（维度 2.3 + 3.7 样板）
  - `cohesion_Rudert_2023_5.md` — "Materials and procedures were identical to Study 3, with the following changes: First...Second..." 系列实验「基线 + 差异清单」结构（维度 3.5 样板）
  - `cohesion_Vilanova_2022_6.md` — Initially / However / Afterward / Then / Finally / Hence 排除漏斗时序链（维度 1.5 + 3.4 样板）
  - `cohesion_Thiele_2025_4.md` — 视频刺激 "Initially...before...resulting in...Then...again...was repeated for two more times, ending in..." 精确秒数模板（维度 1.9 样板）
  - `cohesion_Abramson_2024_4.md` — To assess → we first examined → assumes → In contrast → Accordingly → whereas 约束链（维度 2.4 样板）
  - `cohesion_Landis_2022_5.md` — "To control for the possibility that...Although...does not predict...so we included it..." 控制变量入选理由（维度 3.6 样板）
  - `cohesion_Haider_2022_6.md` — X/M/Y 三角色 + Baron & Kenny (a)(b)(c) 路径分析符号体系（维度 4.2 样板）
  - `cohesion_Park_2019_6.md` — "(see discriminant analyses section) / (see alternative explanations section)" 跨章节交叉引用（维度 4.4 样板）
- **建立软链**（已完成）：
  ```powershell
  # Windows PowerShell（已在本 Skill 创建时执行）
  New-Item -ItemType Directory -Path "D:\method-skill-project\03_skills_output\method-cohesion-diagnostic\references\examples" -Force
  New-Item -ItemType Junction -Path "D:\method-skill-project\03_skills_output\method-cohesion-diagnostic\references\examples\positive" -Target "D:\method-skill-project\02-positive_examples\cohesion"
  ```
- **索引文件**：建议建立 `_INDEX.md`（人读）+ `_INDEX.json`（机读），按本 Skill 4 大维度 / 29 子节归组正例（可选，当前 sibling skill 未强制）

---

## 五、输出格式（固定模板）

诊断完成后，**必须**按以下模板输出。模板中 `[…]` 为占位符，需替换为实际诊断结果。

```markdown
# Method 部分「衔接与连贯」诊断报告

**被检文本**：[文件名 / 段落定位，如 "Study 1 Method 节"]
**诊断时间**：[ISO 日期]
**诊断依据**：Science Research Writing §2.4.2（八组序列词 + 因果/对比连接词）+ checklist.md（117 项）+ rubric.md（严重/中等/轻微三档）+ 顶刊正例 37 例

---

## 1. 维度得分

| 维度 | 检查子节数 | 检查项数 | 违例数（严重/中等/轻微） | 扣分 | 得分 |
|------|------------|----------|--------------------------|------|------|
| 1. 时序衔接准确性 | 9 | 28 | x / x / x | x | x |
| 2. 段落过渡自然性 | 6 | 24 | x / x / x | x | x |
| 3. 模块间逻辑连贯性 | 7 | 36 | x / x / x | x | x |
| 4. 指代与承接清晰性 | 7 | 29 | x / x / x | x | x |
| **合计** | **29** | **117** | **x / x / x** | **x** | **x / 100** |

---

## 2. 整体评价

**等级**：[A / B / C / D / F]
**一句话总结**：[例如："时序衔接整体可读但程序总起句未明确第一步；段落过渡依赖读者脑补；模块间跳转突兀；图表引用顺序错乱。"]

---

## 3. 核心问题（按严重程度排序）

### 3.1 严重违例（必须修改，否则方法节不可复现）

#### 问题 1：[违例类型简述，如 "步骤未按实际执行的时间顺序排列（前后颠倒）"]
- **位置**：[段落 / 句编号，如 "Procedure 子节第 3 句"]
- **原文**：`[原句引用]`
- **违例类型**：checklist §[1.3-a] + rubric §[1.3-a]
- **严重程度判定依据**：[说明为何该顺序使读者无法重建实验；引用教材 §2.4.2 "Words like then or next describe the order of events, but they don't provide information about how long each step took or how soon the next step occurred"]
- **扣分**：[15 分]
- **修改建议**：[具体改写方案，给出 2–3 种备选]
  - 方案 A（编号化）：`First, ... Second, ... Third, ... Finally, ...` → 显式分步，每步以目的状语起句
  - 方案 B（精确序列词）：用 prior to / subsequently / finally 替代 then/next 等口语化衔接词
  - 方案 C（总-分结构）：先总述流程框架（"The procedure consisted of three phases"）再分步展开
- **顶刊正例**：
  - [Author Year] [Brief title]. [Journal], [Vol], [Pages].
  - **原文片段**：`[...]`
  - **适配诊断点**：[1–2 条]

#### 问题 2：[违例类型简述，如 "视频刺激时序未标注精确秒数，时间轴断裂"]
- **位置**：[段落 / 句编号]
- **原文**：`[原句引用]`
- **违例类型**：checklist §[1.9-a] + rubric §[1.9-a]
- **严重程度判定依据**：[说明为何缺秒数使刺激无法复现]
- **扣分**：[12 分]
- **修改建议**：
  - 方案 A（精确秒数）：`Each video lasted 11 s: Initially, both actors looked at the object (1 s), before moving their heads...`
  - 方案 B（重复模式 + 总时长）：`This pattern was repeated for two more times, ending in a moment of eye contact (1 s). The total duration was 11 s.`
  - 方案 C（应急规则嵌入）：`If the toddler cried during the pick-up phase, the toddler would be put down...`
- **顶刊正例**：
  - [Author Year] [Brief title]. [Journal], [Vol], [Pages].
  - **原文片段**：`[...]`
  - **适配诊断点**：[1–2 条]

#### 问题 3：[违例类型简述，如 "系列实验未采用「基线 + 差异清单」结构"]
- **位置**：[段落 / 句编号]
- **原文**：`[原句引用]`
- **违例类型**：checklist §[3.5-a] + rubric §[3.5-a]
- **严重程度判定依据**：[说明为何重复完整程序导致读者无法快速识别改动点]
- **扣分**：[10 分]
- **修改建议**：
  - 方案 A（基线 + 差异清单）：`Materials and procedures were identical to Study X, with the following changes: First, ... Second, ...`
  - 方案 B（每条差异 + 动机）：差异条目逐条编号，并附改动动机（neutralize gender cues / add control condition）
  - 方案 C（跨研究复用回指）：`We used the same procedure as in Study X (see Method of Study X for details).`
- **顶刊正例**：
  - [Author Year] [Brief title]. [Journal], [Vol], [Pages].
  - **原文片段**：`[...]`
  - **适配诊断点**：[1–2 条]

### 3.2 中等违例（修改后可投稿）

#### 维度 1（时序衔接准确性）

- [问题摘要 1 + 位置 + 修改要点 + 顶刊正例（如有）]
- [问题摘要 2 + 位置 + 修改要点 + 顶刊正例（如有）]

#### 维度 2（段落过渡自然性）

- [问题摘要 1 + 位置 + 修改要点 + 顶刊正例（如有）]
- [问题摘要 2 + 位置 + 修改要点 + 顶刊正例（如有）]

#### 维度 3（模块间逻辑连贯性）

- [问题摘要 1 + 位置 + 修改要点 + 顶刊正例（如有）]
- [问题摘要 2 + 位置 + 修改要点 + 顶刊正例（如有）]

#### 维度 4（指代与承接清晰性）

- [问题摘要 1 + 位置 + 修改要点 + 顶刊正例（如有）]
- [问题摘要 2 + 位置 + 修改要点 + 顶刊正例（如有）]

### 3.3 轻微违例（仅归类，不逐一展开）

- 维度 1：x 处（短时距 / 长时距副词混用 / 后续延伸词缺失）
- 维度 2：x 处（段内最小化承接词不足 / 主题切换显式过渡缺失）
- 维度 3：x 处（控制变量入选理由简短 / 测量决策链取舍论证局部省略）
- 维度 4：x 处（缩写首次出现未给全称 / 介词短语嵌套过深 / 符号双向对应局部缺失）

---

## 4. 优化建议（按优先级）

1. **[优先级 P0 — 严重]** [严重违例整改路径，如"对程序步骤重排时序 + 视频刺激补精确秒数 + 系列实验改用「基线 + 差异清单」结构"]
2. **[优先级 P1 — 中等]** [中等违例整改路径，如"统一分析方案编号 + 排除漏斗补逐条理由 + 控制变量入选理由补全 + 跨段连接词多样化"]
3. **[优先级 P2 — 轻微]** [轻微违例整改路径，如"段内补最小化承接词 + 介词短语嵌套不超过三层 + 缩写首次出现给全称"]
4. **[目标期刊对齐]** [如"JPSP 偏 First/Second/Third 显式编号链，PSP 偏 tighter 衔接，需根据投稿目标调整"]
5. **[后续步骤]** [如"修改 1 轮后建议再次调用本 Skill 复检，确保降档规则不再触发；同时建议配合 method-logic-diagnostic 复检方法选择论证、method-structure-diagnostic 复检结构完整性、method-grammar-diagnostic 复检时态/被动"]

---

## 附录 A：诊断依据回链

- 参考教材：《Science Research Writing》(2nd ed.) Unit 2「How to Write about Methods」**§2.4.2**（SEQUENCE LANGUAGE 八组 Group 1–8 + JUSTIFY CHOICES + CAUSE and RESULT + CONTRAST）；§2.2.3 Generic Methods Model 六模块
- 检查清单：`references/checklist.md`（4 大维度 / 29 子节 / 117 项）
- 评分细则：`references/rubric.md`（严重 / 中等 / 轻微三档 + A/B/C/D/F 等级）
- 顶刊正例：`references/examples/positive/`（37 例，含 JPSP / JEP:G / Developmental Psychology / PSPB / OBHDP 等）

## 附录 B：未触发项目（完整性自检）

列出未触发任何违例的 checklist 子节，证明诊断覆盖完整：
- §1.1 时间参照点（Group 1）：未发现违例
- §1.4 短时距（Group 4）：未发现违例
- §1.6 同时性/接口（Group 6）：未发现违例
- §2.1 段首句与总-分结构：未发现违例
- §3.2 子模块间过渡：未发现违例
- §4.1 代词的先行项明确：未发现违例
- ...（按 checklist 顺序列出无违例子节）
```

---

## 六、使用约束

1. **本 Skill 仅诊断，不改写**：所有输出均以「问题定位 + 修改建议」形式给出，最终改写由人类作者完成，避免 AI 改写引入新错误。
2. **清单-细则严格对应**：rubric 中每一条扣分规则都能在 checklist 中找到对应 `- [ ]` 项；任何 rubric 单独新增项均视为误植。
3. **严重违例强制降档**：即便总分 ≥ 90，只要存在 1 处严重违例即降至 B；≥ 3 处严重违例强制 D；总分 < 60 强制 F。
4. **不跨维度诊断**：本 Skill 仅处理「衔接与连贯」维度；结构、逻辑、语法、词汇维度请调用 sibling skill：
   - 结构 → `method-structure-diagnostic`
   - 逻辑 → `method-logic-diagnostic`
   - 语法 → `method-grammar-diagnostic`
   - 词汇 → `method-vocabulary-diagnostic`
   - 规范 → `method-conventions-diagnostic`
5. **正例库只读**：禁止修改 `references/examples/positive/` 下的 `.md` 文件；如需新增正例，请修改源目录 `D:\method-skill-project\02-positive_examples\cohesion\` 并重新建立软链。
6. **教材-清单-细则三对齐**：本 Skill 的所有判定逻辑必须能回溯至 §2.4.2（SEQUENCE LANGUAGE 八组词汇 + CAUSE and RESULT 动词 + CONTRAST 连接词 + JUSTIFY CHOICES 词族）、§2.2.3（Generic Methods Model 六模块）；任何诊断结论若无法引用教材原文锚点即视为误判。
7. **时序准确性优先级最高**：本 Skill 对「步骤是否严格按时间顺序叙述」检查（§1.3）优先级等同于「刺激时序是否完整可复现」（§1.9）——时序混乱或步骤颠倒会让读者完全无法重建实验，必须按 rubric §1.3-a 顶档扣分（−15）。
8. **段落堆砌优先处理**：本 Skill 对「段内连续多句无衔接词堆砌」（§2.4-b）检查优先级仅次于时序准确性——会让阅读完全断裂，扣分按 rubric §2.4-b（−11）严格执行。

---

**版本**：v1.0（与 checklist.md、rubric.md 同步）
**配套**：本目录下 `references/checklist.md`（检查清单）、`references/rubric.md`（评分细则）、`references/examples/positive/`（顶刊正例 37 例），四者一一对应、不得拆分使用。