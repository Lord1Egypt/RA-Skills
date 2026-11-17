## Description:

Generate or edit images with the image-generation-studio CLI through supported Gemini, OpenAI Images-compatible, and OpenAI Responses-compatible adapters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[limkim0530](https://clawhub.ai/user/limkim0530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and agent operators use this skill to generate, edit, compose, or restyle images through configured image providers, models, endpoints, and aliases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and input images are sent to configured image providers using user credentials.

Mitigation: Install and use only with trusted providers; prefer environment variables or per-call keys, and store API keys in config.json only when plaintext local storage is acceptable.

Risk: OpenAI Images-compatible providers may return image URLs that the skill downloads before saving outputs.

Mitigation: Prefer --response-format b64_json when the provider supports it, avoid untrusted custom or proxy providers, and keep generated files inside intended workspace paths.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/limkim0530/skills/image-generation-studio)
- [Gemini Adapter](references/adapter-gemini.md)
- [OpenAI Images-Compatible Adapter](references/adapter-openai-images.md)
- [OpenAI Responses Adapter](references/adapter-openai-responses.md)
- [Configuration Assistant](references/configuration.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON configuration; generated image files are saved as PNG, JPEG, or WebP.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-selected providers and credentials; prompts and input images may be sent to configured external services.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
