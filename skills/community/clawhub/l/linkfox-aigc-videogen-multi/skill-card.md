## Description:

AIGC多场景视频生成 helps an agent create short videos from multiple reference images and prompts through LinkFox AIGC video models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate videos from multiple reference images and prompts, choose supported LinkFox video models and options, and receive local paths to generated media files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends images, prompts, phone numbers, verification codes, tokens, and billing requests to LinkFox services.

Mitigation: Install only if that data sharing is acceptable for the intended use, and avoid submitting sensitive images or prompts unless approved.

Risk: Environment variables can override LinkFox service endpoints.

Mitigation: Use only trusted LinkFox endpoint configuration and avoid endpoint overrides unless the destination is fully trusted.

Risk: The onboarding flow can create billing orders and payment QR codes.

Mitigation: Review the selected plan, payment method, and order details before approving any payment action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-aigc-videogen-multi)
- [多参考图生视频 API 参考](references/api.md)
- [解决认证和算力问题](references/onboarding.md)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration guidance]

**Output Format:** [Plain text or Markdown with local media paths, JSON examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated videos are saved as local media files; raw API responses may be saved as JSON data files when no media is produced.]

## Skill Version(s):

1.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
