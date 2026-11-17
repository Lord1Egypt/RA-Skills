## Description:

Tracks data provenance and lineage by tracing sources, logging transformations, and auditing anchors to support data auditability and compliance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kleberbaum](https://clawhub.ai/user/kleberbaum)

### License/Terms of Use:

MIT

## Use Case:

Developers and data engineers use this skill to introduce provenance and lineage checks into data pipelines, including trace, audit, and version commands for Origin namespace workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The current release may be mistaken for a complete provenance analysis system.

Mitigation: Treat trace and audit output as basic placeholder signals until the skill integrates with real provenance backends.

Risk: Local shell scripts may require permission or line-ending cleanup before execution.

Mitigation: Review scripts manually, set execute permissions if needed, and run them in an appropriate local environment.

## Reference(s):

- [Origin ClawHub skill page](https://clawhub.ai/kleberbaum/skills/origin)
- [Netsnek website](https://netsnek.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and plain-text script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The current release provides placeholder trace and audit behavior through local shell scripts.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter, claw.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
