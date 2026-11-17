## Description:

Jiuma AI's free image generation skill uses the Jiuma AI API to generate images from text prompts with configurable image dimensions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dddcn1](https://clawhub.ai/user/dddcn1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit text prompts to Jiuma AI, poll generation status, and retrieve generated image URLs. It is suited for agent workflows that need lightweight text-to-image generation with optional login for additional free usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and login workflow data are sent to Jiuma services.

Mitigation: Use the skill only when sharing that content with Jiuma is acceptable, and avoid prompts containing sensitive or personal information.

Risk: The Jiuma API key is stored locally in plaintext without enforced private permissions.

Mitigation: Run the skill in an isolated environment and inspect or harden the key file permissions before use.

Risk: The artifact documentation asks the agent to persist a memory entry.

Mitigation: Remove or ignore that memory-recording instruction before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dddcn1/skills/jiuma-free-image-gen)
- [Jiuma text-to-image submit API](https://api.jiuma.com/api/textImage/add)
- [Jiuma text-to-image status API](https://api.jiuma.com/api/textImage/status)
- [Jiuma login guide](artifact/LOGIN.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime response includes task IDs for submitted jobs and image URLs when generation succeeds.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
