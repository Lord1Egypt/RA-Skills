## Description:

pic-gen helps agents turn plain-language image requests into optimized, model-specific prompts and optional image generation calls for Qwen Wanxiang, Banana/Flux, DALL-E 3, Midjourney, and Stable Diffusion formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aoturlab](https://clawhub.ai/user/aoturlab)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and creative teams use pic-gen to refine simple image ideas into model-specific prompts, manage provider configuration, and optionally generate or download images through configured provider APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts can be sent to selected external providers and may contain sensitive information.

Mitigation: Review prompts before generation and avoid submitting confidential, regulated, or customer-sensitive content unless the chosen provider and account are approved for that use.

Risk: API keys may be exposed if pasted into chat, stored directly in config/models.yaml, committed, or left in shell history.

Mitigation: Prefer environment variables, avoid pasting secrets into chat or command history, and do not commit config/models.yaml after adding keys.

Risk: Downloaded image files are written to a user-selected output directory.

Mitigation: Use --download only with a trusted output directory and review generated files before sharing or deploying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aoturlab/skills/pic-gen)
- [DALL-E 3 prompt format reference](references/dalle.md)
- [Flux prompt format reference](references/flux.md)
- [Midjourney prompt format reference](references/midjourney.md)
- [Stable Diffusion / ComfyUI prompt format reference](references/stable-diffusion.md)
- [OpenAI image generation guide](https://platform.openai.com/docs/guides/images)
- [OpenAI image generation API reference](https://platform.openai.com/docs/api-reference/images-create)
- [Black Forest Labs Flux](https://blackforestlabs.ai/flux/)
- [Banana documentation](https://docs.banana.dev/banana-docs)
- [Midjourney parameter documentation](https://docs.midjourney.com/docs/parameter-simplified)
- [Stable Diffusion prompt guide](https://stable-diffusion-art.com/prompts)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands plus text, JSON, or YAML script outputs; optional downloaded image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on configured provider credentials and may include provider-hosted image URLs, local image files, optimized prompts, or configuration summaries with API keys masked.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
