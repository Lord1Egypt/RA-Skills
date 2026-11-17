## Description:

Detect AWS idle and zombie resources consuming cost with zero meaningful utilization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

Developers, cloud engineers, and FinOps teams use this skill to identify idle AWS resources, estimate waste, prioritize cleanup, and generate reviewable AWS CLI cleanup runbooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill inspects AWS resource metadata for cost analysis.

Mitigation: Run it only in authorized AWS account contexts and start with read-only AWS permissions where possible.

Risk: The skill can generate AWS CLI cleanup or deletion commands.

Mitigation: Treat generated commands as review material and require human confirmation before execution.

Risk: Critical resources could be misclassified as idle.

Mitigation: Manually review resources flagged by names such as prod, production, or critical before cleanup.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anmolnagpal/skills/idle-resource-detector)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with waste summaries, resource tables, cleanup priorities, checklists, and inline AWS CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes estimated monthly waste, estimated annual savings, and confirmation flags for resources that require manual review.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
