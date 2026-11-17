## Description:

Guides agents in designing and reviewing inspectable Yes/No, Choice, or Score decisions, with evaluation and human review for consequential uses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gpt-img-2](https://clawhub.ai/user/gpt-img-2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to define typed text-decision criteria, prepare representative evaluations, review results, and plan human escalation for consequential decisions. An optional MCP can help check decision specifications, batches, and result completeness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional MCP setup runs mutable remote code through an unpinned GitHub npx command.

Mitigation: Review the MCP repository before enabling it and pin a reviewed commit or release.

Risk: Incorrect or overconfident decisions could affect consequential outcomes.

Mitigation: Evaluate representative cases and require human review for high-risk decisions; do not treat uncalibrated probabilities as authorization.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/gpt-img-2/skills/jev-ai-decision-workflow)
- [Jev AI overview](https://ai-jev.pro/what-is-jev)
- [Jev API](https://ai-jev.pro/jev-api)
- [Batch processing](https://ai-jev.pro/batch)
- [Optional MCP source](https://github.com/gpt-img-2/jev-ai-decision-workflow-mcp)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration instructions, Shell commands]

**Output Format:** [Markdown with structured decision fields and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes decision criteria, test-set and metric plans, escalation rules, known limits, and next verification steps.]

## Skill Version(s):

1.0.0 (source: ClawHub release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
