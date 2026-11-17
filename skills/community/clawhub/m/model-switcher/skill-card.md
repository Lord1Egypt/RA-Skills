## Description:

Automatically switch between fast and powerful models based on task complexity, including analysis, refactoring, architecture design, optimization, or explicit model-switching requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[puaservice](https://clawhub.ai/user/puaservice)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to route simple tasks to faster models and complex work such as analysis, refactoring, design, debugging, and optimization to more capable models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically route future prompts to a custom model provider before clear user approval.

Mitigation: Require explicit confirmation before model switches for sensitive work, and verify the configured aliases and model provider before installation.

## Reference(s):

- [Model Switcher on ClawHub](https://clawhub.ai/puaservice/skills/model-switcher)
- [puaservice publisher profile](https://clawhub.ai/user/puaservice)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with model-switching command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose active model changes during an agent session.]

## Skill Version(s):

1.0.2 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
