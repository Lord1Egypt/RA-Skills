## Description:

Tracks per-agent token usage and flags waste in parallel dispatch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent orchestrators use this skill after parallel agent runs to review token expenditure, duplication, and coordination overhead. It helps identify waste signals and produce a recommendation about future agent counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Waste estimates and dispatch recommendations depend on having token, findings, and file-access data for comparison; incomplete records can skew the assessment.

Mitigation: Check which evidence is available and identify unmeasured signals before changing future dispatch sizes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-conserve-agent-expenditure)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown review with per-agent checklist findings and a dispatch recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Post-dispatch assessment based on token use, findings, file access, and coordination evidence.]

## Skill Version(s):

1.10.3 (source: server-resolved release, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
