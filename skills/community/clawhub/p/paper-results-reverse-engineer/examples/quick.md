# Example: Quick Mode Output

## Trigger

User says: "快速看一下这篇论文的 Results" / "大概拆一下"

## What You Get

Quick mode outputs: Study Profile + Module B (Results structure map) + Module D (core figures/tables) + Module E (evidence boundary) + self-check summary.

No Module C (sentence-level annotation). No Module F (PPT scripts).

## Example Output Structure

```markdown
# 论文 Results 反向拆解（Quick Mode）

## Metadata
| 字段 | 值 |
|------|----|
| Paper | Li et al. (2021) |
| DOI | ... |
| Analysis Mode | quick |

## Study Profile

### 三轴分类
| 轴 | 类别 | 值 |
|----|------|----|
| Axis 1 | Article Type | Survey / Correlational |
| Axis 2 | Substantive Domain | Health / Clinical Psychology |
| Axis 3 | Data/Method Modality | Questionnaire scores, SEM, mediation, moderation |
| Primary Branch | B. Survey / Correlational / Mediation |

### 基本信息
[Key fields: N, instruments, core variables, statistical methods, Results subsections, core tables/figures]

---

## Module B: Results 结构地图

| 小节 | 回答的问题 | 核心发现 | 对应图表 |
|------|-----------|---------|---------|
| Descriptive statistics | 样本特征和变量分布 | ... | Table 1 |
| Correlation matrix | 变量间零阶相关 | ... | Table 2 |
| Mediation model | 依恋亲近是否中介社会支持→抑郁 | ... | Table 3, Fig 2 |
| Conditional indirect effects | 中介效应是否随自尊水平变化 | ... | Table 4, Fig 3 |

[Additional Results blocks as present]

---

## Module D: 核心图表讲解

### Table 3 — Mediation Path Coefficients
- **问题：** 依恋亲近的中介效应是否显著？
- **关键值：** a path = ..., b path = ..., indirect effect = ..., Bootstrap 95% CI [...]
- **1 分钟讲解脚本：** ...
- **容易误解的点：** ...

### Figure 3 — Johnson–Neyman Plot
[Brief interpretation]

---

## Module E: 证据强度与解释边界

1. **核心主张：** ...
2. **证据类型：** Cross-sectional correlational / statistical mediation
3. **因果语言审查：** ⚠️ Title uses "reduce depression" — replace with associational wording
4. **关键限制：** Cross-sectional; temporal precedence not established
5. **不能证明的内容：** social support causally reduces depression through attachment

---

## 自检摘要

- 无 truncated/todo/待补充：✅
- Study Profile + Module B/D/E 完整：✅
- 三轴分类正确：✅
- 无模板污染：✅

**需人工复核：** 原文正文-表格矛盾（B7a），建议核对 Table 3 a path 值

---

当前使用 quick mode。若需要一般精读版，可使用 standard mode；若需要完整逐句拆解和汇报讲稿，可使用 close-reading mode。
```

## Chat Summary

```
已生成 Quick Mode Markdown：`~/Desktop/OpenClaw_Paper_Analysis/outputs_md/reverse_engineer/Li_2021_Results_Reverse_Analysis.md`

核心摘要：
1. 横断面中介模型显示依恋亲近在 social support → depression 路径中有统计间接效应
2. ⚠️ 该模型是统计中介（非因果中介）；横断面无法确立时间顺序
3. Table 3 a path 与正文可能存在数值矛盾 → 需人工核对

自检通过。1 项 Critical 需人工复核。
```
