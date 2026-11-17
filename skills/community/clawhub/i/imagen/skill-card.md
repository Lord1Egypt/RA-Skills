## Description:

Generates images at cheap, medium, good, or top quality levels using OpenRouter and the active OpenClaw configuration, saving files in the agent workspace by default under ./skills/imagen/out.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perilla](https://clawhub.ai/user/perilla)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to turn a user's image request into a direct OpenRouter image-generation call with selected quality, size, and aspect ratio, then return the generated file path. It is intended for users who want image files created inside the current agent workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The output path option can write outside the declared workspace.

Mitigation: Do not allow --out-dir in normal use, or constrain it to a workspace-owned directory before execution.

Risk: Image prompts are sent to OpenRouter and may expose sensitive prompt content.

Mitigation: Do not include secrets, credentials, regulated personal data, or other sensitive content in prompts sent through this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/perilla/skills/imagen)
- [Publisher profile](https://clawhub.ai/user/perilla)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Text response with generated image file path and brief generation details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated image files are saved under the workspace, normally in skills/imagen/out.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
