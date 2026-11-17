## Description:

GSwitch coordinates a seven-role OpenClaw engineering workflow for problem framing, planning, implementation, review, testing, release, and retrospective documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[garysze77](https://clawhub.ai/user/garysze77)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate specialized agents across product strategy, architecture, design, code review, QA, security, deployment, and shared-memory handoff. It is intended for OpenClaw workflows where work should pass through explicit review and testing gates before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Release guidance can lead agents toward production deployment.

Mitigation: Require fresh user approval before any production action and use scoped deployment credentials that can be revoked.

Risk: Recommended spawning and timeout settings allow broad or long-running agent activity.

Mitigation: Set finite timeouts and conservative spawn, child, and concurrency budgets before enabling the workflow.

Risk: Shared-memory logs may retain sensitive project details.

Mitigation: Disable shared-memory logging for sensitive projects or apply redaction, access controls, and retention limits.

## Reference(s):

- [GSwitch ClawHub skill page](https://clawhub.ai/garysze77/skills/gswitch)
- [garysze77 ClawHub publisher profile](https://clawhub.ai/user/garysze77)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, role handoff notes, configuration JSON, code changes, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses shared append-only daily memory logs and role-specific agent handoffs.]

## Skill Version(s):

1.0.1 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
