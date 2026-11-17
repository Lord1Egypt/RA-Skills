## Description:

Create AI images with GPT Image, Gemini Nano Banana, FLUX, Imagen, and top providers using prompt engineering, style control, and smart editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and external users use this skill to choose image generation providers, write stronger prompts, and plan image generation or editing workflows across cloud and local models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt text and reference images may be sent to the selected image provider.

Mitigation: Use only approved providers for sensitive work, and avoid sending sensitive or regulated content unless the data handling path is approved.

Risk: API keys are required for several cloud providers.

Mitigation: Keep keys in environment variables or a secrets manager, and never paste secret values into chat or committed files.

Risk: Optional local examples use package installation commands.

Mitigation: Run install examples in an isolated environment and pin package versions where practical.

Risk: Provider model names, access, benchmarks, and pricing can change.

Mitigation: Verify current provider documentation and account access before high-value or quality-critical generation work.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/onlyloveher/skills/image-generation-zhouli)
- [Skill Homepage](https://clawic.com/skills/image-generation)
- [Setup - AI Image Generation](artifact/setup.md)
- [API Patterns (2026)](artifact/api-patterns.md)
- [Benchmark Snapshot (2025-2026)](artifact/benchmarks-2026.md)
- [Image Prompting Guide (2026)](artifact/prompting.md)
- [GPT Image (OpenAI)](artifact/gpt-image.md)
- [Google Image Models (Gemini + Imagen)](artifact/gemini.md)
- [FLUX (Black Forest Labs)](artifact/flux.md)
- [Replicate](artifact/replicate.md)
- [Leonardo AI](artifact/leonardo.md)
- [Ideogram](artifact/ideogram.md)
- [Stable Diffusion (Local)](artifact/stable-diffusion.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, configuration notes, and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce provider-specific prompts, model choices, setup steps, and example API calls; generated images are produced only when the agent invokes a selected provider.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
