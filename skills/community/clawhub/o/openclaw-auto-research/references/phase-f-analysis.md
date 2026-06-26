# Phase F: Analysis & Decision (S14-S15)

## S14: RESULT_ANALYSIS — 结果分析

### 输入
- `stage-12/runs/` 和/或 `stage-13/` 的实验结果
- `stage-8/hypotheses.md` — 假设（用于对照分析）

### 产出
- `stage-14/analysis.md` — 分析报告
- `stage-14/experiment_summary.json` — metrics 汇总

### System Prompt

```
You are a quantitative research analyst. Always cite exact numbers from the provided data.
```

### User Prompt 模板

```
Analyze run metrics and produce markdown report with statistical interpretation.
Use the ACTUAL quantitative values provided — do NOT invent numbers.

SANITY CHECKS (perform BEFORE interpreting results):
1. MONOTONICITY: If a condition scales a parameter, check whether metrics move in expected direction.
2. BASELINE CALIBRATION: Are baseline results in the expected range for this dataset?
3. VARIANCE CHECK: Is within-condition variance smaller than between-condition differences?
4. RUNTIME CHECK: Did all conditions run long enough to converge?

Report structure:
- Executive Summary (2-3 sentences)
- Per-condition Results Table (mean ± std for each metric)
- Hypothesis-by-hypothesis Assessment (supported/refuted/inconclusive, with evidence)
- Statistical Tests (paired comparisons, effect sizes)
- Concerns and Limitations
- Recommendations for Next Steps

Experiment results:
{experiment_results}

Original hypotheses:
{hypotheses_text}
```

### 执行步骤

1. 读取实验结果文件（JSON metrics）
2. 读取 `stage-8/hypotheses.md` 作为对照
3. 发送 LLM 请求（max_tokens=8192）
4. 写入 `stage-14/analysis.md`
5. 提取 metrics 汇总写入 `experiment_summary.json`
6. 推送中文摘要（关键发现、假设是否得到支持）

---

## S15: RESEARCH_DECISION — 研究决策

### 输入
- `stage-14/analysis.md` — 分析报告
- `stage-7/synthesis.md` — 综述（上下文）
- `stage-8/hypotheses.md` — 假设

### 产出
- `stage-15/decision.md` — PROCEED / PIVOT / REFINE 决策文档

### System Prompt

```
You are a research program lead making go/no-go decisions.
```

### User Prompt 模板

```
Based on the analysis, make one of three decisions:
- **PROCEED** — results are sufficient, move to paper writing
- **PIVOT** — hypotheses are fundamentally flawed, generate new ones
- **REFINE** — hypotheses are sound but experiments need re-tuning

MINIMUM QUALITY CRITERIA for PROCEED (ALL must be met):
1. At least 2 baselines AND the proposed method have results
2. The primary metric is defined and reported with confidence intervals
3. At least one hypothesis is statistically supported (p < 0.05 or bootstrap CI)
4. No obvious data quality issues flagged in analysis

If choosing REFINE, specify:
- Which specific parameters/conditions to change
- Expected impact of changes
- Maximum additional compute budget

If choosing PIVOT, specify:
- Why current direction is fundamentally flawed
- Suggested new direction

Analysis:
{analysis_text}

Hypotheses:
{hypotheses_text}

Synthesis context:
{synthesis_text}
```

### 执行步骤

1. 读取 `stage-14/analysis.md`、`stage-8/hypotheses.md`、`stage-7/synthesis.md`
2. 发送 LLM 请求
3. 写入 `stage-15/decision.md`
4. 解析决策结果（PROCEED/PIVOT/REFINE）
5. 如果 PIVOT → 回到 S8 重新生成假设
6. 如果 REFINE → 回到 S12 重新执行实验（带修改建议）
7. 如果 PROCEED → 继续 Phase G
8. 推送中文摘要（决策结果 + 理由）
