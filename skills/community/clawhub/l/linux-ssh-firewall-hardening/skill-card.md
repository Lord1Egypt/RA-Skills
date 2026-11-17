## Description:

Guides SSH connectivity diagnosis, SSH port changes, and SSH/firewalld hardening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peterliu-512](https://clawhub.ai/user/peterliu-512)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, system administrators, and operations engineers use this skill to diagnose SSH access failures, reconcile sshd and firewalld port behavior, and apply safer SSH hardening steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privileged SSH and firewalld commands can lock an administrator out if the port, subnet, authentication method, or rollback path is wrong.

Mitigation: Review each command before execution, confirm active key-based access, keep an existing session open, and ensure console or rollback access before changing firewall or sshd settings.

Risk: Example firewall rules use placeholder LAN subnet and port values that may not match the target host.

Mitigation: Replace example network and port values with verified environment-specific values, then validate with sshd -T, firewall-cmd --list-rich-rules, and a new SSH session before removing old access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/peterliu-512/skills/linux-ssh-firewall-hardening)
- [ClawHub publisher profile](https://clawhub.ai/user/peterliu-512)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require administrator review before execution on a target host.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
