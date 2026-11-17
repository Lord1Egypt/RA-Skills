## Description:

PC healthcheck and diagnostics for Linux, Windows, and macOS that collect system information, produce local reports, and provide actionable recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ningtoba](https://clawhub.ai/user/ningtoba)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and end users can use this skill to run local PC diagnostics, review storage, CPU, memory, network, process, service, package, and security-log signals, and receive maintenance recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext diagnostic reports can include broad system and user data.

Mitigation: Use a private output directory with restrictive permissions, treat reports as confidential, and review or redact them before sharing.

Risk: Scheduled use can amplify exposure if the scheduler configuration file is untrusted or writable by others.

Mitigation: Prefer manual runs as a regular user, and schedule the skill only when the config file is trusted and protected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ningtoba/skills/pc-assistant-fixed)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Human-readable text reports and JSON summaries, with shell commands and configuration guidance in Markdown documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are timestamped local files and may include sensitive system and user information.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact install.yaml reports 1.2.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
