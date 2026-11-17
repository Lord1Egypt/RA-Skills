## Description:

Same skill compression power in half the context: 975 tokens vs 2,500.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leegitw](https://clawhub.ai/user/leegitw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent maintainers use this skill to compress verbose agent skill files while preserving key triggers, constraints, and trade-off reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create or update a local calibration history file under .learnings/skill-distiller/.

Mitigation: Review or delete the calibration file if local history retention is not desired.

Risk: Private skill text may be processed by the agent's configured model or provider.

Mitigation: Confirm the configured model and provider before processing private or sensitive skill content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leegitw/skills/neon-skill-distiller-compressed)
- [Project homepage](https://github.com/live-neon/skills/tree/main/skill-distiller/compressed)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with compression metrics, removed and kept section summaries, and compressed skill content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append local calibration metrics under .learnings/skill-distiller/calibration.jsonl.]

## Skill Version(s):

0.2.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
