## Description:

Image Forge routes image generation and image editing requests through curated use-case, style, and subject signals across GPT Image 2-compatible and Gemini-compatible backends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenyqthu](https://clawhub.ai/user/chenyqthu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate, edit, restyle, and compose images for posters, product visuals, avatars, social posts, UI mockups, comics, game assets, infographics, and logo showcase backgrounds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected reference images may be sent to configured GPT, Gemini, or CRS image backends.

Mitigation: Install only when that data sharing is acceptable, and avoid sending sensitive or regulated images unless the selected backend is approved.

Risk: The CRS backend can forward credentials and image payloads to a configured CRS_BASE_URL.

Mitigation: Restrict CRS_BASE_URL to an approved HTTPS host or a trusted local loopback service before use.

Risk: Some bundled prompt templates may steer the agent outside image generation or into sensitive image-use cases.

Mitigation: Remove or quarantine templates that perform agent workflows, visible passport or ID verification imagery, or personal profiling before broad deployment.

Risk: Unpinned dependencies or backend changes can alter runtime behavior.

Mitigation: Pin dependencies and review backend configuration before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenyqthu/skills/image-forge)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [Backend registry](artifact/backends.yaml)
- [Style library index](artifact/styles/index.yaml)
- [Use-case index](artifact/use-cases/index.yaml)
- [YouMind awesome-gpt-image-2](https://github.com/YouMind-OpenLab/awesome-gpt-image-2)
- [EvoLinkAI awesome-gpt-image-2-prompts](https://github.com/EvoLinkAI/awesome-gpt-image-2-prompts)
- [YouMind awesome-nano-banana-pro-prompts](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, API payload guidance, and MEDIA file path outputs for generated image assets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved as PNG, WebP, or JPEG files through configured external image backends.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
