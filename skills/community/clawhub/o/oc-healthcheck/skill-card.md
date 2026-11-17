## Description:

Audit/harden OpenClaw hosts: SSH, firewall, updates, exposure, backups, disk encryption, gateway security.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw operators use this skill to review host and gateway security posture, then prepare a staged, reversible hardening plan based on their operating system, privileges, and access path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Host hardening recommendations or commands could disrupt remote access or change system security settings.

Mitigation: Confirm the user's access path before recommending SSH, firewall, or remote-access changes, and get explicit approval before applying any state-changing action.

## Reference(s):

- [Healthcheck on ClawHub](https://clawhub.ai/hillstreet-ph/skills/oc-healthcheck)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Configuration guidance]

**Output Format:** [Markdown with findings, recommendations, and inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only checks first; staged recommendations with approval before state changes]

## Skill Version(s):

1.0.5 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
