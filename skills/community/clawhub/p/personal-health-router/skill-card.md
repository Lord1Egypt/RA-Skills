## Description:

Track meals, sleep quality, and workouts with automated Feishu persistence and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neverwarm](https://clawhub.ai/user/neverwarm)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and agents use this skill to extract nutrition, sleep, and exercise signals from photos, screenshots, and summaries, then log them to Feishu and rebuild weekly or monthly health reports. It supports personal tracking and operational reporting, not medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes sensitive health records to Feishu, a third-party store.

Mitigation: Use a least-privilege Feishu identity, keep configuration files private, and avoid this skill when local-only storage or strict consent and retention controls are required.

Risk: Backfill and rebuild commands can update many health summary records.

Mitigation: Use available dry-run options first and review every write or backfill command before execution.

Risk: Nutrition estimates and wearable-derived sleep or recovery metrics may be imprecise.

Mitigation: Extract only visible data, state uncertainty, and keep practical suggestions separate from medical diagnosis.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/neverwarm/skills/personal-health-router)
- [Config Template](references/config-template.md)
- [Cross-Domain Branch](references/cross-domain.md)
- [Public Data Model](references/data-model.md)
- [Exercise Branch](references/exercise.md)
- [Nutrition Branch](references/nutrition.md)
- [Sleep Branch](references/sleep.md)
- [Weekly Health Review](references/weekly-review.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and optional JSON output from maintenance scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configurable Feishu table schemas and thresholds; outputs should separate observed evidence, uncertainty, and suggested next steps.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
