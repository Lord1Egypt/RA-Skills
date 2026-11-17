## Description:

Guides the setup and recovery of a dedicated Mac mini agent host with private remote access, power settings, and an explicit reboot-availability trade-off.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexbloch-ia](https://clawhub.ai/user/alexbloch-ia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to keep a dedicated Mac mini agent host reachable after reboots, diagnose remote-access failures, and decide with the owner whether unattended login is appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent private-network SSH access may expose the host if credentials are compromised.

Mitigation: Use a dedicated non-admin agent account and scoped, revocable credentials; restrict deployment to an intentionally managed host.

Risk: Disabling FileVault for automatic login weakens physical security and exposes the logged-in session.

Mitigation: Keep FileVault enabled unless the owner approves the trade-off; consider automatic login only on a dedicated Mac mini in a physically controlled location without personal data.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/alexbloch-ia/skills/mac-mini)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Text]

**Output Format:** [Markdown with shell commands and host status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a setup checklist, reboot drill, failure tree, and fleet health checks.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
