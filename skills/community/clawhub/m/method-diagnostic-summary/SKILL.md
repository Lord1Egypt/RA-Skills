---
name: method-diagnostic-summary
version: 1.0.0
description: 心理学论文Method部分写作全面诊断，整合6个维度输出结构化评分报告与修改建议
sub-skills:
  - method-structure-diagnostic
  - method-grammar-diagnostic
  - method-vocabulary-diagnostic
  - method-logic-diagnostic
  - method-cohesion-diagnostic
  - method-conventions-diagnostic
metadata:
  domain: psychology-academic-writing
  type: summary-skill
  source: Science_Research_Writing_2nd_edition_Unit_2
  companion_skill: method-diagnostic-summary-coordinator
user-invocable: true
---

# Method 部分「全面诊断汇总」Skill

> **Skill 类型**：汇总型（summary / orchestrator）
> **作用范围**：心理学实证论文 Method 部分（不含 Introduction / Results / Discussion）
> **首要目标**：作为 Method 节诊断的**总入口**，并行调用 6 个分项 Skill，按权重汇总评分，输出综合评级 + 分维度详情 + 优先级整改路径
>
> **核心立场**：Method 节的全面质量 = **结构（可复现性）+ 语法（时态/语态）+ 逻辑（论证链）+ 词汇（术语精确）+ 衔接（时序/过渡）+ 规范（引用/伦理）** 六维联动。本 Skill 不直接进行单维度诊断，而是**编排 6 个分项 Skill + 加权汇总 + 强制降档判定 + 输出完整报告**。

---

## 一、功能说明

### 1.1 Skill 定位

`method-diagnostic-summary` 是 Method 节诊断的**总入口 Skill**，负责：

1. **接收用户输入**（Method 节文本 + 用户可选的诊断选项）
2. **并行调用 6 个分项 Skill**（`method-structure-diagnostic` / `method-grammar-diagnostic` / `method-vocabulary-diagnostic` / `method-logic-diagnostic` / `method-cohesion-diagnostic` / `method-conventions-diagnostic`）
3. **收集各维度结果**（每维度的得分、违例清单、修改建议、顶刊正例）
4. **加权汇总得分**（按预设权重计算综合得分）
5. **触发强制降档判定**（沿用分项 Skill 的强制降档规则 + 学术诚信一票否决）
6. **按固定模板输出完整报告**

### 1.2 与分项 Skill 的职责边界

| Skill | 职责 |
|-------|------|
| **6 个分项 Skill** | 单维度诊断 + 单维度评分 + 单维度修改建议 |
| **method-diagnostic-summary（本 Skill）** | 调用 6 个分项 Skill + 按权重加权汇总 + 输出综合评级 + 定位最弱维度 + 给出投稿建议 |

**禁止行为**：
- 本 Skill **不得**直接进行单维度诊断（必须调用分项 Skill）
- 本 Skill **不得**自行修改分项 Skill 的评分（必须以分项 Skill 输出为准）
- 本 Skill **不得**新增分项 Skill 未识别的违例（汇总报告的核心是"整合"而非"扩展"）

**必须行为**：
- 必须依次调用 6 个分项 Skill（或用户显式指定的维度组合）
- 必须按 `references/rubric.md` 第一节权重表加权计算
- 必须检查强制降档条件并优先于综合得分
- 必须按最弱维度排序整改优先级

### 1.3 6 个分项 Skill 简介

| 分项 Skill | 诊断维度 | 权重 | 核心诊断能力 |
|-----------|----------|------|-------------|
| `method-structure-diagnostic` | 结构与篇章逻辑 | 25% | 11 维度（模块齐全度 / 样本与功效 / 设计要素 / 测量与材料 / 程序与分析 + 横切的逻辑与组织）；判断文本能否让读者在不联系作者的前提下**精确复制**该研究 |
| `method-grammar-diagnostic` | 语法与句法规范 | 20% | 4 大维度（时态一致性 / 被动语态 / 句法结构 / 介冠词搭配）；判断句法层面是否让读者准确理解「这工作是谁做的」 |
| `method-vocabulary-diagnostic` | 词汇与学术用语 | 15% | 4 大维度（学术动词准确性 / 学术名词短语 / 固定搭配 / 量尺与措辞）；判断技术动词与名词短语选择的精确性 |
| `method-logic-diagnostic` | 逻辑与论证 | 20% | 4 大维度 22 子节 124 项（方法选择合理性 / 研究设计逻辑自洽性 / 变量与控制说明完整性 / 局限性与问题说明恰当性）；判断方法选择是否被合理论证、研究设计是否逻辑自洽 |
| `method-cohesion-diagnostic` | 衔接与连贯 | 10% | 4 大维度 29 子节 117 项（时序衔接准确性 / 段落过渡自然性 / 模块间逻辑连贯性 / 指代与承接清晰性）；判断时序衔接是否精确可复现、段落是否自然过渡、模块间跳转是否有承接 |
| `method-conventions-diagnostic` | 学术规范 | 10% | 4 大维度 21 子节 67 项（引用格式与标注规范性 / 现有方法改编说明准确性 / 伦理与透明声明完整性 / 术语与格式一致性）；判断引用归属是否清晰、Option 1/2/3 标注是否归类正确、伦理与 TOP 声明是否齐备 |

---

## 二、执行步骤（5 步）

```
Step 1 接收输入 → Step 2 并行调用 6 个分项 Skill → Step 3 收集各维度结果 → Step 4 加权汇总 + 强制降档 → Step 5 按固定模板输出报告
```

### Step 1 — 接收用户输入

接收以下输入：

| 输入项 | 必填 | 说明 |
|---|---|---|
| **Method 节文本** | ✓ | 必填；用户提交的待诊断 Method 节全文（可粘贴或通过文件路径提供） |
| **目标期刊** | ○ | 选填；如用户提供，按目标期刊规范调整各维度判定标准（如 JPSP 偏 passive / OBHDP 接受 active） |
| **诊断维度组合** | ○ | 选填；如用户提供维度组合（如"只看结构 + 逻辑 + 规范"），按用户选择调用分项 Skill；默认调用全部 6 个 |
| **输出粒度** | ○ | 选填；"完整报告"（默认）/"简化报告"（仅综合得分 + 维度表 + 关键问题）/"最小报告"（仅综合得分 + 评级） |
| **是否包含修改建议** | ○ | 选填；默认 true；如 false，仅输出诊断结果不输出修改建议 |

### Step 2 — 并行调用 6 个分项 Skill

按以下规则调用分项 Skill：

```
调用方式：sessions_spawn 或本地直接调用（视运行环境）
调用顺序：并行启动 6 个调用，无依赖关系
输入参数：每个分项 Skill 接收相同的 Method 节文本 + 目标期刊 + 用户指定选项
超时控制：每个分项 Skill 调用超时 60 秒；超时则该维度按 50 分保守赋值并标注"调用超时，保守赋值"
```

**调用伪代码**：

```
results = {}
for skill in [structure, grammar, vocabulary, logic, cohesion, conventions]:
    spawn(skill, inputs={
        "method_text": user_input.method_text,
        "target_journal": user_input.target_journal,
        "options": user_input.options
    })
    results[skill] = await_result(skill, timeout=60s)

# 若用户指定维度组合
if user_input.dimension_subset:
    results = {k: v for k, v in results.items() if k in user_input.dimension_subset}
```

**降级处理**：
- 若某个分项 Skill 调用失败（超时 / 错误），该维度按 50 分保守赋值，并在报告中标注"该维度调用失败，保守赋值"
- 若用户指定维度组合，跳过未指定的分项 Skill，权重按比例再分配（见 `references/rubric.md` §2.3）

### Step 3 — 收集各维度结果

每个分项 Skill 返回以下结构化结果：

| 字段 | 类型 | 说明 |
|---|---|---|
| `dimension_score` | int (0–100) | 该维度原始得分 |
| `dimension_grade` | str (A/B/C/D/F) | 该维度子评级 |
| `violations_severe` | list | 严重违例清单 |
| `violations_moderate` | list | 中等违例清单 |
| `violations_minor` | list | 轻微违例清单 |
| `positive_examples` | list | 该维度命中的顶刊正例清单（用于修改建议展示） |
| `mandatory_demotion` | bool | 是否触发强制降档条件 |
| `mandatory_demotion_reason` | str | 强制降档原因 |
| `academic_integrity_violation` | bool | 是否触发一票否决条件（学术诚信） |

本 Skill 收集所有 6 个分项 Skill 的结构化结果，构造汇总数据：

```
summary = {
    "total_violations_severe": sum of 6 dimensions' violations_severe counts,
    "total_violations_moderate": sum of 6 dimensions' violations_moderate counts,
    "total_violations_minor": sum of 6 dimensions' violations_minor counts,
    "all_violations_severe": concat of 6 dimensions' violations_severe,
    "all_violations_moderate": concat of 6 dimensions' violations_moderate,
    "all_violations_minor": concat of 6 dimensions' violations_minor,
    "dimension_scores": {6 dims: scores},
    "dimension_grades": {6 dims: grades},
    "mandatory_demotions": [list of (dimension, reason)],
    "academic_integrity_violations": [list of (dimension, reason)]
}
```

### Step 4 — 加权汇总 + 强制降档判定

#### 4.1 综合得分计算

按 `references/rubric.md` 第一节权重表加权汇总：

```
dimension_weights = {
    "structure": 0.25,
    "grammar": 0.20,
    "logic": 0.20,
    "vocabulary": 0.15,
    "cohesion": 0.10,
    "conventions": 0.10
}

# 若有维度被跳过，按比例再分配（见 rubric §2.3）
weights = rebalance_weights(dimension_weights, active_dimensions)

composite_score = Σ (dimension_score[d] × weights[d] for d in active_dimensions)
composite_score = round(composite_score, 2)
```

#### 4.2 整体评级判定

按 `references/rubric.md` 第三节五档等级：

```
composite_grade = (
    "A" if composite_score >= 90 else
    "B" if composite_score >= 80 else
    "C" if composite_score >= 70 else
    "D" if composite_score >= 60 else
    "F"
)
```

#### 4.3 强制降档判定（优先于综合得分）

按 `references/rubric.md` 第四节强制降档规则：

```
final_grade = composite_grade

# 1. 学术诚信一票否决（最高优先级）
if any academic_integrity_violation:
    final_grade = "F"
    demotion_reason = "学术诚信底线触发：{list violations}"

# 2. 各分项 Skill 强制降档
elif any mandatory_demotion:
    max_allowed_grade = max grade from mandatory_demotions
    if composite_grade > max_allowed_grade:
        final_grade = max_allowed_grade
        demotion_reason = "分项 Skill 强制降档：{list reasons}"
```

**强制降档条件速查**（详见 `references/rubric.md` 第四节）：

| 触发条件 | 评级上限 |
|---------|---------|
| 虚假引用 / IRB 缺失 / 知情同意缺失 / 预注册与数据完全不符 / 公开声明为假 | **F（一票否决）** |
| 1 处严重问题（method-conventions） | B（最高 89 分） |
| 2 处严重问题（method-conventions） | C（最高 79 分） |
| 3 处及以上严重问题 | D（最高 69 分） |
| 5 大核心模块缺失 ≥ 2 个（method-structure） | D（最高 69 分） |
| 严重违例 ≥ 3 处（method-logic） | D（最高 69 分） |
| 严重违例 ≥ 3 处（method-cohesion） | D（最高 69 分） |
| 严重时态 / 语态错误 ≥ 3 处（method-grammar） | D（最高 69 分） |
| 严重术语 / 短语错误 ≥ 3 处（method-vocabulary） | C（最高 79 分） |

#### 4.4 优先级整改路径排序

按子评级从弱到强排序：

```
priority_order = sorted(
    active_dimensions,
    key=lambda d: (dimension_grades[d], dimension_scores[d])
)
# 优先级最高 = 子评级最低 + 得分最低
```

### Step 5 — 按固定模板输出报告

按本 Skill 第四节「输出格式」的固定模板输出汇总报告。

---

## 三、评分规则

### 3.1 维度权重表

| # | 维度 | 对应 Skill | 权重 |
|---|------|------------|------|
| 1 | **结构** | `method-structure-diagnostic` | **25%** |
| 2 | **语法** | `method-grammar-diagnostic` | **20%** |
| 3 | **逻辑** | `method-logic-diagnostic` | **20%** |
| 4 | **词汇** | `method-vocabulary-diagnostic` | **15%** |
| 5 | **衔接** | `method-cohesion-diagnostic` | **10%** |
| 6 | **规范** | `method-conventions-diagnostic` | **10%** |
| | **合计** | — | **100%** |

### 3.2 综合得分计算方式

```
综合得分 = Σ (各维度得分 × 对应权重)

标准计算示例：
- 结构 92 × 0.25 = 23.00
- 语法 85 × 0.20 = 17.00
- 逻辑 88 × 0.20 = 17.60
- 词汇 90 × 0.15 = 13.50
- 衔接 80 × 0.10 = 8.00
- 规范 78 × 0.10 = 7.80
- 合计 = 86.90 → 四舍五入为 87 分
```

**四舍五入规则**：最终得分 = round(综合得分 × 100) / 100，保留两位小数。

**缺失维度处理**：

| 情况 | 处理 |
|------|------|
| 维度对应文本完全缺失（如 Methods 节没有 Measures 段） | 该维度按 0 分计算，并标注"模块缺失，未评估" |
| 维度对应文本极短不足以诊断（<500 词） | 该维度按 50 分保守赋值，并标注"样本不足，保守赋值" |
| 维度评估被用户显式跳过 | 权重按比例再分配到其他维度 |

### 3.3 整体等级划分

| 综合得分区间 | 等级 | 投稿建议 |
|------------|------|----------|
| **90–100** | 优秀（A） | 可直接投稿顶刊 |
| **80–89** | 良好（B） | 建议修改 1 轮后投稿顶刊 / 主流 SSCI |
| **70–79** | 合格（C） | 建议修改 1–2 轮后投稿；优先整改严重问题 |
| **60–69** | 待改进（D） | 需结构性补写；建议请导师 / 同行评审后再投稿 |
| **<60** | 不合格（F） | 必须重写；不推荐当前版本投稿 |

### 3.4 强制降档规则（沿用分项 Skill 规则）

- **一票否决**：虚假引用 / IRB 缺失（有人体被试）/ 知情同意缺失（有人体被试）/ 预注册与数据完全不符 / 数据公开声明为假 → 强制 F 档
- **常规强制降档**：1 处严重问题（conventions）→ 最高 B；2 处 → 最高 C；3 处及以上 → 强制 D
- **优先级**：一票否决 > 各分项 Skill 强制降档 > 综合得分判定

---

## 四、输出格式（固定模板）

诊断完成后，**必须**按以下模板输出汇总报告。模板中 `[…]` 为占位符，需替换为实际诊断结果。

```markdown
# Method 节「全面诊断汇总」报告

**被检文本**：[文件名 / 段落定位，如 "Study 1 Method 节"]
**诊断时间**：[ISO 日期]
**诊断依据**：6 个分项 Skill（structure / grammar / vocabulary / logic / cohesion / conventions）加权汇总
**目标期刊**：[用户指定 / 默认（不指定）]
**诊断维度**：6 维度（结构 25% / 语法 20% / 逻辑 20% / 词汇 15% / 衔接 10% / 规范 10%）

---

## 1. 综合得分

**综合得分**：[X.XX 分 / 100 分]
**整体评级**：[A / B / C / D / F]
**强制降档触发**：[如触发，标注原因：如"严重问题 ≥3 处 → 强制 D 档"；如未触发，标注"未触发强制降档"]
**投稿建议**：[可直接投稿 / 建议修改 1 轮后投稿 / 建议修改 1–2 轮后投稿 / 需结构性补写 / 必须重写]

---

## 2. 维度得分详情

| 维度 | 权重 | 分项 Skill 得分 | 加权得分 | 子评级 | 强制降档 |
|------|------|----------------|----------|--------|---------|
| 结构 | 25% | X | X.XX | A/B/C/D/F | [如有触发] |
| 语法 | 20% | X | X.XX | A/B/C/D/F | [如有触发] |
| 逻辑 | 20% | X | X.XX | A/B/C/D/F | [如有触发] |
| 词汇 | 15% | X | X.XX | A/B/C/D/F | [如有触发] |
| 衔接 | 10% | X | X.XX | A/B/C/D/F | [如有触发] |
| 规范 | 10% | X | X.XX | A/B/C/D/F | [如有触发] |
| **合计** | **100%** | — | **X.XX** | — | — |

> **子评级映射**：90–100 优秀 (A) / 80–89 良好 (B) / 70–79 合格 (C) / 60–69 待改进 (D) / <60 不合格 (F)

---

## 3. 整体评价

**一句话总结**：[例如："结构与逻辑达到顶刊水平；规范与衔接需补强；最弱维度为规范（78 分），优先级整改。"]

**核心优劣**：
- **优势**：[例如"结构 92 分（11 维度几乎全达标）+ 逻辑 88 分（论证链三段式完整）；时序衔接准确；IRB 编号完整"]
- **短板**：[例如"规范 78 分（Option 1/2/3 标注欠准确）+ 衔接 80 分（程序总起句缺 first）；存在 2 处严重问题待修"]

---

## 4. 核心问题汇总（按严重程度排序）

### 4.1 严重问题（必须修改）

| # | 来源维度 | 问题类型 | 位置 | 扣分 | 修改优先级 |
|---|---------|---------|------|------|-----------|
| 1 | [维度] | [问题简述] | [子模块 / 段落] | X | P0 |
| 2 | [维度] | [问题简述] | [子模块 / 段落] | X | P0 |
| 3 | [维度] | [问题简述] | [子模块 / 段落] | X | P0 |
| ... | ... | ... | ... | ... | ... |

**严重问题逐项说明**（每个问题含位置 / 原文 / 修改建议 / 顶刊正例）：

#### 问题 1：[违例类型简述]
- **来源维度**：[structure / logic / conventions / 等]
- **位置**：[段落 / 句编号]
- **原文**：`[原句引用]`
- **修改建议**：[具体可执行动作]
- **顶刊正例**：[Author Year] [Brief title]. [Journal], [Vol], [Pages].（参考正例：`examples/positive/<skill>_<Author>_<Year>_<n>.md`）

#### 问题 2：[违例类型简述]
...

### 4.2 中等问题（修改后可投稿）

按维度分组列出：

#### 结构维度
- [问题摘要 1 + 位置 + 修改要点]
- [问题摘要 2 + 位置 + 修改要点]

#### 语法维度
- [问题摘要 1 + 位置 + 修改要点]
- [问题摘要 2 + 位置 + 修改要点]

#### 逻辑维度
- [问题摘要 1 + 位置 + 修改要点]
- [问题摘要 2 + 位置 + 修改要点]

#### 词汇维度
- [问题摘要 1 + 位置 + 修改要点]
- [问题摘要 2 + 位置 + 修改要点]

#### 衔接维度
- [问题摘要 1 + 位置 + 修改要点]
- [问题摘要 2 + 位置 + 修改要点]

#### 规范维度
- [问题摘要 1 + 位置 + 修改要点]
- [问题摘要 2 + 位置 + 修改要点]

### 4.3 轻微问题（仅归类汇总）

| 维度 | 轻微问题数 | 主要类型 |
|------|-----------|---------|
| 结构 | x | [如"模块标题大小写不统一 / 段落长度超标"] |
| 语法 | x | [如"个别介词欠精确 / 冠词冗余"] |
| 逻辑 | x | [如"INDICATE CARE 副词局部不足 / 局限披露语气局部欠妥"] |
| 词汇 | x | [如"个别动词欠学术化 / 量尺锚点措辞欠统一"] |
| 衔接 | x | [如"段内最小化承接词不足 / 缩写首次出现未给全称"] |
| 规范 | x | [如"拉丁语斜体规则 / 希腊字母大小写 / 单位前后空格"] |
| **合计** | **x** | — |

---

## 5. 优先级整改路径

按子评级从弱到强排序（F → D → C → B → A）：

1. **[最弱维度（最低子评级）]**：[整改要点 + 必改问题清单 + 预估提升空间]
2. **[次弱维度]**：[整改要点 + 必改问题清单 + 预估提升空间]
3. **[再次弱维度]**：[整改要点 + 必改问题清单 + 预估提升空间]
4. **[达标维度（B 及以上）]**：[可选优化点]

**整改目标设定**：
- 目标 1：解决所有严重问题（学术诚信问题 P0 处理）
- 目标 2：把 D 维度提升至 C 以上（重点整改最弱维度）
- 目标 3：把 C 维度提升至 B 以上（如有 C 维度）
- 目标 4：综合得分 ≥ 80（B 档，可投稿顶刊 / 主流 SSCI）
- 目标 5：综合得分 ≥ 90（A 档，可直接投稿顶刊）

---

## 6. 各分项 Skill 详细报告

汇总报告对每个分项 Skill 提供 1 行摘要 + 详细报告链接：

| 分项 Skill | 子评级 | 关键问题 | 详细报告 |
|-----------|--------|---------|---------|
| `method-structure-diagnostic` | A/B/C/D/F | [1–3 个关键问题] | [查看报告链接] |
| `method-grammar-diagnostic` | A/B/C/D/F | [1–3 个关键问题] | [查看报告链接] |
| `method-vocabulary-diagnostic` | A/B/C/D/F | [1–3 个关键问题] | [查看报告链接] |
| `method-logic-diagnostic` | A/B/C/D/F | [1–3 个关键问题] | [查看报告链接] |
| `method-cohesion-diagnostic` | A/B/C/D/F | [1–3 个关键问题] | [查看报告链接] |
| `method-conventions-diagnostic` | A/B/C/D/F | [1–3 个关键问题] | [查看报告链接] |

---

## 7. 整体优化建议

1. **[优先级 P0 — 严重 / 学术诚信]** [严重违例整改路径，如"删除虚假引用 + 补 IRB 编号 + 独立 TOP 段落 + 声明预注册偏离"]
2. **[优先级 P1 — 最弱维度整改]** [按子评级排序，逐维度整改]
3. **[优先级 P2 — 中等问题全面整改]** [中等违例逐项处理]
4. **[优先级 P3 — 轻微问题归类优化]** [轻微问题批量优化]
5. **[目标期刊对齐]** [按目标期刊规范调整判定标准]
6. **[后续步骤]** [如"修改 1 轮后建议再次调用本 Skill 复检，确保综合得分 ≥ 80"]

---

## 附录 A：评分规则回链

- 权重表：本文件第三节 §3.1
- 综合得分计算方式：本文件第三节 §3.2
- 整体等级划分：本文件第三节 §3.3
- 强制降档规则：本文件第三节 §3.4 + 详细见 `references/rubric.md` 第四节
- 投稿建议矩阵：见 `references/rubric.md` 第六节

## 附录 B：未触发项目（完整性自检）

汇总 Skill 本身不直接识别违例，而是通过分项 Skill 识别。附录 B 列出本次诊断中各分项 Skill 已检查但未触发违例的子节清单，证明诊断覆盖完整。

| 分项 Skill | 已检查但未触发违例的子节 |
|-----------|------------------------|
| `method-structure-diagnostic` | [按结构 rubric 顺序列出无违例子节] |
| `method-grammar-diagnostic` | [按语法 rubric 顺序列出无违例子节] |
| `method-vocabulary-diagnostic` | [按词汇 rubric 顺序列出无违例子节] |
| `method-logic-diagnostic` | [按逻辑 rubric 顺序列出无违例子节] |
| `method-cohesion-diagnostic` | [按衔接 rubric 顺序列出无违例子节] |
| `method-conventions-diagnostic` | [按规范 rubric 顺序列出无违例子节] |
```

---

## 五、使用约束

1. **本 Skill 仅汇总，不诊断**：所有违例识别由 6 个分项 Skill 完成，本 Skill 只负责编排 + 汇总 + 输出。
2. **权重不可调整**（除非用户显式指定）：本 Skill 的权重表是**预设值**，对应顶刊审稿人敏感度排序；如用户要求调整权重（如"我想让语法占 30%"），需用户显式说明，本 Skill 记录在报告附录但不主动修改。
3. **强制降档优先**：本 Skill 强制降档条件沿用各分项 Skill 的判定，不得放宽或收紧；若用户要求"忽略学术诚信问题"，本 Skill 拒绝执行（学术诚信底线不可妥协）。
4. **不跨维度整合**：本 Skill 不得将不同维度的违例合并为一个问题（如不得把"结构问题"和"逻辑问题"合并为"方法描述不清"）；违例归属以分项 Skill 输出为准。
5. **分项 Skill 失败处理**：若分项 Skill 调用失败，按 50 分保守赋值 + 标注"调用失败"；不允许在分项 Skill 失败时直接跳过该维度（除非用户显式跳过）。
6. **报告完整性**：汇总报告必须包含本文件第四节列出的所有模块（一/综合得分 二/维度详情 三/整体评价 四/核心问题汇总 五/优先级整改路径 六/各分项报告 七/整体优化建议 + 附录 A/B），不得删减一级标题。
7. **运行效率**：6 个分项 Skill 应**并行调用**（不串行）；单维度调用超时 60 秒，超时则按降级处理。
8. **本 Skill 不引入新扣分点**：所有评分与扣分规则来自 6 个分项 Skill 的 rubric.md，本 Skill 不得新增任何扣分点。
9. **回溯一致**：同一份 Method 文本，每次调用本 Skill 的综合得分应保持一致（除非分项 Skill 内部规则有更新）；如发现得分波动，先检查分项 Skill 版本号是否变更。
10. **学术诚信一票否决**：本 Skill 对学术诚信问题（虚假引用 / IRB 缺失 / 知情同意缺失 / 预注册与数据不符 / 数据公开声明为假）触发 F 档**不可被任何"理由"覆盖**——即便用户认为"已修改"，也必须由各分项 Skill 重新诊断后再次汇总。

---

## 六、与其他 Skill 的协同关系

### 6.1 上游 Skill（本 Skill 调用的）

- `method-structure-diagnostic`：结构与篇章诊断
- `method-grammar-diagnostic`：语法与句法诊断
- `method-vocabulary-diagnostic`：词汇与学术用语诊断
- `method-logic-diagnostic`：逻辑与论证诊断
- `method-cohesion-diagnostic`：衔接与连贯诊断
- `method-conventions-diagnostic`：学术规范诊断

### 6.2 下游 Skill（被本 Skill 调用的）

无（本 Skill 是诊断链的终点，不调用其他 Skill）。

### 6.3 并列 Skill

无（本 Skill 是 Method 节诊断的最高层 Skill）。

### 6.4 协同示例

```
用户调用 method-diagnostic-summary
    ↓
并行调用 6 个分项 Skill
    ↓
各分项 Skill 调用各自的 references/checklist.md + references/rubric.md + references/examples/positive/
    ↓
6 个分项 Skill 返回结构化结果
    ↓
本 Skill 汇总 + 加权 + 强制降档判定
    ↓
输出综合报告（含分项报告链接）
```

---

**版本**：v1.0（与 6 个分项 Skill v1.0 同步）
**配套**：`references/rubric.md`（汇总评分规则）+ 6 个分项 Skill 的 `SKILL.md` + `references/checklist.md` + `references/rubric.md` + `references/examples/positive/`
**重要约束**：汇总评分完全基于分项 Skill 输出，本 Skill 不引入新的扣分点；任何超出分项 Skill 的"加额外"判定均视为误植。