## Description:

LeClaw is a hierarchical agent collaboration framework for OpenClaw that provides task management and collaboration capabilities. Use when creating Issues, managing Approvals, tracking Goals, organizing Projects, or managing hierarchical agents (CEO/Manager/Staff).

This skill is ready for commercial/non-commercial use.

## Publisher:

[saullockyip](https://clawhub.ai/user/saullockyip)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use LeClaw to coordinate hierarchical OpenClaw teams through CLI-managed issues, approvals, goals, projects, activity logging, heartbeat checks, and onboarding workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may store API keys in plaintext as part of onboarding.

Mitigation: Store API keys in a real secret store instead of TOOLS.md and pass them only to authorized leclaw CLI commands.

Risk: Activity logs may persist private reasoning or secrets and can be read by other agents.

Mitigation: Keep secrets and sensitive reasoning out of activity.log, and limit log access to agents with a valid need.

Risk: Heartbeat workflows can create autonomous task polling and execution behavior.

Mitigation: Disable heartbeat task creation by default or gate it with explicit authorization and quiet-hour controls.

Risk: The --refresh workflow can read cross-agent local OpenClaw state.

Mitigation: Require explicit authorization before using --refresh and review which local state files are accessible.

## Reference(s):

- [LeClaw on ClawHub](https://clawhub.ai/saullockyip/skills/leclaw)
- [LeChat](https://clawhub.ai/saullockyip/lechat)
- [HEARTBEATS Templates](HEARTBEATS_Templates.md)
- [LeClaw Hiring Guide](hiring/hiring.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, tables, checklists, and workflow templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance assumes access to OpenClaw, LeChat, and the leclaw CLI with per-agent API keys.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
