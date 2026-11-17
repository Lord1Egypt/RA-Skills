## Description:

GNano Ihogmn helps agents configure GNano image generation from a user-provided token and run text-to-image or image-to-image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielchen59](https://clawhub.ai/user/danielchen59)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to validate GNano API access, discover available image-generation settings, and generate images from text prompts or reference images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens may be exposed through command history, logs, or local task state.

Mitigation: Use a revocable token, avoid pasting secrets into shared logs or commands, and do not store the token in plaintext task files.

Risk: Reference images and prompts are uploaded to the configured remote GNano service.

Mitigation: Keep the API URL on the trusted GNano HTTPS endpoint and avoid sending private, sensitive, or person-identifying images unless upload is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danielchen59/skills/gnano-ihogmn)
- [GNano service](https://gnano.ihogmn.top)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Chinese Markdown guidance with bash commands; scripts return JSON status and can write image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python >=3.8, requests >=2.31.0, a user-provided GNano API token, and outbound HTTPS access to the configured GNano endpoint.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
