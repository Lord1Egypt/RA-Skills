## Description:

Control Huawei HiLink USB LTE modems via their local REST API for SMS, signal and status checks, SIM PIN handling, prepaid balance queries, and connection monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[and0r](https://clawhub.ai/user/and0r)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to manage Huawei HiLink USB LTE modems connected to systems they control. It helps with SMS operations, LTE signal and network checks, SIM PIN entry or status checks, prepaid balance queries, and modem network setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script can affect modem state, including sending or deleting SMS messages and changing SIM PIN-related settings.

Mitigation: Use the skill only with modems you control, review commands before execution, and avoid SMS delete or PIN-changing operations unless those changes are intended.

Risk: SIM PINs and modem configuration can be exposed if stored in weakly protected config files or passed through command lines or agent transcripts.

Mitigation: Avoid storing SIM PINs in the config file when possible, avoid placing real PINs in prompts or shell history, and restrict config file permissions.

Risk: The security review found that crafted inputs or a modified config file could make the script run unintended commands or change modem data.

Mitigation: Review and fix the script before routine use, keep configuration files trusted and permission-restricted, and scan changes before deployment.

## Reference(s):

- [HiLink API Reference](artifact/references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/and0r/skills/hilink-lte)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and plain-text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include modem status, signal values, SMS content, SIM state, device information, and setup guidance for local HiLink modem access.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
