## Description:

Creates animated 9:16 infographic reels from a topic, article URL, YouTube URL, or prepared script by turning the input into a structured brief, visual archetype, image prompt, animation prompt, and publishing-ready reel assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and content teams use this skill to transform educational or explanatory material into dense vertical infographic reels. The workflow supports free-form topics, article URLs, YouTube URLs, and prepared markdown scripts, then produces a reusable brief, visual prompt, animation prompt, generated image, generated video, caption, hashtags, and CTA.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can use third-party generation and research services and may consume media-generation credits.

Mitigation: Confirm cost-bearing generation steps before running them, and keep the existing approval checkpoint before video animation.

Risk: Generated educational or health-oriented infographic copy can become misleading if source claims are weak or unverifiable.

Mitigation: Verify factual claims with research sources before placing them in the visual prompt, and use softer wording when evidence is uncertain.

Risk: Generated files and reusable briefs are saved in the workspace.

Mitigation: Review the output folder before sharing or publishing, especially when inputs include private URLs, transcripts, or brand-specific material.

Risk: The release evidence calls out provider wording around Gemini and Higgsfield.

Mitigation: Check which provider will create the base image and which credentials or plugins are active when strict provider control is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/infografia-reel-formula100k)
- [Publisher profile](https://clawhub.ai/user/formula100k)
- [Visual archetypes](artifact/references/arquetipos.md)
- [Archetype classifier](artifact/references/clasificador.md)
- [Prompt builder](artifact/references/prompt-builder.md)
- [Animation presets](artifact/references/animation-presets.md)
- [Input pipeline](artifact/references/input-pipeline.md)
- [Brand kit](artifact/references/brandkit.md)
- [Word substitution](artifact/references/word-substitution.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance, YAML brief data, prompt text, local generated media files, captions, hashtags, and CTA text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets 9:16 reel assets and writes outputs under entregables/infografias/<slug-tema>/ when media generation is available.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
