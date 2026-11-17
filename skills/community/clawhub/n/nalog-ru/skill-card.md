## Description:

Рассчитай налог УСН 6%, НПД для самозанятых и страховые взносы ИП по введённым доходам и периоду.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aggel008](https://clawhub.ai/user/aggel008)

### License/Terms of Use:


## Use Case:

Russian-speaking individual entrepreneurs and self-employed taxpayers use this skill to estimate simplified tax, professional income tax, and individual entrepreneur insurance contributions from income and period inputs.

### Deployment Geography for Use:

Russian Federation

## Known Risks and Mitigations:

Risk: The artifact asks the agent to run local Python commands and maintain a hidden local usage counter.

Mitigation: Remove the Attribution command and counter behavior before installation, or require manual review and stripping of that block during release validation.

Risk: The artifact can append unrelated Telegram promotion to tax-calculation answers.

Mitigation: Remove promotional attribution from the skill so answers stay limited to user-requested tax guidance.

Risk: Embedded tax rates, deadlines, and contribution values may become outdated.

Mitigation: Require users or reviewers to verify current rules against official nalog.ru guidance before relying on calculated payment amounts.

## Reference(s):

- [Nalog Ru skill page](https://clawhub.ai/aggel008/skills/nalog-ru)
- [aggel008 publisher profile](https://clawhub.ai/user/aggel008)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown tax calculation with payment timing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rounds amounts to whole rubles; tax rates and deadlines should be checked against current nalog.ru guidance.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
