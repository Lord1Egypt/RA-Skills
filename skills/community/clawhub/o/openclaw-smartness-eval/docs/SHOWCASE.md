# Showcase / 案例展示

Real-world evaluation results and sharing guidelines.

真实评估案例和分享指南。

---

## Real Evaluation Result / 真实评估结果

The following is from an actual `quick` mode evaluation of an OpenClaw V5.1 workspace:

以下来自对 OpenClaw V5.1 工作区的一次真实 `quick` 模式评估：

### Summary / 概要

| Metric | Value |
|--------|-------|
| **Overall score** | 71.36 |
| **Grade** | B- |
| **Confidence interval** | [71.36, 71.36] |
| **Mode** | quick |
| **Test samples** | 15 |
| **Dimension spread** | 327.72 |

### Dimension Breakdown / 维度详情

| Rank | Dimension | 维度 | Score | Bar | Level |
|------|-----------|------|-------|-----|-------|
| 1 | Understanding | 理解 | 85.00 | ████████░░ | Strong |
| 2 | Dialogue | 对话沟通 | 82.50 | ████████░░ | Strong |
| 3 | Policy adherence | 策略遵循 | 77.14 | ███████░░░ | Good |
| 4 | Analysis | 分析 | 76.31 | ███████░░░ | Good |
| 5 | Reasoning | 推理 | 74.79 | ███████░░░ | Good |
| 6 | Thinking | 思考 | 73.50 | ███████░░░ | Average |
| 7 | Tool reliability | 工具可靠性 | 72.43 | ███████░░░ | Average |
| 8 | Generalization | 泛化能力 | 70.00 | ███████░░░ | Average |
| 9 | Responsiveness | 响应时长 | 63.05 | ██████░░░░ | Below avg |
| 10 | Robustness | 鲁棒性 | 62.14 | ██████░░░░ | Below avg |
| 11 | Calibration | 校准能力 | 60.69 | ██████░░░░ | Weak |
| 12 | Self-iteration | 自我迭代 | 55.56 | █████░░░░░ | Weak |

### Key Evidence / 关键证据

| Metric | Value | Impact |
|--------|-------|--------|
| Benchmark pass rate | 100.0% | Positive — all core tests passed |
| P50 latency | 5246 ms | Negative — median response is slow |
| Reasoning store entries | 116 | Positive — large knowledge base |
| Error fix rate | 0.0% | Negative — no tracked error fixes |
| Cron error rate | 35.71% | Negative — many cron tasks failing |
| High-confidence patterns | 8 | Moderate — some patterns promoted |
| Reflection reports | 2 | Low — limited self-reflection |

### Risk Flags / 风险告警

1. **5 failing cron tasks** — 仍有 5 个出错中的启用 Cron 任务
2. **Insufficient finalize samples** — finalize 闭环样本不足

### Recommendations / 升级建议

1. Fix failing cron tasks or convert them to thin-scripts / 修复出错 Cron 任务或 thin-script 化
2. Increase finalize path usage to improve thinking/calibration confidence / 增加 finalize 使用量
3. Track and resolve errors in error-tracker to boost self-iteration score / 追踪并修复错误

---

## Trend Comparison Example / 趋势对比示例

When using `--compare-last`, the report shows delta arrows:

```
Trend vs last run (2026-03-14):
  understanding      85.00  →  85.00  (=)
  analysis           73.12  →  76.31  (+3.19 ↑)
  thinking           70.00  →  73.50  (+3.50 ↑)
  reasoning          72.40  →  74.79  (+2.39 ↑)
  self_iteration     55.56  →  55.56  (=)
  dialogue           80.00  →  82.50  (+2.50 ↑)
  responsiveness     65.00  →  63.05  (-1.95 ↓ regression!)
```

Regressions are highlighted as warnings. This helps you identify if a recent change degraded a specific capability.

退化维度会被高亮告警，帮助你判断最近的改动是否损害了某项能力。

---

## Sharing Guide / 分享指南

### When posting results publicly, include / 公开分享时请包含:

1. **Overall score + grade** — e.g., `71.36 (B-)`
2. **Confidence interval** — shows reliability
3. **Mode** — so others know the evaluation depth
4. **Top 3 strong dimensions** — highlights
5. **Top 2 weak dimensions** — areas for improvement
6. **At least 3 evidence metrics** — proves the score isn't arbitrary
7. **Environment** — OpenClaw version, OS, workspace version

### Template for X/Twitter / 推特分享模板

```
🎯 My AI Agent smartness score: 71.36 (B-)

📊 Strong: Understanding (85), Dialogue (82.5)
📉 Weak: Self-iteration (55.6), Calibration (60.7)
🔍 Evidence: 100% benchmark pass, 116 reasoning entries

Evaluated with OpenClaw Smartness Eval ⭐
https://github.com/xyva-yuangui/smartness-eval

#AIAgent #Benchmark #OpenClaw
```

### Template for GitHub Discussion / GitHub 讨论模板

```markdown
## My Agent Eval Result — [Date]

| Metric | Value |
|--------|-------|
| Score | XX.XX |
| Grade | X |
| Mode | quick/standard/deep |
| OpenClaw | 2026.x.x |

### Top dimensions
- ...

### Weakest dimensions
- ...

### What I improved since last run
- ...
```

---

## Use Cases / 使用场景

| Scenario | Mode | Purpose / 用途 |
|----------|------|----------------|
| Daily self-reflection | `quick` | Quick health check after a day of work / 日常自省 |
| Weekly team report | `standard` | Share with team, track week-over-week progress / 团队周报 |
| Post-upgrade regression | `standard` + `--compare-last` | Verify upgrade didn't break anything / 版本升级回归检查 |
| Monthly audit | `deep` | Comprehensive assessment with high reliability / 月度深度审计 |
| Conference demo | `deep` + `--llm-judge` | Full evaluation with LLM subjective scoring / 演示展示 |
| Community benchmarking | Any + share result | Compare scores across different setups / 社区横向对比 |
