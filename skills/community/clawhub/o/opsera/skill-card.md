## Description:

Use the bundled Opsera executable as the Xshell replacement for VPN-launched sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tao-vin](https://clawhub.ai/user/tao-vin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run remote commands and transfer files through current VPN-created Xshell .xsh SSH tunnel sessions with the bundled Opsera executable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a missing bundled executable that would handle SSH credentials and remote command and file operations.

Mitigation: Review the Opsera executable source and binary provenance before installing or using the skill.

Risk: The skill is intended to operate over SSH sessions using stored .xsh connection details.

Mitigation: Use it only with trusted VPN and Xshell sessions, confirm the intended remote host before execution, and avoid exposing passwords.

## Reference(s):

- [Opsera GitHub Repository](https://github.com/tao-vin/opsera)
- [Opsera Releases](https://github.com/tao-vin/opsera/releases)
- [ClawHub Skill Page](https://clawhub.ai/tao-vin/skills/opsera)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local .xsh session details and writes Opsera events under the user's local application data directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
