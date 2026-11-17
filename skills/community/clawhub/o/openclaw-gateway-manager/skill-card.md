## Description:

Openclaw Gateway Manager helps agents inspect and manage OpenClaw gateway instances, including status checks, port changes, restarts, validation, instance creation, deletion, and port scanning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seastaradmin](https://clawhub.ai/user/seastaradmin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators who run OpenClaw gateways across local, JVS Claw, QClaw, cloud, or custom setups use this skill to inspect gateway status, change ports, restart or verify gateways, and create or remove gateway instances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scripts can create persistent user-level services for OpenClaw gateways.

Mitigation: Review generated LaunchAgent or systemd user service files before enabling them, and use only trusted instance names and numeric ports.

Risk: Create and delete workflows can modify or remove OpenClaw configuration, session, memory, and service files.

Mitigation: Confirm the target instance and backup location before execution, and avoid create/delete workflows until stronger input, path, and process validation is added.

Risk: The security review notes insufficient validation for arguments, target paths, and process identity.

Mitigation: Do not pass untrusted arguments through an agent; manually validate ports, instance identifiers, and target directories before running scripts.

## Reference(s):

- [Common ports reference](artifact/references/common-ports.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command snippets and script invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local shell workflows that read or modify OpenClaw configuration files and user-level service definitions.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
