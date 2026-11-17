---
name: method-vocabulary-diagnostic
version: 1.0.0
description: 诊断心理学论文Method部分的词汇与学术用语问题，检查学术动词、固定搭配、术语规范，输出评分与顶刊正例参考
metadata:
  domain: psychology-academic-writing
  dimension: vocabulary
  source: Science_Research_Writing_2nd_edition_§2.4.2
  companion_skills: [method-structure-diagnostic, method-grammar-diagnostic, method-logic-diagnostic]
user-invocable: true
---

# Method 部分「词汇与学术用语」诊断 Skill

> 覆盖《Science Research Writing》(2nd ed.) §2.4「Useful Words and Phrases」与 §2.4.2「Language for the Methods section」（基于 2,500+ 篇 STEMM 论文词频分析），专用于心理学实证论文 Method 节的词汇与学术用语层诊断。

---

## 一、诊断依据

本 Skill 的全部判定逻辑基于以下 **4 项不可拆分** 的依据，运行时按顺序加载：

| # | 依据 | 路径 | 用途 |
|---|------|------|------|
| 1 | **参考教材** | `D:\method-skill-project\01-reference\Science-Research-Writing-Second-Edition_102-167.pdf` 第 28–40 页（即 §2.4 + §2.4.2） | 来源动词、研究动词、技术动词、因果动词、空间动词、借鉴/比较三档（Option 1/2/3）、序列词、严谨性副词、happy words、INDICATE PROBLEMS 等核心词表 |
| 2 | **检查清单** | `references/checklist.md` | 4 大维度 / 43 子类 / 207 `- [ ]` 项，作为违规定位与命中判定的对照表 |
| 3 | **评分细则** | `references/rubric.md` | 严重 / 中等 / 轻微三档扣分（10–15 / 5–9 / 1–4 分/处）+ 90/80/70/60 四档等级 |
| 4 | **顶刊正例** | `references/examples/positive/` | 51 个 `.md` 文件（软链至 `02-positive_examples/vocabulary/`），含 JPSP / JEP:G / Developmental Psychology / PSPB / Behavioral Sciences 等顶刊 Method 节片段 |

> **教材原文摘录锚点**（用于本 Skill 内部一致性自检）：
> - §2.4 核心论点：「Use the language of methods sections, not the language of everyday life」—— 学术动词 + 动词+介词搭配 + 术语层级一致 + 正式语体
> - §2.4.2 三类来源动词：材料/设备来源动词（obtained/purchased/acquired/provided/supplied…）+ 通用研究动词（attempt/conduct/consider/determine/investigate/report/verify）+ 跨学科技术动词（80+ 个）
> - §2.4.2「COMPARE WITH」三档：Option 1 完全相同 / Option 2 相似 / Option 3 显著不同
> - §2.4.2「INDICATE CARE」+「INDICATE PROBLEMS」副词清单

---

## 二、核心检查项（4 大维度）

依据 `checklist.md` 提炼为以下 4 个诊断维度，运行时按此顺序扫描。

### 维度 1：学术动词准确性（对应 checklist §1，共 11 子类）

| 子项 | 关键判定 |
|------|----------|
| 1.1 材料/设备来源动词 | `was obtained from` / `was purchased from` / `was a kind gift from` 等 11 个标准动词；商业来源给公司+地点；个人赠予给姓名+单位；不混用 `obtained` vs `acquired` |
| 1.2 通用学术研究动词 | `attempt` / `conduct` / `consider` / `determine` / `investigate` / `report` / `verify`；不混用 `study`/`research`/`investigation`/`examination`；不用 `look at`/`find out` |
| 1.3 跨学科技术动词（80+） | `was adapted` / `administered` / `calibrated` / `plotted` / `synthesised` 等；操作动词与主语匹配；同操作全文用同一动词；无 -ize 类生造 |
| 1.4 因果 / 结果动词 | 25 个因果动词（`achieve`/`allow`/`enable`/`facilitate`/`prevent` 等）；避免 `made`/`gave`/`got`；避免动词堆砌 |
| 1.5 材料位置 / 空间关系动词 | 25 个位置动词（`align`/`assemble`/`install`/`mount`/`position` 等）；区分 `fit` vs `install` vs `mount` vs `position`；几何方位副词规范 |
| 1.6 操纵 / 处理动词 | 隐蔽用 `disguised as`；刻意用 `deliberately manipulated`；改编用 `adapted from`/`based on`；排除用 `excluded`/`discarded`/`removed`；随机化用 `randomly assigned`/`counterbalanced` |
| 1.7 测量 / 评分动词 | 三档：`measured`（客观量）/ `assessed`（含主观）/ `estimated`（统计估计）；五档评分（`rated`/`scored`/`coded`/`categorized`/`classified`）；记忆/识别/操纵检验/行为观察动词不混用 |
| 1.8 数据处理 / 统计动词 | EFA/CFA 动词（`conducted`/`extracted`/`rotated`/`replicated`）；SEM/LTA 拟合动词（`fitted`/`estimated`/`tested`）；数据清洗动词（`cleaned`/`screened`/`winsorized`）；区分 `performed` vs `conducted` |
| 1.9 严谨性副词 | 27 个「INDICATE CARE」副词（`carefully`/`precisely`/`rigorously` 等）；形容词/副词形式不混用；不用 `very`/`really`/`extremely` |
| 1.10 「happy words」积极修饰词 | 13 个规范形容词（`accurate`/`consistent`/`robust`/`reliable`/`suitable` 等）；不用 `great`/`nice`/`good`/`awesome`/`cool`；与严谨性副词配套 |
| 1.11 局限 / 困难表达动词 | `limited by`/`minimised`/`inevitable`/`unavoidable` 等；不推卸（`we couldn't`）；不贬低（`our method was bad`） |

### 维度 2：固定搭配规范性（对应 checklist §2，共 10 子类）

| 子项 | 关键判定 |
|------|----------|
| 2.1 借鉴 / 比较搭配（COMPARE WITH 三档） | Option 1 用 `according to`/`as described by`/`identical to`；Option 2 用 `adapted from`/`essentially the same`/`with some modifications`；Option 3 用 `a novel step was`/`unlike`/`with the following modifications`；`by/of` 后接研究者名，`in` 后接文献 |
| 2.2 对比 / 让步连词（CONTRAST） | 段内对比用 `however`/`whereas`/`by contrast`；条件用 `either…or…`/`both…and…`；让步用 `although`/`despite`；不用口语 `but`/`and`/`also` |
| 2.3 序列连接词（SEQUENCE LANGUAGE 8 组） | Group 1 实验前 `prior to`/`previously`；Group 2 开始 `firstly`/`initially`；Group 3 顺序 `subsequently`/`followed by`；Group 4 短间隔 `shortly after`；Group 5 较晚 `eventually`/`later`；Group 6 同时 `simultaneously`/`while`；Group 7 结尾 `finally`；Group 8 实验后 `afterwards`；避免 `and then`/`after that`/`next thing`；时间状语精确化 |
| 2.4 理由 / 目的搭配（JUSTIFY CHOICES） | 显式目的 `in order to`/`with the aim of`/`so as to`/`chosen for/to`/`designed for/to`；不省略目的（每个操作附 `to ensure`/`to account for`）；区分 `so as to` vs `in order to` vs `to` |
| 2.5 因果信号连接词 | `because`/`since`/`therefore`/`thus`/`hence`/`consequently`/`thereby`；`so` 单独承担因果 → 改为 `therefore`/`thus`/`hence` |
| 2.6 介词决定动词 / 名词含义 | `evidence of` vs `evidence for`（存在/可能存在）；`substituted for` vs `substituted with`（方向）；`hit by` vs `hit with`（意图）；`coated with` vs `coated by`（过程）；介词搭配一致 |
| 2.7 来源 / 引用搭配 | 引用紧贴被引用方法/结果；多文献格式统一（`Smith et al. (2010)` 或 `(Smith et al., 2010)`）；改编引用与完全相同引用区分 |
| 2.8 量表 / 测量方法搭配 | 量尺锚点格式统一（`1 (strongly disagree) to 7 (strongly agree)` 或 `1 = strongly disagree to 7 = strongly agree`）；「assessed via / measured by / evaluated using」按语义选；量表报告公式化；缩写首次给全称 |
| 2.9 数据呈现搭配 | 统计值报告统一（`M = 3.51 (SD = 1.35)` 或 `M = 3.51, SD = 1.35`）；范围含端点；样本量绑定；排除量化 |
| 2.10 标点 / 缩写搭配 | 引号使用；破折号三类（em/en/hyphen）；缩写首次给全称；单位空格（5 s, 650 ms）；百分号无空格（72.43%） |

### 维度 3：专业术语一致性（对应 checklist §3，共 8 子类）

| 子项 | 关键判定 |
|------|----------|
| 3.1 核心概念术语全文统一 | `participants`/`subjects`/`respondents`/`individuals` 四选一；`condition`/`group`/`level` 三选一；`stimulus`/`material`/`item` 按对象选；`response`/`rating` 按反应类型选；`task`/`paradigm`/`procedure`/`trial` 按颗粒度选 |
| 3.2 构念名即小节标题 | `Dehumanization.` / `Prejudice.` / `Mortality Salience.` 直命名；子节标题以正式名为主、必要时冒号后接通俗名；同名小标题全文一致 |
| 3.3 操纵 / 测量命名体系 | 操纵条件标签全文一致（`caring / uncaring`）；测量命名体系内部自洽；操纵材料命名可识别；量表/范式版本号一致（`HEXACO-60` vs `HEXACO-100`） |
| 3.4 缩略词管理 | 首次给全称（`SEM`/`FIML`/`ECS`/`IAT`/`LTA`）；同名缩略词全文一致（`SEM` 不混用 `S.E.M.`/`sem`）；自创缩略词遵循首字母规则 |
| 3.5 构念定义 → 测量工具 → 评分 → 量尺 链条 | `构念定义 → 测量工具 → 条目/题项 → 计分 → 量尺锚点 → 信度` 顺序报告；量尺锚点逐字；计分方向显式；信度规范（`Cronbach's α = .86`） |
| 3.6 题项 / 操纵材料原文引用 | 题项完整原文（带引号或斜体）；操纵材料以参与者视角原文；多题项编号一致；原文引用前给位置/上下文 |
| 3.7 统计符号 / 量表符号 | 统计符号格式一致（`M`/`SD`/`α`/`ω`/`CR`/`AVE`/`CFI`/`RMSEA`/`SRMR`）；量表锚点全文一致；p 值格式一致；效应量格式一致；置信区间格式一致 |
| 3.8 工具版本 / 数据集名 | 量表版本号一致；数据集/样本来源名一致；平台名称一致（`MTurk` 不混用 `Amazon Mechanical Turk`）；软件版本一致 |

### 维度 4：正式语体恰当性（对应 checklist §4，共 14 子类）

| 子项 | 关键判定 |
|------|----------|
| 4.1 避免口语化连接词 | 不用 `then`/`and then`/`next thing` 单独衔接；不用 `but`/`also`/`and` 单独让步；不用 `so` 单独因果；优先 Group 1–8 序列词 |
| 4.2 避免口语化动词 | 不用 `do/did`/`get/got`/`make/made`/`have/had`/`give/gave`/`go/went`/`look at`/`figure out` 替代正式动词 |
| 4.3 避免口语化语气 | 不用 `I`/`you`/反问/感叹/缩写形式（`don't`/`can't`）/俚语（`a bunch of`）/夸张副词（`very`/`really`） |
| 4.4 避免口语化名词 / 量词 | 不用 `a lot of`/`big`/`thing`/`kind of`；集合名词用 `a set of`/`a battery of`/`a series of` |
| 4.5 严谨性副词使用规范 | 操作附严谨性副词（`carefully`/`precisely`/`gently`/`thoroughly`/`rigorously` 等）；与具体操作匹配（`tightly clamped`/`gently inverted`）；不滥用（每段 ≤ 3 处）；与 `every`/`each`/`both`/`all` 配套 |
| 4.6 「happy words」使用规范 | 用规范形容词（`reliable`/`robust`/`precise`）；不用口语积极词（`great`/`nice`/`awesome`/`amazing`）；以方法效果为单位不以个人感受为单位 |
| 4.7 局限性表达规范（INDICATE PROBLEMS） | 程度副词+形容词（`slightly problematic`/`less than ideal`）；否定副词+形容词（`negligible`/`not significant`）；责任最小化（`inevitable`/`unavoidable`/`limited by`）；客观归因（`it was difficult to`）；三段式（`Although X was difficult, Y was negligible`）；不推卸不贬低不隐瞒 |
| 4.8 目的 / 理由表达规范 | 每个操作附目的（`to ensure`/`in order to`/`to account for`）；不罗列无目的；目的状语 `To + V` 开头；多层释义递进界定操纵构念 |
| 4.9 操纵 / 测量描述的语体层级 | 抽象 → 具体两层（`We assessed X. Specifically, …`）；目的 → 方法 → 结果三层；同行衔接（`Similar to…`）；本题对比（`Unlike previous studies…`） |
| 4.10 释义与术语解释 | 缩略语/术语首次同位语解释（`paraphrases, that is, the definition for…`）；操纵构念三层递进（`in other words`/`that is`/`specifically`/`for example`）；操作定义结构化（`核心 because + That is + For example`） |
| 4.11 题项 / 操纵材料引用语体 | 题项原文使用引号；操纵材料参与者视角原文；引用配上下文（`presented on the screen`）；多题项编号一致 |
| 4.12 焦点信号词 | `Specifically`（抽象后具体）；`In specific`（更正式）；`Moreover`/`Furthermore`/`Additionally`（添加信息）；`In contrast`/`On the other hand`（对比） |
| 4.13 引用风格统一 | 引用紧贴被引用方法/结果；格式全文一致；自我引用位置规范；多文献顺序一致 |
| 4.14 整体段落语气一致 | 全文「研究者报告」第三人称客观；段落开头避免悬念（`Unexpectedly`/`Notably`）；句末避免弱化（`…kind of worked` → `…did not reach significance`）；不出现语气词（`well`/`actually`/`basically`） |

---

## 三、执行步骤（6 步）

```
Step 1 读取规则 → Step 2 扫描文本 → Step 3 对照核验 → Step 4 计算得分 → Step 5 匹配正例 → Step 6 输出结果
```

### Step 1 — 读取规则

加载以下 3 份规则文件至内存：
- `references/checklist.md`（4 大维度 / 43 子类 / 207 项 `- [ ]`）
- `references/rubric.md`（严重 / 中等 / 轻微扣分区间 + 90/80/70/60 四档等级）
- `references/examples/positive/` 正例库（51 个 `.md` 文件，按文件名 `vocabulary_<Author>_<Year>_<n>.md` 索引）

构建内存映射表：`{checklist_id → (severity, score_range, positive_examples[])}`。

### Step 2 — 扫描文本

按 Method 节实际段落顺序（Participants / Design / Measures / Procedure / Analysis），逐句扫描。建议扫描粒度：
- 一句 = 一个扫描单元
- 程序链整段 = 一个聚合单元（用于检测序列词堆砌）

扫描时同步记录：
- 动词类别（来源动词 / 研究动词 / 技术动词 / 因果动词 / 空间动词 / 操纵动词 / 测量动词 / 评分动词 / 统计动词）
- 介词搭配（`of`/`for`/`with`/`by`/`in` 等方向性介词）
- 术语一致（被试/条件/刺激/反应/任务/操纵/测量等核心概念术语）
- 口语化标记（`do/did/make/got/look at/figure out` 等）
- 严谨性副词（`carefully`/`precisely`/`rigorously` 等）
- 局限 / 困难表达模式（程度副词+形容词 / 否定副词+形容词 / 责任最小化）
- 量尺锚点格式、统计符号格式、引用格式

### Step 3 — 对照核验

每发现一处违例，按以下逻辑归类：

```
1. 在 checklist 中找到对应的 `- [ ]` 项（按 checklist_id，如 1.1-b / 2.6-b / 3.5-a）
2. 在 rubric 中确定 severity（严重 / 中等 / 轻微）
3. 在 rubric 扣分区间内取具体分数（按违例严重度在该区间内）
4. 同项多处违例按 N × 单项扣分累计，但同一段落内的同类型重复计入 1 次
5. 一处违例触发多规则 → 按最严重等级判定一次，不重复扣分
6. 单子类累计扣分达上限时封顶（见 rubric 各子类末标注）
```

**严重性判定核心问题**：违反后是否让读者无法判断方法的操作含义、归属或学术可信度？
- 核心方法学术动词误用导致操作含义歧义 → 严重（10–15 分）
- 专业术语错误引发学术误解（介词方向、混用）→ 严重（10–15 分）
- 固定搭配不规范、用词口语化、术语前后不一致 → 中等（5–9 分）
- 个别用词可优化、词汇丰富度不足 → 轻微（1–4 分）

### Step 4 — 计算得分

```
原始得分 = 100 − Σ(各处扣分)
最终等级 = A (≥ 90) / B (80–89) / C (70–79) / D (60–69) / 不通过 (< 60)
强制 D = 严重违例 ≥ 4 项
封底 = 0 分（扣分上限 100 分）
```

详见 `references/rubric.md` 末尾「90 / 80 / 70 / 60 四档等级说明」。

### Step 5 — 匹配正例

按本 Skill 第四节「正例调用规则」从 `references/examples/positive/` 中匹配正例。匹配成功后读取该正例文件，提取「原文片段 / 来源文献 / 适配诊断点」三段内容。

### Step 6 — 输出结果

按本 Skill 第五节「输出格式」的固定模板输出诊断报告。模板含 4 个必备模块：
1. 维度得分表
2. 整体评价
3. 核心问题（按严重度排序 + 修改建议 + 顶刊正例）
4. 优化建议

---

## 四、正例调用规则

### 4.1 触发条件

| 违例等级 | 是否调用正例 |
|----------|--------------|
| **严重** | **必须调用 1 个**（核心动词误用 / 术语错误 / 介词方向错误类） |
| **中等** | **每个维度最多 2 个**（避免正例轰炸） |
| **轻微** | **不调用正例**（仅在「优化建议」中归类汇总） |
| 无违例 | 不调用正例 |

### 4.2 匹配逻辑

**主路径**（按 checklist 检查项编号匹配）：

1. 根据 Step 3 命中的 checklist_id（如 `1.1`、`1.7`、`2.6`、`3.5`、`4.7`），在正例库的「适配诊断点」段中扫描关键词：
   - 维度 1（学术动词）：`obtained`/`acquired`/`assessed`/`measured`/`estimated`/`scored`/`coded`/`disguised`/`deliberately manipulated`/`adapted`/`reverse`/`anchored`/`slider` 等
   - 维度 2（固定搭配）：`Likert`/`range`/`M =`/`SD =`/`as described`/`adapted from`/`following`/`Cronbach's α` 等
   - 维度 3（术语一致）：`participants`/`subjects`/`condition`/`scale (Author, Year)`/`developed by` 等
   - 维度 4（正式语体）：`Specifically`/`In particular`/`Furthermore`/`Similar to`/`Following`/`we assessed` 等
2. 提取关键词出现 ≥ 2 次且与当前违例类型语义相关的正例 1 个。
3. 若命中多个正例，按以下优先级选 1 个：
   - 优先文件名较新者（年份大者）
   - 同年优先编号靠后者（编号越大适配诊断点越细）
   - 同年同号优先文件名较短者

**回退路径**（主路径无匹配时）：

1. 扫描所有正例文件的标题与首段，匹配违例类型关键词（中文/英文双语匹配）。
2. 若仍无匹配，跳过正例引用，仅在「修改建议」中给出词汇改写模板。

### 4.3 展示要求

每条命中的正例在「核心问题」模块中按以下三行格式展示：

```
**顶刊正例**：[Author Year] [Brief title]. [Journal], [Vol/Issue], [Pages].
**原文片段**：[截取 50–150 字核心句段，含必要的上下文]
**适配诊断点**：[从正例「适配诊断点」段选 1–2 条最相关的]
```

引用要求：
- 作者名用「姓 + 年」格式（Gao 2025 / Kteily 2016 / Rudert 2023）
- 不省略期刊名
- 片段前标注引用句首（如「Method 段 Measures 子节第一段」）

### 4.4 正例目录维护

- **正例库**：51 个 `.md` 文件，软链至 `D:\method-skill-project\02-positive_examples\vocabulary\`
- **文件名规范**：`vocabulary_<Author>_<Year>_<n>.md`（n 为该文献片段序号）
- **正例结构**：四段式——① 片段类型 ② 原文片段 ③ 来源文献 ④ 适配诊断点
- **典型正例**：
  - `vocabulary_Kteily_2016_2.md` —— 标准化量表与滑块的精确描述（构念名即小节标题、`Specifically` 抽象→具体、量尺锚点完整）
  - `vocabulary_Gao_2025_2.md` —— 问卷改编来源与示例题项（双层谱系、`modified version` vs `adapted` 区分、量表公式化报告）
  - `vocabulary_Rudert_2023_2.md` —— 操纵材料原文引用（参与者可见完整定义、`核心 because + That is + For example` 三要素）
- **建立软链**（一次性）：
  ```bash
  # Windows PowerShell
  New-Item -ItemType Junction -Path "D:\method-skill-project\03_skills_output\method-vocabulary-diagnostic\references\examples\positive" -Target "D:\method-skill-project\02-positive_examples\vocabulary"
  ```
- **索引文件**：建议建立 `_INDEX.md`（人读）+ `_INDEX.json`（机读），按本 Skill 4 大维度 / 43 子项归组正例（可选，当前 sibling skill 未强制）

---

## 五、输出格式（固定模板）

诊断完成后，**必须**按以下模板输出。模板中 `[…]` 为占位符，需替换为实际诊断结果。

```markdown
# Method 部分「词汇与学术用语」诊断报告

**被检文本**：[文件名 / 段落定位，如 "Study 1 Method 节"]
**诊断时间**：[ISO 日期]
**诊断依据**：Science Research Writing §2.4.2 + checklist.md + rubric.md + 顶刊正例 51 例

---

## 1. 维度得分

| 维度 | 检查子类数 | 违例数（严重/中等/轻微） | 扣分 | 得分 |
|------|------------|--------------------------|------|------|
| 1. 学术动词准确性 | 11 | x / x / x | x | x |
| 2. 固定搭配规范性 | 10 | x / x / x | x | x |
| 3. 专业术语一致性 | 8 | x / x / x | x | x |
| 4. 正式语体恰当性 | 14 | x / x / x | x | x |
| **合计** | **43** | **x / x / x** | **x** | **x / 100** |

---

## 2. 整体评价

**等级**：[A / B / C / D / 不通过]
**一句话总结**：[例如："学术动词选择准确，固定搭配规范；问题集中在介词方向性搭配（substituted for/with）与量尺锚点格式不统一。"]

---

## 3. 核心问题（按严重程度排序）

### 3.1 严重违例（必须修改，否则有学术可信度风险）

#### 问题 1：[违例类型简述，如 "介词方向性搭配错误：substituted for/with 互换"]
- **位置**：[段落 / 句编号，如 "Measures 子节第 3 句"]
- **原文**：`[原句引用]`
- **违例类型**：checklist §[2.6-b] + rubric §[2.6-b]
- **严重程度判定依据**：[说明为何该错误导致操作含义歧义：例如 "substituted for Y = X 替换 Y；substituted with Y = Y 替换 X，主语与宾语方向相反"]
- **扣分**：[x 分]
- **修改建议**：[具体改写方案，给出 1–2 种备选]
  - 方案 A（方向修正）：`X was substituted for Y` → `X was substituted with Y`
  - 方案 B（改写句式）：`We replaced Y with X` / `Y was replaced by X` / `We substituted Y with X`
- **顶刊正例**：
  - [Author Year] [Brief title]. [Journal], [Vol], [Pages].
  - **原文片段**：`[...]`
  - **适配诊断点**：[1–2 条]

#### 问题 2：[...]
#### 问题 3：[...]

### 3.2 中等违例（修改后可投稿）

#### 维度 1（学术动词准确性）

- [问题摘要 1 + 位置 + 修改要点 + 顶刊正例（如有）]
- [问题摘要 2 + 位置 + 修改要点 + 顶刊正例（如有）]

#### 维度 2（固定搭配规范性）

- [问题摘要 + 位置 + 修改要点 + 顶刊正例（如有）]
- [问题摘要 + 位置 + 修改要点 + 顶刊正例（如有）]

#### 维度 3（专业术语一致性）

- [问题摘要 + 位置 + 修改要点 + 顶刊正例（如有）]

#### 维度 4（正式语体恰当性）

- [问题摘要 + 位置 + 修改要点 + 顶刊正例（如有）]

### 3.3 轻微违例（仅归类，不逐一展开）

- 维度 1：x 处（happy words 使用不足 / 严谨性副词匮乏）
- 维度 2：x 处（标点 / 缩写 / 排版细节）
- 维度 3：x 处（统计符号格式 / 版本号一致性）
- 维度 4：x 处（口语化副词 / 模糊量词）

---

## 4. 优化建议（按优先级）

1. **[优先级 P0 — 严重]** [严重违例整改路径，如 "全文扫一遍介词方向性搭配（substituted for/with、coated with/by、hit by/with），按操作方向逐一修正"]
2. **[优先级 P1 — 中等]** [中等违例整改路径，如 "统一核心术语全文一致：participants vs subjects vs respondents 选一；统计符号 M/SD/α 全文用同一格式"]
3. **[优先级 P2 — 轻微]** [轻微违例整改路径，如 "happy words 与严谨性副词配套：a reliable method based on HPLC / a robust analytical method"]
4. **[目标期刊对齐]** [如 "JPSP 近年 Method 节术语高度统一，PSP 偏 British English，需根据投稿目标调整"]
5. **[后续步骤]** [如 "修改 1 轮后建议再次调用本 Skill 复检，确保降档规则不再触发"]

---

## 附录 A：诊断依据回链

- 参考教材：Science Research Writing (2nd ed.) §2.4.2（PDF 页 28–40）
- 检查清单：references/checklist.md（4 大维度 / 43 子类 / 207 项）
- 评分细则：references/rubric.md（严重 / 中等 / 轻微三档 + 90/80/70/60 四档等级）
- 顶刊正例：references/examples/positive/（51 例，含 JPSP / JEP:G / Developmental Psychology / PSPB / Behavioral Sciences 等）

## 附录 B：未触发项目（完整性自检）

列出未触发任何违例的 checklist 子项，证明诊断覆盖完整：
- §1.1 材料/设备来源动词：未发现违例
- §1.2 通用学术研究动词：未发现违例
- §2.10 标点 / 缩写搭配：未发现违例
- §3.7 统计符号 / 量表符号：未发现违例
- ...（按 checklist 顺序列出无违例子项）
```

---

## 六、使用约束

1. **本 Skill 仅诊断，不改写**：所有输出均以「问题定位 + 修改建议」形式给出，最终改写由人类作者完成，避免 AI 改写引入新错误。
2. **清单-细则严格对应**：rubric 中每一条扣分规则都能在 checklist 中找到对应 `- [ ]` 项；任何 rubric 单独新增项均视为误植。
3. **严重违例强制降档**：即便总分 ≥ 90，只要存在 1 处严重违例即降至 B；≥ 4 处严重违例强制 D。
4. **不跨维度诊断**：本 Skill 仅处理「词汇与学术用语」维度；结构、语法、逻辑维度请调用 sibling skill：
   - 结构 → `method-structure-diagnostic`
   - 语法 → `method-grammar-diagnostic`
   - 逻辑 → `method-logic-diagnostic`
5. **正例库只读**：禁止修改 `references/examples/positive/` 下的 `.md` 文件；如需新增正例，请修改源目录 `D:\method-skill-project\02-positive_examples\vocabulary\` 并重新建立软链。
6. **介词方向性敏感**：本 Skill 对介词决定动词/名词含义的检查（§2.6）优先级最高——这类错误会直接改变句子操作含义，必须按严重判定。

---

**版本**：v1.0（与 checklist.md、rubric.md 同步）
**配套**：本目录下 `references/checklist.md`（检查清单）、`references/rubric.md`（评分细则）、`references/examples/positive/`（顶刊正例 51 例），三者一一对应、不得拆分使用。
