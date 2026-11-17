## Description:

Generate high-quality images from text descriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fchange](https://clawhub.ai/user/fchange)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate images from text prompts through Gitee AI models, adjusting model, size, negative prompt, guidance scale, and inference-step parameters as needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to Gitee AI and require a Gitee AI API key.

Mitigation: Install only when that external service use is acceptable for the intended prompts and environment.

Risk: Passing the API key with --api-key may expose it through shell history or process listings.

Mitigation: Set GITEEAI_API_KEY through the environment or a secret manager instead of passing the key on the command line.

Risk: The bundled script depends on the openai package without a pinned version.

Mitigation: Pin and review the openai dependency in controlled or production environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fchange/skills/moark-image-gen)
- [Gitee AI API endpoint](https://ai.gitee.com/v1)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Markdown with generated image link and concise parameter summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns an image URL from the Gitee AI API; default output does not download the image.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
