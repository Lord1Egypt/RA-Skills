# Paper Highlight Rules

Use this reference to keep annotations stable across papers.

## Core Principle

Highlight reusable information, not transient importance. A sentence deserves color only if it is likely to help with later paper writing, review, comparison, rebuttal, implementation planning, or fast re-reading.

## Reusable Sentence Tests

Mark a sentence when at least one of these is true:

- It states the paper's task, input-output setup, or optimization target.
- It explains why existing work is insufficient.
- It summarizes the proposed method or a key module.
- It states a contribution or novelty claim that can be compared with prior work.
- It records a main empirical takeaway or final conclusion.
- It defines a notation, assumption, or protocol that later claims depend on.
- It states a limitation, failure mode, or future direction worth revisiting.

Do not mark a sentence when most of its value is local to the current read:

- Transition sentence
- Generic background claim
- Pure literature scene-setting
- Formula-adjacent detail with no reusable interpretation
- Implementation trivia
- Numeric detail without a durable takeaway

## Color Legend

### Required

- Yellow: goal, task, problem definition
- Orange: motivation, gap, challenge, prior limitation
- Blue: proposed method, architecture, training or inference mechanism
- Pink: contribution list, novelty statement, explicit difference from prior work
- Green: main result, ablation takeaway, conclusion

### Optional

- Purple: assumptions, definitions, notation, protocol, setup constraints
- Gray: limitations, failure cases, caveats, future work

## Section Bias

Use section-aware priorities to stay sparse:

- Abstract: yellow, orange, blue, green, pink
- Introduction: orange first, then yellow, pink, blue
- Related work: orange and pink only when the sentence is clearly reusable
- Method: blue first, then purple, then pink
- Experiments: green first, then gray; use blue only for method-specific evaluation mechanics
- Conclusion: green and gray

## Density Guardrails

- Default to 4-7 highlights per page.
- Target about 40-55 highlights for a longer paper, then trim obvious noise if needed.
- When a page already has 7 highlights, require a strong reason to add another one.
- If several adjacent sentences make the same point, mark only the best summary sentence.

## Highlight Levels

- `low`: fixed baseline
- `medium`: aim for about `1.25x` the `low` count
- `high`: aim for about `1.5x` the `low` count
- `exteme`: allow up to about `2x` the `low` count when the paper provides enough reusable sentences

## Note Modes

- `default`: a title `TLDR` paragraph + concise section `flow` summaries
- `full`: denser version of `default`
- `flow`: a title `TLDR` paragraph + concise section `flow` summaries
- `hightlight`: deprecated compatibility alias; currently behaves like `none`
- `none`: no note annotations

## Opacity

- `light`: default; use pastel colors at `0.5` opacity for most PDFs
- `dark`: use only when the PDF is visually faint and light marks disappear

## Review Checklist

Before finishing, ask:

- Can the color alone tell me what type of information this is?
- Could I still understand the highlight without rereading the whole paragraph?
- Would I want this sentence one week later?
- Did I keep the page readable?
