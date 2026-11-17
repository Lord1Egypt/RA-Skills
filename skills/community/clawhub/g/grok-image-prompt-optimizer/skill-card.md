## Description:

Optimizes text-to-image prompts for Grok and similar image models, with emphasis on aviation posters, safety campaign visuals, official publicity images, and Chinese-language contest briefs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamkingab](https://clawhub.ai/user/iamkingab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and prompt designers use this skill to turn vague image briefs into structured bilingual image prompts, negative prompts, and quick tuning options for poster-style image generation. It is especially tailored to Chinese civil-aviation, cabin-safety, and official public-service poster concepts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is opinionated toward Chinese/English prompt output and Chinese civil-aviation poster conventions, which may be unsuitable for other regions, languages, or visual domains.

Mitigation: Explicitly provide the desired language, region, visual style, and domain when using it outside Chinese aviation or safety-poster contexts.

Risk: Generated image prompts for aviation, transport, healthcare, industrial safety, or emergency scenes could imply inaccurate equipment, procedures, or layouts if the source brief is underspecified.

Mitigation: Review generated prompts for domain plausibility before image generation, and supply required equipment, procedure, safety, and layout details in the brief.

## Reference(s):

- [Aviation Poster Patterns](artifact/references/aviation-poster-patterns.md)
- [ClawHub skill page](https://clawhub.ai/iamkingab/skills/grok-image-prompt-optimizer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown sections containing Chinese and English prompts, a negative prompt, and quick tweak options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution or system access; output is prompt-writing guidance for downstream image generation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
