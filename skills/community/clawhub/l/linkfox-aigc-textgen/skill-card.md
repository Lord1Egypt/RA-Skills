## Description:

Generates text with LinkFox AIGC models from prompts, with optional image or video URL context for multimodal analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate marketing copy, translations, summaries, image descriptions, and video-content analysis through an asynchronous LinkFox text-generation workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, media URLs, and generated outputs are sent to a remote LinkFox service.

Mitigation: Avoid submitting sensitive prompts, personal data, confidential media URLs, or regulated data unless the user has approved that remote processing.

Risk: The skill can use credential-bearing requests and supports environment-variable endpoint overrides.

Mitigation: Keep endpoint override variables unset unless the destination is controlled and trusted, and store API keys in a secret manager rather than shell profiles where possible.

Risk: Onboarding flows can handle phone login, API-key issuance, billing plans, payment orders, and payment QR generation.

Mitigation: Confirm the plan, price, payment method, and user intent before generating any order or payment QR code.

## Reference(s):

- [AI 生文 API 参考](references/api.md)
- [解决认证和算力问题](references/onboarding.md)
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/skills/linkfox-aigc-textgen)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Generated text or JSON response envelopes; guidance may include Markdown and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Small responses are emitted as full JSON; large responses may be saved to a file with a JSON envelope containing content and savedPath.]

## Skill Version(s):

1.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
