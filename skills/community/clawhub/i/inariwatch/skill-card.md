## Description:

AI monitoring that fixes your code - query alerts, trigger remediations, rollback deploys, chat with your infrastructure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orbita-pos](https://clawhub.ai/user/orbita-pos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to monitor production projects, investigate alerts and deployment failures, and request remediations through InariWatch. It supports status queries, root-cause analysis, PR risk assessment, rollbacks, uptime monitoring, codebase search, and post-incident review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The InariWatch token may grant access to production monitoring, deployment, and remediation actions.

Mitigation: Use the least-privileged token available, keep it scoped to the intended projects, and review the installed MCP package version before use.

Risk: Remediation, rollback, reindexing, and alert-state actions can change live deployments, code, or operations state.

Mitigation: Require explicit human confirmation before every high-impact action and verify results after execution.

Risk: AI-generated fixes or operational analysis may be incomplete or incorrect for a specific incident.

Mitigation: Review proposed changes, CI results, security scan output, and remediation status before relying on the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/orbita-pos/skills/inariwatch)
- [InariWatch homepage](https://inariwatch.com)
- [InariWatch app](https://app.inariwatch.com)

## Skill Output:

**Output Type(s):** [guidance, analysis, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use InariWatch MCP tools after the user provides an INARIWATCH_TOKEN; high-impact actions require explicit confirmation.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
