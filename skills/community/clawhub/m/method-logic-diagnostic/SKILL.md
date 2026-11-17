---
name: method-logic-diagnostic
version: 1.0.0
description: 诊断心理学论文 Method 部分的逻辑与论证问题，检查方法合理性、设计自洽性、变量与控制严谨性、局限披露恰当性，输出评分与顶刊正例参考
metadata:
  domain: psychology-academic-writing
  dimension: logic
  source: Science_Research_Writing_2nd_edition_Unit_2
  companion_skills: [method-structure-diagnostic, method-grammar-diagnostic, method-vocabulary-diagnostic]
user-invocable: true
---

# Method 部分「逻辑与论证」诊断 Skill

> 覆盖《Science Research Writing》(2nd ed.) **Unit 2**「How to Write about Methods」关于**方法选择论证**、**6 组件 Methods model**、**Option 1/2/3 三档与既有方法的关系定位**、**局限披露原则**的全部规则，专用于心理学实证论文 Method 节的**逻辑与论证维度**诊断。
>
> **核心立场**：「Methods section」≠ 客观描述的清单；它是一段「**This is exactly what I did/used, and I had good reasons for making those decisions**」的论证（教材 §2.2.2, p.81）。诊断目的：判断作者的**方法选择是否被合理论证**、**研究设计是否逻辑自洽**、**变量与控制说明是否完整**、**局限披露是否即时且恰当**。

---

## 一、诊断依据

本 Skill 的全部判定逻辑基于以下 **4 项不可拆分** 的依据，运行时按顺序加载：

| # | 依据 | 路径 | 用途 |
|---|------|------|------|
| 1 | **参考教材** | `D:\method-skill-project\01-reference\Science_Research_Writing_Methods.pdf` Unit 2（66 页） | §2.2.1–2.2.3 方法选择论证 + 6 组件 Methods model；§2.4.2 Option 1/2/3 三档比较框架 + JUSTIFY CHOICES / INDICATE CARE / INDICATE PROBLEMS 词族；§2.5.1 动词时态与 agentless passive 归属判定；§2.3.2 系列实验方法继承-修改逻辑 |
| 2 | **检查清单** | `references/checklist.md` | **4 大维度 / 22 子节 / 124 项** `- [ ]` 列表（方法选择合理性 25 项 + 研究设计逻辑自洽性 34 项 + 变量与控制说明完整性 30 项 + 局限性与问题说明恰当性 35 项），作为违规定位与命中判定的对照表 |
| 3 | **评分细则** | `references/rubric.md` | 严重 / 中等 / 轻微三档扣分（**10–15 / 5–9 / 1–4 分/处**）+ A/B/C/D/F 五档等级（90/80/70/60/<60）+ 124 扣分点与 checklist 严格一一对应 |
| 4 | **顶刊正例** | `references/examples/positive/` | **49 个 `.md` 文件**，软链至 `D:\method-skill-project\02-positive_examples\logic\`，含 JPSP / JEP:G / Developmental Psychology / PSPB / JCCP / JESP / OBHDP 等顶刊 Method 节片段，按「**论证链示范**」「**设计逻辑样板**」「**变量控制范本**」「**局限披露范式**」四类诊断用途归组 |

> **教材原文摘录锚点**（用于本 Skill 内部一致性自检）：
> - §2.2.2 核心论点：「**your reasons are obvious to you, but they are not always obvious to readers. If you don't provide justification for your choices, the reader may wonder why you did things in a particular way**」（教材 p.80）
> - §2.2.3 Methods 6 组件模型：**OVERVIEW → DETAILS(±justify ±care) → FIGURE/TABLE → COMPARE → BACKGROUND(Present Simple) → PROBLEMS**（教材 p.88）
> - §2.4.2 Option 1/2/3 三档：**Option 1 完全相同（identical to / as described by）；Option 2 相似（adapted from / with some modifications）；Option 3 显著不同（unlike / with the following modifications）**（教材 p.109–110）
> - §2.2.2 局限披露：「**mention them first where they occur — in this case, in the Methods section — and then refer to them again at the end**」（教材 p.86）
> - §2.4.2 INDICATE PROBLEMS 三段式：「**Conventionally, writers use language that minimises the problem and its effects, minimises your responsibility, maximises the good aspects and/or suggests a solution**」（教材 p.86）

---

## 二、核心检查项（4 大维度，22 子节，124 项）

依据 `checklist.md` 提炼为以下 **4 个诊断维度**，运行时按此顺序扫描。每个维度下分若干子节，标注与 checklist 的对应关系。

### 维度 1：方法选择合理性（对应 checklist §一，共 5 子节 / 25 项）

> **诊断核心问题**：每项关键方法选择是否伴随「为什么是它而不是别的」的实质论证？论证链是否为「事实/文献支撑 → 选择 → 优势」三段式？

| 子节 | 关键判定 |
|------|----------|
| 1.1 方法/范式选择给出实质理由（非默认路径） | 关键方法选择均有「whereas prior work… we… because…」对比框架；对备选方法的取舍原因显式交代；资料来源限制（IAPS 禁线）作为替换理由被说明；二级文献/二手数据的「did not have control over…」明示 |
| 1.2 论证链三段式（事实→选择→优势） | 选择理由以可量化事实支撑（语料规模 → 机器学习；零膨胀比例 → ZINB）；选择理由引用文献佐证；优势列举采用平行结构（First/Second/Third 或 (a)/(b)/(c)）；每条优势落到本研究的具体可验证收益；论证逻辑无跳跃 |
| 1.3 与既有方法的关系明确定位（Option 1/2/3） | 与前人方法按三档归类（identical / similar / significantly different）；相同给出文献出处；相似说明调整参数；不同说明差异点及方法学意义；系列实验方法继承-修改用「identical to X except that…」显式表达；工具修订引用原版并指明修订部分 |
| 1.4 操作化选择经得起方法学审查 | 间接测量 vs 直接测量取舍说明；经典指标选择（平行分析 vs Kaiser 准则）给出取舍理由；Bayesian vs frequentist 框架说明理论优势；操纵实现方式匹配理论构念而非可操作性；对照材料构建标准明确且可复现 |
| 1.5 关键方法选择语言到位 | 目的状语串联（in order to / with the aim of / so as to / thereby）；选优词（accurate / robust / conservative / suitable / powerful）与选优动词（enable / ensure / permit / allow / facilitate）配合使用；谨慎副词（carefully / tightly / independently / repeatedly / precisely）体现操作严谨；本研究过去时 vs 标准程序现在时不混用 |

### 维度 2：研究设计逻辑自洽性（对应 checklist §二，共 7 子节 / 34 项）

> **诊断核心问题**：假设—设计—测量—分析链条是否贯通？替代解释是否被显式排除？关键变量操作化是否无歧义？控制变量清单是否完整？多研究/多实验设计是否逻辑一致？

| 子节 | 关键判定 |
|------|----------|
| 2.1 假设—设计—测量—分析链条贯通 | Method 中引用的假设/研究问题能在实验设计中被直接检验；每个 IV 的每个水平在材料/程序中有对应操纵且物理可量化；关键 DV 指明测量时点与聚合单位（trial/block/session）；多假设研究中每个假设对应至少 1 个设计特征；假设与统计模型一一映射 |
| 2.2 替代解释被显式排除 | 对每个核心效应给出至少一个竞争假设/替代解释；竞争假设被转化为可检验的不同预测（含相对预测）；控制组构造逻辑显式——在什么维度上「匹配」或「随机化」隔离关键变量；操纵的前置信息（filler、人口学、基线）标准化以隔离混淆；关键比较点被明文标注（"the information central to our manipulation"） |
| 2.3 关键变量操作化无歧义 | 技术术语首次出现即给出排比定义或「时间窗组合」定义；计数变量给出 0 与正值的判定标准；复合指标的算法明确写出（差异分、加权分、log 转换）；数据预处理中的几何变换附带可复现的数学描述；构念—指标对应关系单一对应，无同一变量被多重解读 |
| 2.4 控制变量/混淆变量清单完整 | 自变量操纵之外的潜在混淆变量被显式识别；每个被纳入控制的变量附带入选理由（非默认清单）；控制变量在分析中的角色明确（协变量/分层因子/匹配变量/排除条件）；未控制的潜在混淆被显式声明并说明为何可接受；实验组间的等价性证据被提供（基线平衡检验、前测无差异、操作检验） |
| 2.5 多研究/多实验设计逻辑一致 | 系列实验中每个研究的角色定位清晰（pilot → 主实验 → 边界条件 → 推广）；系列实验间变量继承/修改用一致句式表达；后研究的样本量直接锚定前研究观测到的效应量，样本量决策可追溯；后研究在材料/操纵/测量上的任何偏离都标注目的；系列实验之间分析策略保持家族相似性 |
| 2.6 操控性细节足以复现 | 步骤按时间顺序形成完整环节链，无跳步；精确时序（毫秒、间隔、练习/正式试验数量）逐一报告；演示/练习与正式阶段的差异被主动澄清（"Note that…therefore differed from…"）；操作步骤不仅写「做了什么」还写「为什么这样做」（in order to / to ensure）；关键决策（编码方案、心化策略）括号内解释理由 |
| 2.7 设计约束与备选权衡透明 | 因现实约束放弃的更优方案被明示；备选设计（如 cross-classified vs 传统多层模型）的取舍原因被指出；设计选择与目标期刊惯例的对应关系被标注；操纵失败、刺激失效、控制失配的预案或检验被事先描述 |

### 维度 3：变量与控制说明完整性（对应 checklist §三，共 6 子节 / 30 项）

> **诊断核心问题**：IV/DV/控制变量的说明是否足够可复现？测量工具的心理测量学属性是否被报告？刺激与材料的控制是否充分？流程中的变量控制是否到位？

| 子节 | 关键判定 |
|------|----------|
| 3.1 自变量（IV）说明 | 每个 IV 给出名称、水平数、水平值（连续变量给出范围或代表值）；每个水平的物理或符号操纵给出可复现细节；水平间差异被框定为单一维度的变化（最小改动原则）；操纵前的前置信息（基线、filler）标准化处理；操纵检验（manipulation check）的存在、内容与时点被显式说明 |
| 3.2 因变量（DV）说明 | 每个 DV 给出测量工具、聚合单位（trial / participant / session）、分析单位；测量边界与剔除准则明确（如反应时 < 200 ms 或 > 3000 ms 视为无效）；复合 DV 的合成算法与权重依据被说明；多 DV 之间的优先级与统计控制策略（MANOVA / 多元校正）被说明；状态性 vs 倾向性测量被明确区分，不混用 |
| 3.3 控制变量/协变量说明 | 控制变量的测量方式（自报、行为、观察）被说明；控制变量被使用的位置（分组匹配 / 协方差 / 分层 / 排除）被说明；控制变量的入选标准（理论依据 / 前测相关 / 既有发现）被说明；心化（centering）的目的（去均值、组内/组间分离）逐变量说明；共线性或多重共线性的处理被说明 |
| 3.4 测量工具的心理测量学属性 | 报告样本中的信度（α 或 ω），并说明是否达到常用阈值；报告构念效度证据或引用既有文献（前人验证、与金标准相关）；量表锚点、条目数、计分方向、是否反向计分明确；量表改编时标注「adapted from / translated from / revised version of」及改动内容；跨文化或跨语言使用的量表给出翻译与回译程序 |
| 3.5 刺激与材料的控制说明 | 刺激来源（既有库 / 自建 / 商业）逐项标注；刺激抽样范围明确（"wide range of specific phrasings"），并以目的（不绑定单一措辞）佐证；多版本刺激的内容特异性控制被说明（≥3 版本 / 措辞变体 / 间接与直接语言并用）；刺激匹配标准（如内容最低相关 + 语言尽量接近）逐条列出；替换刺激时说明替换原因（IAPS 禁线 → OASIS）与可比性补救 |
| 3.6 流程中的变量控制 | 主试、场所、设备的标准化程序被说明；主试效应（experimenter effects）通过盲法或脚本控制；被试盲态（盲法 / 假故事 / cover story）有明确陈述；时间效应（每天同一时段、季节性）通过排程或统计控制；顺序效应通过随机化、拉丁方、计数器平衡 |

### 维度 4：局限性与问题说明恰当性（对应 checklist §四，共 7 子节 / 35 项）

> **诊断核心问题**：局限是否在发生处即时披露（而非堆到结尾）？样本量与功效局限是否如实标注？样本代表性与流失偏差是否被披露？局限披露的语气是否「最小化问题+最小化责任+最大化优势+指向解决方案」？

| 子节 | 关键判定 |
|------|----------|
| 4.1 局限在发生处即时披露（非堆到结尾） | 与方法选择直接相关的局限性在该方法首次出现时即被提及；局限披露伴随补救或缓冲策略（敏感性分析、Monte Carlo、robustness check）；不在文章末段首次披露关键方法局限；每条局限披露后接其对未来研究的具体启示（"Future work should…"）；局限以最小化语气陈述，不夸张也不藏匿 |
| 4.2 样本量与功效局限如实标注 | 先验功效分析要素齐全：目标效应量、功效水平（.80 / .95）、α 水平、工具（G*Power / BUCCS / simr）；无法做先验功效分析时，坦诚说明并改用敏感性 / Monte Carlo / 模拟分析；后验功效在效应方向明朗后给出可检最小效应作为样本量解读；功效不足被主动披露，并说明影响哪些结论；多研究系列中样本量衔接可追溯（前研究效应量 → 后研究样本量） |
| 4.3 样本代表性与流失偏差 | 报告样本同质化或人口学覆盖不足（如 race/ethnicity inconsistent），并说明其限制；纵向 / 面板数据报告流失分析（保留者 vs 流失者 vs 初始样本的差异检验 + 效应量）；报告超募量与目标量的关系及超募理由；报告排除规则的逐条原因与人数（基于先验准则，非事后挑选）；招募-排除-最终样本漏斗完整呈现 |
| 4.4 操作化与测量的局限 | 自陈 / 单维 / 单一情境测量的局限被提及，建议后续使用多方法 / 行为 / 神经指标；量表在某群体中的有效性未被确认时显式说明（"validity has not been established in this population"）；间接测量低估效应的局限被指出（"BTA beliefs are typically larger with direct measures"）；测量时点不足以推因果时被显式声明；自评 vs 他评、单时点 vs 多时点的局限在适用情况下被提及 |
| 4.5 设计与外部效度局限 | 实验情境 vs 现实情境的差距被指出；样本对总体的代表性被评估；单一文化 / 语言 / 国家样本的局限被指出，跨文化推广性被讨论；操纵的人为性（artificiality）被识别（"the manipulation may not capture…in real life"）；平行实验间的效应差异被指出并讨论可推广性边界 |
| 4.6 局限披露的语气与归属 | 局限披露以自我审视口吻（"our study is limited by…"、"we note that…"）而非辩护；局限披露伴随可操作的改进建议；当使用了非完美方案时，明示替代方案存在并说明为何仍选此；局限不被埋藏在冗长补充段落中，主要局限在正文 Method 或 Discussion 显眼位置；局限披露与本研究的核心论断分离 |
| 4.7 局限语言与表述规范（INDICATE PROBLEMS 四组） | **最小化问题**措辞（slightly / minor / negligible / minimal / not significant）；**最小化责任**措辞（it is recognised that / inevitably / as far as possible / limited by）；**最大化优势**措辞（acceptable / fairly well / reasonably robust / quite good）；**指向解决方案**措辞（Future work should…/ Future studies should…）；局限披露不削弱本研究贡献（既不回避也不否认发现的稳健性） |

---

## 三、执行步骤（6 步）

```
Step 1 读取规则 → Step 2 扫描文本 → Step 3 对照核验 → Step 4 计算得分 → Step 5 匹配正例 → Step 6 输出结果
```

### Step 1 — 读取规则

加载以下 4 份规则文件至内存：
- `references/checklist.md`（4 大维度 / 22 子节 / **124 项 `- [ ]`**）
- `references/rubric.md`（严重 / 中等 / 轻微扣分区间 + A/B/C/D/F 等级表 + 降档规则）
- `references/examples/positive/` 正例库（49 个 `.md` 文件，按文件名 `logic_<Author>_<Year>_<n>.md` 索引；n 为该文献片段序号）
- 教材 Unit 2（66 页）核心论点锚点（见第一节表末）

构建内存映射表：`{checklist_id → (severity, score_range, positive_examples[])}`。

### Step 2 — 扫描文本

按 Method 节实际段落顺序（Participants / Design / Measures / Procedure / Analysis），逐段扫描。建议扫描粒度：
- **一段 = 一个聚合扫描单元**（用于检测论证链三段式、Option 1/2/3 定位、局限即时披露）
- **一句 = 一个细分扫描单元**（用于检测 INDICATE CARE / INDICATE PROBLEMS 副词、目的状语 in order to / with the aim of、过去时 vs 现在时分工）

扫描时同步记录：

| 扫描字段 | 用途 |
|---------|------|
| 方法选择及配套论证 | 维度 1（事实→选择→优势三段式） |
| 假设/问题提及与设计对应 | 维度 2（链条贯通） |
| 替代解释、控制组构造 | 维度 2.2 |
| 操作化定义（构念→指标） | 维度 2.3 + 3.1–3.2 |
| 控制变量清单与入选理由 | 维度 2.4 + 3.3 |
| 系列实验「identical except that」表达 | 维度 2.5 |
| 时序精确度（毫秒、间隔、阶段） | 维度 2.6 |
| 限制披露的位置与语言模式 | 维度 4 |
| 心理测量学属性（α / ω）报告 | 维度 3.4 |
| 刺激抽样范围与版本数 | 维度 3.5 |
| 主动/被动语态与限定词（in this study / here） | 维度 1.5（归属） |

### Step 3 — 对照核验

每发现一处违例，按以下逻辑归类：

```
1. 在 checklist 中找到对应的 `- [ ]` 项（按 checklist_id，如 1.1-a / 2.1-a / 3.4-a / 4.7-a）
2. 在 rubric 中确定 severity（严重 / 中等 / 轻微）
3. 在 rubric 扣分区间内取具体分数（按违例严重度在该区间内）
4. 同项多处违例按 N × 单项扣分累计，但单处封顶区间内高值
5. 一处违例触发多规则 → 按最严重等级判定一次，不重复扣分
```

**严重性判定核心问题清单**（按重要性排序）：

| 关键问题 | 严重等级触发 |
|---------|--------------|
| 假设—设计不可对应（假设无法被设计检验） | **严重**（rubric §2.1，−15） |
| 无可量化事实支撑的方法选择（孤证「这是常用做法」） | **严重**（rubric §1.2，−10） |
| 自变量操纵之外的混淆变量未被识别 | **严重**（rubric §2.4，−12） |
| 每个 IV 的每个水平无对应物理操纵 | **严重**（rubric §2.1，−12） |
| 步骤链断裂（缺环节导致不可复现） | **严重**（rubric §2.6，−12） |
| 与前人方法的关系未按 Option 1/2/3 归类 | **严重**（rubric §1.3，−10） |
| 操纵实现方式不匹配理论构念（仅为可操作性） | **严重**（rubric §1.4，−10） |
| 构念—指标多重解读（同一变量被赋予不同构念） | **严重**（rubric §2.3，−10） |
| 未报告样本中的信度（α / ω） | **严重**（rubric §3.4，−10） |
| 先验功效分析要素缺失且无替代策略 | **严重**（rubric §4.2，−10–12） |
| 实验组间无等价性证据（无基线平衡 / 前测） | **严重**（rubric §2.4，−10） |
| 引用位置错误（错挂他人未做的工作） | **严重**（rubric §1.3，−12） |
| 替代解释未被显式排除（仅给出主假设） | **严重**（rubric §2.2，−10） |

仅影响论证充分性或表述严谨度 → 中等；仅措辞、格式、措辞层级问题 → 轻微。

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
| **严重** | **必须调用 1 个**（核心方法选择未论证 / 设计不可复现 / 控制变量缺失） |
| **中等** | **每个维度最多 2 个**（避免正例轰炸） |
| **轻微** | **不调用正例**（仅在「优化建议」中归类汇总） |
| 无违例 | 不调用正例 |
| **用户显式要求** | 不论等级均调用（如「请给顶刊参考」「需要范例」） |

### 4.2 匹配逻辑（按诊断用途四分类 → 文件名映射）

正例库按「**论证链示范 / 设计逻辑样板 / 变量控制范本 / 局限披露范式**」四类诊断用途归组，运行时按以下主路径匹配：

**主路径**（按 checklist 检查项编号匹配）：

| 违例所在子节 | 优先匹配正例（`examples/positive/` 下） | 诊断用途 |
|--------------|-----------------------------------------|----------|
| §1.1 方法选择理由缺失 | `logic_Petsko_2022_3.md`、`logic_Kteily_2016_3.md`、`logic_Phillips_2021_2.md` | 论证链三段式（理论-操作映射 / 覆盖故事 + 操纵关键点标注 / 刺激抽样论证） |
| §1.3 Option 1/2/3 定位缺失 | `logic_Alves_2022_4.md`、`logic_Werchan_2024_4.md`、`logic_Abramson_2024_2.md` | 系列实验「identical except that」表述 + 刺激替换理由 |
| §1.4 操作化选择理由 | `logic_Plate_2023_4.md`、`logic_Petsko_2022_3.md` | 多准则递进呈现 + 操纵机制先行说明 |
| §2.1 假设-设计-测量链条断裂 | `logic_Carpenter_2019_4.md`、`logic_Vilanova_2022_4.md` | 程序可复现 + 样本量闭环论证 |
| §2.2 替代解释排除 | `logic_Kteily_2016_3.md`、`logic_Petsko_2022_3.md` | 控制组构造逻辑（"who disagreed with whom was randomized"）+ filler 标准化 |
| §2.5 系列实验方法继承-修改 | `logic_Alves_2022_4.md`、`logic_Abramson_2024_2.md` | "identical to … except that" 句式 + 跨研究混淆控制 |
| §2.6 操控性细节可复现 | `logic_Carpenter_2019_4.md`、`logic_Plate_2023_4.md` | 时序完整环节链 + 「Note that…therefore differed from」自我澄清 |
| §2.7 设计约束与备选权衡 | `logic_Abramson_2024_2.md`、`logic_Vilanova_2022_4.md` | 资源约束坦诚说明 + 工具/参数/文献来源闭环 |
| §3.4 心理测量学属性 | `logic_Werchan_2024_4.md`、`logic_Vilanova_2022_4.md` | BIC/LMR/熵值多准则递进 + 信度/样本量满足要求回扣 |
| §3.5 刺激控制说明 | `logic_Phillips_2021_2.md`、`logic_Alves_2022_4.md` | 措辞变体稳健性论证 + IAPS→OASIS 替换理由 |
| §4.1 局限即时披露 | `logic_Abramson_2024_2.md`、`logic_Carpenter_2019_4.md` | 在方法选择处即披露 + 「Note that」主动澄清 |
| §4.2 样本量与功效 | `logic_Vilanova_2022_4.md`、`logic_Abramson_2024_2.md` | G*Power/Soper 闭环 + 功效模拟 .50–.77 主动披露 |
| §4.3 样本代表性与流失 | `logic_Abramson_2024_2.md` | 同质化样本 + 功效不足坦诚说明 |
| §4.6 局限披露语气 | `logic_Abramson_2024_2.md`、`logic_Carpenter_2019_4.md` | "our study is limited by…" + 自我审视口吻 |

**回退路径**（主路径无匹配时）：

1. 扫描所有正例文件的「适配诊断点」段，匹配违例类型关键词：
   - 论证链：`whereas` / `because` / `in order to` / `thereby`
   - 三档比较：`identical to` / `adapted from` / `with the following modifications`
   - 操控细节：`prior to` / `subsequently` / `Note that` / `milliseconds`
   - 局限披露：`limited by` / `negligible` / `Future work should` / `it is recognised that`
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
- 作者名用「姓 + 年」格式（Abramson 2024 / Kteily 2016 / Vilanova 2022 / Phillips 2021）
- 不省略期刊名（缩写或全称皆可，但需在第一次出现时给出全称）
- 片段前标注引用句首（如「Method 段 Design 子节第二段」「Studies 1a and 1b Method (Procedure)」）
- **不二次分发正例原文**：每份正例节选不超过 5 句；单报告引用正例不超过 3 份

### 4.4 正例目录维护

- **正例库**：49 个 `.md` 文件，软链至 `D:\method-skill-project\02-positive_examples\logic\`
- **文件名规范**：`logic_<Author>_<Year>_<n>.md`（n 为该文献片段序号）
- **正例结构**：四段式——① 片段类型（含逻辑诊断用途）② 原文片段 ③ 来源文献 ④ 适配诊断点
- **典型正例**：
  - `logic_Vilanova_2022_4.md` — 样本量论证完整闭环（G*Power + Soper 工具链 + α/.80 + 效应量文献来源 + 「本样本满足要求」回扣）
  - `logic_Phillips_2021_2.md` — 刺激抽样 + 措辞变体 + 稳健性论证（「not dependent on any specific phrasing」+ 4 例 + Table 4）
  - `logic_Abramson_2024_2.md` — 资源约束坦诚 + 功效模拟 .50–.77 先行呈现 + 「should be treated with caution」预警 + 情境差异纳入控制
  - `logic_Kteily_2016_3.md` — 覆盖故事四步递进 + filler 标准化 + 操纵关键点明文标注（「the information central to our manipulation」）+ 物理参数精确量化（96/96 vs 96/67）
  - `logic_Carpenter_2019_4.md` — 时序完整环节链 + 「Note that…therefore differed from」演示/练习自我澄清 + 训练前 8 演示 + 10 练习明确量化
- **建立软链**（已完成）：
  ```powershell
  # Windows PowerShell（已在本 Skill 创建时执行）
  New-Item -ItemType Directory -Path "D:\method-skill-project\03_skills_output\method-logic-diagnostic\references\examples" -Force
  New-Item -ItemType Junction -Path "D:\method-skill-project\03_skills_output\method-logic-diagnostic\references\examples\positive" -Target "D:\method-skill-project\02-positive_examples\logic"
  ```
- **索引文件**：建议建立 `_INDEX.md`（人读）+ `_INDEX.json`（机读），按本 Skill 4 大维度 / 22 子节归组正例（可选，当前 sibling skill 未强制）

---

## 五、输出格式（固定模板）

诊断完成后，**必须**按以下模板输出。模板中 `[…]` 为占位符，需替换为实际诊断结果。

```markdown
# Method 部分「逻辑与论证」诊断报告

**被检文本**：[文件名 / 段落定位，如 "Study 1 Method 节"]
**诊断时间**：[ISO 日期]
**诊断依据**：Science Research Writing Unit 2 + checklist.md（124 项）+ rubric.md（严重/中等/轻微三档）+ 顶刊正例 49 例

---

## 1. 维度得分

| 维度 | 检查子节数 | 检查项数 | 违例数（严重/中等/轻微） | 扣分 | 得分 |
|------|------------|----------|--------------------------|------|------|
| 1. 方法选择合理性 | 5 | 25 | x / x / x | x | x |
| 2. 研究设计逻辑自洽性 | 7 | 34 | x / x / x | x | x |
| 3. 变量与控制说明完整性 | 6 | 30 | x / x / x | x | x |
| 4. 局限性与问题说明恰当性 | 7 | 35 | x / x / x | x | x |
| **合计** | **22** | **124** | **x / x / x** | **x** | **x / 100** |

---

## 2. 整体评价

**等级**：[A / B / C / D / F]
**一句话总结**：[例如："方法选择论证链三段式基本到位、设计逻辑自洽；问题集中在控制变量入选理由缺失与局限披露未即时附补救策略。"]

---

## 3. 核心问题（按严重程度排序）

### 3.1 严重违例（必须修改，否则方法学可信度受损）

#### 问题 1：[违例类型简述，如 "方法选择无可量化事实支撑，仅「这是常用做法」"]
- **位置**：[段落 / 句编号，如 "Design 子节第 2 句"]
- **原文**：`[原句引用]`
- **违例类型**：checklist §[1.2-a] + rubric §[1.2-a]
- **严重程度判定依据**：[说明为何该选择缺乏事实/文献支撑；引用教材 §2.2.2 "your reasons are obvious to you, but they are not always obvious to readers"]
- **扣分**：[x 分]
- **修改建议**：[具体改写方案，给出 2–3 种备选]
  - 方案 A（事实支撑）：`In contrast to prior work, we used X because Y` → 加入具体可量化事实（如语料规模、零膨胀比例、效应量来源）
  - 方案 B（Option 2 句式）：`We adapted the procedure of [Author, Year] with the following modifications: ...`
  - 方案 C（INDICATE CARE）：`The procedure was independently repeated for each participant to ensure...`
- **顶刊正例**：
  - [Author Year] [Brief title]. [Journal], [Vol], [Pages].
  - **原文片段**：`[...]`
  - **适配诊断点**：[1–2 条]

#### 问题 2：[违例类型简述，如 "假设-设计-测量链条断裂：假设 H1 不可在设计中检验"]
- **位置**：[段落 / 句编号]
- **原文**：`[原句引用]`
- **违例类型**：checklist §[2.1-a] + rubric §[2.1-a]
- **严重程度判定依据**：[说明为何该假设无对应设计特征可检验；引用教材 §2.2.3 "In the following sections, we outline how both our hypotheses translate into [model]"]
- **扣分**：[x 分]
- **修改建议**：
  - 方案 A（IV 水平对齐）：`Each level of IV was operationalised as ...` → 给出每个水平的物理或符号操纵
  - 方案 B（DV 测量时点明确）：`DV was measured at Time 1 (pre-test) and Time 2 (post-test)`
  - 方案 C（统计模型映射）：`H1 was tested via 2 (condition) × 2 (gender) ANOVA on the composite score`
- **顶刊正例**：
  - [Author Year] [Brief title]. [Journal], [Vol], [Pages].
  - **原文片段**：`[...]`
  - **适配诊断点**：[1–2 条]

#### 问题 3：[违例类型简述，如 "样本量论证缺失：未报告先验功效分析"]
- **位置**：[段落 / 句编号]
- **原文**：`[原句引用]`
- **违例类型**：checklist §[4.2-a] + rubric §[4.2-a]
- **严重程度判定依据**：[说明为何未做功效论证损害结论可信度]
- **扣分**：[x 分]
- **修改建议**：
  - 方案 A（先验 G*Power）：`Sample size was determined via G*Power 3.1 to detect r = .30 with α = .05 and power = .80, requiring N = 84`
  - 方案 B（后验敏感性）：`Given our final N = 120, sensitivity analyses indicated we could detect r ≥ .25 with 80% power`
  - 方案 C（坦诚 + 替代）：`No a priori power calculation was performed due to [reason]; we therefore conducted Monte Carlo simulations to determine the detectable effect size`
- **顶刊正例**：
  - [Author Year] [Brief title]. [Journal], [Vol], [Pages].
  - **原文片段**：`[...]`
  - **适配诊断点**：[1–2 条]

### 3.2 中等违例（修改后可投稿）

#### 维度 1（方法选择合理性）

- [问题摘要 1 + 位置 + 修改要点 + 顶刊正例（如有）]
- [问题摘要 2 + 位置 + 修改要点 + 顶刊正例（如有）]

#### 维度 2（研究设计逻辑自洽性）

- [问题摘要 1 + 位置 + 修改要点 + 顶刊正例（如有）]
- [问题摘要 2 + 位置 + 修改要点 + 顶刊正例（如有）]

#### 维度 3（变量与控制说明完整性）

- [问题摘要 1 + 位置 + 修改要点 + 顶刊正例（如有）]

#### 维度 4（局限性与问题说明恰当性）

- [问题摘要 1 + 位置 + 修改要点 + 顶刊正例（如有）]

### 3.3 轻微违例（仅归类，不逐一展开）

- 维度 1：x 处（目的状语 / 谨慎副词使用不足 / 时态分工局部混乱）
- 维度 2：x 处（"Note that…"自我澄清缺失 / 时序精确度不足）
- 维度 3：x 处（量尺锚点格式不统一 / 心化目的未说明）
- 维度 4：x 处（INDICATE PROBLEMS 四组词族使用不充分）

---

## 4. 优化建议（按优先级）

1. **[优先级 P0 — 严重]** [严重违例整改路径，如"对所有方法选择补足事实/文献支撑 + Option 1/2/3 三档定位"]
2. **[优先级 P1 — 中等]** [中等违例整改路径，如"统一控制变量入选理由 + 替代解释显式排除 + 局限披露即时附补救"]
3. **[优先级 P2 — 轻微]** [轻微违例整改路径，如"全文补 INDICATE CARE 副词 + INDICATE PROBLEMS 三段式词族 + 严谨性目的状语 in order to / with the aim of"]
4. **[目标期刊对齐]** [如"JPSP 近年 Method 偏论证显式（whereas…because），PSP 偏论证简洁，需根据投稿目标调整"]
5. **[后续步骤]** [如"修改 1 轮后建议再次调用本 Skill 复检，确保降档规则不再触发；同时建议配合 method-structure-diagnostic 复检结构完整性、method-grammar-diagnostic 复检时态/被动"]

---

## 附录 A：诊断依据回链

- 参考教材：《Science Research Writing》(2nd ed.) Unit 2「How to Write about Methods」（PDF 66 页，§2.2.1–2.2.3 方法选择论证 + 6 组件 Methods model，§2.4.2 Option 1/2/3 三档 + JUSTIFY CHOICES / INDICATE CARE / INDICATE PROBLEMS 词族，§2.5.1 动词时态与 agentless passive 归属判定）
- 检查清单：`references/checklist.md`（4 大维度 / 22 子节 / 124 项）
- 评分细则：`references/rubric.md`（严重 / 中等 / 轻微三档 + A/B/C/D/F 等级）
- 顶刊正例：`references/examples/positive/`（49 例，含 JPSP / JEP:G / Developmental Psychology / PSPB / JCCP / JESP / OBHDP 等）

## 附录 B：未触发项目（完整性自检）

列出未触发任何违例的 checklist 子节，证明诊断覆盖完整：
- §1.1 方法/范式选择给出实质理由：未发现违例
- §1.5 关键方法选择语言到位：未发现违例
- §2.4 控制变量/混淆变量清单完整：未发现违例
- §3.2 因变量（DV）说明：未发现违例
- §4.7 局限语言与表述规范：未发现违例
- ...（按 checklist 顺序列出无违例子节）
```

---

## 六、使用约束

1. **本 Skill 仅诊断，不改写**：所有输出均以「问题定位 + 修改建议」形式给出，最终改写由人类作者完成，避免 AI 改写引入新错误。
2. **清单-细则严格对应**：rubric 中每一条扣分规则都能在 checklist 中找到对应 `- [ ]` 项；任何 rubric 单独新增项均视为误植。
3. **严重违例强制降档**：即便总分 ≥ 90，只要存在 1 处严重违例即降至 B；≥ 3 处严重违例强制 D；总分 < 60 强制 F。
4. **不跨维度诊断**：本 Skill 仅处理「逻辑与论证」维度；结构、语法、词汇维度请调用 sibling skill：
   - 结构 → `method-structure-diagnostic`
   - 语法 → `method-grammar-diagnostic`
   - 词汇 → `method-vocabulary-diagnostic`
5. **正例库只读**：禁止修改 `references/examples/positive/` 下的 `.md` 文件；如需新增正例，请修改源目录 `D:\method-skill-project\02-positive_examples\logic\` 并重新建立软链。
6. **教材-清单-细则三对齐**：本 Skill 的所有判定逻辑必须能回溯至 §2.2.1–2.2.3（方法选择论证 + 6 组件 Methods model）、§2.4.2（Option 1/2/3 三档 + INDICATE CARE/PROBLEMS 词族）、§2.5.1（agentless passive 归属判定）；任何诊断结论若无法引用教材原文锚点即视为误判。
7. **维度 4 局限披露即时性优先**：本 Skill 对「局限是否在发生处即时披露」检查（§4.1）优先级仅次于「假设-设计对应」——把关键方法局限堆到 Discussion 才披露，会导致读者回溯式信任崩塌，扣分按「不在文章末段首次披露关键方法局限」项（中等 −6 分）严格执行。
8. **假设-设计链条不可设计检验 → 严重 15 分**：违反后让整篇论文的因果主张失去方法学基础，必须按 rubric §2.1-a 顶档扣分。

---

**版本**：v1.0（与 checklist.md、rubric.md 同步）
**配套**：本目录下 `references/checklist.md`（检查清单）、`references/rubric.md`（评分细则）、`references/examples/positive/`（顶刊正例 49 例），四者一一对应、不得拆分使用。