## Description:

Converts articles or supplied knowledge points into a series of visual knowledge cards with selectable layouts, visual styles, platform presets, and optional character integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hash-panda](https://clawhub.ai/user/hash-panda)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, educators, and developers use this skill to turn long-form articles or concise knowledge points into structured card outlines, image prompts, and generated card image files for social or educational publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may save pasted source content, generated prompts, outlines, and images to local disk.

Mitigation: Avoid using confidential text unless local copies are acceptable, and review generated output directories before sharing or publishing.

Risk: The skill may create a persistent EXTEND.md preference file.

Mitigation: Review the saved preference file after setup and remove or edit project, XDG, or user-level preferences that should not persist.

Risk: Configured character image paths may reference sensitive or unintended local files.

Mitigation: Review any character image path before use and keep role references limited to approved assets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hash-panda/skills/panda-knowledge-card)
- [Project homepage](https://github.com/hash-panda/panda-skills#panda-knowledge-card)
- [Workflow](references/workflow.md)
- [Card Layouts](references/card-layouts.md)
- [Extraction Rules](references/extraction-rules.md)
- [Prompt Construction](references/prompt-construction.md)
- [Platform Presets](references/platform-presets.md)
- [Styles](references/styles.md)
- [Presets](references/presets.md)
- [First-Time Setup](references/config/first-time-setup.md)
- [Preferences Schema](references/config/preferences-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown outlines, saved prompt files, generated image files, configuration notes, and a completion report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local preference files and save source content, prompts, outlines, and generated images to disk.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
