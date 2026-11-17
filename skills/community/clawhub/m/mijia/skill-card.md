## Description:

Control Xiaomi Mijia smart home devices from an agent using natural-language mappings and CLI commands for lamp power, brightness, color temperature, status, and lighting modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hqman](https://clawhub.ai/user/hqman)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent operate configured Xiaomi Mijia smart home devices, especially desk lamps, through approved CLI commands and natural-language command mappings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change the state of a configured real-world Mijia device, including power, brightness, color temperature, and lighting mode.

Mitigation: Require explicit user confirmation before executing device-changing commands.

Risk: The skill depends on Xiaomi account/device access and the mijiaapi package.

Mitigation: Run with only the required Xiaomi account and device ID access, and pin and lock dependencies before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hqman/skills/mijia)
- [mijia-api library](https://github.com/Do1e/mijia-api)
- [uv package manager](https://github.com/astral-sh/uv)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and CLI status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured MIJIA_LAMP_DID environment variable and Xiaomi account login.]

## Skill Version(s):

0.1.0 (source: evidence.release.version and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
