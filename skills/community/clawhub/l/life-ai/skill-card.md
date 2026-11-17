## Description:

Helps users record and review personal health, routines, time, synthetic financial data, and life decisions in local Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[threeparam](https://clawhub.ai/user/threeparam)

### License/Terms of Use:

MIT-0

## Use Case:

People who want to maintain personal health and life records use this skill to log daily habits, review trends, and compare major decisions against their own constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal health and financial records can be sensitive.

Mitigation: Keep the user-confirmed data directory private, follow the documented collection limits, and use synthetic financial amounts.

Risk: Nutrition estimates from photos can be imprecise when portions are unclear.

Mitigation: Label estimates by source and use ranges when portion sizes are uncertain.

Risk: The security scan reported no findings but had partial coverage because some referenced paths were absent from the bundle.

Mitigation: Review the complete referenced files before relying on the scan result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/threeparam/skills/life-ai)
- [Data schema and privacy boundaries](artifact/references/data-schema.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational text and Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates personal logs, reviews, and decision records from user-provided information.]

## Skill Version(s):

2.0.0 (source: frontmatter, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
