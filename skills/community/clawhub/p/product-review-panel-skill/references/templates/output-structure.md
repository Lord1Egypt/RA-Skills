# Output Structure / 评审输出结构

The full output skeleton of a panel review. Steps 0-8 produce sections in this exact order.

## Complete output skeleton (Chinese)

```
[Section 0: Disclaimer block from references/templates/disclaimer.md]

[Section 1: P9 intake dialogue — only if intake occurs; format from intake-dialogue.md]

[Section 2: Internal — PRD classification done, NOT printed]

[Section 3: Panel intro card from references/templates/panel-intro-card.md]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 第 1 轮：平行评审
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【专家姓名 1】 倾向 [GO / NO-GO / CONDITIONAL]

[≤ 80 字的评审意见，使用专家自己的框架和语气]

📍 追问：[他想问 PM 的一个具体问题]

───

【专家姓名 2】 倾向 ...

[同上]

───

[... 其余专家 ...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚔️ 第 2 轮：对线（如适用）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

(只有当 GO 和 NO-GO 同时出现时显示，否则跳过此 section)

【GO 派代表 → NO-GO 派代表】

[GO 派的最强反驳，≤ 100 字]

【NO-GO 派回应】

[NO-GO 派的最强回应，≤ 100 字]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[Section 7: The Closer 终审块 from references/personas/closer.md]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 反对意见 / Dissent
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

由 [反对方专家姓名] 提出：

最强论点：
  "[反对方 Round 1 或 Round 2 中的原话或近似原话]"

未来翻车前兆信号（如出现，应回到反对方立场）：
  1. [可观测信号 1，含时间窗口和阈值]
  2. [可观测信号 2，含时间窗口和阈值]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
建议下一步
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

立即可做：
  • [具体动作 1]
  • [具体动作 2]
  • [具体动作 3]

需要补充的关键证据：
  • [P9 跳过项 1]
  • [P9 跳过项 2]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Complete output skeleton (English)

Mirrors the Chinese structure with these English section headers:

```
📋 Round 1: Parallel Reviews
⚔️ Round 2: Debate (if triggered)
[The Closer · Final Verdict]
⚠️ Dissent
Next Steps
```

Within each section, use English equivalents of all labels (e.g. "倾向" → "Tendency", "追问" → "Follow-up").

## Section length budgets

| Section | Lines |
|---|---|
| 0 — Disclaimer | 4-6 |
| 1 — Intake | 0 to ~15 (0 if PRD solid; ~15 for full 5-round intake) |
| 3 — Panel intro card | ~25 (depends on panel size) |
| 4 — Round 1 | ~10 per expert × N |
| 6 — Round 2 | ~12 total (only if triggered) |
| 7 — The Closer | ~20 |
| 8 — Dissent | ~10 |
| 9 — Next Steps | ~10 |

**Total target**: 100-180 lines for a full review. If exceeding 200, tighten Round 1 word budgets.

## Visual rules

- `━` (heavy) — between major sections (looks like a meeting agenda divider)
- `───` (lighter) — between experts within Round 1
- `▸` — for expert names in the panel intro card
- `📋 ⚔️ ⚠️ 🎤` — for flagging major sections; do **not** use other emoji elsewhere
- **Bold** sparingly: only for the verdict word and expert names; everything else stays unbolded
- Code-block-style box around The Closer verdict block (use the `━` framing)

## Dissent section rules

**The Dissent section is always included**, even when all experts agreed on the verdict. In that case:

- If one expert raised any concern in Round 1 (even while voting GO), surface it here
- If literally nobody had any concern, write: `本次评审无显著反对意见。但请仍按 The Closer 给出的翻车前兆信号监控上线后表现。`

A unanimous panel with zero dissent is rare and itself a signal — The Closer should have flagged it at Step 7.

## What NOT to put in the output

- Numeric scores (e.g., "Cagan: 3.5/5"). Tendency labels only.
- Em-dashes in expert names (use full names)
- Time stamps, dates
- The skill's own meta-commentary ("Now I'm going to run Round 2...")
- Apologies or hedges from the skill itself ("This is just one perspective...")
