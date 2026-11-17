---
name: method-grammar-diagnostic
version: 1.0.0
description: 诊断心理学论文Method部分的语法与句法问题，检查时态、被动语态、句子结构规范，输出评分与顶刊正例参考
metadata:
  domain: psychology-academic-writing
  dimension: grammar
  source: Science_Research_Writing_2nd_edition_§2.5.1
  companion_skills: [method-structure-diagnostic, method-logic-diagnostic, method-vocabulary-diagnostic]
user-invocable: true
---

# Method 部分「语法与句法」诊断 Skill

> 覆盖《Science Research Writing》(2nd ed.) §2.5.1「Verb tense and the agentless passive」及其相关语言规范，专用于心理学实证论文 Method 节的语法与句法层诊断。

---

## 一、诊断依据

本 Skill 的全部判定逻辑基于以下 **4 项不可拆分** 的依据，运行时按顺序加载：

| # | 依据 | 路径 | 用途 |
|---|------|------|------|
| 1 | **参考教材** | `references/../01-reference/Science-Research-Writing-Second-Edition_102-167.pdf` 第 41–48 页（即 §2.5.1 + §2.5.2） | 时态分工原则、五种 agentless passive 消歧策略、介词使用规则、`make it impossible for the reader not to understand` 核心原则 |
| 2 | **检查清单** | `references/checklist.md` | 4 大维度 / 25 小节 / 110+ `- [ ]` 项，作为违规定位与命中判定的对照表 |
| 3 | **评分细则** | `references/rubric.md` | 严重 / 中等 / 轻微三档扣分（10–15 / 5–9 / 1–4 分/处）+ A/B/C/D 等级 + 降档规则 |
| 4 | **顶刊正例** | `references/examples/positive/` | 47 个 `.md` 文件（软链至 `02-positive_examples/grammar/`），含 JPSP / JEP:G / Developmental Psychology / PSPB / JCCP 等顶刊 Method 节片段 |

> **教材原文摘录锚点**（用于本 Skill 内部一致性自检）：
> - §2.5.1 核心论点：「THE AIM IS NOT SIMPLY TO MAKE IT POSSIBLE FOR THE READER TO UNDERSTAND; THE AIM IS TO MAKE IT IMPOSSIBLE FOR THE READER NOT TO UNDERSTAND」
> - 五种 agentless passive 用法（自研 / 借鉴 / 标准程序 / Figure 内混合 / 期刊要求 Present Simple）的消歧策略见 PDF 第 42–43 页
> - 时态分工原则：「Past Simple 报告 what you did，Present Simple 描述 standard procedures or equipment」

---

## 二、核心检查项（4 大维度）

依据 `checklist.md` 提炼为以下 4 个诊断维度，运行时按此顺序扫描。

### 维度 1：时态一致性（对应 checklist §1，共 6 小节）

| 子项 | 关键判定 |
|------|----------|
| 1.1 本研究操作 | 一般过去时贯穿（recruited / coded / estimated / fitted） |
| 1.2 标准程序 / 设备 / 软件 | 一般现在时恒常属性（the eye tracker records…, Mplus uses…） |
| 1.3 既有证据 / 既定事实 | 现在完成时或一般现在时 + 引用（have been shown to…, following prior research） |
| 1.4 同段并列要素时态一致 | 时间链 First/Next/Finally 一律过去时；排除规则 (a)(b)(c) 平行动词 |
| 1.5 时态与所指对象对齐 | 「was collected」vs「is collected」不混用 = 严重归属歧义 |
| 1.6 完成后强制核查 | 逐句核查动词时态，存疑即改 |

### 维度 2：被动语态规范（对应 checklist §2，共 5 小节，**全 Skill 重头戏**）

| 子项 | 关键判定 |
|------|----------|
| 2.1 主-被动体例统一 | 段间不无序切换主-被动；目标期刊体例事先对齐 |
| 2.2 agentless passive 消歧（§2.5.1 五种用法） | 用法 1（自研）→ 主动 We + 限定词；用法 2（借鉴）→ 引用；用法 3（标准）→ 引用 / 标准化标识；用法 4（Figure 混合）→ 显式声明；用法 5（Present Simple 期刊）→ 限定词 |
| 2.3 主动语态规范使用 | We + 过去时；目的状语 To + V 开头；避免「We conducted a study in which…」 |
| 2.4 被动语态合理场景 | 接受方被动（were asked）；材料主语被动（was placed in…）；避免连续 5+ 句无施事被动堆砌 |
| 2.5 归属清晰（ownership） | In this study / here / in our model 标注本研究；as described by / adapted from / unlike 三分关系 |

### 维度 3：句子结构合理性（对应 checklist §3，共 6 小节）

| 子项 | 关键判定 |
|------|----------|
| 3.1 句式模板 | To + V 开头；三段式论证（are inappropriate because → Thus we estimated → robust SE）；量表报告公式 |
| 3.2 时间顺序与序列标记 | In a first step / Subsequently / Upon completion；避免口语 then/and then；时间状语精确化（650 ms、every 5 s） |
| 3.3 条件、对照与平行结构 | 实验条件仅关键形容词对位变化；either…or… 完整陈述；多研究同构 |
| 3.4 长句内部结构 | 破折号 / 括号 / 插入语分层；避免介词链 5+；修饰语贴近被修饰名词；关键概念 i.e. 注释 |
| 3.5 复合句与从句类型分工 | 原因 because / 目的 to ensure / 条件 when / 让步 although / 时间 after，每个操作附理由 |
| 3.6 强调与总结句 | These results indicate…；Together, these X tests validate…；Thus / Hence / Therefore |

### 维度 4：语法准确性（对应 checklist §4，共 8 小节）

| 子项 | 关键判定 |
|------|----------|
| 4.1 主谓一致 | 单数可数 → 单数谓语；集体名词 a battery of / a series of 配合 of 后名词 |
| 4.2 名词与冠词 | 单数可数名词必须带冠词；缩略词首次给全称 |
| 4.3 介词使用 | evidence of vs for；substituted for vs with；with 歧义敏感；避免介词链 |
| 4.4 代词指代 | it / they / this / these 指代无歧义；this study 不被误读为引用文献 |
| 4.5 比较与量化结构 | than 前后比较对象平行；范围含端点；数值绑定样本量 |
| 4.6 数、量、单位、符号 | 数值与单位留空格（5 s, 650 ms）；百分号无空格（72.43%）；en-dash 用于范围（18–79） |
| 4.7 标点、缩写与排版 | 缩写首次给全称；em-dash 用于插入语；句号位置正确 |
| 4.8 一致性 | participants / subjects 不混用；M/SD 报告格式全文一致 |

---

## 三、执行步骤（6 步）

```
Step 1 读取规则 → Step 2 扫描文本 → Step 3 对照核验 → Step 4 计算得分 → Step 5 匹配正例 → Step 6 输出结果
```

### Step 1 — 读取规则

加载以下 3 份规则文件至内存：
- `references/checklist.md`（结构化 `- [ ]` 项）
- `references/rubric.md`（扣分区间 + 等级表）
- `references/examples/positive/_INDEX.json`（正例索引）

构建内存映射表：`{checklist_id → (severity, score_range, positive_examples[])}`。

### Step 2 — 扫描文本

按 Method 节实际段落顺序（Participants / Design / Measures / Procedure / Analysis），逐句扫描。建议扫描粒度：
- 一句 = 一个扫描单元
- 程序链整段 = 一个聚合单元（用于检测时间链时态一致性）

扫描时同步记录：动词时态、被动/主动、归属限定词（in this study / here）、主语类型（人称 / 材料 / 数据）、冠词、介词搭配、并列项动词形式。

### Step 3 — 对照核验

每发现一处违例，按以下逻辑归类：

```
1. 在 checklist 中找到对应的 `- [ ]` 项（按 checklist_id）
2. 在 rubric 中确定 severity（严重 / 中等 / 轻微）
3. 在 rubric 扣分区间内取具体分数（按违例严重度在该区间内）
4. 同项多处违例按 N × 单项扣分累计，但单处封顶区间内高值
5. 一处违例触发多规则 → 按最严重等级判定一次，不重复扣分
```

**严重性判定核心问题**：违反后是否让读者无法判断方法的归属、责任主体或时间链？「是」= 严重；仅影响可读性 = 中等；仅排版或搭配瑕疵 = 轻微。

### Step 4 — 计算得分

```
原始得分 = 100 − Σ(各处扣分)
降档判定 = 严重违例数 + 系统性违例上调
最终等级 = A (90–100) / B (80–89) / C (70–79) / D (60–69)
强制 D = 严重违例 ≥ 3 处
不通过 = 总分 < 60 或严重 ≥ 3
```

详见 `references/rubric.md` 第四节「等级说明」与 4.1「等级降档规则」。

### Step 5 — 匹配正例

按本 Skill 第四节「正例调用规则」从 `references/examples/positive/_INDEX.json` 中匹配正例。匹配成功后读取该正例文件，提取「原文片段 / 来源文献 / 适配诊断点」三段内容。

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
| **严重** | **必须调用 1 个**（归属 / 时态错位 / 学术诚信类） |
| **中等** | **每个维度最多 2 个**（避免正例轰炸） |
| **轻微** | **不调用正例**（仅在「优化建议」中归类汇总） |
| 无违例 | 不调用正例 |

### 4.2 匹配逻辑

**主路径**（按 checklist 检查项编号匹配）：

1. 根据 Step 3 命中的 checklist_id（如 `1.5`、`2.2.用法1`、`3.4`），在 `_INDEX.json` 中查 `checklist_id → 正例文件名[]` 映射表。
2. 若命中多个正例，按以下优先级选 1 个：
   - 优先文件名较新者（年份大者）
   - 同年优先编号靠后者（编号越大适配诊断点越细）
   - 同年同号优先文件名较短者

**回退路径**（主路径无匹配时）：

1. 在所有正例文件的「适配诊断点」段中扫描违例类型关键词（如「agentless passive」「time chain」「parallel structure」「hanging modifier」）。
2. 提取关键词出现 ≥ 2 次且与当前违例类型语义相关的正例 1 个。
3. 若仍无匹配，跳过正例引用，仅在「修改建议」中给出语法改写模板。

### 4.3 展示要求

每条命中的正例在「核心问题」模块中按以下三行格式展示：

```
**顶刊正例**：[Author Year] [Brief title]. [Journal], [Vol/Issue], [Pages].
**原文片段**：[截取 50–150 字核心句段，含必要的上下文]
**适配诊断点**：[从正例「适配诊断点」段选 1–2 条最相关的]
```

引用要求：
- 作者名用「姓 + 年」格式（Abramson 2024 / Kteily 2016 / Damian 2018）
- 不省略期刊名
- 片段前标注引用句首（如「Method 段 Procedure 子节第二段」）

### 4.4 正例目录维护

- **正例库**：47 个 `.md` 文件，软链至 `D:\method-skill-project\02-positive_examples\grammar\`
- **索引文件**：`_INDEX.md`（人读）+ `_INDEX.json`（机读）
- **索引生成**：参考 sibling skill `method-structure-diagnostic/references/examples/positive/_INDEX.json` 的格式，按本 Skill 的 4 大维度 / 25 子项归组
- **更新触发**：当正例库新增 / 删除文件，或 checklist 结构调整时，重跑索引脚本

---

## 五、输出格式（固定模板）

诊断完成后，**必须**按以下模板输出。模板中 `[…]` 为占位符，需替换为实际诊断结果。

```markdown
# Method 部分「语法与句法」诊断报告

**被检文本**：[文件名 / 段落定位，如 "Study 1 Method 节"]
**诊断时间**：[ISO 日期]
**诊断依据**：Science Research Writing §2.5.1 + checklist.md + rubric.md + 顶刊正例 47 例

---

## 1. 维度得分

| 维度 | 检查小节数 | 违例数（严重/中等/轻微） | 扣分 | 得分 |
|------|------------|--------------------------|------|------|
| 1. 时态一致性 | 6 | x / x / x | x | x |
| 2. 被动语态规范 | 5 | x / x / x | x | x |
| 3. 句子结构合理性 | 6 | x / x / x | x | x |
| 4. 语法准确性 | 8 | x / x / x | x | x |
| **合计** | **25** | **x / x / x** | **x** | **x / 100** |

---

## 2. 整体评价

**等级**：[A / B / C / D / 不通过]
**一句话总结**：[例如："主-被动体例统一、时态分工基本到位；问题集中在 agentless passive 归属标记缺失与排除规则并列项动词形式不一致。"]

---

## 3. 核心问题（按严重程度排序）

### 3.1 严重违例（必须修改，否则有学术诚信风险）

#### 问题 1：[违例类型简述，如 "用法 1 自研工作未标 in this study"]
- **位置**：[段落 / 句编号，如 "Participants 子节第 2 句"]
- **原文**：`[原句引用]`
- **违例类型**：checklist §[x.x] + rubric §[x.x]
- **严重程度判定依据**：[引用 §2.5.1 原文片段，说明为何归属歧义]
- **扣分**：[x 分]
- **修改建议**：[具体改写方案，给出 2–3 种备选]
  - 方案 A（主动化）：`We collected / We modified ...`
  - 方案 B（限定词）：`In this study, X was collected...`
  - 方案 C（假主语）：`This experiment / The procedure described above ...`
- **顶刊正例**：
  - [Author Year] [Brief title]. [Journal], [Vol], [Pages].
  - **原文片段**：`[...]`
  - **适配诊断点**：[1–2 条]

#### 问题 2：[...]

### 3.2 中等违例（修改后可投稿）

#### 维度 2（被动语态规范）

- [问题摘要 1 + 位置 + 修改要点 + 顶刊正例（如有）]
- [问题摘要 2 + 位置 + 修改要点 + 顶刊正例（如有）]

#### 维度 3（句子结构合理性）

- [问题摘要 + 位置 + 修改要点 + 顶刊正例（如有）]

### 3.3 轻微违例（仅归类，不逐一展开）

- 维度 1：x 处（介词 / 排版细节）
- 维度 2：x 处（缩略词未给全称 / 主动语态冗余）
- 维度 4：x 处（数值空格 / 量表锚点格式）

---

## 4. 优化建议（按优先级）

1. **[优先级 P0]** [严重违例整改路径，如"全文扫一遍 agentless passive，按用法 1–5 加限定词或主动化"]
2. **[优先级 P1]** [中等违例整改路径，如"统一主-被动体例：确定以 we + 过去时为骨架，材料/数据步骤用被动"]
3. **[优先级 P2]** [轻微违例整改路径，如"全文统计符号格式统一：M/SD 用 M = x.xx, SD = x.xx"]
4. **[目标期刊对齐]** [如 "JPSP 近年 Method 偏主动，PSP 偏被动，需根据投稿目标调整"]
5. **[后续步骤]** [如 "修改 1 轮后建议再次调用本 Skill 复检，确保降档规则不再触发"]

---

## 附录 A：诊断依据回链

- 参考教材：Science Research Writing (2nd ed.) §2.5.1（PDF 页 41–48）
- 检查清单：references/checklist.md（4 大维度 / 25 小节 / 110+ 项）
- 评分细则：references/rubric.md（严重 / 中等 / 轻微三档 + A/B/C/D 等级）
- 顶刊正例：references/examples/positive/（47 例，含 JPSP / JEP:G / Developmental Psychology / PSPB / JCCP 等）

## 附录 B：未触发项目（完整性自检）

列出未触发任何违例的 checklist 子项，证明诊断覆盖完整：
- §1.2 标准程序 / 设备 / 软件：未发现违例
- §3.1 句式模板：未发现违例
- ...（按 checklist 顺序列出无违例子项）
```

---

## 六、使用约束

1. **本 Skill 仅诊断，不改写**：所有输出均以「问题定位 + 修改建议」形式给出，最终改写由人类作者完成，避免 AI 改写引入新错误。
2. **清单-细则严格对应**：rubric 中每一条扣分规则都能在 checklist 中找到对应 `- [ ]` 项；任何 rubric 单独新增项均视为误植。
3. **严重违例强制降档**：即便总分 ≥ 90，只要存在 1 处严重违例即降至 B；≥ 3 处严重违例强制 D。
4. **不跨维度诊断**：本 Skill 仅处理「语法与句法」维度；结构、逻辑、词汇维度请调用 sibling skill：
   - 结构 → `method-structure-diagnostic`
   - 逻辑 → `method-logic-diagnostic`
   - 词汇 → `method-vocabulary-diagnostic`
5. **正例库只读**：禁止修改 `references/examples/positive/` 下的 `.md` 文件；如需新增正例，请修改源目录 `D:\method-skill-project\02-positive_examples\grammar\` 并重新建立软链与索引。

---

**版本**：v1.0（与 checklist.md、rubric.md 同步）
**配套**：本目录下 `references/checklist.md`（检查清单）、`references/rubric.md`（评分细则）、`references/examples/positive/`（顶刊正例 47 例），四者一一对应、不得拆分使用。