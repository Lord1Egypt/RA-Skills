## Description: <br>
Google Model Armor: Create a new Model Armor template. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators managing Google Model Armor use this skill to prepare a gws CLI command that creates a Model Armor template for a chosen GCP project, location, and template ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill prepares a write command that creates cloud security configuration. <br>
Mitigation: Confirm user intent and the exact project, location, template ID, preset, or JSON body before running the command. <br>
Risk: An untrusted CLI or incorrect active GCP account could apply changes in the wrong environment. <br>
Mitigation: Verify the installed gws CLI, review shared authentication guidance, and confirm the active GCP account and project before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-modelarmor-create-template) <br>
- [gws-shared](../gws-shared/SKILL.md) <br>
- [gws-modelarmor](../gws-modelarmor/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws CLI and user confirmation before executing the write command.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; artifact metadata.version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
