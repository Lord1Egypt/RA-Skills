# Worked Example: Full Reverse Engineering

The example below uses a synthetic but realistic sleep-and-memory paper Results section, modeled on typical Journal of Sleep Research / Neurobiology of Learning and Memory style. All data, citations, and statistics are fabricated for illustration.

---

## Source Text (Input)

> **Results**
>
> **3.1 Sleep architecture**
>
> As expected, total sleep time did not differ between the nap (M = 87.2 min, SD = 12.4) and overnight sleep conditions (M = 425.6 min, SD = 38.7). The nap condition contained an average of 21.3 min (SD = 8.1) of SWS and 18.7 min (SD = 6.4) of REM sleep. In the overnight condition, participants obtained 89.4 min (SD = 22.1) of SWS and 102.3 min (SD = 28.6) of REM.
>
> **3.2 Memory consolidation across conditions**
>
> To assess whether sleep-dependent memory consolidation differed between the nap and overnight conditions, we examined change in recall accuracy from the immediate test to the delayed test. Overall, both conditions showed significant memory retention above chance (all ps < .001), but the magnitude of consolidation differed markedly.
>
> As shown in Figure 2A, overnight sleep produced a substantially larger consolidation benefit (M = +18.3%, SD = 7.2) than the nap (M = +6.1%, SD = 5.8). A 2 (Condition) × 2 (Memory Type: declarative vs. procedural) mixed ANOVA confirmed a significant main effect of Condition, F(1, 34) = 14.62, p < .001, ηp² = .30, with overnight sleep outperforming the nap. The main effect of Memory Type was also significant, F(1, 34) = 5.41, p = .026, ηp² = .14, driven by greater consolidation of declarative than procedural memories. Importantly, the Condition × Memory Type interaction was not significant, F(1, 34) = 1.23, p = .275, suggesting that the advantage of overnight sleep was comparable across memory types.
>
> Consistent with prior work (Diekelmann & Born, 2010), declarative memory consolidation was positively correlated with SWS duration in the overnight condition (r = .48, p = .003), but not in the nap condition (r = .19, p = .271). This dissociation may reflect the greater absolute amount of SWS in the overnight condition, providing more opportunities for hippocampal-neocortical dialogue.
>
> **3.3 Slow oscillation-spindle coupling**
>
> We next asked whether the quality of sleep physiology, beyond sleep duration, predicted memory outcomes. Using automated detection algorithms, we identified discrete slow oscillations (0.5–1 Hz) and sleep spindles (12–16 Hz) during NREM sleep and quantified their temporal coupling (see Figure 3A for an example trace).
>
> Strikingly, the precision of SO-spindle coupling (measured as the phase-locking value, PLV) was a strong predictor of overnight declarative memory consolidation (r = .61, p < .001; Figure 3B), even after controlling for total SWS duration (partial r = .53, p = .001). This relationship was not observed for procedural memory (r = .12, p = .482), suggesting a degree of memory-type specificity. We note that the sample size for this analysis was modest (N = 36), which may limit the generalizability of these correlational findings.
>
> These results suggest that it is not merely the amount of sleep, but the precise temporal coordination of NREM oscillations, that drives memory consolidation — a point we develop further in the Discussion.

---

## Module A: Literature Info Table

| 字段 | 内容 |
|------|------|
| 研究主题 | 睡眠时长（nap vs. overnight）和睡眠生理（慢振荡-纺锤波耦合）对陈述性与程序性记忆巩固的影响 |
| 研究问题 | (1) 不同时长睡眠条件下的记忆巩固有无差异？(2) 记忆类型是否调节睡眠的巩固效应？(3) NREM 振荡耦合是否超越睡眠时长预测记忆？ |
| 核心假设 | 推测假设：overnight sleep 的巩固效果优于 nap；SWS 与陈述性记忆相关；SO-spindle coupling 是比睡眠时长更好的预测因子 |
| 样本/材料/任务 | N = 36（根据 3.3 小节推断）；任务包含陈述性记忆任务和程序性记忆任务（具体任务见 Method，本节未详述） |
| 自变量(IV) | Condition (nap vs. overnight, within- or between-subjects 未明确)；Memory Type (declarative vs. procedural)；SO-spindle coupling PLV (连续预测变量) |
| 因变量(DV) | Recall accuracy change (%); Correlation coefficients (r); PLV |
| Results 总体功能 | 从描述性睡眠参数 → 行为巩固效应 → 神经生理机制，逐步递进回答"睡眠如何巩固记忆" |

---

## Module B: Results Structure Map

### 3.1 Sleep architecture
- **回答的问题:** 两种睡眠条件的睡眠结构参数是否如预期？
- **对应图表:** 无（纯描述性段落）
- **主要结果:** 两种条件的总睡眠时间和睡眠阶段分布符合预期
- **作者想让读者得出的结论:** 睡眠条件操作有效，后续差异不是由意外睡眠结构差异造成的
- **接近 Discussion:** 早期（描述性铺垫）

### 3.2 Memory consolidation across conditions
- **回答的问题:** nap vs. overnight sleep 的巩固效果差异？是否有记忆类型特异性？
- **对应图表:** Figure 2A
- **主要结果:** overnight > nap，且两种记忆类型均如此；SWS 与陈述性记忆相关仅在 overnight 条件显著
- **作者想让读者得出的结论:** 睡眠时长重要，但记忆类型的交互不显著（暗示机制可能是通用的）
- **接近 Discussion:** 中期（主要行为结果）

### 3.3 Slow oscillation-spindle coupling
- **回答的问题:** 睡眠生理质量（而非数量）能否预测记忆巩固？
- **对应图表:** Figure 3A, 3B
- **主要结果:** SO-spindle coupling 显著预测陈述性记忆，控制 SWS 时长后仍然显著
- **作者想让读者得出的结论:** 神经振荡的时间耦合是比睡眠时长更核心的机制
- **接近 Discussion:** 晚期（机制层面，已开始暗示理论和临床意义）

---

## Module C: Sentence Function Annotation

### ¶1 (3.1 Sleep architecture)

> S1: As expected, total sleep time did not differ between the nap (M = 87.2 min, SD = 12.4) and overnight sleep conditions (M = 425.6 min, SD = 38.7).
- **Label 5:** Report specific result (with "As expected" carrying a faint Label 9 flavor, but the primary function is descriptive reporting of sleep times)

> S2: The nap condition contained an average of 21.3 min (SD = 8.1) of SWS and 18.7 min (SD = 6.4) of REM sleep.
- **Label 5:** Report specific result

> S3: In the overnight condition, participants obtained 89.4 min (SD = 22.1) of SWS and 102.3 min (SD = 28.6) of REM.
- **Label 5:** Report specific result

**段落功能总结:** 纯描述性段落，建立基线，没有统计检验。

### ¶2 (3.2 opening)

> S1: To assess whether sleep-dependent memory consolidation differed between the nap and overnight conditions, we examined change in recall accuracy from the immediate test to the delayed test.
- **Label 1:** Restate aim/question

> S2: Overall, both conditions showed significant memory retention above chance (all ps < .001), but the magnitude of consolidation differed markedly.
- **Label 3:** Overview result trend (前半句) + **Label 7:** Evaluative emphasis ("differed markedly")

> S3: As shown in Figure 2A, overnight sleep produced a substantially larger consolidation benefit (M = +18.3%, SD = 7.2) than the nap (M = +6.1%, SD = 5.8).
- **Label 4 + 5:** Invite to view figure + report specific result

> S4: A 2 (Condition) × 2 (Memory Type: declarative vs. procedural) mixed ANOVA confirmed a significant main effect of Condition, F(1, 34) = 14.62, p < .001, ηp² = .30, with overnight sleep outperforming the nap.
- **Label 6:** Report statistical evidence

> S5: The main effect of Memory Type was also significant, F(1, 34) = 5.41, p = .026, ηp² = .14, driven by greater consolidation of declarative than procedural memories.
- **Label 6:** Report statistical evidence

> S6: Importantly, the Condition × Memory Type interaction was not significant, F(1, 34) = 1.23, p = .275, suggesting that the advantage of overnight sleep was comparable across memory types.
- **Label 7 + 11:** Evaluative emphasis ("Importantly") + Note non-significant + **Label 10:** Explain/interpret (the "suggesting that..." clause)

> S7: Consistent with prior work (Diekelmann & Born, 2010), declarative memory consolidation was positively correlated with SWS duration in the overnight condition (r = .48, p = .003), but not in the nap condition (r = .19, p = .271).
- **Label 8:** Compare with prior work + **Label 6:** Report statistical evidence

> S8: This dissociation may reflect the greater absolute amount of SWS in the overnight condition, providing more opportunities for hippocampal-neocortical dialogue.
- **Label 10:** Explain/interpret result

### ¶3 (3.3 Slow oscillation-spindle coupling)

> S1: We next asked whether the quality of sleep physiology, beyond sleep duration, predicted memory outcomes.
- **Label 1:** Restate aim/question

> S2: Using automated detection algorithms, we identified discrete slow oscillations (0.5–1 Hz) and sleep spindles (12–16 Hz) during NREM sleep and quantified their temporal coupling (see Figure 3A for an example trace).
- **Label 2:** Restate key method + **Label 4:** Invite to view figure

> S3: Strikingly, the precision of SO-spindle coupling (measured as the phase-locking value, PLV) was a strong predictor of overnight declarative memory consolidation (r = .61, p < .001; Figure 3B), even after controlling for total SWS duration (partial r = .53, p = .001).
- **Label 7:** Evaluative emphasis ("Strikingly") + **Label 6:** Report statistical evidence + **Label 4:** Invite to view figure

> S4: This relationship was not observed for procedural memory (r = .12, p = .482), suggesting a degree of memory-type specificity.
- **Label 11:** Note non-significant/inconsistent + **Label 10:** Explain/interpret

> S5: We note that the sample size for this analysis was modest (N = 36), which may limit the generalizability of these correlational findings.
- **Label 12:** Acknowledge limitation

> S6: These results suggest that it is not merely the amount of sleep, but the precise temporal coordination of NREM oscillations, that drives memory consolidation — a point we develop further in the Discussion.
- **Label 13:** Hint at implication + **Label 14:** Transition to Discussion

---

## Module D: Figure/Table Guide

### Figure 2A

1. **Question answered:** Does overnight sleep produce greater memory consolidation than a nap? Is the benefit consistent across memory types?
2. **Axes/groups/colors/error bars (inferred from text):**
   - Y-axis: Change in recall accuracy (%)
   - X-axis: Two conditions (nap vs. overnight), with two bars per condition (declarative vs. procedural)
   - Error bars: ±1 SD (based on reported values)
   - Colors: （请提供图表截图，目前仅根据 caption 和正文推断）
3. **Author's reader guidance:** "As shown in Figure 2A, overnight sleep produced a substantially larger consolidation benefit..."
4. **Key pattern:** Overnight > nap for both memory types; magnitude of overnight advantage appears comparable across declarative and procedural memories (no significant interaction)
5. **Primary:** Main effect of Condition (overnight > nap); **Auxiliary:** Memory Type effect (declarative > procedural overall)
6. **PPT narration logic:**
   - Start: "这张图展示了 nap 和 overnight sleep 条件下记忆巩固的变化。"
   - Point to nap bars: "午睡组的变化约 6%。"
   - Point to overnight bars: "而整夜睡眠组的变化约为 18%，是午睡组的 3 倍。"
   - Note overlap: "注意两种记忆类型的模式相似——交互作用不显著——说明睡眠的巩固优势不特定于某一种记忆类型。"
   - Bridge: "接下来我们看是不是睡得越多效果越好..."
7. **1-minute narration script (Chinese):**
   > "这张图回答的核心问题是：睡得更久是不是记得更牢？横轴是两种睡眠条件——午睡大约 90 分钟，整夜睡眠大约 7 小时。纵轴是记忆准确率的变化百分比。深色是陈述性记忆，浅色是程序性记忆。最关键的信息在这里：整夜睡眠组的记忆提升大约是午睡组的 3 倍。而且这个优势在两种记忆类型中都出现了——交互作用不显著。这说明睡眠时长确实重要，但更好的问题是：睡眠里到底发生了什么在驱动这个效应？我们下一张图来回答。"

### Figure 3A / 3B

1. **Question answered:** Does the temporal coupling of slow oscillations and sleep spindles predict memory consolidation beyond sleep duration?
2. **Axes/groups:** Figure 3A: example EEG trace; Figure 3B: scatter plot with PLV on x-axis, declarative memory change on y-axis
3. **Author's reader guidance:** "Strikingly, the precision of SO-spindle coupling... was a strong predictor of overnight declarative memory consolidation (r = .61, p < .001; Figure 3B)"
4. **Key pattern:** Strong positive correlation (r = .61) between PLV and declarative memory; no correlation for procedural memory
5. **Primary:** SO-spindle coupling–declarative memory correlation; **Auxiliary:** null correlation with procedural memory
6. **PPT narration logic:**
   - Show example trace (3A) briefly: "这是慢振荡（慢波）和纺锤波耦合的一个示例片段。"
   - Transition to scatter plot (3B): "我们量化了每个人的耦合精度（横轴），然后看它能不能预测记忆巩固（纵轴）。"
   - Point to correlation line: "相关性 r = 0.61，即使在控制了总 SWS 时长后仍然显著——说明不是睡得久，而是睡得好。"
   - Note specificity: "而且这种关系只在陈述性记忆中出现，程序性记忆没有——存在记忆类型特异性。"
   - Caveat: "当然，N = 36，相关性的结论需要更大样本验证。"
7. **1-minute narration script (Chinese):**
   > "上一张图告诉我们睡得久似乎更好，但真正的问题是：睡眠质量。什么叫睡眠质量？我们关注的是慢振荡和睡眠纺锤波的时间耦合——可以理解为大脑在睡眠中'通信'的精准度。图 3A 是一个示例，红框标出了慢振荡和纺锤波紧密耦合的时刻。图 3B 是散点图：横轴是每个人的耦合精度，纵轴是记忆巩固效果。每个点是一个人。这条线的 r = 0.61，非常强。更重要的是，即使我们把每个人睡了多久纳入控制，这个相关仍然存在。而且你看程序性记忆——完全没有关系。所以结论是：不是 sleep quantity，而是 sleep quality——慢振荡和纺锤波耦合的精准度——在驱动记忆巩固。当然，由于样本量只有 36 人，这个发现需要在更大样本中重复。"

---

## Module E: Writing Strategy Extraction

| Strategy | Source excerpt | Transferable pattern |
|----------|---------------|---------------------|
| 结果开头方式 | "To assess whether sleep-dependent memory consolidation differed between the nap and overnight conditions, we examined..." | 用目的句开头重建研究问题，同时给出分析框架（compare X and Y on Z） |
| 图表引导句 | "As shown in Figure 2A, overnight sleep produced a substantially larger consolidation benefit (M = +18.3%, SD = 7.2) than the nap (M = +6.1%, SD = 5.8)." | "As shown in Figure X, [条件A] [方向] [条件B] (M = ..., SD = ...)" — 一句话包含图表指引 + 描述性统计 |
| 关键发现句 | "Strikingly, the precision of SO-spindle coupling... was a strong predictor of overnight declarative memory consolidation (r = .61, p < .001; Figure 3B), even after controlling for total SWS duration (partial r = .53, p = .001)." | Evaluative adverb + finding + statistics + robustness check (control analysis) |
| 不显著结果表达 | "Importantly, the Condition × Memory Type interaction was not significant, F(1, 34) = 1.23, p = .275, suggesting that the advantage of overnight sleep was comparable across memory types." | 不回避不显著交互，用 "importantly" 框定为有意义的信息（非失败），并提供 substantive interpretation |
| 对比既有研究表达 | "Consistent with prior work (Diekelmann & Born, 2010), declarative memory consolidation was positively correlated with SWS duration in the overnight condition (r = .48, p = .003), but not in the nap condition (r = .19, p = .271)." | "Consistent with [citation], [result X in condition Y], but not in [condition Z]" — 一边对齐文献，一边指出边界条件 |
| 限制表达 | "We note that the sample size for this analysis was modest (N = 36), which may limit the generalizability of these correlational findings." | "We note that [limitation], which may [specific consequence]" — 具体、诚实地承认 |
| 结果意义表达 | "These results suggest that it is not merely the amount of sleep, but the precise temporal coordination of NREM oscillations, that drives memory consolidation" | "These results suggest that it is not merely X, but Y, that drives Z" — 对比句式制造张力 |

### 可模仿的英文句型

1. "As shown in Figure X, [condition A] produced a substantially larger [DV] (M = ..., SD = ...) than [condition B] (M = ..., SD = ...)."
2. "Strikingly, [key predictor] was a strong predictor of [outcome] (r = .XX, p < .001), even after controlling for [covariate] (partial r = .XX, p = .00X)."
3. "This dissociation may reflect [mechanism], providing more opportunities for [process]."
4. "We note that [limitation], which may limit [specific aspect of interpretation]."
5. "Importantly, [non-significant result with stats], suggesting that [substantive interpretation of null]."

### 对应的中文学术表达

1. "如图 X 所示，[条件A] 在 [因变量] 上的表现显著优于 [条件B]。"
2. "值得注意的是，[关键预测因子] 即使在控制了 [协变量] 之后，仍然显著预测了 [结果]。"
3. "这一分离现象可能反映了 [机制]，为 [过程] 提供了更多机会。"
4. "需要指出，[限制条件] 可能限制了 [结论范围]。"
5. "重要的是，[不显著结果] 并不显著，说明 [对零结果的实质性解读]。"

---

## Module F: Critical Check

- [ ] **结果与讨论混杂:** ⚠️ 轻微。Section 3.3 的最后两句（"These results suggest that it is not merely the amount of sleep..."）已经进入了 Discussion 层面，但因为是最后一段且带有过渡功能，可接受。Section 3.2 的 "This dissociation may reflect the greater absolute amount of SWS..." 属于解释（Label 10），在 Results 中常见但不推荐过度展开。

- [ ] **过度解释:** ⚠️ "providing more opportunities for hippocampal-neocortical dialogue" — 这是机制性解释，但数据本身只是相关性证据（SWS 时长与记忆的相关）。作者用了 "may reflect" 做弱化，但 "providing more opportunities" 的措辞暗示了因果方向。

- [ ] **选择性强调:** ⚠️ Section 3.3 强调了 SO-spindle coupling 对陈述性记忆的预测（r = .61），但相对弱化了它对程序性记忆不显著的事实（仅一句话带过）。虽未隐藏，但篇幅分配确实不对称。

- [x] **统计结果报告不足:** Section 3.1 没有报告任何统计检验（仅报告了 M 和 SD）。不清楚作者是否只做了描述，还是遗漏了推断统计。

- [ ] **图表与正文对应不清:** Figure 2A 在正文中被描述为展示两种记忆类型 × 两种条件，但 caption 未在 Results 中完整给出，无法判断对应是否完整。

- [ ] **不显著结果被写得像显著:** 无明显风险。不显著的交互效应被如实报告，且给出了 p 值和 F 值。

- [ ] **因果表达过强:** ⚠️ "even after controlling for total SWS duration (partial r = .53, p = .001)" — 控制分析暗示 SO-spindle coupling "独立于" SWS 时长预测记忆，但仍属相关证据。作者措辞谨慎（"predictor" 而非 "cause"），但读者可能从中推断因果。

---

## Module G: Final Summary

### 1. 写作逻辑

这篇 Results 采用了经典的**递进式（ladder）结构**：从描述性基础（睡眠参数）→ 行为效应（记忆巩固差异）→ 机制解释（SO-spindle coupling）。每个小节都在回答一个越来越深入的问题，而不是平行罗列独立结果。Section 3.1 建立操作有效性，Section 3.2 展示主要行为发现（含不显著交互的诚实报告），Section 3.3 上升到神经生理机制并设置理论 hook 过渡到 Discussion。

### 2. 最值得模仿的 3 点

1. **不显著交互的正面呈现** — "Importantly, the interaction was not significant, suggesting that..." 将零结果框定为有意义的信息，而非失败。
2. **Strikingly + robustness check 的组合** — 评价性副词设定期望，控制分析增加说服力，最后用 "We note that" 诚实承认限制。
3. **Section 3.3 最后一句的"点题+过渡"双功能** — "These results suggest that... — a point we develop further in the Discussion." 同时提示意义和预告讨论，信息密度极高。

### 3. 最需要警惕的 3 点

1. **相关 ≠ 因果** — 即使做了 partial correlation，"predictor" 也不等于 "cause"。读的时候要提醒自己这一点。
2. **Section 3.1 缺统计检验** — 如果没有显著性检验，就无法判断 nap 和 overnight 的睡眠参数是否"没有差异"。
3. **记忆类型特异性的证据不对称** — SO-spindle coupling 对陈述性记忆的相关被详细展开，对程序性记忆的零相关仅一句话。是否有选择性报告的风险？

### 4. 对你自己写 Results 的启发

- 用递进式而非平行式组织：从基础条件 → 主要发现 → 机制/细化分析。
- 不显著的结果先报告统计量，再给实质性解读，用 "Importantly" / "Notably" 框定。
- 每个分析段落至少包含：目的句 + 图表引导 + 统计证据 + 一句话解释或限制。
- 最后一段同时完成 "提示意义" 和 "过渡到 Discussion" 两个功能，不要只收尾不铺垫。
