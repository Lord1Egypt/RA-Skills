## Description:

Recognizes food photos, logs daily calorie intake, and generates date-range calorie reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bobo23456](https://clawhub.ai/user/bobo23456)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to estimate calories from meal photos, log daily intake, and review lunch, dinner, and snack calories across a requested date range.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private meal records and temporary food images may be stored in shared workspace locations.

Mitigation: Store records and temporary images in a skill-private directory with clear retention and deletion practices.

Risk: Raw meal images may remain after calorie logging.

Mitigation: Delete raw images after processing unless the user explicitly asks to retain them.

Risk: Report generation can read loosely scoped workspace files.

Mitigation: Validate report date and range arguments, and restrict reads to expected skill-owned record paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bobo23456/skills/photo-calorie-tracker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-style calorie tracking report with kcal values, target comparison, and incomplete-day status labels.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a daily calorie target of 2100 kcal unless configuration changes; breakfast is excluded from calculations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
