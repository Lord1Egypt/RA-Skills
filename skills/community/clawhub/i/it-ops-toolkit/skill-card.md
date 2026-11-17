## Description:

It Ops Toolkit helps agents select and run Python-based IT operations utilities for network diagnostics, system monitoring, service checks, troubleshooting, and practical data utilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[microsnow](https://clawhub.ai/user/microsnow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site reliability engineers, and IT operations teams use this skill to translate natural-language operational requests into diagnostics, checks, troubleshooting steps, and utility commands across Windows, Linux, and macOS environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote SSH, batch checks, port scans, log reads, and RTSP stream tests can affect or expose infrastructure when run on unintended systems.

Mitigation: Require explicit confirmation before these actions and use the skill only on systems where the operator has authorization.

Risk: Remote monitoring can expose privileged access paths.

Mitigation: Use least-privilege SSH accounts and normal host-key verification.

Risk: Passwords, tokens, and RTSP credentials may be exposed through chat, command arguments, URLs, or diagnostic output.

Mitigation: Avoid placing secrets in chat, command arguments, or RTSP URLs; review generated outputs before sharing them.

Risk: Diagnostic output may contain hostnames, IP addresses, service names, logs, or other sensitive infrastructure details.

Mitigation: Treat outputs as sensitive operational data and restrict storage or redistribution according to the environment's security policy.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/microsnow/skills/it-ops-toolkit)
- [Source repository](https://github.com/microsnow/it-ops-toolkit.git)
- [Commands reference](references/commands_reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and interpreted diagnostic text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command outputs or infrastructure details from authorized diagnostic runs.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
