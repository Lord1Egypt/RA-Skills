## Description:

Optimize OpenClaw model configuration by declaring missing model capabilities such as vision or multimodal input, context window, max output tokens, and reasoning support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yay2008](https://clawhub.ai/user/yay2008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect OpenClaw model configuration, identify missing capability declarations, and prepare safe updates to model defaults after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect capability values can change OpenClaw model behavior or leave features unavailable.

Mitigation: Confirm capability values against the user's provider or endpoint before applying them.

Risk: Editing OpenClaw model defaults can disrupt an existing configuration.

Mitigation: Create the required openclaw.json backup and review changes before restarting OpenClaw.

## Reference(s):

- [Common Model Capabilities Reference](references/model-capabilities.md)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Code, Shell commands]

**Output Format:** [Markdown with JSON configuration snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces user-confirmed OpenClaw configuration changes and restart reminders.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
