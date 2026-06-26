# Test Case 4: Figure Screenshot + Caption + Body Text

## Scenario
User uploads a bar chart screenshot showing a 2×2 interaction (sleep vs. wake × pre vs. post), plus caption and body text.

## Input

```
[上传图表截图 — bar chart with 4 bars:
  X-axis: Pre-test, Post-test
  Two bar groups per timepoint: Sleep (blue) and Wake (orange)
  Y-axis: Recall Accuracy (%)
  Error bars visible (SEM lines)
  Visual pattern: both groups similar at Pre-test (~45%),
  Sleep bar rises to ~72% at Post-test, Wake bar rises to ~51%]

Figure caption:
Figure 1. Mean recall accuracy (±SEM) at pre-test and post-test for the sleep (blue) and wake (orange) conditions. **p < .01, ***p < .001.

Body text:
As shown in Figure 1, both groups performed similarly at pre-test, but diverged significantly at post-test. A 2 (Condition: sleep vs. wake) × 2 (Time: pre vs. post) mixed ANOVA confirmed a significant interaction, F(1, 38) = 12.47, p < .001, ηp² = .25. Follow-up t-tests revealed a significant increase from pre- to post-test in the sleep group, t(19) = 6.83, p < .001, d = 1.53, whereas the wake group showed only a marginal improvement, t(19) = 2.01, p = .058, d = 0.45.
```

## Expected Agent Behavior

### Step 1: Use image tool to analyze the figure screenshot
Agent should call the `image` tool with a prompt like:
"Analyze this bar chart from a psychology paper. Extract: (1) X-axis labels and meaning, (2) Y-axis label and units, (3) bar groupings and colors, (4) error bar type if discernible, (5) which bars differ visually, (6) any statistical annotations visible on the chart."

### Step 2: Cross-reference in Module D

Expected output markers:

**Module D, Item 2 (Axes/groups/colors/error bars):**
- Y-axis: Recall Accuracy (%) `[图片识别]`
- X-axis: Pre-test, Post-test `[图片识别]`
- Bars: Blue = Sleep, Orange = Wake `[图片识别 + caption]`
- Error bars: SEM `[caption]`
- Significance stars: ** and *** annotated on chart `[图片识别]`

**Module D, Item 4 (Key pattern):**
"视觉上，两组在 Pre-test 基本相等（~45%），Post-test 时 Sleep 组上升到 ~72% 而 Wake 组仅 ~51%。时间×条件的交互模式在视觉上表现为显著的 'fan-spread'。"

**Module D, Item 7 (1-minute narration):**
> "这张图展示了本实验最核心的发现：睡眠是否增强了记忆保持？横轴是测试时间——训练后立即测和间隔后延时测。纵轴是回忆准确率。蓝色是睡眠组，橙色是清醒组。看左边——训练后立即测，两组基本一样，都在 45% 左右。但看右边——延时测时，睡眠组的准确率跳到了 72%，而清醒组只到了 51%。这个差距在统计上是一个显著的交互效应，F = 12.47，p < .001，效应量 ηp² = .25。所以结论很清楚：睡眠并没有让你学得更好，但它阻止了你遗忘。"

### Step 3: Module F cross-check
- [ ] 图表与正文对应不清: Check: do the "~45% / ~72% / ~51%" values from vision match the body text? The body text didn't report these specific means — it skipped to ANOVA. The reader must infer values from the chart. This is a **minor gap** — the body should state the descriptive statistics explicitly.
- [ ] 选择性强调: The body calls wake improvement "marginal" (p = .058). Is this framing consistent with what the figure shows visually? The wake bar does go up slightly — the word "marginal" is an evaluative choice.

### Step 4: Source tagging
Throughout Module D, agent must mark each piece of information's source:
- `[图片识别]` — read from screenshot
- `[caption]` — from figure caption
- `[正文]` — from body text paragraph
- `[无法确定]` — when neither source resolves the detail
