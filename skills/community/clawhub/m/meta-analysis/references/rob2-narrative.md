# RoB 2 Result Narrative Templates / 偏倚风险结果章节文字模板

> **用法**：配合技能 `rob2` / `rob_summary` task 产出的 traffic-light 图与 summary bar
> 图使用。本文件提供**投稿可贴**的英文段落模板；中文版本仅供理解，不建议直接照搬
> （投稿语言以目标期刊为准）。
>
> **重要前提**：模板基于 RoB 2（Sterne 2019）5 域判定（Randomization / Deviations /
> Missing data / Measurement / Selection of reported result），其它工具请按对应
> 域名替换：ROB1（6 域）/ ROBINS-I（7 域）。

---

## 1. Overall Risk of Bias Statement / 整体偏倚风险陈述

### 1.1 模板

**All studies at low risk / 全部低偏倚**：

> Across all {k} included studies, the overall risk of bias was judged to be **low**
> in all five RoB 2 domains. The randomization process, deviations from intended
> interventions, missing outcome data, measurement of the outcome, and selection of
> the reported result were adequately reported in every study.

**Mostly low, with some concerns in specific domains / 多数低偏倚，特定域有顾虑**：

> Of the {k} included studies, {n_low} ({pct_low}%) were judged to be at **low risk**
> of bias overall, and {n_sc} ({pct_sc}%) at **some concerns**. No study was rated as
> high risk of bias overall. Concerns were concentrated in the domains of
> **{concern_domain1}** and **{concern_domain2}**, primarily due to
> {reason_e.g. "lack of pre-specified analysis plan"}.
> *(see Appendix Fig. X for the traffic-light plot and Fig. Y for the summary bar.)*

**Any high risk / 出现高偏倚**：

> Of the {k} included studies, {n_high} ({pct_high}%) were judged to be at **high risk**
> of bias overall, primarily driven by concerns in **{domain}** ({reason}). The remaining
> {n_rest} studies were at low risk ({n_low}) or some concerns ({n_sc}).
> *(see Appendix Fig. X for the traffic-light plot and Fig. Y for the summary bar.)*

### 1.2 计算

| 整体判定 | 规则 |
|---|---|
| **Low** | 所有 5 域均 Low |
| **Some concerns** | 无 High，且 ≥1 域为 Some concerns |
| **High** | ≥1 域为 High |

`%` 数字按整体判定统计；不要把单域的 Some concerns 比例直接报告为"Some concerns in {pct}% studies"。

---

## 2. Domain-by-Domain Narrative / 逐域措辞

### 2.1 D1 — Randomization process / 随机化过程

> The randomization process was adequately described in {n}/{k} studies ({pct}%);
> {n_uc}/{k} studies provided insufficient information on allocation concealment and
> were judged to have **some concerns**. {n_h}/{k} studies used a non-random
> sequence generation and were rated as **high risk** in this domain.

### 2.2 D2 — Deviations from intended interventions / 偏离既定干预

> Deviations from intended interventions were **balanced** and unlikely to affect
> the outcome in {n}/{k} studies ({pct}%). {n_sc}/{k} studies raised **some concerns**
> due to {reason_e.g. "open-label design with subjective outcomes"} and were judged
> accordingly. {n_h}/{k} studies reported substantial crossover or unbalanced
> co-interventions, leading to a **high risk** rating in this domain.

### 2.3 D3 — Missing outcome data / 缺失结局数据

> Outcome data were **complete or near-complete** (≤{threshold}% missing) in
> {n}/{k} studies ({pct}%). {n_sc}/{k} studies had missing data between
> {lo}–{hi}% without robust sensitivity analysis, leading to **some concerns**.
> {n_h}/{k} studies had substantial missingness (>{threshold}%) that was likely
> related to the true value, rated as **high risk** in this domain.

> ⚠️ 阈值（常用 5% / 10% / 20%）应**事先在方法学部分定义**，不要在结果中临时调整。

### 2.4 D4 — Measurement of the outcome / 结局测量

> Outcome measurement was **appropriate and blinded** to intervention status in
> {n}/{k} studies ({pct}%). {n_sc}/{k} studies used assessor-unblinded methods
> for a **subjective** outcome, leading to **some concerns**. {n_h}/{k} studies
> used unblinded assessment of an objectively measurable outcome and were rated
> as **high risk** in this domain.

> ⚠️ "subjective vs objective" 的判定应基于**既定方法学**（如 Cochrane Handbook
> 对结局属性的分类），不要在结果中事后定义。

### 2.5 D5 — Selection of the reported result / 报告结果选择

> All pre-specified outcomes reported in the methods were also reported in the
> results of {n}/{k} studies ({pct}%), with no indication of selective reporting.
> {n_sc}/{k} studies raised **some concerns** because the trial registry entry
> was retrospective or absent. {n_h}/{k} studies were rated as **high risk** due
> to {reason_e.g. "multiple eligible outcomes in the methods, only one reported"}.

---

## 3. Implications for the Synthesis / 对合并分析的提示

### 3.1 与 GRADE 的联动

RoB 2 评价结果直接进入 GRADE 的"偏倚风险"维度（5 降级因素之一）：

| 整体判定分布 | GRADE 降级建议 |
|---|---|
| 全部 Low | 不降级（除非有其它降级因素） |
| Some concerns 为主，无 High | 视占比：**Some concerns >50%** 降 1 级 |
| 任何 High 出现 | 视占比：**High ≥25%** 降 1 级；**High ≥50%** 降 2 级 |

> 阈值（如 25% / 50%）应在**方法学部分**预先指定。修改后用技能 `grade` task
> （`references/grade` 详见 §3.2 协议）接收 `risk_of_bias` 参数。

### 3.2 敏感性分析

> When at least one study was judged to be at high risk of bias overall, we
> performed a **sensitivity analysis** by excluding these studies. The pooled
> effect estimate changed from **{orig}** ({ci_orig}) to **{sens}** ({ci_sens}),
> corresponding to a **{pct_change}%** change in effect magnitude
> (see Appendix Fig. Z).

> 模板未给 "unchanged / minimal change / substantial change" 的阈值——仍须
> 在方法学部分预先定义什么叫"实质性改变"。

---

## 4. Reading the Figures / 读图说明模板

### 4.1 Traffic-light Plot（图 X）

> Figure X presents the risk-of-bias assessment for each of the {k} included studies
> across the five RoB 2 domains. Green cells indicate a low risk of bias, yellow
> cells indicate some concerns, and red cells indicate a high risk of bias.

### 4.2 Summary Bar Plot（图 Y）

> Figure Y summarizes the risk-of-bias assessment across studies, showing the
> proportion of studies with low risk, some concerns, and high risk for each
> RoB 2 domain. The {domain} domain had the highest proportion of studies with
> some concerns ({pct}%), while the {domain2} domain had the highest proportion
> of studies with low risk ({pct}%).

---

## 5. Reproducibility Notes / 可复现性记录

- RoB 2 评价应**双评价者独立完成**（单人评价需说明局限性）。
- 一致性：双评价者 Cohen's kappa（按整体判定 Include/Exclude-style? No ——
  按 3 等级 Low/Some/High 的加权 kappa）报告在方法学部分。
- 任何评价分歧都应在文中**预先在方法学部分说明如何仲裁**（第三方裁定 / 讨论一致）。
- 评价表（D1..D5 矩阵）应作为补充材料上传，保证他人可重现评价。

---

## 6. References / 引用

- Sterne JAC, Savović J, Page MJ, et al. (2019). RoB 2: a revised tool for assessing
  risk of bias in randomised trials. *BMJ*, 366, l4898.
- RoB 2 tool & guidance: https://www.riskofbias.info/welcome/rob-2-0-tool
- GRADE handbook: https://gdt.gradepro.org/app/handbook/handbook.html
