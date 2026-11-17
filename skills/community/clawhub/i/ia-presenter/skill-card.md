## Description:

Write, lint, package, preview, and theme iA Presenter presentations, including Markdown decks with speaker notes, media, charts, layouts, and custom theme files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daaab](https://clawhub.ai/user/daaab)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and presentation authors use this skill to turn notes or articles into iA Presenter Markdown decks, package .iapresenter bundles, validate deck structure, and create or install custom themes for iA Presenter 2.x.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Preview and automation helpers can open iA Presenter, alter local app state, or capture the full screen.

Mitigation: Require explicit user approval before preview screenshots, app preference changes, or any workflow that captures the screen.

Risk: Theme installation can replace or modify custom themes in the user's iA Presenter Themes folder.

Mitigation: Confirm the destination theme name and replacement intent before using theme install or force options, and keep a backup of existing theme files when replacing.

Risk: Decks may reference remote media that contacts third-party services during rendering.

Mitigation: Prefer local media assets for private decks and review remote URLs before packaging or previewing a deck.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daaab/skills/ia-presenter)
- [iA Presenter Markdown syntax](references/syntax.md)
- [Layouts](references/layouts.md)
- [Content blocks](references/content-blocks.md)
- [Tables and charts](references/charts.md)
- [Custom themes](references/themes.md)
- [Rendering engine CSS](references/engine-css.md)
- [File format, import/export, shortcuts, automation](references/file-format.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, and generated deck or theme files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce .iapresenter bundles, theme folders, screenshots, and validation reports when helper scripts are run.]

## Skill Version(s):

1.0.3 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
