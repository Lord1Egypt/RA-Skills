## Description:

OrgX operations execution contract for OpenClaw. Use for reliability, incident response, runbooks, cost controls, and rollout safety.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hopeatina](https://clawhub.ai/user/hopeatina)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to guide reliability work, incident response, runbooks, cost controls, rollout safety, and production change planning in OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide production changesets when mutation tools are exposed.

Mitigation: Use scoped tool access, approval gates, rollback plans, and verification checklists before applying production changes.

Risk: Operational guidance may be incomplete without the target environment's current reliability, incident, or rollout context.

Mitigation: Review proposed runbooks and mitigations against live service context before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with operational guidance, runbook steps, checklists, and proposed commands or configuration when appropriate.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use OrgX operations tools for activity reporting, human decisions, and changesets when those tools are available in scope.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
