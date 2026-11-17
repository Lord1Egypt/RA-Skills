## Description:

Generate monthly ledger statistics in CNY with amount and ratio by tag/category, top expense breakdown, and labeled charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shing19](https://clawhub.ai/user/shing19)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance-focused agents use this skill to generate monthly CNY ledger summaries with category ratios, top expense breakdowns, and chart files from local ledger data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default reporting month is based on Asia/Taipei time, which can be incorrect for ledgers maintained in another timezone or near month boundaries.

Mitigation: Confirm the intended reporting month explicitly before running the report when timezone alignment matters.

Risk: The skill reads local ledger data and writes summary and chart files under project report paths.

Mitigation: Run it only in the intended workspace and review generated files before sharing or deleting them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shing19/skills/ledger-monthly-report)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files]

**Output Format:** [Markdown summary with generated JSON and PNG chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses CNY amounts, month selection, local ledger data, and optional chart cleanup.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
