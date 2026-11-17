## Description:

OpenClaw model management tool for viewing, setting, and managing the large language models used by OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[williamxxu](https://clawhub.ai/user/williamxxu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect available OpenClaw models, view model status, set the default model, and manage fallback models after explicit user authorization for changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted model ID can be interpreted as shell syntax and lead to arbitrary local command execution.

Mitigation: Only use trusted, exact model IDs; do not pass model names copied from untrusted text; replace shell execution with argument-list subprocess calls and validate model IDs.

Risk: Model-changing commands can alter default or fallback model configuration, which may cause service disruption or unexpected cost.

Mitigation: Run set and fallback add/remove only after explicit user authorization, and add a confirmation or policy check before applying changes.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Changing the default or fallback model can update OpenClaw model configuration.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
