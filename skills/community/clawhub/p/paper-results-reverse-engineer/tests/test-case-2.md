# Test Case 2: Figure Caption + Single Paragraph — ERP Study

## Input

```
Figure 2 caption:
Figure 2. Grand-average ERPs time-locked to probe onset at electrode Pz. (A) Waveforms for remembered (solid line) and forgotten (dashed line) items in the sleep condition. (B) The same contrast in the wake condition. The gray shaded area marks the 300–500 ms time window used for statistical analysis. Topographic maps show the Remembered > Forgotten difference in this window.

Results paragraph:
To examine the neural correlates of sleep-dependent memory enhancement, we compared ERP responses to subsequently remembered versus forgotten items across the sleep and wake conditions. As shown in Figure 2, in the sleep condition, remembered items elicited a more positive-going waveform between 300–500 ms post-probe compared to forgotten items. This late positive component (LPC) difference was confirmed by a significant Condition × Memory interaction, F(1, 30) = 7.89, p = .009, ηp² = .21. Follow-up analyses revealed that the LPC old/new effect was significant in the sleep condition, t(15) = 3.45, p = .003, d = 0.89, but not in the wake condition, t(15) = 1.12, p = .280, d = 0.27. Importantly, the magnitude of the LPC effect in the sleep condition correlated positively with overnight memory retention (r = .55, p = .027), suggesting that this enhanced neural differentiation between remembered and forgotten items reflects more effective consolidation.
```

## Expected Output Structure

### Module A (abbreviated — limited to what can be inferred)
- 研究主题: Neural correlates (ERP LPC) of sleep-dependent memory enhancement
- 研究问题: Does sleep enhance the neural differentiation between remembered and forgotten items (LPC old/new effect)?
- 核心假设: Sleep group shows larger LPC old/new effect than wake group; LPC magnitude correlates with behavioral retention
- 样本: N = 32 (16 per group, inferred from df)
- 任务: Probe recognition with EEG (inferred from "probe onset")
- IV: Condition (sleep/wake, between), Memory (remembered/forgotten, within)
- DV: ERP amplitude (300–500 ms at Pz), recognition accuracy

### Module B (abbreviated — single paragraph)
- 回答的问题: Does sleep enhance neural differentiation of remembered vs. forgotten items? And does this correlate with behavior?
- 对应图表: Figure 2 (A, B, topographic maps)
- 主要结果: Significant Condition × Memory interaction; LPC effect significant only in sleep group; LPC correlates with behavioral retention
- 结论: Sleep enhances neural signatures of successful encoding/retrieval

### Module C
```
S1: To examine the neural correlates of sleep-dependent memory enhancement, we compared ERP responses...
→ Label 1 (restate aim)

S2: As shown in Figure 2, in the sleep condition, remembered items elicited a more positive-going waveform...
→ Label 4 + 5 (invite figure + report specific result)

S3: This late positive component (LPC) difference was confirmed by a significant Condition × Memory interaction...
→ Label 6 (statistical evidence)

S4: Follow-up analyses revealed that the LPC old/new effect was significant in the sleep condition... but not in the wake condition...
→ Label 6 + 11 (statistical evidence + note non-significant)

S5: Importantly, the magnitude of the LPC effect in the sleep condition correlated positively with overnight memory retention...
→ Label 7 + 6 (evaluative emphasis + statistical evidence)

S6: ...suggesting that this enhanced neural differentiation between remembered and forgotten items reflects more effective consolidation.
→ Label 13 (hint at implication)
```

**段落结构分析:**
- S1: 建立分析框架（目的句）
- S2: 图表引导 + 描述性发现
- S3: 统计确认
- S4: 简单效应检验 + 诚实报告零结果
- S5–S6: 脑-行为相关 + 意义提示

这个段落是一个典型的 "mini Results story"：目的 → 描述 → 统计 → 细化 → 脑-行为桥接 → 意义。

### Module D: Figure 2 Guide
1. **Question:** Does the brain differentiate remembered from forgotten items differently after sleep vs. wake?
2. **Axes/groups:**
   - Panel A (sleep): x = time, y = μV at Pz; solid = remembered, dashed = forgotten
   - Panel B (wake): same axes
   - Gray shading: 300–500 ms (LPC window)
   - Topographic maps: Remembered − Forgotten difference
3. **Author's guidance:** "As shown in Figure 2, in the sleep condition, remembered items elicited a more positive-going waveform..."
4. **Key pattern:** LPC old/new effect present in sleep, absent in wake; topography likely shows parietal positivity
5. **Primary:** Condition × Memory interaction; brain-behavior correlation; **Auxiliary:** topographic distribution detail
6. **PPT narration logic:**
   - "这张图展示了睡眠如何改变大脑对记住和遗忘项目的区分。"
   - Point to Panel A: "在睡眠组，记住的项目（实线）在 300–500 毫秒出现了更正的电位——这就是经典的 LPC 新旧效应。"
   - Point to Panel B: "但在清醒组，实线和虚线几乎重叠——没有新旧效应。"
   - Point to topographic maps: "地形图显示这种差异集中在顶叶。"
   - Bridge to correlation: "更重要的是，这个 LPC 效应越大的人，行为上的记忆保持也越好。"
7. **1-minute narration:**
   > "这张图回答的问题是：睡眠是否改变了大脑对记忆的神经标记？图 A 是睡眠组，实线是后来记住的项目，虚线是忘记的项目。在 300 到 500 毫秒的灰色窗口里——也就是经典的 LPC 成分——记住的项目诱发了一个更正的波形。这是标准的'新旧效应'。但图 B 清醒组——实线和虚线基本没有分离。统计上也证实：交互效应显著，睡眠组有显著的新旧效应（d = 0.89），而清醒组没有（d = 0.27）。更关键的是，LPC 效应越大的人，行为上的记忆保持也越好——r = 0.55。这说明睡眠可能是在加强记忆的神经表征质量。"

### Module E: Writing Strategy
- **开头方式:** "To examine [mechanism], we compared [measure] across [conditions]" → 目的句 + 方法预览
- **图表引导:** "As shown in Figure X, in [condition A], [phenomenon]" → 同时完成引导和描述
- **统计桥接:** "[phenomenon] was confirmed by [inferential test]" → 描述→统计的过渡
- **不显著报告:** "the LPC effect was significant in the sleep condition... but not in the wake condition, t = 1.12, p = .280, d = 0.27" → 完整报告统计量，不说"marginally significant"
- **脑-行为关联:** "[neural measure] correlated positively with [behavioral measure] (r = .XX, p = .XXX), suggesting that..." → 相关 + 解释性推测

### Module F: Critical Check
- [ ] 结果与讨论混杂: S6 "reflects more effective consolidation" 已有解释性质，但在 Results 中可接受（Label 13）
- [x] 统计报告: 完整报告了 F, t, df, p, ηp², d, r
- [ ] 因果表达: "reflects more effective consolidation" 略微偏强——这只是相关证据
- [ ] 选择性强调: 清醒组零结果被如实报告，无选择性隐藏
- [x] 图表对应: 波形描述与 Figure 2 的 caption 一致

### Module G
- **写作逻辑:** 从脑电现象描述 → 统计确认 → 条件对比 → 脑-行为关联 → 意义提示，是典型的 ERP 结果段落结构
- **最值得模仿:** (1) 描述→统计的桥接句; (2) 不显著结果的完整报告; (3) 脑-行为相关的"correlated (stats), suggesting that..." 模式
- **需警惕:** 相关 ≠ 因果；这篇只报告了 300–500 ms 窗口，是否有窗口选择偏差？
