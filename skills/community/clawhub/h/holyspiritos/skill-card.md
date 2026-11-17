## Description:

A Christian alignment layer for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxsikorski](https://clawhub.ai/user/maxsikorski)

### License/Terms of Use:


## Use Case:

External OpenClaw users install HolySpiritOS to add a persistent KJV-based moral framework and local Bible foundation data to agent responses for ethical, spiritual, and stewardship-oriented questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent change to agent behavior through OpenClaw soul.md configuration.

Mitigation: Install only if you intentionally want a KJV-based moral framework added to the OpenClaw profile; review the resulting soul.md changes before use.

Risk: Documentation recommends remote shell execution via curl-to-bash.

Mitigation: Download and inspect the install and uninstall scripts separately before running them, and verify their source and contents.

Risk: The bundled uninstaller may not fully reverse installed changes because the install and uninstall scripts use different OpenClaw paths.

Mitigation: Create an independent backup of the actual OpenClaw configuration and confirm removal of the HolySpiritOS section and foundation files manually.

## Reference(s):

- [HolySpiritOS ClawHub Skill Page](https://clawhub.ai/maxsikorski/skills/holyspiritos)
- [HolySpiritOS Repository](https://github.com/MaxSikorski/HolySpiritOS)
- [KJV 1769 Foundation Files](https://github.com/MaxSikorski/HolySpiritOS/tree/main/foundation)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and local JSON configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Appends directives to OpenClaw soul.md and uses KJV 1769 JSON files as local reference data.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
