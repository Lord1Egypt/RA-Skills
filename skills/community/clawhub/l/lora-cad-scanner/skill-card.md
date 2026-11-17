## Description:

LoRa Channel Activity Detection scanner for LilyGo T3 v1.6 and optional HackRF One workflows that helps an agent guide setup, scanning, decoding, local logging, and alerting for LoRa RF monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arsatyants](https://clawhub.ai/user/arsatyants)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and authorized RF operators use this skill to configure a LilyGo T3 and Raspberry Pi as a persistent LoRa band monitor, optionally using HackRF sweep data to focus the scan range. It supports setup guidance, packet decoding context, local report files, and Telegram alert workflow configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can support continuous RF packet capture and decoded payload handling, including device identifiers or packet contents.

Mitigation: Install and operate it only for authorized RF monitoring, minimize retained payload data, and treat captured packet contents as untrusted.

Risk: Configured agent or Telegram delivery can forward captured RF metadata or payload details outside the local workspace.

Mitigation: Send structured metadata by default, require explicit user configuration for external delivery, and avoid forwarding raw packet payloads unless they have been reviewed.

Risk: The monitor uses local persistence and a writable workspace import path that can increase execution risk.

Mitigation: Remove the writable workspace import override, pin dependencies, protect local logs and hit databases, and run the monitor under a dedicated low-privilege account.

Risk: A long-running serial monitor can keep collecting data if deployment boundaries are unclear.

Mitigation: Add explicit start, stop, retention, and cleanup procedures before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/arsatyants/skills/lora-cad-scanner)
- [Setup Guide](references/setup.md)
- [SX1276 CAD Register Reference](references/sx1276-cad.md)
- [HackRF + LilyGo Combined Workflow](references/hackrf-workflow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code, shell commands, configuration steps, and generated code or file guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe local RF scan logs, decoded packet metadata, alert files, and hardware-specific setup steps.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
