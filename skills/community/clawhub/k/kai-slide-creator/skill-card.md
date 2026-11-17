## Description:

Slide Creator generates zero-dependency HTML presentations with 22 style presets, play mode, and presenter mode for pitch decks, product launches, technical talks, and solution presentations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaisersong](https://clawhub.ai/user/kaisersong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, presenters, and content teams use this skill to turn prompts or structured briefs into browser-native HTML slide decks with selected visual styles, speaker notes, editing controls, and validation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated decks can silently send edited presentation content, including speaker notes, back to the hosting server when saving.

Mitigation: Edit and save decks only from trusted local files or trusted origins; avoid saving generated non-Blue-Sky decks from untrusted HTTP/HTTPS origins.

Risk: The Electron preload file requires review before use in a desktop wrapper.

Mitigation: Remove preload.cjs from the skill package or audit it together with the desktop main-process handlers before desktop-wrapper deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kaisersong/skills/kai-slide-creator)
- [Project Homepage](https://github.com/kaisersong/slide-creator)
- [Live Demo](https://kaisersong.github.io/slide-creator/demos/blue-sky-en.html)
- [Style Index](references/style-index.md)
- [Workflow](references/workflow.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance plus JSON briefs and self-contained HTML slide deck files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated decks may include presenter mode, inline editing, speaker notes, and optional per-deck evaluation JSON.]

## Skill Version(s):

2.27.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
