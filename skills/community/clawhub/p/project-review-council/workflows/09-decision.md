# Phase 9 — 委员会决议

## 输入

P1-P8 全部产出。

## 处理

1. 综合所有阶段，形成决议
2. 按 [rubrics/decision-matrix.md](../rubrics/decision-matrix.md) 给出建议
3. 按 [rubrics/grade-scale.md](../rubrics/grade-scale.md) 给出最终评级
4. 输出 ≥ `min_report_words`(默认 3000) 字的完整评审报告

## 输出：按 [templates/executive-summary.md](../templates/executive-summary.md) 模板

包含：
- Executive Summary
- 最大的三个优点
- 最大的三个问题
- 最大的三个风险
- 最值得立即修复的问题
- 建议：继续 / 暂停 / 重构 / 放弃
- 下一阶段路线图
- 最终评级：A+ / A / B+ / B / C / D / F
- "如果这是你的项目，你会不会继续做？为什么？"

## Exit Gate

- 字数 ≥ `min_report_words`
- 4 项建议（继续/暂停/重构/放弃）必须有明确推荐
- 评级与综合分一致（查 [rubrics/grade-scale.md](../rubrics/grade-scale.md)）
- 所有结论标注证据等级

## Decision Gate

| 情况 | 动作 |
|------|------|
| 报告 < `min_report_words` 字 | 扩充 |
| 评级与综合分矛盾 | 修正 |
| `enable_phase_10: true` | 进入 P10 红蓝对抗 |
| `enable_phase_10: false` | 结束，输出决议 |

## Retry / Rollback

- **Retry**：报告缺项 → 补全
- **Rollback**：发现新 Fatal 风险 → 回退 P5 重排

## 用户检查点

展示决议摘要，确认后进入 P10。
