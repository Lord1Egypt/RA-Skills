## Description:

Google Model Armor: Sanitize a user prompt through a Model Armor template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators who use the gws CLI use this skill to sanitize prompt text, stdin, or JSON request bodies through a specified Google Model Armor template.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt text or JSON is sent to the configured Google Model Armor template.

Mitigation: Install only when you intend to use the gws CLI with Google Model Armor and review the selected Google Cloud project and template before sending sensitive content.

Risk: The artifact depends on shared gws authentication and global settings that are not bundled with this skill.

Mitigation: Review the shared gws environment configuration before use, including authentication, project, location, and global CLI behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-modelarmor-sanitize-prompt)
- [gws-shared](../gws-shared/SKILL.md)
- [gws-modelarmor](../gws-modelarmor/SKILL.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI flag tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI and a Google Model Armor template resource name; accepts prompt text, stdin, or a JSON request body.]

## Skill Version(s):

1.0.12 (source: ClawHub release evidence; artifact metadata version 0.22.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
