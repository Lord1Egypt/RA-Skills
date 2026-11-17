## Description:

Intel Local Windows Computer Use helps an agent use Chinese or English commands to query or change supported Windows system settings through a local Windows CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[makejiang](https://clawhub.ai/user/makejiang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill on supported Intel Windows systems to query system status and adjust power, device, display, shell, app, language, time, privacy, and notification settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change local Windows system settings and some actions may require Administrator privileges.

Mitigation: Use it only for the documented supported categories, review the requested action before execution, and rely on normal Windows elevation prompts rather than bypassing permissions.

Risk: The release packages native code, downloads models and binaries, and creates persistent runtime state under %USERPROFILE%\.openvino.

Mitigation: Install only from a trusted publisher, validate downloaded components in the target environment, and remove %USERPROFILE%\.openvino when a clean uninstall is required.

Risk: The security verdict is suspicious because the capability surface is broader than the documentation clearly discloses.

Mitigation: Perform security review and sandboxed testing before broad deployment, especially on machines with sensitive user data or administrative access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/makejiang/skills/local-computer-use)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Windows shell commands and JSON response expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require repeated continuation commands while local models download on first run.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
