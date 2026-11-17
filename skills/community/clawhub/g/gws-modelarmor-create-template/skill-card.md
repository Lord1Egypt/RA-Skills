## Description:

Google Model Armor: Create a new Model Armor template.

This skill is ready for commercial/non-commercial use.

## Publisher:

[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Google Workspace or Google Cloud operators use this skill to prepare gws CLI commands for creating a Google Model Armor template in a selected project and location.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill prepares a command that creates a persistent Google Cloud Model Armor template.

Mitigation: Confirm the target project, location, template ID, preset, and JSON body before allowing execution.

Risk: The skill depends on the gws CLI running with Google Cloud credentials.

Mitigation: Install and use it only in environments where the active credentials and project context are intended for this operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/skills/gws-modelarmor-create-template)
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gws CLI and Google Cloud credentials; the create-template command performs a cloud write action.]

## Skill Version(s):

1.0.12 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
