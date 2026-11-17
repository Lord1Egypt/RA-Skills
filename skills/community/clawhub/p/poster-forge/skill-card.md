## Description:

Universal image and poster generator with Chinese and English text support, using AI generation, HTML screenshots, or PIL text rendering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huuuwnnn-droid](https://clawhub.ai/user/huuuwnnn-droid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create posters, social media images, cover images, infographics, comparison charts, and tutorial cards from concise content and style instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts may be sent to Pollinations.ai when AI mode or auto mode uses the AI engine.

Mitigation: Avoid sensitive or proprietary prompt text unless external service use is acceptable, or choose local-only text or HTML modes where possible.

Risk: HTML rendering uses unescaped user text in unsandboxed Chromium.

Mitigation: Avoid untrusted HTML-like content and run HTML rendering in a restricted environment.

Risk: The security verdict requires review before installation.

Mitigation: Review and scan the skill before deployment, following the clawscan guidance in this context.

## Reference(s):

- [Poster Forge ClawHub skill page](https://clawhub.ai/huuuwnnn-droid/skills/poster-forge)
- [Noto Sans CJK SC Bold font asset](https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Bold.otf)
- [Noto Sans CJK SC Regular font asset](https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Image files generated through command-line execution, with concise Markdown guidance for agent use]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports AI, HTML, text, and auto-fallback rendering modes with social and print size presets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
