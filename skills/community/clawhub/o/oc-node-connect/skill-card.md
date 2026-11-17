## Description:

Diagnose OpenClaw Control UI browser and native Android, iOS, or macOS node connection failures across route, auth, pairing, QR/setup-code, and reconnect states.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw operators and developers use this skill to diagnose browser Control UI or native node connection failures and verify that one exact client connects successfully to its intended Gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Device-approval steps may go beyond the stated connection-diagnosis purpose, and the security scan is incomplete because a local reference could not be resolved.

Mitigation: Review the approval behavior before installing; use the skill only when pairing approvals are needed and acceptable, and verify the exact pending request on the locked Gateway before approving it.

## Reference(s):

- [Node Connect on ClawHub](https://clawhub.ai/hillstreet-ph/skills/oc-node-connect)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with diagnostic steps and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tailored to the selected client and Gateway; includes route, authentication, pairing, and connection verification steps.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
