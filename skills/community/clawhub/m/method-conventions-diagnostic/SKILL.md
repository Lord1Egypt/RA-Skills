---
name: method-conventions-diagnostic
version: 1.0.0
description: 诊断心理学论文Method部分的学术规范问题，检查引用标注、伦理声明、格式惯例，输出评分与顶刊正例参考
metadata:
  domain: psychology-academic-writing
  dimension: conventions
  source: Science_Research_Writing_2nd_edition_Unit_2_sections_2.2_to_2.5
  companion_skills: [method-structure-diagnostic, method-logic-diagnostic, method-cohesion-diagnostic, method-grammar-diagnostic, method-vocabulary-diagnostic]
user-invocable: true
---

# Method 部分「学术规范」诊断 Skill

> 覆盖《Science Research Writing》(2nd ed.) **Unit 2**「How to Write about Methods」**§2.2–2.5** 关于**引用标注规范**（引用位置 + Option 1/2/3 现有方法标注三档 + 主动/被动语态归属判定）、**伦理与透明声明**（IRB 编号 + 知情同意 + TOP/JARS 标准）、**术语与格式惯例**（缩写、单位、数字、量表锚点、符号体系）的全部规则，专用于心理学实证论文 Method 节的**学术规范维度**诊断。
>
> **核心立场**：Method 节的学术规范 = **引用归属清晰 + 现有方法标注准确 + 伦理与透明声明完整 + 术语格式高度一致**四维联动。诊断目的：判断作者的**引用是否让他人背负本研究工作**、**Option 1/2/3 标注是否归类正确**、**伦理与 TOP 声明是否齐备**、**格式惯例是否前后一致**。

---

## 一、诊断依据

本 Skill 的全部判定逻辑基于以下 **4 项不可拆分** 的依据，运行时按顺序加载：

| # | 依据 | 路径 | 用途 |
|---|------|------|------|
| 1 | **参考教材** | `D:\method-skill-project\01-reference\Science_Research_Writing_Methods.pdf` Unit 2（66 页） | §2.4.2 Option 1/2/3 现有方法标注三档（p.109–110）+ by/in 介词搭配（p.109 注释）+ 引文位置规则（p.11）+ 不得让前人背负本研究工作（p.85）+ "the difference may represent the key contribution"（p.84）；§2.2.3 Generic Methods Model 六模块（p.88）；§2.4.2 GIVE THE SOURCE 短语族（p.100：were obtained from / was a kind gift from / was purchased from）+ CAUSE/RESULT + CONTRAST 词族；§2.5.1 主动/被动语态归属判定（p.113–115：agentless passive + Past Simple vs Present Simple） |
| 2 | **检查清单** | `references/checklist.md` | **4 大维度 / 21 子节 / 67 项 `- [ ]`**（引用格式与标注规范性 26 项 + 现有方法改编说明准确性 27 项 + 伦理与透明声明完整性 37 项 + 术语与格式一致性 26 项 + 附录完整性自检 5 项），作为违规定位与命中判定的对照表 |
| 3 | **评分细则** | `references/rubric.md` | 严重 / 中等 / 轻微三档扣分（**10–15 / 5–9 / 1–4 分/处**）+ A/B/C/D/F 五档等级（90/80/70/60/<60）+ **强制降档规则**（严重问题 ≥3 处强制 D，<60 强制 F）+ 165 扣分点与 checklist 严格一一对应 |
| 4 | **顶刊正例** | `references/examples/positive/` | **51 个 `.md` 文件**，软链至 `D:\method-skill-project\02-positive_examples\conventions\`，含 JPSP / JEP:G / Developmental Psychology / PSPB / OBHDP / BMC Psychology / Behavioral Sciences 等顶刊 Method 节规范片段，按「**引用归属样板**」「**Option 1/2/3 标注范式**」「**伦理与 TOP 声明范本**」「**格式惯例样板**」四类诊断用途归组 |

> **教材原文摘录锚点**（用于本 Skill 内部一致性自检）：
> - §2.4.2 Option 1 短语族："according to / as described by/in / as detailed by/in / as explained by/in / as in / as proposed by/in / as reported by/in / as reported previously / as suggested by/in / can be found in / described elsewhere / details are given in / following x et al. / given by/in / identical to / in accordance with / previously shown in/by / the same as that of/in / using the method of/in"（教材 p.109）
> - §2.4.2 Option 2 短语族："a (modified) version of / adapted from / almost the same as / based on / essentially identical / essentially the same / except for/that / largely the same / more or less identical / partly based on / practically the same / similar (to) / slightly modified / virtually the same"（教材 p.109）
> - §2.4.2 Option 3 短语族："a novel step was / adapted from / although in many ways similar / although similar to / based on / except for/that / instead (of) / loosely based on / partly based on / unlike / with the following modifications"（教材 p.110）
> - §2.4.2 引文位置："**Remember that citation references do not automatically go at the end of a sentence**"（教材 p.11）；"**you need to be particularly careful about the location of your citation references or [you might] accidentally credit someone with work they have not done — perhaps even with your own work**"（教材 p.85）
> - §2.4.2 Option 3 关键贡献："**the difference may represent the key contribution of your study**"（教材 p.84）
> - §2.5.1 主动/被动语态归属："**Science writers generally use an agentless passive verb (was/is found), rather than passive + agent...This type of ambiguity is highly detrimental to the success of your research paper as it risks you losing ownership of your contribution and unknowingly crediting another researcher with all or part of your work**"（教材 p.113）
> - §2.5.1 主动/被动规避方案："**Move to the active: We collected/modified X. / Add words or phrases such as here / in this work / in our model. / Use a 'dummy' grammatical subject such as This experiment / The procedure described above**"（教材 p.114–115）

---

## 二、核心检查项（4 大维度，21 子节，67 项）

依据 `checklist.md` 提炼为以下 **4 个诊断维度**，运行时按此顺序扫描。每个维度下分若干子节，标注与 checklist 的对应关系。

### 维度 1：引用格式与标注规范性（对应 checklist §一，共 4 子节 / 26 项）

> **诊断核心问题**：每条引用是否紧跟所归属的语句？引用位置是否会让他人背负本研究工作？Option 1/2/3 标注是否归类正确？首次出现的缩写是否给全称？

| 子节 | 关键判定 |
|------|----------|
| 1.1 引用位置与归属清晰 | Method 节中每条引用 reference 都紧跟所归属的语句 / 工具 / 程序，不堆放句末或段落末（教材 p.11）；引用位置明确，不会让读者误把前人的工作当作本研究的工作（avoid "accidentally credit someone with work they have not done"，教材 p.85）；既有方法描述后引用紧跟：adapted from / following / according to 直接接在被引用语句旁；数据来源 / 样本来源 / 设备来源的引用紧跟其出处；同一句子内出现多个引用时，引用顺序与研究叙述的时间顺序一致；多引用编号列表按期刊格式编号正确；Option 1/2/3 三档表述后引用位置正确；引用的内容与所引用文献的实际内容一致（避免"虚假引用"） |
| 1.2 引用格式与期刊一致性 | 引用格式与目标期刊的 Guide for Authors 一致（APA 作者-年份制 vs Elsevier 编号制 vs Nature 编号上标）；作者-年份制引用格式正确（单作者 / 双作者 / 三作者及以上）；同一文献全文引用格式一致，不混用 APA / Vancouver / Harvard 等；年份均为发表年份；期刊名缩写符合 ISO 4 标准；DOI / 期刊链接按目标期刊规范附上；二次引用按目标期刊规范处理；个人通讯的引用方式符合规范；数据已发表 / 未发表的标准引用方式使用正确 |
| 1.3 Option 1/2/3 现有方法标注的语法正确性 | Option 1（完全相同）使用 by/in 介词搭配正确：by 引导研究者（as described by Ross），in 引导研究（as described in Ross et al., 2020）（教材 p.109 注释）；Option 1 短语选词正确（according to / as described by/in / as reported by/in / identical to / following / using the method of / same as）；Option 2（相似）使用准确的「改编」短语（adapted from / a (modified) version of / based on / with some modifications / except for/that / essentially the same as）；Option 2 形容词比较级正确（essentially / largely / more or less / virtually / practically the same）；Option 3（显著不同）使用「差异」短语（unlike / instead of / loosely based on / although similar to / with the following modifications）；Option 3 差异点显式陈述（"the difference may represent the key contribution of your study"，教材 p.84）；CONTRAST 连接词（however / whereas / by contrast）作为 Option 3 的辅助手段使用正确；同一方法既引用前人又呈现本研究的「相同 + 差异」并存时，Option 1 与 Option 3 不混用同一短语 |
| 1.4 引用与缩写的全称展开 | 首次出现的机构缩写（IRB / APA / OSF / TOP / JARS）展开全称；首次出现的量表 / 任务 / 软件缩写给出全称与原始文献（PANAS = Positive and Negative Affect Schedule, Watson et al., 1988）；后续段落直接使用缩写，不重复展开；自创缩写（如多研究内的程序名）首次出现给完整命名；术语首次出现给定义或同位语；拉丁语术语（et al. / in vitro / per capita / a priori / post hoc）斜体或不斜体按目标期刊规范 |

### 维度 2：现有方法改编说明准确性（对应 checklist §二，共 5 子节 / 27 项）

> **诊断核心问题**：改编来源是否明确标注？改编的具体差异点是否逐条列出？改编动机是否显式交代？Option 3 显著差异是否被识别为本研究的关键贡献？工具 / 设备 / 材料来源是否完整标注？

| 子节 | 关键判定 |
|------|----------|
| 2.1 改编透明性 | 改编后的方法明确标注改编来源（adapted from / a modified version of）；改编的具体差异点逐条列出（First... Second... Third... 或 (a)(b)(c)）；改编动机 / 理由被显式交代（why adapted: to suit the present sample / to avoid X / to control for Y）；改编是否经过原作者许可 / 是否为开源范式被标注；改编是否在 OSF / 期刊补充材料公开；改编后方法的预注册版本与最终使用版本是否一致被标注 |
| 2.2 Option 2 改编差异点呈现 | with some modifications / with some changes / with some adjustments / with some alterations 短语使用正确；改编差异点单条不超 1–2 句，便于审稿人快速识别；改编差异点按重要程度排序；改编差异点未与原始方法原文混在一起；改编后的测量参数（题目数 / 锚点 / 计分方向）单独交代；改编后的刺激（图片 / 视频 / 文本）来源 + 改编内容明确；改编后的程序时序与原始方法差异被标注 |
| 2.3 Option 3 显著不同的差异论证 | 与现有方法的差异被识别为本研究的关键贡献（教材 p.84 "the difference may represent the key contribution of your study"）；差异的具体表征（材料 / 程序 / 测量 / 理论模型）逐条说明；差异的方法学意义 / 优势 / 改进点被论证（in order to / with the aim of / thereby）；差异点的取舍权衡被显式说明；差异未被夸大（avoid claiming novelty when difference is minor） |
| 2.4 工具 / 设备 / 材料来源标注 | 商品化试剂 / 耗材给出供应商与产地（如 "FBS was purchased from Gibco, UK"；教材 p.100 正例）；自制设备 / 材料说明构造规格（型号 / 尺寸 / 参数）；礼赠来源标注（"a kind gift from Dr. X at Institution Y"，教材 p.100 正例）；学术来源的样本 / 数据集标注来源；数据库引用给出数据库名称 + 访问链接（TEDS / SOEP / Add Health / HRS）；公开刺激库的引用（IAPS / OASIS / Nencki / CASO）按目标期刊规范标注；商业软件版本号完整（"SPSS 26.0" / "R Version 4.3, R Core Team, 2024"，教材正例） |
| 2.5 系列实验的方法继承—修改表达 | 多研究论文中，Study 2/3 引用 Study 1 的方法时使用 "identical to Study 1, with the following changes" 句式；差异清单以 First / Second / Third 编号；每条差异附带改动动机；跨研究复用元素显式回指；跨研究样本口径一致；跨研究的变量命名、缩写、量表锚点完全一致；跨研究分析策略保持家族相似性 |

### 维度 3：伦理与透明声明完整性（对应 checklist §三，共 6 子节 / 37 项）

> **诊断核心问题**：IRB / 伦理委员会批准编号 + 知情同意 + 报酬范围 + 豁免说明是否齐备？TOP / JARS 四要素（样本量 + 排除 + 操纵 + 测量）是否声明？预注册状态 + 链接 + 偏离说明是否透明？数据 / 代码 / 材料三层公开是否声明？功效分析四要素是否齐备？

| 子节 | 关键判定 |
|------|----------|
| 3.1 伦理批准与知情同意 | IRB / 伦理委员会名称 + 批准编号完整给出；知情同意程序被描述；弱势群体（儿童 / 老年人 / 病患）的特殊同意程序被说明；报酬 / 补偿金额范围被报告；报酬与数据完整性的挂钩机制被描述；报酬与预注册标准的挂钩被透明化；伦理豁免说明（如使用公开数据 / 档案数据："we are exempt from an Institutional Review Board approval"，Entringer 正例）；伦理准则声明（Helsinki Declaration / APA Ethics Code / Belmont Report）按目标期刊要求 |
| 3.2 Transparency & Openness Promotion (TOP) 声明 | 单独"Transparency and Openness"段落存在，明确按 JARS（Appelbaum et al., 2018）声明（Altgassen 正例）；样本量确定方式（a priori power / sequential BF / resource constraints）被声明；所有数据排除（all data exclusions）被声明；所有操纵（all manipulations）被声明；所有测量（all measures）被声明；数据（data）公开声明；分析代码（analysis code）公开声明；研究材料（research materials）公开声明；预注册状态如实声明；预注册链接给出；修订预注册（如有）的透明处理；数据 / 代码 / 材料链接的有效性 |
| 3.3 预注册的规范表述 | 预注册内容明确（hypotheses / design / analysis plan / sample size plan）；预注册平台引用规范（AsPredicted.org / OSF / ClinicalTrials.gov）；预注册编号 / 链接完整；"As preregistered, ..." 句式锚定预注册承诺（Buttner / Costin 正例）；与预注册的偏离被显式说明（deviations from preregistration）；偏离原因被合理说明；预注册标签 / 术语修订的脚注式说明；序贯分析设计透明 |
| 3.4 数据与材料可用性声明 | 数据可用性段落或注释；数据 + 代码 + 材料三层公开声明（Damian 正例）；输出文件是否公开；可复现性声明（"necessary to reproduce the results" 用语）；数据库访问政策与申请流程；二手数据 / 公开数据的访问途径清晰；数据限制声明 |
| 3.5 排除 / 筛选 / 样本流程的规范报告 | 排除流程按时间漏斗顺序呈现；排除规则逐条标注理由；排除规则与预注册的对应被说明（"As preregistered, we excluded..."）；排除率合理；选择效应自查；最终样本的人口学完整报告；样本代表性与同质化局限性被显式声明；流失分析（保留者 vs 流失者差异检验） |
| 3.6 功效分析报告 | 先验功效分析要素齐全：目标效应量 + α + 功效 + df / 条件数 + 工具（Gaesser 正例：d = .25, G*Power, Faul et al., 2007）；效应量来源被交代；G*Power / Soper / simr / BUCCS 等工具引用规范；功效分析结果与实际样本量对应（Georgeac 正例）；后验 / 敏感性分析被说明；Monte Carlo 模拟 / 序贯 BF 设计透明报告；功效不足时的最小可检效应量被报告 |

### 维度 4：术语与格式一致性（对应 checklist §四，共 6 子节 / 26 项）

> **诊断核心问题**：学术术语是否精确？缩略语与符号是否全文一致？数字、时间、单位格式是否前后一致？表格 / 图 / 公式格式是否符合目标期刊？标题 / 子标题 / 段落格式是否规范？

| 子节 | 关键判定 |
|------|----------|
| 4.1 学术术语的精确使用 | 心理测量学术语精确（Cronbach's alpha / McDonald's omega / intraclass correlation / composite reliability）；统计术语精确（mean / standard deviation / confidence interval / effect size / p-value）；测量单位统一（ms vs milliseconds / s vs seconds），不混用；量尺锚点统一（1 = strongly disagree, 7 = strongly agree），不跨段落更换锚点；抽样术语精确；研究设计术语精确；样本术语精确（participants / subjects / respondents / patients），不混用；因果语言谨慎使用 |
| 4.2 缩略语与符号体系一致性 | 缩略语首次出现给全称 + 缩写，后续段落直接使用缩写；同一概念全文使用同一缩写，不中途切换；数学 / 统计符号全文一致（X / M / Y / λ / β / Δ / α / ω / η² / Cohen's d）；路径图符号与文字描述双向对应（X / M / Y 角色清晰，Baron & Kenny (a)(b)(c) 一致）；Greek 字母大小写正确；斜体规则正确（统计符号斜体：t / F / M / SD / N；缩写与拉丁语斜体：et al. / i.e. / e.g.）；引号使用规范；大小写规则一致 |
| 4.3 数字、时间、单位的格式 | 数字格式统一（阿拉伯数字 vs 中文数字；小数点 vs 逗号）；千位分隔符按目标期刊规范；样本量 N = 大写斜体（按 APA 规范）；百分比格式一致；时间格式统一（11 s / 11 sec / 11 seconds），全文一致；日期格式按目标期刊规范；货币格式与目标地区一致；温度单位一致；测量单位前后无多余空格 |
| 4.4 表格 / 图 / 公式格式一致性 | 表格格式符合目标期刊；表格内变量名与正文叙述使用同一缩写 / 全称；图编号连续（图 1 / 图 2 / Figure 1 / Figure 2）；公式编号连续（Eq. 1 / Equation 1）；图 / 表 / 公式在正文中的引用顺序与编号顺序一致；图 / 表的脚注 / 标注完整；补充材料（Supplemental Materials）的引用与正文标注一致 |
| 4.5 标题 / 子标题 / 段落格式 | Method 节一级标题与目标期刊一致（METHOD / Method / Methods / MATERIALS AND METHODS）；子标题命名规范（Participants / Design / Measures / Procedure / Analysis / Transparency & Openness）；子标题大小写规范（APA title case vs sentence case）；段落起首缩进 / 不空行按目标期刊规范；段落长度合理（避免一段超过 200 字造成堆砌） |
| 4.6 目标期刊规范符合性 | 全文体例（passive vs active）符合目标期刊主流风格；参考文献列表格式与目标期刊一致（APA 7th vs AMA vs Vancouver）；引用顺序与目标期刊规范一致（alphabetical vs order of appearance）；附录 / 补充材料格式与目标期刊一致；全文作者署名 + 通讯作者 + ORCID iD 标注符合目标期刊；关键词（keywords）数量与格式符合目标期刊 |

---

## 三、执行步骤（6 步）

```
Step 1 读取规则 → Step 2 扫描文本 → Step 3 对照核验 → Step 4 计算得分 → Step 5 匹配正例 → Step 6 输出结果
```

### Step 1 — 读取规则

加载以下 4 份规则文件至内存：
- `references/checklist.md`（4 大维度 / 21 子节 / **67 项 `- [ ]` + 5 项附录自检**）
- `references/rubric.md`（严重 / 中等 / 轻微扣分区间 + A/B/C/D/F 等级表 + **强制降档规则**）
- `references/examples/positive/` 正例库（51 个 `.md` 文件，按文件名 `conventions_<Author>_<Year>_<n>.md` 索引；n 为该文献片段序号）
- 教材 Unit 2 §2.4.2 / §2.5.1 核心论点锚点（见第一节表末）

构建内存映射表：`{checklist_id → (severity, score_range, positive_examples[])}`。

### Step 2 — 扫描文本

按 Method 节实际段落顺序（Participants / Measures / Procedure / Analysis / Transparency & Openness），逐段扫描。建议扫描粒度：
- **一段 = 一个聚合扫描单元**（用于检测 Option 1/2/3 归类、TOP 声明完整性、改编透明性）
- **一句 = 一个细分扫描单元**（用于检测引用位置、缩写全称、术语一致性、量尺锚点、单位格式）

扫描时同步记录：

| 扫描字段 | 用途 |
|---------|------|
| 引用位置（紧跟所归属语句 vs 句末堆叠） | 维度 1.1（核心：防止让他人背负本研究工作） |
| Option 1/2/3 归类正确性 | 维度 1.3（核心：改编差异点定位） |
| IRB 编号 + 知情同意 + 报酬范围 | 维度 3.1（核心：学术诚信底线） |
| TOP 四要素（样本量/排除/操纵/测量） | 维度 3.2（核心：JARS 合规性） |
| 预注册状态 + 链接 + 偏离说明 | 维度 3.3（核心：透明声明） |
| 数据 / 代码 / 材料三层公开声明 | 维度 3.4（核心：可复现性） |
| 首次缩写的全称展开 | 维度 1.4（细节：避免读者回查） |
| 数字 / 单位 / 时间格式一致性 | 维度 4.3（细节：目标期刊符合性） |
| 量表锚点 + 量表名称大小写 | 维度 4.1 + 4.2（细节：术语一致性） |
| 表格 / 图 / 公式编号顺序 | 维度 4.4（细节：格式一致性） |
| 拉丁语术语斜体规则 | 维度 1.4（细节：排版规范） |
| 样本量 + 功效分析四要素 | 维度 3.6（核心：方法学严谨） |

### Step 3 — 对照核验

每发现一处违例，按以下逻辑归类：

```
1. 在 checklist 中找到对应的 `- [ ]` 项（按 checklist_id，如 1.1-a / 2.1-a / 3.1-a / 4.3-a）
2. 在 rubric 中确定 severity（严重 / 中等 / 轻微）
3. 在 rubric 扣分区间内取具体分数（按违例严重度在该区间内）
4. 同项多处违例按 N × 单项扣分累计，但单处封顶区间内高值
5. 一处违例触发多规则 → 按最严重等级判定一次，不重复扣分
```

**严重性判定核心问题清单**（按重要性排序）：

| 关键问题 | 严重等级触发 |
|---------|--------------|
| 虚假引用（引用未做的工作） | **严重**（rubric §1.1-j，−15） |
| 引用位置错位让他人背负本研究工作（"accidentally credit someone with work they have not done"） | **严重**（rubric §1.1-b，−13） |
| 缺失 IRB / 伦理委员会批准编号（有人体被试） | **严重**（rubric §3.1-a，−12） |
| 单独"Transparency and Openness"段落缺失 | **严重**（rubric §3.2-a，−12） |
| 与预注册的偏离未显式说明（deviations from preregistration 未声明） | **严重**（rubric §3.3-e，−11） |
| 多研究论文未用 "identical to Study X, with the following changes" 句式 | **严重**（rubric §2.5-a，−11） |
| 先验功效分析四要素缺失（效应量 / α / 功效 / 工具） | **严重**（rubric §3.6-a，−11） |
| Method 节引用位置不紧跟所归属语句（堆放句末） | **严重**（rubric §1.1-a，−11） |
| 知情同意程序未描述（有人体被试） | **严重**（rubric §3.1-b，−10） |
| 改编来源未标注（adapted from 缺失） | **严重**（rubric §2.1-a，−10） |
| Option 3 显著差异未识别为关键贡献 | **严重**（rubric §2.3-a，−10） |
| 数据可用性声明缺失 | **严重**（rubric §3.4-a，−10） |
| 数据 + 代码 + 材料三层公开声明缺失 | **严重**（rubric §3.4-b，−10） |
| 预注册状态未声明（preregistered / not preregistered） | **严重**（rubric §3.2-i，−10） |
| 礼赠来源未标注（"a kind gift from" 缺失） | **严重**（rubric §2.4-c，−10） |
| 伦理豁免说明缺失（使用公开 / 档案数据） | **严重**（rubric §3.1-g，−10） |
| 伦理准则声明缺失（Helsinki / APA / Belmont） | **严重**（rubric §3.1-h，−10） |

仅影响格式一致性或表述规范度 → 中等；仅个别标注细节或格式小瑕疵 → 轻微。

### Step 4 — 计算得分

```
原始得分 = 100 − Σ(各处扣分)
最终等级 = A (90–100) / B (80–89) / C (70–79) / D (60–69) / F (<60)
强制 D = 严重违例 ≥ 3 处
强制 F = 总分 < 60
封底 = 0 分（扣分上限 100 分）
```

**强制降档规则**（学术诚信底线）：
- 1 处严重问题 → 最高 B 档
- 2 处严重问题 → 最高 C 档
- 3 处及以上严重问题 → 强制 D 档
- 总分 < 60 → 强制 F 档

详见 `references/rubric.md` 第六节「评分档位说明」与第七节「评分使用提示」。

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
| **严重** | **必须调用 1 个**（虚假引用 / IRB 缺失 / 预注册偏离未声明 / TOP 段落缺失） |
| **中等** | **每个维度最多 2 个**（避免正例轰炸） |
| **轻微** | **不调用正例**（仅在「优化建议」中归类汇总） |
| 无违例 | 不调用正例 |
| **用户显式要求** | 不论等级均调用（如「请给顶刊参考」「需要范例」） |

### 4.2 匹配逻辑（按诊断用途四分类 → 文件名映射）

正例库按「**引用归属样板 / Option 1/2/3 标注范式 / 伦理与 TOP 声明范本 / 格式惯例样板**」四类诊断用途归组，运行时按以下主路径匹配：

**主路径**（按 checklist 检查项编号匹配）：

| 违例所在子节 | 优先匹配正例（`examples/positive/` 下） | 诊断用途 |
|--------------|-----------------------------------------|----------|
| §1.1 引用位置与归属 | `conventions_Abramson_2024_6.md`、`conventions_Kane_2017_5.md`、`conventions_Damian_2018_6.md` | IRB + ICC 引用紧跟；样本量 / 排除 / 操纵 / 测量声明紧跟所归属语句；数据 + 脚本 + 去标识数据三层声明 |
| §1.2 引用格式 | `conventions_Kane_2017_5.md`、`conventions_Haider_2022_4.md` | Simmons et al., 2012 透明声明引用 + 数据库访问政策引用；R 包版本号引用规范 |
| §1.3 Option 1 标注 | `conventions_Haider_2022_4.md`、`conventions_Entringer_2026_6.md` | "as in prior work" / "details are reported in X" Option 1 短语族 + by/in 介词搭配 |
| §1.3 Option 2 标注 | `conventions_Costin_2019_5.md`、`conventions_Buttner_2024_5.md` | "As specified in our preregistration" / "As preregistered" + adapted from 改编标注 |
| §1.3 Option 3 标注 | `conventions_Alves_2022_5.md` | 标签差异脚注式说明 + 改名理由交代 |
| §2.1 改编透明性 | `conventions_Alves_2022_5.md`、`conventions_Asaba_2025_6.md` | 预注册标签 → 最终标签差异说明 + 排除规则预注册对应 |
| §2.2 Option 2 差异点 | `conventions_Phillips_2021_4.md`、`conventions_Asaba_2025_6.md` | with some modifications 短语 + 排除规则逐条标注 |
| §2.4 工具/材料来源 | `conventions_Entringer_2026_6.md`、`conventions_Haider_2022_4.md`、`conventions_Carpenter_2019_6.md` | R 版本号 + 包引用 + 软件版本号完整；TEDS / SOEP 数据库访问政策；报酬范围 M=$X |
| §2.5 系列实验方法 | `conventions_Altgassen_2025_6.md`、`conventions_Asaba_2025_6.md` | 三研究统一 Transparency and Openness 段落 + Study 1/2/3 预注册状态分别声明 |
| §3.1 伦理批准 | `conventions_Abramson_2024_6.md`、`conventions_Benitez-Agudelo_2025_5.md`、`conventions_Kowialiewski_2022_5.md`、`conventions_Entringer_2026_6.md` | Herzog Hospital 伦理委员会 / Helsinki + CIPI 编号 / CER Grenoble Alpes Avis 编号 / IRB 豁免 + 公开数据理由 |
| §3.2 TOP 声明 | `conventions_Altgassen_2025_6.md`、`conventions_Diaz-Guerra_2026_5.md`、`conventions_Kane_2017_5.md`、`conventions_Entringer_2026_6.md` | JARS 标准句式 + OSF 单链接 + 数据 / 代码 / 材料公开 + 多数据源可用性 + 修订预注册透明 |
| §3.3 预注册 | `conventions_Buttner_2024_5.md`、`conventions_Costin_2019_5.md`、`conventions_Alves_2022_5.md`、`conventions_Asaba_2025_6.md`、`conventions_Entringer_2026_6.md` | "As preregistered, we excluded..." 锚定承诺 + AsPredicted 编号 + 标签修订脚注 + 序贯 BF 设计 + 修订预注册透明处理 |
| §3.4 数据可用性 | `conventions_Damian_2018_6.md`、`conventions_Haider_2022_4.md`、`conventions_Entringer_2026_6.md` | measures + scripts + de-identified data 三层声明 + "necessary to reproduce the results" 措辞 + 数据库访问政策 |
| §3.5 排除流程 | `conventions_Asaba_2025_6.md`、`conventions_Buttner_2024_5.md`、`conventions_Costin_2019_5.md` | 起始样本 → 排除总数 → 排除后样本 → 按预注册标准逐条 n；报酬与预注册挂钩 |
| §3.6 功效分析 | `conventions_Gaesser_2019_5.md`、`conventions_Georgeac_2022_5.md`、`conventions_Deri_2017_5.md`、`conventions_Asaba_2025_6.md` | 效应量 + α + 功效 + G*Power 引用四要素；η²=0.020 保守估计 + G*Power 推荐 N=475；d=0.16 with 80% power；序贯 BF 起始 n=24 + 停止规则 |
| §4.1 术语精确 | `conventions_Benitez-Agudelo_2025_5.md`、`conventions_Chu_2017_5.md` | Cohen's d 分类阈值（negligible / small / medium / large / very large / huge）；Fisher's z → Pearson's r 转换 + I² 异质性阈值 |
| §4.4 表/图/公式 | `conventions_Phillips_2021_4.md`、`conventions_Gao_2025_6.md` | 表格 4 列示措辞变体 + 假设汇总表（Table 4 details）；图 1 路径图（Figure 2 illustrates） |
| §4.5 标题/段落 | `conventions_Entringer_2026_6.md`、`conventions_Gao_2025_6.md` | 一级标题"Transparency and Openness"独立成段 + 二级标题逐研究分块 |
| §4.6 期刊规范 | `conventions_Altgassen_2025_6.md`、`conventions_Haider_2022_4.md` | APA 7th 期刊符合性 + ORCID / 数据 DOI / OSF 永久 URL 链接规范 |

**回退路径**（主路径无匹配时）：

1. 扫描所有正例文件的「适配诊断点」段，匹配违例类型关键词：
   - 引用归属：`adapted from` / `identical to` / `following` / `according to`
   - Option 1/2/3：`as described by` / `a (modified) version of` / `with some modifications` / `with the following modifications` / `instead of`
   - 伦理与 TOP：`Informed consent` / `IRB` / `ethics committee` / `preregistered` / `OSF` / `JARS` / `Transparency and Openness`
   - 数据可用性：`data` / `scripts` / `materials` / `OSF` / `necessary to reproduce`
   - 格式惯例：`Cronbach's alpha` / `Fisher's z` / `Table 1` / `Figure 2`
2. 提取关键词出现 ≥ 2 次且与当前违例类型语义相关的正例 1 个。
3. 若仍无匹配，跳过正例引用，仅在「修改建议」中给出规范改写模板。

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
- 作者名用「姓 + 年」格式（Altgassen 2025 / Damian 2018 / Entringer 2026 / Asaba 2025）
- 不省略期刊名（缩写或全称皆可，但需在第一次出现时给出全称）
- 片段前标注引用句首（如「Method 段 Transparency and Openness 段落」「Studies 1–3 Method (Participants)」）
- **不二次分发正例原文**：每份正例节选不超过 5 句；单报告引用正例不超过 3 份

### 4.4 正例目录维护

- **正例库**：51 个 `.md` 文件，软链至 `D:\method-skill-project\02-positive_examples\conventions\`
- **文件名规范**：`conventions_<Author>_<Year>_<n>.md`（n 为该文献片段序号，5/6 表明片段位于第几个子节）
- **正例结构**：四段式——① 片段类型（含学术规范诊断用途）② 原文片段 ③ 来源文献 ④ 适配诊断点
- **典型正例**：
  - `conventions_Altgassen_2025_6.md` — 三研究统一 Transparency and Openness 段落 + JARS 标准句式 + OSF 单链接 + 预注册状态分研究声明（维度 3.2 样板）
  - `conventions_Damian_2018_6.md` — measures + scripts + de-identified data + output files 四层公开 + "necessary to reproduce the results" 措辞（维度 3.4 样板）
  - `conventions_Entringer_2026_6.md` — 多数据源可用性分级说明 + IRB 豁免理由 + R 版本号 + 包引用 + 修订预注册透明处理（维度 2.4 + 3.1 + 3.2 + 3.3 样板）
  - `conventions_Abramson_2024_6.md` — Herzog Hospital 伦理委员会 + 监护人知情同意 + ICC N=32/N=38 + .62–.82 区间（维度 3.1 + 3.5 样板）
  - `conventions_Benitez-Agudelo_2025_5.md` — Helsinki + CIPI/2024(611) 编号 + Holm-Bonferroni αadj 公式 + Cohen's d 六档分类阈值（维度 3.1 + 3.5 + 4.1 样板）
  - `conventions_Asaba_2025_6.md` — 序贯 BF 起始 n=24 + 评估间隔 + 三条停止规则 + 排除总数 20 + 按预注册标准逐条 n（维度 3.3 + 3.5 样板）
  - `conventions_Gaesser_2019_5.md` — 先验功效四要素：d=.25 + i.e. 括号说明 + G*Power + Faul et al., 2007 引用（维度 3.6 样板）
  - `conventions_Georgeac_2022_5.md` — η²=0.020 保守小效应 + 三条件 + α=.05 + 80% power + G*Power 推荐 N=475（维度 3.6 样板）
  - `conventions_Costin_2019_5.md` — As specified in our preregistration + 注意力检查 64 cases + 缺失处理 + T2 更高报酬（维度 3.3 + 3.5 样板）
  - `conventions_Buttner_2024_5.md` — As preregistered 锚定 + 排除 n=2/2/1 + 14-day 序列 + 报酬与预注册挂钩（维度 3.3 + 3.5 样板）
  - `conventions_Alves_2022_5.md` — 预注册标签 → 最终标签差异脚注式说明 + 改名理由（维度 2.1 + 3.3 样板）
  - `conventions_Diaz-Guerra_2026_5.md` — 未预注册声明 + 伦理豁免 + OSF 材料 + JARS 合规 + 样本量理由（维度 3.2 样板）
  - `conventions_Kane_2017_5.md` — 开篇即声明"样本量 / 排除 / 操纵 / 测量"（呼应 Simmons et al., 2012）+ 数据材料 OSF 链接（维度 3.2 样板）
  - `conventions_Haider_2022_4.md` — 预注册 + OSF 代码链接 + 问卷公开途径 + R 4.0.5 + lavaan 0.6-9 + ggplot2 3.3.5 版本号（维度 2.4 + 3.4 样板）
  - `conventions_Kowialiewski_2022_5.md` — CER Grenoble Alpes Avis-2019-04-09-2 编号 + 知情同意 + 被试独立性（维度 3.1 样板）
  - `conventions_Deri_2017_5.md` — AsPredicted #3311 预注册编号 + 样本量 + 效应量 d=0.16 + 80% power 一句到位（维度 3.6 样板）
  - `conventions_Carpenter_2019_6.md` — UCLA IRB#15–001476 + 报酬 $37.60–$44.60 + 5.33 hr + 9–35 days + 组间 t[59] 平衡性检验（维度 2.4 + 3.1 样板）
- **建立软链**（已完成）：
  ```powershell
  # Windows PowerShell（已在本 Skill 创建时执行）
  New-Item -ItemType Directory -Path "D:\method-skill-project\03_skills_output\method-conventions-diagnostic\references\examples" -Force
  New-Item -ItemType Junction -Path "D:\method-skill-project\03_skills_output\method-conventions-diagnostic\references\examples\positive" -Target "D:\method-skill-project\02-positive_examples\conventions"
  ```
- **索引文件**：建议建立 `_INDEX.md`（人读）+ `_INDEX.json`（机读），按本 Skill 4 大维度 / 21 子节归组正例（可选，当前 sibling skill 未强制）

---

## 五、输出格式（固定模板）

诊断完成后，**必须**按以下模板输出。模板中 `[…]` 为占位符，需替换为实际诊断结果。

```markdown
# Method 部分「学术规范」诊断报告

**被检文本**：[文件名 / 段落定位，如 "Study 1 Method 节"]
**诊断时间**：[ISO 日期]
**诊断依据**：Science Research Writing Unit 2 §2.4.2（Option 1/2/3 三档 + by/in 介词搭配 + 引文位置规则）+ §2.5.1（主动/被动语态归属判定）+ checklist.md（67 项）+ rubric.md（严重/中等/轻微三档 + 强制降档规则）+ 顶刊正例 51 例

---

## 1. 维度得分

| 维度 | 检查子节数 | 检查项数 | 违例数（严重/中等/轻微） | 扣分 | 得分 |
|------|------------|----------|--------------------------|------|------|
| 1. 引用格式与标注规范性 | 4 | 26 | x / x / x | x | x |
| 2. 现有方法改编说明准确性 | 5 | 27 | x / x / x | x | x |
| 3. 伦理与透明声明完整性 | 6 | 37 | x / x / x | x | x |
| 4. 术语与格式一致性 | 6 | 26 | x / x / x | x | x |
| **合计** | **21** | **67** | **x / x / x** | **x** | **x / 100** |

---

## 2. 整体评价

**等级**：[A / B / C / D / F]
**强制降档**：[如触发，标注原因：如"严重问题 ≥3 处 → 强制 D 档"；如未触发，标注"未触发强制降档"]
**一句话总结**：[例如："引用位置基本归位，但 IRB 编号缺失且 TOP 段落未独立；Option 1/2/3 标注基本正确；术语与格式存在多处不一致。"]

---

## 3. 核心问题（按严重程度排序）

### 3.1 严重违例（必须修改，否则触及学术诚信底线）

#### 问题 1：[违例类型简述，如 "虚假引用：引用未做的工作"]
- **位置**：[段落 / 句编号，如 "Measures 子节第 2 句"]
- **原文**：`[原句引用]`
- **违例类型**：checklist §[1.1-j] + rubric §[1.1-j]
- **严重程度判定依据**：[说明为何该引用属于学术诚信问题；引用教材 §2.4.2 "accidentally credit someone with work they have not done"（p.85）+ "if you don't provide appropriate citation references...this has a negative effect"（p.80）]
- **扣分**：[15 分]
- **修改建议**：[具体改写方案，给出 2–3 种备选]
  - 方案 A（删除虚假引用）：`[删除未做工作的引用，仅保留实际引用的内容]`
  - 方案 B（改写归属）：`We adapted X from [Author, Year] for the purpose of [motivation]` → 明确归属
  - 方案 C（增加 in this study 标注）：`In this study, we used X following [Author, Year]` → 区分本研究与前人工作
- **顶刊正例**：
  - [Author Year] [Brief title]. [Journal], [Vol], [Pages].
  - **原文片段**：`[...]`
  - **适配诊断点**：[1–2 条]

#### 问题 2：[违例类型简述，如 "IRB 编号缺失"]
- **位置**：[段落 / 句编号]
- **原文**：`[原句引用]`
- **违例类型**：checklist §[3.1-a] + rubric §[3.1-a]
- **严重程度判定依据**：[说明为何 IRB 编号是顶刊硬性要求]
- **扣分**：[12 分]
- **修改建议**：
  - 方案 A（标准句式）：`The study was approved by the [University] Ethics Committee (protocol #XXX-XXXX)`
  - 方案 B（Helsinki + 编号）：`The study complied with the Helsinki Declaration and was approved by [Institution] Ethics Committee (CIPI/2024(611))`
  - 方案 C（豁免说明）：`This study was exempt from IRB approval because [reason: archival public-domain data / existing publicly available datasets]`
- **顶刊正例**：
  - [Author Year] [Brief title]. [Journal], [Vol], [Pages].
  - **原文片段**：`[...]`
  - **适配诊断点**：[1–2 条]

#### 问题 3：[违例类型简述，如 "TOP 段落未独立 / 预注册偏离未声明"]
- **位置**：[段落 / 句编号]
- **原文**：`[原句引用]`
- **违例类型**：checklist §[3.2-a] 或 §[3.3-e] + rubric §[3.2-a] 或 §[3.3-e]
- **严重程度判定依据**：[说明为何 JARS 合规与预注册偏离声明是顶刊硬性要求]
- **扣分**：[12 分 / 11 分]
- **修改建议**：
  - 方案 A（独立 TOP 段落）：`Transparency and Openness. We report how we determined our sample size, all data exclusions, all manipulations, and all measures in the study, and we follow the APA Journal Article Reporting Standards (JARS; Appelbaum et al., 2018).`
  - 方案 B（OSF 链接）：`All data, analysis code, and research materials are available on the Open Science Framework at https://osf.io/[id]/`
  - 方案 C（预注册偏离说明）：`We note that, in response to reviewer requests, we modified [X]; the modified analysis was preregistered at [link] prior to being conducted`
- **顶刊正例**：
  - [Author Year] [Brief title]. [Journal], [Vol], [Pages].
  - **原文片段**：`[...]`
  - **适配诊断点**：[1–2 条]

### 3.2 中等违例（修改后可投稿）

#### 维度 1（引用格式与标注规范性）

- [问题摘要 1 + 位置 + 修改要点 + 顶刊正例（如有）]
- [问题摘要 2 + 位置 + 修改要点 + 顶刊正例（如有）]

#### 维度 2（现有方法改编说明准确性）

- [问题摘要 1 + 位置 + 修改要点 + 顶刊正例（如有）]
- [问题摘要 2 + 位置 + 修改要点 + 顶刊正例（如有）]

#### 维度 3（伦理与透明声明完整性）

- [问题摘要 1 + 位置 + 修改要点 + 顶刊正例（如有）]
- [问题摘要 2 + 位置 + 修改要点 + 顶刊正例（如有）]

#### 维度 4（术语与格式一致性）

- [问题摘要 1 + 位置 + 修改要点 + 顶刊正例（如有）]
- [问题摘要 2 + 位置 + 修改要点 + 顶刊正例（如有）]

### 3.3 轻微违例（仅归类，不逐一展开）

- 维度 1：x 处（首次缩写未给全称 / 二次引用处理欠规范 / 个人通讯格式欠规范）
- 维度 2：x 处（改编差异点单条超过 1–2 句 / 自制设备规格欠详细）
- 维度 3：x 处（数据限制声明缺失 / 报酬挂钩机制未描述 / 序贯设计停止规则未全部列出）
- 维度 4：x 处（希腊字母大小写 / 引号使用 / 单位前后空格 / 百分比格式 / 日期格式）

---

## 4. 优化建议（按优先级）

1. **[优先级 P0 — 严重 / 学术诚信]** [严重违例整改路径，如"删除虚假引用 + 补 IRB 编号 + 独立 TOP 段落 + 声明预注册偏离 + 数据 / 代码 / 材料三层公开"]
2. **[优先级 P1 — 中等]** [中等违例整改路径，如"Option 1/2/3 标注三档归类正确 + 改编差异点逐条列出 + 控制变量入选理由 + 缩写首次出现给全称 + 数字 / 单位格式全文统一"]
3. **[优先级 P2 — 轻微]** [轻微违例整改路径，如"拉丁语术语斜体规则统一 + 量尺锚点一致 + 表格编号连续 + 希腊字母大小写统一"]
4. **[目标期刊对齐]** [如"JPSP 偏 APA 7th + independent sample t[59] 标注 + OSF 永久链接；BMC Psychology 偏 numbered references + Helsinki 完整声明 + Cohen's d 六档分类；需根据投稿目标调整"]
5. **[后续步骤]** [如"修改 1 轮后建议再次调用本 Skill 复检，确保强制降档规则不再触发；同时建议配合 method-structure-diagnostic 复检结构完整性、method-logic-diagnostic 复检方法选择论证、method-cohesion-diagnostic 复检衔接连贯性、method-grammar-diagnostic 复检时态/被动"]

---

## 附录 A：诊断依据回链

- 参考教材：《Science Research Writing》(2nd ed.) Unit 2「How to Write about Methods」§2.4.2（Option 1/2/3 现有方法标注三档 + by/in 介词搭配 + 引文位置规则 + GIVE THE SOURCE 短语族）；§2.5.1（主动/被动语态归属判定 + agentless passive + Past/Present Simple）；§2.2.3 Generic Methods Model 六模块
- 检查清单：`references/checklist.md`（4 大维度 / 21 子节 / 67 项 + 5 项附录自检）
- 评分细则：`references/rubric.md`（严重 / 中等 / 轻微三档 + A/B/C/D/F 等级 + **强制降档规则**）
- 顶刊正例：`references/examples/positive/`（51 例，含 JPSP / JEP:G / Developmental Psychology / PSPB / OBHDP / BMC Psychology / Behavioral Sciences 等）

## 附录 B：未触发项目（完整性自检）

列出未触发任何违例的 checklist 子节，证明诊断覆盖完整：
- §1.1 引用位置与归属清晰：未发现违例
- §1.4 引用与缩写的全称展开：未发现违例
- §3.2 TOP 声明：未发现违例
- §3.4 数据与材料可用性声明：未发现违例
- §4.2 缩略语与符号体系一致性：未发现违例
- §4.5 标题 / 子标题 / 段落格式：未发现违例
- ...（按 checklist 顺序列出无违例子节）
```

---

## 六、使用约束

1. **本 Skill 仅诊断，不改写**：所有输出均以「问题定位 + 修改建议」形式给出，最终改写由人类作者完成，避免 AI 改写引入新错误。
2. **清单-细则严格对应**：rubric 中每一条扣分规则都能在 checklist 中找到对应 `- [ ]` 项；任何 rubric 单独新增项均视为误植。
3. **学术诚信底线不可妥协**：本 Skill 对「虚假引用 / IRB 编号缺失 / 知情同意缺失 / 预注册偏离未声明 / TOP 段落缺失 / 数据未公开」六类核心严重问题强制降档（参见 rubric 第七节强制降档规则）；任何一类触发即应在投稿前解决，不可"先投稿后修订"。
4. **不跨维度诊断**：本 Skill 仅处理「学术规范」维度；结构、逻辑、衔接、语法、词汇维度请调用 sibling skill：
   - 结构 → `method-structure-diagnostic`
   - 逻辑 → `method-logic-diagnostic`
   - 衔接 → `method-cohesion-diagnostic`
   - 语法 → `method-grammar-diagnostic`
   - 词汇 → `method-vocabulary-diagnostic`
5. **正例库只读**：禁止修改 `references/examples/positive/` 下的 `.md` 文件；如需新增正例，请修改源目录 `D:\method-skill-project\02-positive_examples\conventions\` 并重新建立软链。
6. **教材-清单-细则三对齐**：本 Skill 的所有判定逻辑必须能回溯至 §2.4.2（Option 1/2/3 三档 + by/in 介词搭配 + 引文位置规则）、§2.5.1（agentless passive + Past/Present Simple 归属判定）、§2.2.3（Generic Methods Model 六模块）；任何诊断结论若无法引用教材原文锚点即视为误判。
7. **Option 1/2/3 三档归类优先**：本 Skill 对「Option 3 显著差异是否被识别为关键贡献」检查（§2.3-a）优先级仅次于「虚假引用」——"the difference may represent the key contribution of your study"（教材 p.84），按 rubric §2.3-a（−10）严格执行。
8. **TOP 四要素必须齐备**：本 Skill 对「Transparency & Openness 段落四要素」检查（§3.2）优先级等同于「IRB 编号」——JARS（Appelbaum et al., 2018）标准是顶刊投稿的硬性要求，扣分按 rubric §3.2-a（−12）严格执行。
9. **格式问题不掩盖学术问题**：本 Skill 对「术语与格式一致性」（维度 4）的检查优先级最低，但若某格式问题导致方法学可读性受损（如量尺锚点不一致导致后续分析无法复现），可升级为严重问题。

---

**版本**：v1.0（与 checklist.md、rubric.md 同步）
**配套**：本目录下 `references/checklist.md`（检查清单）、`references/rubric.md`（评分细则）、`references/examples/positive/`（顶刊正例 51 例），四者一一对应、不得拆分使用。