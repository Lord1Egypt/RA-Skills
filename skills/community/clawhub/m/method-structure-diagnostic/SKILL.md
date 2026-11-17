---
name: method-structure-diagnostic
version: 1.0.0
description: 诊断心理学论文 Method 部分的结构完整性与篇章逻辑，检查核心子模块是否齐全、内容要素是否完整，输出评分与顶刊正例参考
metadata:
  domain: psychology-academic-writing
  dimension: structure
user-invocable: true
---

# Method 结构与篇章诊断（structure-diagnostic）

> **Skill 类型**：诊断型（diagnostic）
> **作用范围**：心理学实证论文 Method 部分（不含 Introduction / Results / Discussion）
> **首要目标**：判断文本能否让读者在不联系作者的前提下**精确复制**该研究——这是 Science Research Writing (2nd ed.) 对 Method 部分的核心要求

---

## 一、诊断依据

本 Skill 的诊断结论必须由以下 **4 项依据** 同时支撑，缺一不可；评分不能脱离任一依据单独生成。

| # | 依据 | 路径 / 来源 | 用途 |
|---|------|-------------|------|
| 1 | **参考教材** | 《Science Research Writing》(2nd ed.), Unit 2: *How to Write about Methods*，§2.1–2.5（原文 PDF 见 `01-reference/Science-Research-Writing-Second-Edition_102-167.pdf`） | 提供 Method 通用 6 模块模型、总-分叙事逻辑、子模块组织原则、动词时态/介词/冠词规则 |
| 2 | **检查清单** | `references/checklist.md` | 提供 83 项结构检查点（模块齐全度 + 子模块要素 + 结构逻辑 + 段落组织） |
| 3 | **评分细则** | `references/rubric.md` | 提供每项扣分值（严重 10–15 / 中等 5–9 / 轻微 1–4）与分数档位（90–100 / 80–89 / 70–79 / 60–69 / <60） |
| 4 | **顶刊正例** | `references/examples/positive/structure_*.md`（来自 JPSP / JEP:G / Developmental Psychology / PSPB / OBHDP 等顶刊） | 提供已验证的结构样板，用于对照匹配与修改建议 |

> 引用以上文件时请使用仓库相对路径；不得在用户可见输出中泄露评分细则中的具体扣分编号，仅以「严重 / 中等 / 轻微」档位呈现。

---

## 二、核心检查项（11 维度，来自 checklist 与 rubric 的提炼）

诊断时按以下 **11 个维度** 逐条扫描；每条命中即映射到对应 rubric 扣分项。11 维度对应 checklist 的 4 个一级标题 + 7 个二级要素类。

### A. 模块齐全度（对应 rubric §一）
1. **五大核心模块齐全性**——Participants / Design / Measures / Procedure / Analysis 是否各自独立成段
2. **Transparency & Openness 声明**——预注册、数据/脚本公开、未公开部分理由
3. **多研究独立成章**——Study 1/2/3 各自拥有完整 Method（多研究论文必查）
4. **正文与补充材料分工**——可复现关键信息在正文，冗长细节进 SI
5. **研究三要素覆盖**——who（被试）/ what（材料工具）/ how（程序）

### B. 样本与功效（对应 rubric §二-Participants）
6. **功效分析与样本量依据**——目标 N、效应量假设、α、功效、分析工具（G*Power 等）
7. **漏斗式样本流程**——起始样本 → 各排除环节人数与原因 → 最终样本（含人口学）

### C. 设计要素（对应 rubric §二-Design）
8. **设计一句话定义 + IV/DV 操作定义**——条件数 × 因素结构 × 被试间/内/混合
9. **控制变量、操纵检验、盲法报告**——入选理由、检验时点、保障方式

### D. 测量与材料（对应 rubric §二-Measures）
10. **测量组织与材料构造**——总纲句 + 构念独立成段 + 漏斗式可复现流程（母库 → 提取 → 缩减 → 最终集）

### E. 程序与分析（对应 rubric §二-Procedure + 数据分析）
11. **程序步骤链与分析方案**——时序完整 + 精确序列语言 + 统计方法与预注册一致性 + 缺失与多重比较处理

### 逻辑与组织（横切维度，对应 rubric §三、四）
贯穿 11 维度同步扫描：
- **总-分叙事**（top-down：先 general 再 specific，段落入口句立焦点）
- **时态与归属**（本研究过去时，标准程序现在时；用 In this study / here / in our model 区分自己与他人）
- **理由与谨慎措辞**（in order to / to ensure / tightly / precisely / slightly / negligible）

---

## 三、执行步骤（6 步，固定流程）

每接到一段 Method 文本，按以下顺序执行；任何一步中断都不得直接出评分。

### Step 1：读取规则
- 加载 `references/checklist.md`（83 项）与 `references/rubric.md`（扣分表）
- 加载教材 §2.1–2.5 的 6 模块模型与时态/介词/冠词规则

### Step 2：扫描文本
- 切分 Method 为**子模块**（Participants / Design / Measures / Procedure / Analysis + 可选的 Transparency & Openness / Supplemental Materials reference）
- 标注每个子模块的**段落数、入口句、关键词、引用**（用于后续匹配正例）

### Step 3：对照核验
- 对 11 个维度逐条核验 → 在 checklist 上标记 ✅/❌/⚠️（部分符合）
- 每条 ❌ 找到 rubric 中的对应扣分项，记录档位（严重 / 中等 / 轻微）与扣分值
- ⚠️ 按 50%–100% 酌扣

### Step 4：计算得分
- 起评 **100 分**
- 严重项扣 10–15；中等项扣 5–9；轻微项扣 1–4
- 同维度多个问题**独立计扣**（不因重复豁免）
- 最终得分 = max(0, 100 − Σ各项扣分)
- 落入 **60 分以下**视为「复现性严重受损」，强制标注「需结构性大改」

### Step 5：匹配正例
- 对每个 ❌ 或 ⚠️ 项，从 `references/examples/positive/structure_*.md` 中挑出**最相关**的 1 份正例
- 匹配优先级：
  1. 子模块类型相同（Participants → Participants 正例；操纵材料 → Phillips 等）
  2. 研究设计类型相同（数据库 vs 在线实验 vs 纵向 vs 多研究）
  3. 期刊风格相近（JPSP 倾向多研究独立成章；JEP:G 倾向单研究紧凑结构）
- 每个核心问题**最多引用 1 份正例**，禁止堆砌

### Step 6：输出结果
- 按下文 §五「输出格式」固定模板生成报告
- 报告顺序固定：维度得分 → 整体评价 → 已识别模块 → 核心问题（按严重程度）→ 优化建议

---

## 四、正例调用规则

### 4.1 触发条件
满足以下任一条件时**必须**调用正例：
- (a) 存在 1 个及以上严重级问题
- (b) 用户明确要求「给出范例」/「参考顶刊」
- (c) 核心问题所在子模块（Participants / Measures / Procedure）正例库中已有对应类型

### 4.2 匹配逻辑

| 核心问题所属子模块 | 优先匹配正例（`examples/positive/` 下） |
|---|---|
| Participants（数据库研究） | `structure_Werchan_2024_1.md` / `structure_Haider_2022_1.md` / `structure_Diaz-Guerra_2026_1.md` |
| Participants（在线招募 + 漏斗式排除） | `structure_Vilanova_2022_1.md` / `structure_Carpenter_2019_1.md` / `structure_Costin_2019_1.md` |
| Participants（多研究样本口径一致性） | `structure_Kteily_2016_1.md` |
| Transparency & Openness 声明 | `structure_Abramson_2024_1.md` / `structure_McLean_2019_1.md` |
| Measures（总纲句 + 构念逐条） | `structure_Kteily_2016_1.md` |
| Measures（操纵材料 + 完整引述） | `structure_Phillips_2021_1.md` |
| Procedure（在线实验任务设计） | `structure_Zhou_2016_1.md` |

> 匹配时**只挑 1 份最相关的**，不要把整个目录罗列给用户。

### 4.3 展示要求
正例在输出中的呈现必须满足：
1. **文件路径明确**：以 `references/examples/positive/<filename>.md` 形式给出
2. **片段节选贴合问题**：从该文件中提取 1–3 句最贴切原文，**不得整段照搬**
3. **改动指引具体**：明确指出用户文本应参考其哪一句、模仿哪一结构（如「漏斗顺序」「总纲句引导」）
4. **不喧宾夺主**：正例作为「修改建议」的支撑材料，禁止挤占「核心问题」本身的篇幅

### 4.4 不调用正例的场景
- 用户问题完全属于轻微级（措辞 / 时态 / 衔接细节）——给出 SRW 教材规则即可，不调正例
- 正例库中无直接对应类型（如单被试设计、临床干预等非常规研究）——只引教材规则
- 用户显式要求「仅诊断不范例」

---

## 五、输出格式（固定模板）

> 模板严格按以下顺序与标题输出。**不得增删一级标题**；二级标题可按问题数量裁剪。

```markdown
# Method 结构诊断报告

> 诊断对象：<Method 文本标题或前 60 字>
> 诊断依据：Science Research Writing §2.1–2.5 + checklist + rubric + 顶刊正例
> 诊断维度：结构与篇章逻辑（11 维度）

---

## 一、维度得分（100 分制）

| 维度 | 满分 | 扣分 | 实得 | 档位 |
|------|------|------|------|------|
| 模块齐全度（A1–A5） | 25 | X | X | 严重/中等/轻微 |
| 样本与功效（B6–B7） | 20 | X | X | 严重/中等/轻微 |
| 设计要素（C8–C9） | 15 | X | X | 严重/中等/轻微 |
| 测量与材料（D10） | 15 | X | X | 严重/中等/轻微 |
| 程序与分析（E11） | 15 | X | X | 严重/中等/轻微 |
| 逻辑与组织（横切） | 10 | X | X | 严重/中等/轻微 |
| **合计** | **100** | **Σ** | **X** | — |

> 档位映射：90–100 优秀 / 80–89 良好 / 70–79 合格 / 60–69 基本合格 / <60 结构性大改

---

## 二、整体评价

<2–4 句直评：是否可复现、结构清晰度、最突出的优劣点>

---

## 三、已识别模块

| 子模块 | 状态 | 备注 |
|--------|------|------|
| Participants | ✅ 完整 / ⚠️ 部分 / ❌ 缺失 | <一句话> |
| Design | … | … |
| Measures | … | … |
| Procedure | … | … |
| Analysis | … | … |
| Transparency & Openness | … | … |

---

## 四、核心问题（按严重程度排序）

### 问题 1（严重，扣 X 分）

- **位置**：<子模块名 / 段落定位>
- **表现**：<1–2 句具体描述，含原文引用>
- **违反条目**：checklist §X.XX + rubric §X.XX
- **修改建议**：<具体可执行动作>
- **顶刊正例参考**：`references/examples/positive/structure_XXX.md`
  > 关键借鉴：<1–3 句节选 + 一句话说明模仿什么>

### 问题 2（中等，扣 X 分）

…（同结构）

### 问题 N（轻微，扣 X 分）

…

---

## 五、优化建议（优先级 P0 → P2）

- **P0（必须改）**：<核心严重问题 1–3 条>
- **P1（建议改）**：<中等问题 1–3 条>
- **P2（可选）**：<轻微问题 0–3 条>

---

## 六、正例调用清单（如已触发）

| 引用文件 | 触发问题 | 用于支撑的修改建议 |
|----------|----------|---------------------|
| `structure_XXX_YYYY_1.md` | 问题 1 | 漏斗式样本流程 |
| `structure_XXX_YYYY_1.md` | 问题 3 | Measures 总纲句 |

---

*报告生成时间：<ISO 日期>*
*Skill 版本：method-structure-diagnostic v1.0.0*
```

---

## 六、约束与边界

1. **不诊断范围**：Introduction / Results / Discussion 不在本 skill 职责内；用户若一并提交，应明确告知并仅评 Method。
2. **不做事实核查**：本 skill 只评**结构与篇章**，不评判实验设计本身的科学性（操纵是否有效、统计是否得当 → 由 `method-logic-diagnostic` 处理）。
3. **不替代语言校对**：语法、词汇、拼写等由 `method-grammar-diagnostic` / `method-vocabulary-diagnostic` / `method-conventions-diagnostic` 各自负责；本 skill 仅在「影响结构可读性」时附带提及（如段落超长堆砌）。
4. **评分一致性**：相同文本每次输出得分必须一致；扣分依据来自 `references/rubric.md`，不得自行新增或调整扣分值。
5. **正例使用纪律**：单报告引用正例不超过 3 份；正例节选不超过 5 句/份；不二次分发正例原文。
6. **诚实声明**：当 Method 文本过短（<500 词）或残缺（如只有 Participants 段），应明确告知「样本不足以完整诊断」并仅对可见部分评分，不得为凑齐 11 维度强行推断。

---

## 七、与其他 Skill 的协同

| Skill | 协同关系 |
|-------|----------|
| `method-grammar-diagnostic` | 本 skill 发现「段落堆砌 / 句间衔接弱」时，引导用户跑语法 skill |
| `method-vocabulary-diagnostic` | 本 skill 发现「时态 / 介词 / 冠词」错误时，引导用户跑词汇 skill |
| `method-logic-diagnostic` | 本 skill 完成后建议运行逻辑 skill，覆盖统计方法、操纵逻辑、因果链 |
| `method-conventions-diagnostic` | 期刊格式（标题层级、引用风格、缩写规范）由该 skill 单独处理 |

---

*本 Skill 由 OpenClaw `skill-creator` 工作流生成，符合 v1 规范。所有引用文件路径相对于 Skill 根目录。*