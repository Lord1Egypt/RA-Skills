## Description:

Find signal-based prospects, verify work emails, send personalized daily emails from your mailbox, and manage replies and opt-outs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otto-iron](https://clawhub.ai/user/otto-iron)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams and founders use this skill to run a small, signal-based outreach campaign from their own mailbox, review drafts, and handle replies and opt-outs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on an external service for mailbox access and scheduling, and its setup and implementation are unverified.

Mitigation: Use a dedicated mailbox, review Nodo's permissions and credential handling, confirm how to stop scheduled work and revoke access, and store mailbox credentials only as a Nodo secret.

Risk: Automated outreach or reply handling could send unsuitable messages or exceed the user's intended volume.

Mitigation: Agree on the target and approved reply facts, review drafts before scheduling, set a firm low daily cap, include an opt-out, and honor opt-outs permanently.

## Reference(s):

- [Cold Email Autopilot on ClawHub](https://clawhub.ai/otto-iron/skills/nodo-cold-email-autopilot)
- [Nodo](https://nodo.com)
- [Nodo MCP setup guide](https://mcp.nodo.com/start.md)

## Skill Output:

**Output Type(s):** [Text, Configuration instructions, Guidance]

**Output Format:** [Personalized email drafts, reply suggestions, and campaign setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drafts and reply suggestions are for user review; campaign settings follow the agreed audience and daily cap.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
