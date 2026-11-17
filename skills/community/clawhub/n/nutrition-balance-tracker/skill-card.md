## Description:

Tracks daily nutrition intake, hydration, and energy balance against fat-loss, maintenance, or muscle-gain goals using local estimation helpers and practical non-medical guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to log meals, hydration, and exercise and receive an estimated daily nutrition balance report for fat loss, maintenance, or muscle gain. It is intended for everyday wellness tracking, not medical diagnosis or clinical nutrition planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Nutrition outputs may be mistaken for precise medical or clinical diet advice.

Mitigation: Present results as rough wellness estimates, keep advice non-clinical, and recommend professional support for medical conditions, pregnancy, eating-disorder concerns, or extreme goals.

Risk: Food logs, body metrics, hydration entries, and exercise entries can be incomplete, sensitive, or uncertain.

Mitigation: Ask only for the minimum information needed, label low-confidence calculations, and make clear that accuracy depends on user-provided inputs.

Risk: The default user-facing report is Chinese-language, which may not fit all release contexts.

Mitigation: Use this release only where Chinese-language nutrition reports are acceptable, or localize the output before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/nutrition-balance-tracker)
- [Nutrition Targets Reference](references/nutrition-targets.md)
- [Safety Boundaries](references/safety-boundaries.md)
- [Intents and Prompts](references/intents-and-prompts.md)
- [Output Template](references/output-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown nutrition report with estimated totals, balance status labels, issues, suggestions, and a disclaimer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language report output; estimates depend on user-provided food, profile, hydration, and exercise logs.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
