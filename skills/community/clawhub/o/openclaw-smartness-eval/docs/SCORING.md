# Scoring Formulas / 评分公式详解 (v0.3.0)

This document explains how each of the **14** dimension scores is computed, how they combine into an overall score, and how grades are assigned.

本文档详细说明 14 个维度的计算公式、总分合成方式和等级划分。

> **v0.3.0 changes:** Added `planning` and `hallucination_control` dimensions; all formula inputs normalized to 0–100 before weighting; all weights per dimension verified to sum to exactly 1.0; aligned with CLEAR framework and T-Eval standards.

---

## Overall Score / 总分

```
overall_score = Σ(dimension_score_i × weight_i)
```

All weights sum to 100%. The final score is on a 0–100 scale.

### Weight Table / 权重表

| # | Dimension | 维度 | Weight | Category |
|---|-----------|------|--------|----------|
| 1 | Understanding | 理解 | 9% | Main |
| 2 | Analysis | 分析 | 9% | Main |
| 3 | Thinking | 思考 | 9% | Main |
| 4 | Reasoning | 推理 | 13% | Main |
| 5 | Self-iteration | 自我迭代 | 9% | Main |
| 6 | Dialogue | 对话沟通 | 9% | Main |
| 7 | Responsiveness | 响应时长 | 5% | Main |
| 8 | Robustness | 鲁棒性 | 7% | Expanded |
| 9 | Generalization | 泛化能力 | 5% | Expanded |
| 10 | **Planning** | **规划能力** | **5%** | **Expanded (NEW)** |
| 11 | **Hallucination Control** | **幻觉控制** | **6%** | **Expanded (NEW)** |
| 12 | Policy adherence | 策略遵循 | 5% | Expanded |
| 13 | Tool reliability | 工具可靠性 | 4% | Expanded |
| 14 | Calibration | 校准能力 | 5% | Expanded |

> Weights are configurable in `config/config.json` under `"weights"`.

---

## Normalization Principle / 归一化原则

All metric inputs are normalized to a **0–100** scale before weighting. This ensures formula transparency — every weight directly represents its contribution percentage.

所有指标输入在加权前均归一化到 **0–100** 范围。权重直接代表贡献百分比。

```python
# Example: real interaction count (raw 0–50) → normalized 0–100
n_interaction = min(count, 50) / 50 * 100
```

---

## Per-Dimension Formulas / 各维度公式

Each dimension score blends **task test results** with **real runtime metrics**. All weights sum to 1.00.

每个维度的分数由 **任务测试得分** 和 **真实运行指标** 加权合成，所有权重之和 = 1.00。

### 1. Understanding / 理解 (9%)

```
understanding = task_score × 0.45          # task-suite pass rate
              + benchmark_pass_rate × 0.15 # core benchmark
              + n_interaction × 0.25       # real interaction count (cap 50, normalized)
              + n_intent_coverage × 0.15   # unique intent types (cap 8, normalized)
```
**Weights: 0.45 + 0.15 + 0.25 + 0.15 = 1.00** ✓

**Data sources:** task-suite tests tagged `understanding`, benchmark history, message-analyzer log.

---

### 2. Analysis / 分析 (9%)

```
analysis = task_score × 0.40              # task-suite pass rate
         + benchmark_pass_rate × 0.15     # core benchmark
         + reasoning_depth × 0.20         # high-confidence ratio (0–1 → 0–100)
         + n_dup_rate_inv × 0.15          # inverted duplicate reply rate
         + n_reasoning_total × 0.10       # reasoning store entries (cap 120, normalized)
```
**Weights: 0.40 + 0.15 + 0.20 + 0.15 + 0.10 = 1.00** ✓

**Data sources:** task-suite tests tagged `analysis`, reasoning store, regression metrics.

---

### 3. Thinking / 思考 (9%)

```
thinking = task_score × 0.35             # task-suite pass rate
         + repeat_error_control × 0.20   # 100 - repeat_ratio * 100
         + finalize_rate × 0.15          # finalize approval ratio (0–1 → 0–100)
         + n_reasoning_high × 0.15       # high-confidence entries (cap 40, normalized)
         + n_reflection × 0.15           # reflection reports (cap 10, normalized)
```
**Weights: 0.35 + 0.20 + 0.15 + 0.15 + 0.15 = 1.00** ✓

**Data sources:** task-suite tests tagged `thinking`, error-tracker, finalize log, reasoning store, reflection reports.

---

### 4. Reasoning / 推理 (13%)

```
reasoning = task_score × 0.35            # task-suite pass rate
          + benchmark_pass_rate × 0.15   # core benchmark
          + reasoning_depth × 0.25       # high-confidence ratio (0–1 → 0–100)
          + n_reasoning_total × 0.15     # reasoning entries (cap 120, normalized)
          + finalize_rate × 0.10         # finalize approval ratio
```
**Weights: 0.35 + 0.15 + 0.25 + 0.15 + 0.10 = 1.00** ✓

**Data sources:** task-suite tests tagged `reasoning`, benchmark history, reasoning store (SQLite), finalize log.

---

### 5. Self-iteration / 自我迭代 (9%)

```
self_iteration = task_score × 0.25       # task-suite pass rate
               + error_fix_rate × 0.20   # errors fixed / total errors
               + error_verify_rate × 0.15 # verified / fixed
               + promoted_ratio × 0.15   # promoted patterns / high-conf patterns
               + n_reflection × 0.15     # reflection reports (cap 10, normalized)
               + repeat_decline × 0.10   # 100 - repeat_ratio * 100
```
**Weights: 0.25 + 0.20 + 0.15 + 0.15 + 0.15 + 0.10 = 1.00** ✓

**Data sources:** task-suite tests tagged `self_iteration`, error-tracker, pattern-library, reflection reports.

---

### 6. Dialogue / 对话沟通 (9%)

```
dialogue = task_score × 0.40             # task-suite pass rate
         + n_dialogue_int × 0.20         # interaction count (cap 30, normalized)
         + benchmark_pass_rate × 0.15    # core benchmark
         + high_risk_handling × 0.15     # 100 if high-risk seen, else 50
         + n_intent_coverage × 0.10      # intent diversity (cap 8, normalized)
```
**Weights: 0.40 + 0.20 + 0.15 + 0.15 + 0.10 = 1.00** ✓

**Data sources:** task-suite tests tagged `dialogue`, benchmark history, message-analyzer log.

---

### 7. Responsiveness / 响应时长 (5%)

This dimension uses **non-linear penalty scoring** rather than linear blending:

该维度使用非线性惩罚评分：

```python
score = 100.0

# P50 penalty (if median latency exceeds 1500ms)
if p50 > 1500:
    score -= min(25, ((p50 - 1500) / 1000) ** 1.5 * 5)

# P95 penalty (if tail latency exceeds 5000ms)
if p95 > 5000:
    score -= min(35, ((p95 - 5000) / 2000) ** 1.4 * 8)

# Timeout penalty
score -= min(20, timeout_rate * 100)

score = clamp(score, 0, 100)
```

**Data sources:** response-latency-metrics, regression-metrics cron timeout rate.

---

### 8. Robustness / 鲁棒性 (7%)

```
robustness = task_score × 0.30           # task-suite pass rate
           + repeat_error_control × 0.20 # 100 - repeat_ratio * 100
           + cron_health × 0.20          # 100 - cron_error_ratio * 100
           + benchmark_pass_rate × 0.15  # core benchmark
           + alert_control × 0.15        # 100 - normalized alert count
```
**Weights: 0.30 + 0.20 + 0.20 + 0.15 + 0.15 = 1.00** ✓

**Data sources:** task-suite tests tagged `robustness`, error-tracker, cron-governor, benchmark, alerts.jsonl.

---

### 9. Generalization / 泛化能力 (5%)

```
generalization = task_score × 0.35       # task-suite pass rate
               + n_intent_coverage × 0.25 # unique intent categories (cap 8, normalized)
               + n_orch_diversity × 0.25  # orchestrator log count (cap 10, normalized)
               + benchmark_pass_rate × 0.15 # core benchmark
```
**Weights: 0.35 + 0.25 + 0.25 + 0.15 = 1.00** ✓

**Data sources:** task-suite tests tagged `generalization`, message-analyzer, orchestrator log.

---

### 10. Planning / 规划能力 (5%) — NEW in v0.3

Aligned with **T-Eval** (ACL 2024) planning dimension and **CLEAR** efficacy dimension.

```
planning = task_score × 0.30             # task-suite pass rate
         + finalize_rate × 0.25          # finalize approval ratio (0–1 → 0–100)
         + n_reasoning_total × 0.20      # reasoning entries (cap 120, normalized)
         + n_orch_diversity × 0.15       # orchestrator diversity (cap 10, normalized)
         + n_reflection × 0.10           # reflection reports (cap 10, normalized)
```
**Weights: 0.30 + 0.25 + 0.20 + 0.15 + 0.10 = 1.00** ✓

**Data sources:** task-suite tests tagged `planning`, finalize log, reasoning store, orchestrator log, reflection reports.

**Rationale:** Planning requires multi-step workflow execution (finalize pipeline), accumulated reasoning patterns (reasoning store), diverse pipeline usage (orchestrator), and reflective plan review (reflection reports).

---

### 11. Hallucination Control / 幻觉控制 (6%) — NEW in v0.3

Aligned with **CLEAR** assurance dimension and **Anthropic** safety/trust evaluation.

```
hallucination_control = task_score × 0.25     # task-suite pass rate
                      + reasoning_depth × 0.25 # high-confidence accuracy (0–1 → 0–100)
                      + repeat_error_ctrl × 0.20 # 100 - repeat_ratio * 100
                      + benchmark_pass_rate × 0.15
                      + hp_error_ctrl × 0.15   # 100 - high_priority_open_ratio * 100
```
**Weights: 0.25 + 0.25 + 0.20 + 0.15 + 0.15 = 1.00** ✓

**Data sources:** task-suite tests tagged `hallucination_control`, reasoning store, error-tracker, benchmark.

**Rationale:** Low hallucination correlates with high reasoning accuracy (not blindly high-confidence), low repeated errors (not persistently wrong), and controlled high-priority error rate.

---

### 12. Policy Adherence / 策略遵循 (5%)

```
policy = task_score × 0.35              # task-suite pass rate
       + cron_thin × 0.25              # thin-script compliance ratio
       + cron_health × 0.20            # 100 - cron_error_ratio * 100
       + high_risk_confirm × 0.20      # 100 if high-risk interaction seen, else 60
```
**Weights: 0.35 + 0.25 + 0.20 + 0.20 = 1.00** ✓

**Data sources:** task-suite tests tagged `policy`, cron-governor-report, message-analyzer log.

---

### 13. Tool Reliability / 工具可靠性 (4%)

```
tool_reliability = task_score × 0.30     # task-suite pass rate
                 + benchmark_pass_rate × 0.20
                 + cron_health × 0.20    # 100 - cron_error_ratio * 100
                 + cron_thin × 0.15      # thin-script compliance
                 + n_rule_candidates × 0.15 # rule candidates (cap 10, normalized)
```
**Weights: 0.30 + 0.20 + 0.20 + 0.15 + 0.15 = 1.00** ✓

**Data sources:** task-suite tests tagged `tool`, cron report, benchmark, rule-candidates.json.

---

### 14. Calibration / 校准能力 (5%)

```
calibration = task_score × 0.30          # task-suite pass rate
            + conf_accuracy × 0.25       # composite: reasoning_depth×0.6 + (1-repeat_ratio)×0.4
            + finalize_rate × 0.20       # finalize approval ratio
            + hp_error_ctrl × 0.25       # 100 - high_priority_open_ratio * 100
```
**Weights: 0.30 + 0.25 + 0.20 + 0.25 = 1.00** ✓

**Data sources:** task-suite tests tagged `calibration`, reasoning store, finalize log, error tracker.

---

## Confidence Interval / 置信区间

For `deep` mode, each test is run `repeat` times. The 95% CI is computed as:

```
CI = [overall - 1.96 × σ / √n,  overall + 1.96 × σ / √n]
```

Where `σ` is the standard deviation of per-run overall scores and `n` is the number of repeat runs.

For `quick`/`standard` modes (single run), CI = [score, score].

---

## Trend Delta / 趋势变化

When `--compare-last` is used, the system loads the most recent entry from `history.jsonl` and computes:

```
delta_i = current_dimension_i - previous_dimension_i
```

Dimensions with delta < -5 are flagged as **degradation alerts** (退化告警).

---

## Grade Scale / 等级划分

| Grade | Score range | 含义 |
|-------|-------------|------|
| A+ | ≥ 92 | Exceptional / 卓越 |
| A | ≥ 88 | Excellent / 优秀 |
| A- | ≥ 84 | Very good / 良好偏上 |
| B+ | ≥ 80 | Good / 良好 |
| B | ≥ 76 | Above average / 中等偏上 |
| B- | ≥ 72 | Average / 中等 |
| C+ | ≥ 68 | Below average / 中等偏下 |
| C | ≥ 64 | Passing / 及格 |
| D | < 64 | Needs improvement / 需要改进 |

---

## Dimension Spread / 维度离散度

```
spread = variance(all 14 dimension scores)
```

High spread indicates unbalanced capability — some dimensions are strong while others lag.

高离散度表示能力不均衡，部分维度强而部分维度弱。

---

## Customizing Weights / 自定义权重

Edit `config/config.json`:

```json
{
  "weights": {
    "main": {
      "understanding": 9,
      "analysis": 9,
      "thinking": 9,
      "reasoning": 13,
      "self_iteration": 9,
      "dialogue_communication": 9,
      "responsiveness": 5
    },
    "expanded": {
      "robustness": 7,
      "generalization": 5,
      "planning": 5,
      "hallucination_control": 6,
      "policy_adherence": 5,
      "tool_reliability": 4,
      "calibration": 5
    }
  }
}
```

Weights are normalized to sum to 100% at runtime, so you can use any scale.
权重在运行时会自动归一化为 100%，所以可以使用任意尺度。

---

## Industry Alignment / 行业标准对齐

v0.3.0 evaluation dimensions are aligned with established frameworks:

| This project | CLEAR (2024) | T-Eval (ACL 2024) | Anthropic Agent Eval |
|---|---|---|---|
| Understanding | Efficacy | Understanding | Instruction following |
| Analysis | Efficacy | Reasoning | Code-based graders |
| Thinking | Assurance | Review | Safety evaluation |
| Reasoning | Efficacy | Reasoning | Model-based graders |
| Self-iteration | Reliability | — | Regression evals |
| Dialogue | Efficacy | Instruction Following | Conversational eval |
| Responsiveness | Latency | — | Latency tracking |
| Robustness | Reliability | — | Non-determinism handling |
| Generalization | Efficacy | Retrieval | Capability evals |
| **Planning** | **Efficacy** | **Planning** | **Task decomposition** |
| **Hallucination Control** | **Assurance** | **— (safety)** | **Safety/trust** |
| Policy adherence | Assurance | — | Safety evaluation |
| Tool reliability | Reliability | — | Code-based graders |
| Calibration | Assurance | Review | LLM-as-judge calibration |
