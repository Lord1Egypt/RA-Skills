# Test Case 1: Full Results Section — Sleep & Emotional Memory

## Input

```
Results

3.1 Emotional memory consolidation across sleep stages

To test whether sleep-dependent consolidation of emotional memories varies by sleep stage, we examined recognition memory for negative, neutral, and positive images after a 12-hour retention interval containing either nocturnal sleep (N = 28) or daytime wake (N = 26).

Overall, sleep benefitted emotional memory: participants in the sleep group showed higher recognition accuracy for negative images (M = 0.81, SD = 0.09) compared to the wake group (M = 0.72, SD = 0.11; Figure 2A). A 2 (Group) × 3 (Valence) mixed ANOVA on d' scores revealed a significant Group × Valence interaction, F(2, 104) = 6.32, p = .003, ηp² = .11. Follow-up t-tests confirmed that the sleep benefit was significant for negative images, t(52) = 3.12, p = .003, d = 0.84, and neutral images, t(52) = 2.45, p = .018, d = 0.66, but not for positive images, t(52) = 1.08, p = .285, d = 0.29.

Remarkably, the sleep group's advantage for negative images remained significant after controlling for pre-sleep recognition performance, F(1, 51) = 5.87, p = .019, ηp² = .10, suggesting that sleep does not merely preserve pre-sleep differences but actively enhances negative memory.

3.2 The role of REM sleep duration

We next examined whether REM sleep duration specifically predicted emotional memory benefit. In the sleep group, polysomnography revealed an average REM duration of 94.2 min (SD = 28.6). Consistent with the emotional trade-off hypothesis, REM duration positively correlated with negative image recognition (r = .51, p = .006) but negatively correlated with neutral image recognition (r = -.43, p = .023; Figure 3A). This double dissociation suggests that REM sleep selectively strengthens emotional memories at the expense of neutral ones.

## Expected Output Structure

After receiving this input, the agent should produce:

### Module A
- 研究主题: Sleep-dependent consolidation of emotional vs. neutral memories, role of REM
- 研究问题: Does sleep preferentially consolidate emotional memories? Does REM duration predict this effect?
- 核心假设: Sleep benefits emotional (esp. negative) > neutral > positive memories; REM drives selective emotional enhancement
- 样本: N = 54 (28 sleep, 26 wake)
- IV: Group (sleep/wake), Valence (neg/neu/pos)
- DV: Recognition accuracy, d', correlations with REM

### Module B
- 3.1: 睡眠是否选择性巩固情绪记忆？
- 3.2: REM 时长是否特异性地预测情绪记忆的巩固？

### Module C (key sentences)
- S1 (3.1): "To test whether..." → Label 1 (restate aim)
- S2: "Overall, sleep benefitted..." → Label 3 (overview trend)
- "As shown in Figure 2A" → Label 4 (invite figure)
- "A 2 × 3 mixed ANOVA..." → Label 6 (statistical evidence)
- "Remarkably, the sleep group's advantage..." → Label 7 + 6 + 13
- "We next examined whether REM sleep duration..." → Label 1
- "Consistent with the emotional trade-off hypothesis..." → Label 9
- "This double dissociation suggests..." → Label 10 + 13

### Module D
- Figure 2A: Bar chart, Group × Valence, key pattern = sleep > wake for negative > neutral > positive (interaction)
- Figure 3A: Scatter plot, x = REM duration, y = recognition, positive slope for neg, negative slope for neutral

### Module E
- "Remarkably" as evaluative emphasis
- "remained significant after controlling for" as robustness check pattern
- "This double dissociation suggests that X at the expense of Y" as interpretation frame
- 不显著结果: "but not for positive images, t(52) = 1.08, p = .285" → honest null reporting

### Module F (check)
- [x] 轻微 results-discussion 混杂: 3.2 末句已是 interpretation ("suggests that REM selectively strengthens...")
- [x] 因果表达需注意: "REM duration positively correlated with" — correlation, not causation
- [x] 统计报告: 报告了 t, df, p, d, ηp² — 较完整
- [x] 选择性强调: positive stimuli null result 仅一笔带过

### Module G
- 值得模仿: (1) 控制分析增强说服力; (2) "double dissociation" 作为高级结果组织方式; (3) 不显著结果的诚实报告
- 需警惕: 相关 ≠ 因果; "at the expense of" 暗示零和但可能是负相关假象
