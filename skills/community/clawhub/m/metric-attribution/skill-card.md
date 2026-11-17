## Description:

This skill guides agents through metric fluctuation attribution by querying Aloudata CAN Gateway metrics, decomposing contributing factors and dimensions, checking external events, and producing a concise diagnostic report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackyujun](https://clawhub.ai/user/jackyujun)

### License/Terms of Use:

MIT-0

## Use Case:

Business analysts, operators, and data-oriented agents use this skill to investigate why a metric rose or fell, quantify factor and dimension contributions, and summarize likely causes with supporting data and external-event context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Business metric names, dimensions, regions, platforms, or time windows may be exposed through Gateway API calls or external-event search.

Mitigation: Review the skill before installation, limit use to non-confidential business context unless approved, and require confirmation before sending sensitive metric context to search providers.

## Reference(s):

- [Aloudata homepage](https://aloudata.com/)
- [ClawHub skill page](https://clawhub.ai/jackyujun/skills/metric-attribution)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with API request examples, JSON query bodies, optional Python chart code, and concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CAN_API_KEY for Gateway API access; may include waterfall chart generation instructions when factor decomposition applies.]

## Skill Version(s):

1.0.4 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
