## Description:

Searches and compares flights across multiple airlines for best deals, with supporting travel booking workflows powered by Fliggy (Alibaba Group).

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiejinsong](https://clawhub.ai/user/xiejinsong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to collect route parameters, run FlyAI flight searches, compare carrier options by recommendation, price, speed, or directness, and present bookable results in Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install an unpinned global npm CLI before use.

Mitigation: Review before installing, obtain explicit consent, and prefer a pinned or local FlyAI CLI installation.

Risk: Unsafe shell-style command templates could mishandle user-supplied travel parameters.

Mitigation: Pass origin, destination, dates, and sort options as safe process arguments rather than pasted shell strings.

Risk: Route and date queries are sent to FlyAI/Fliggy and returned options are constrained to that provider's booking links.

Mitigation: Tell users that search data is processed by FlyAI/Fliggy and that booking availability is provider-scoped.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiejinsong/skills/multi-airline-compare)
- [Parameter Collection & Output Templates](references/templates.md)
- [Scenario Playbooks](references/playbooks.md)
- [Failure Recovery](references/fallbacks.md)
- [Execution Runbook](references/runbook.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flight results must come from FlyAI CLI output and include booking links when available.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
