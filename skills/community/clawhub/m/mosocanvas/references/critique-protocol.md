# Critique Protocol

Load this file when judging a visual idea, reference strategy, existing output, or proposed repair.

## Judge a named target

Name the exact object or decision: headline hierarchy, crop, brand promise, portrait skin, logo placement, reference use, output size, or preservation claim. Do not evaluate “the whole design” when the failure is local.

## Judgment types

| Type | Use when | Evidence threshold |
|---|---|---|
| `technical` | corruption, malformed text, export, anatomy, clipping, resolution | observable or tool-measured |
| `functional` | primary message, readability, carrier fit, viewing distance | observable plus task context |
| `intent_mismatch` | output contradicts confirmed brief or Visual Spec | direct spec reference |
| `contextual_cliche` | familiar mechanisms replace the specific proposition | name repeated mechanisms and their consequence |
| `preference` | reasonable viewers may disagree without task failure | label as subjective |
| `intentional_rule_break` | user knowingly chooses roughness, density, discomfort, or unreadability | judge control and consistency, not rule compliance |
| `unknown` | evidence or context is insufficient | ask or lower confidence |

Never merge these types into an aesthetic total score.

## Severity

- `0 pass`: Explain the mechanism that works and its most fragile point. Do not give empty praise.
- `1 risk`: The consequence is plausible but context-dependent. Give a way to test it.
- `2 conflict`: Evidence shows material damage to purpose, hierarchy, carrier, or confirmed intent. Require a repair or accepted tradeoff.
- `3 blocker`: Missing asset, impossible constraint, safety or permission issue, or mutually exclusive requirements. Taste disagreement cannot be severity 3.

## Evidence sequence

Write each material critique in this order:

1. `observed`: visible fact or supplied constraint without interpretation.
2. `claim`: falsifiable interpretation tied to a judgment type.
3. `consequence`: likely effect on purpose, audience, carrier, or execution.
4. `confidence`: low, medium, or high.
5. `alternative_explanations`: at least one plausible alternative for severity 2+.
6. `repairs`: conservative and authored; experimental only when useful.
7. `preserve`: what already works and must survive repair.

Use the structured contract in `../schemas/critique.schema.json` when another tool or evaluation consumes the result.

## Rebuild after rejection

For every severity 2 or 3 judgment:

- **Conservative repair:** change the smallest mechanism that can restore function.
- **Authored direction:** offer a stronger reinterpretation of the proposition, not more decoration.
- **Experimental direction:** include only when the user accepts a higher failure risk.

If the whole direction fails, explain why local polishing will not fix it.

## User override

For severity 2+, explain the tradeoff once. If the user insists, record:

```yaml
user_override: user_insisted
known_tradeoff: <specific consequence>
preserve_intent: true
```

Judge later work against that decision. Do not quietly revert it or raise the same taste objection again unless new technical or safety evidence appears.

## Language boundaries

Do not say:

- “你没审美”, “土”, “廉价的人才会喜欢”, or any attack on identity or competence.
- “高级”, “电影感”, “年轻人喜欢”, “色彩心理证明” without a defined mechanism and context.
- “完全保持”, “像素未变”, or “已经修复” without verification.

Prefer:

- “这个方向目前不成立，因为……”
- “粗糙不是问题；当前失效的是……”
- “这是风格分歧，不是功能错误。”
- “我看到的是……；这可能导致……；另一种解释是……”

## Recognize successful work

Do not oppose for performance. State precisely:

- which purpose the mechanism serves;
- why it fits the carrier and viewing condition;
- what remains fragile;
- what should not be added or regenerated.
