## Description:

Linux Omniscient helps an agent route tasks across reasoning, code execution, and Linux desktop, hardware, device, network, and IoT control scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to propose and run Linux-oriented desktop automation, hardware inspection, device-control, network, and IoT workflows through script commands and generated code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Linux desktop, device, network, and IoT control can affect local system state or connected equipment.

Mitigation: Use only in a contained environment where this scope is acceptable, and supervise camera, audio, serial, IoT, and power actions.

Risk: Safeguards are not reliably implemented or scoped.

Mitigation: Review the skill before installing and prefer narrower skills with enforced confirmations for destructive operations.

Risk: Tokens or Wi-Fi passwords passed on command lines may be exposed in process history or logs.

Mitigation: Do not pass real tokens or Wi-Fi passwords on command lines; use safer secret-handling patterns outside the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjiaocheng/skills/linux-omniscient)
- [Command reference](artifact/references/command_reference.md)
- [Security checklist](artifact/references/security_checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run broad Linux device-control workflows; high-risk actions require review and supervision.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
