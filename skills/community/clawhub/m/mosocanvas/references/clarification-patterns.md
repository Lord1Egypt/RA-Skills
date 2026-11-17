# Clarification Patterns

Load this file only when missing information could change the selected visual strategy or cause a material error.

## Four gates

Check these gates without calculating a pseudo-precise ambiguity score:

1. `outcome_known`: What should the viewer know, feel, or do?
2. `context_known`: Who sees it, on which carrier, at what scale or duration?
3. `constraints_known`: What must appear, remain, or never appear?
4. `strategy_selectable`: Can at least one decisive visual mechanism be chosen?

Classify each unknown as `blocking`, `consequential`, or `optional`. Ask only blocking or consequential questions.

## Question rules

- Ask 0–3 questions in one round.
- Do not re-ask information available from the user, an attachment, brand rules, or verified carrier specifications.
- Offer 2–3 plain-language choices when the user lacks design vocabulary. Explain the visible consequence of each.
- If the user says “不确定”, recommend one reversible default with its reason and cost.
- Stop when remaining unknowns affect only low-cost execution details.
- Do not convert adjectives into templates: advanced ≠ black and gold; cinematic ≠ teal and orange; lonely ≠ blue rain.

## High-value transformations

| Vague phrase | Ask or distinguish | Do not assume |
|---|---|---|
| “高级” | value through order, craft, rarity, distance, or cultural specificity? | minimalism or black-gold |
| “电影感” | event tension, point of view, dramatic light, or frame rhythm? | letterbox and teal-orange |
| “孤独但温暖” | safe solitude or failed connection? | empty blue room |
| “年轻人喜欢” | which community, region, and action? | trend collage |
| “有冲击力” | scale, crop, semantic conflict, or motion? | saturation and large text |
| “简约但信息都要” | what must be read first, second, and only on closer view? | equal-size content |
| “参考这个风格” | which mechanisms: palette, texture, hierarchy, atmosphere, or medium? | copying subject and composition |
| “更专业” | technical repair, brand fit, or stylistic authority? | generic polish |

## When not to execute directly

Pause when:

- purpose or carrier is missing and plausible answers require opposite compositions;
- constraints are mutually exclusive;
- a requested edit lacks the source, target region, or authoritative logo/text asset;
- the user requests guaranteed identity or pixel preservation without a suitable tool;
- a cultural, legal, identity, or permissions issue requires authoritative confirmation.

## Compact question patterns

Use questions like:

- “缩成信息流缩略图时，第一眼必须读到品牌名，还是先被画面吸引？”
- “你要的神秘来自信息缺失、画外事件，还是人物拒绝表达？三者的构图不同。”
- “参考图里最不可替代的是印刷颗粒、蓝红光色，还是安静的日常叙事？”
- “如果文字必须一字不差，我建议把生图和排版拆开；你接受这种两阶段执行吗？”

## Record assumptions

When proceeding without an answer, write the assumption and its reversibility into the Visual Spec. Never hide an assumption inside a generation prompt.
