## Description:

Automatically classifies task complexity and routes simple tasks to local models while reserving more complex work for configured provider models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freepengyang](https://clawhub.ai/user/freepengyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to choose an appropriate local or cloud model path at the start of a task, preserving context continuity and matching model cost or capability to task complexity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud routing can send confidential prompts to configured provider endpoints.

Mitigation: Review provider settings before using cloud routing and keep sensitive tasks on approved local or enterprise providers.

Risk: The setup wizard may create or overwrite local provider configuration at ~/.model-router/config.json.

Mitigation: Back up existing configuration and review the generated provider settings before relying on the router.

Risk: The workflow and prompts are primarily Chinese-language, which may affect operator review in non-Chinese environments.

Mitigation: Have a Chinese-literate reviewer confirm provider choices, routing labels, and generated configuration before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freepengyang/skills/hermes-model-router)
- [Publisher profile](https://clawhub.ai/user/freepengyang)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown-style guidance with command examples and interactive command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local provider configuration at ~/.model-router/config.json when the setup wizard is run.]

## Skill Version(s):

v1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
