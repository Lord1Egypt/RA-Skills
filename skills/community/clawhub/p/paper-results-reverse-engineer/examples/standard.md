# Example: Standard Mode Output

## Trigger

User says: "正常生成" / "常规精读" — or no mode specified (v3.0 default = standard).

## What You Get

Full Study Profile + Module A–G. Module C at paragraph/cluster level (2–4 clusters per paragraph). Module F: condensed (PPT page suggestions + one-liners + evidence boundaries, no full verbatim scripts).

## Example Output Structure

```markdown
# 论文 Results 反向拆解

## Metadata
| 字段 | 值 |
|------|----|
| Paper | Bolier et al. (2013) |
| Year | 2013 |
| Journal | BMC Public Health |
| Study Design | Meta-analysis / Systematic Review |
| Adaptive Branch | G. Meta-analysis |
| Analysis Mode | standard |
| Generated at | 2025-05-25T19:00:00+08:00 |

## Study Profile

### 三轴分类
| 轴 | 类别 | 值 | 来源 |
|----|------|----|------|
| Axis 1 | Article Type | Meta-analysis / Systematic Review | [原文Methods] |
| Axis 2 | Substantive Domain | Positive Psychology / Health Psychology | [原文推断] |
| Axis 3 | Data/Method Modality | Meta-analytic effect sizes (Cohen's d / Hedges' g) | [原文Methods] |
| Primary Branch | G. Meta-analysis / Systematic Review | ... | [教学性说明] |
| Why NOT other branches | Not single experiment (A), not RCT paper (C), not simulation (I) | ... | [教学性说明] |

### 基本信息
[Complete Study Profile fields with source tags]

---

## Module A: Study Profile 与文献信息表
[Extended Study Profile as formatted table]

## Module B: Results 结构地图

原文显式小节标题：
- Description of studies（加粗小标题）
- Subgroup analyses（加粗小标题）
- Publication bias（加粗小标题）

Skill 教学性补充分块 [教学性补充]：
- Identification → Study characteristics → Post-test effects → Follow-up effects → Subgroup analyses → Publication bias → Sensitivity

| Block | 回答的问题 | 数据/分析 | 对应图表 | 主要结果 | 作者想让读者得出的结论 |
|-------|-----------|----------|---------|---------|---------------------|
| Post-test effects | PPIs 对幸福感的总效应？ | Random-effects meta-analysis, k=39 | Table 2, Fig 2 | d=0.34 (SWB), 0.23 (PWB), 0.23 (Depression) | PPIs 有效但效应偏小 |
| Follow-up effects | 效应能否维持？ | RE meta-analysis, k=6 | Table 2 | d=0.21 (SWB), 0.16 (PWB), 0.17 (Depression, ns) | 部分维持，但证据有限 |
| ... | ... | ... | ... | ... | ... |

## Module C: Results 段落/句群拆解

功能标签说明：**1** 重提研究目的/假设 | **2** 重提关键方法 | **3** 总述结果趋势 | **4** 邀请查看图表 | **5** 报告具体结果 | **6** 报告统计证据 | **7** 评价性强调 | **8** 与既有研究比较 | **9** 与预测/模型/理论比较 | **10** 解释结果原因 | **11** 指出不显著/不一致 | **12** 承认限制/异常 | **13** 提示结果意义 | **14** 过渡到 Discussion

### Post-test Effects 段落

**[句群 1]** (Label 3 + 5) — 总述主效应趋势
> "The overall effect sizes for the main outcomes..."

**[句群 2]** (Label 6 + 10) — 统计证据 + 解释异质性
> "For SWB, the pooled effect size was d=0.34 (95% CI=0.22–0.45, p<.001; I²=67%)..."

**[句群 3]** (Label 11) — 报告不显著
[Per-paragraph annotation, 2–4 clusters per paragraph, with function labels + one interpretive note per cluster]

## Module D: 表格/图表讲解

### Figure 2 — Forest Plot (SWB Primary Outcome)
1. **回答的问题：** 各研究和总体合并后的 SWB 效应及精度
2. **结构：** Forest plot — study-level ES + CI + weights + pooled ES diamond
3. **作者引导方式：** "As shown in Figure 2, the overall effect..."
4. **关键模式：** Pooled d=0.34 [0.22, 0.45], moderate I²=67%
5. **1 分钟讲解脚本：** ...
6. **容易误解的点：** Pooled ES 小而显著 ≠ 每个个体的改善幅度，I²=67% 提示研究间效应差异较大

### Figure 4 — Funnel Plot + Trim and Fill
[Interpretation with G6 publication bias guardrail]

## Module E: 证据强度与解释边界

1. **核心主张：** PPIs 对 SWB、PWB 和抑郁有小而显著的正面效应
2. **证据类型：** Meta-analytic pooled evidence from 39 randomized controlled studies
3. **备择解释：** 发表偏倚部分影响估计（Trim and Fill 后 d 下降但仍非零）
4. **证据链强度：** 中 — RCT 元分析，但研究质量偏低、异质性中等、发表偏倚存在
5. **因果语言审查：** ...
6. **缺失环节：** Follow-up 证据薄弱（k 仅 6，约为 post-test 的 1/3）
7. **不能证明的内容：** PPIs 的长期效应、某种 PPI 类型的优越性、最佳干预配置

## Module F: PPT / 汇报讲解版本

### PPT 页码建议

| 页码 | 内容 | 核心讲法 | 关键图表 |
|------|------|---------|---------|
| 1 | 研究问题与纳入 | 正面心理学干预是否有效？纳入 39 个 RCT | PRISMA flow |
| 2 | 主效应：post-test | 三个结局均有小而显著的效应 (d=0.23–0.34) | Forest plot (Fig 2) |
| 3 | 调节分析 | 时长、形式、招募途径各有影响，但不能组合为最优方案 | Table 4 |
| 4 | 发表偏倚 | 存在发表偏倚，但校正后效应仍在 | Funnel plot (Fig 4) |
| 5 | 证据边界 | 低质量研究偏多、随访证据弱、不能确定最优方案 | — |

**证据边界（必须强调）：**
- 调节效应来自单独亚组分析，不能组合成"最优配置"
- 调节变量是研究间比较，不能做因果解读
- Follow-up 结果不能直接与 post-test 比较（研究集不同、k 少 2/3）

## Module G: 自检与反模板污染检查

[G0–G8 self-check with verification against original paper]

---

当前使用 standard mode。若需要完整逐句 Results 拆解、完整图表讲解和 PPT 讲稿，可使用 close-reading mode；若只需快速了解，可使用 quick mode。
```

## Chat Summary

```
已生成 Standard Mode Markdown：`~/Desktop/OpenClaw_Paper_Analysis/outputs_md/reverse_engineer/Bolier_2013_Results_Reverse_Analysis.md`

核心摘要：
1. 39 个 RCT 的 meta 分析：PPIs 对 SWB (d=0.34)、PWB (d=0.23)、抑郁 (d=0.23) 有小而显著的正面效应
2. ⚠️ 研究质量偏低 (平均 5/10)、异质性中等 (I²=67%)、发表偏倚存在 → 效应量可能被高估
3. Follow-up 证据薄弱 (k=6)，不能直接与 post-test 比较 d 值

自检：
- 完整：✅ | 无模板污染：✅ | 因果语言正确：✅
- 需人工复核：1 项 Important（低质量研究中效应更大的解释）
```
