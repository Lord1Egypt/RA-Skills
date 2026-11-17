## Description:

Meta Industry Chain Analysis helps an agent conduct industry-chain and sector research by decomposing supply chains, identifying supply-side bottlenecks, checking conclusions against evidence, red-teaming weak claims, and tracking reversals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and research agents use this skill to produce traceable industry-chain research, locate constrained supply-chain segments, and avoid unsupported stock recommendations or price targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The learner can persist user preferences, notes, and usage history in learned_patterns.json.

Mitigation: Avoid recording sensitive business details, inspect or clear learned_patterns.json periodically, and deploy only where local state retention is acceptable.

Risk: The learner accepts a skill directory path and writes learning state there without documented path limits.

Mitigation: Run it only with an intended skill directory and prefer a dedicated, reviewable state path with documented deletion and retention behavior.

Risk: The skill supports financial and industry research workflows that could be mistaken for trading advice.

Mitigation: Keep outputs limited to research leads and evidence-backed analysis; do not provide buy, sell, price target, or position-sizing recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/meta-industry-chain-analysis)
- [Distillation report](artifact/distillation_report.md)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance, configuration]

**Output Format:** [Markdown analysis with evidence notes and optional JSON learning-state updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local learned_patterns.json state to record capability usage, preferences, errors, and reflection notes.]

## Skill Version(s):

1.0.0 (source: evidence release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
