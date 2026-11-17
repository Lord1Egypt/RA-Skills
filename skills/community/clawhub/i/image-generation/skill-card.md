## Description:

Create AI images with GPT Image, Gemini Nano Banana, FLUX, Imagen, and top providers using prompt engineering, style control, and smart editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers, designers, and other users use this skill to choose image-generation providers, write prompts, plan edits, and manage model-specific setup for AI-generated visuals and consistent asset sets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference images may be sent to the selected image provider.

Mitigation: Use the skill only with providers approved for the content, and avoid sensitive or regulated images unless provider policy allows it.

Risk: API keys and optional package installs can increase setup exposure.

Mitigation: Use environment variables for secrets and run optional pip installs in a dedicated virtual environment with pinned dependencies where possible.

Risk: Model aliases, provider endpoints, and benchmark rankings can drift after publication.

Mitigation: Resolve aliases to official provider model IDs and re-check current provider documentation or rankings when quality is critical.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/image-generation)
- [Skill Homepage](https://clawic.com/skills/image-generation)
- [Setup - AI Image Generation](artifact/setup.md)
- [Image Prompting Guide (2026)](artifact/prompting.md)
- [API Patterns (2026)](artifact/api-patterns.md)
- [Benchmark Snapshot (2025-2026)](artifact/benchmarks-2026.md)
- [GPT Image (OpenAI)](artifact/gpt-image.md)
- [Google Image Models (Gemini + Imagen)](artifact/gemini.md)
- [FLUX (Black Forest Labs)](artifact/flux.md)
- [Stable Diffusion (Local)](artifact/stable-diffusion.md)
- [Ideogram API](https://ideogram.ai/api)
- [Leonardo AI Documentation](https://docs.leonardo.ai/)
- [Replicate](https://replicate.com/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code blocks and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider-specific API call examples, model-routing guidance, and optional local preference-memory setup.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
