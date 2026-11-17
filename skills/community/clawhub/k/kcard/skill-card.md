## Description:

Creates concise knowledge cards from text, files, URLs, or images by extracting key points, choosing a concept, memo, process, or comparison structure, outputting Markdown, and rendering a PNG image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn notes, articles, files, URLs, or images into concise memory cards. It helps produce reusable Markdown cards and rendered PNG images for study, documentation, and quick reference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Card Markdown can be rendered as active browser content with network access.

Mitigation: Render only trusted or sanitized Markdown, and block browser network access when rendering material from untrusted people or websites.

Risk: The skill writes fetched or local content into Markdown and PNG files.

Mitigation: Review the input source, output path, and generated card before sharing or deploying the files.

Risk: Renderer dependencies and browser behavior may vary across environments.

Mitigation: Run the renderer in an isolated Python environment with pinned dependencies when reliability or isolation matters.

## Reference(s):

- [Card Templates](references/card-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/goog/skills/kcard)

## Skill Output:

**Output Type(s):** [Markdown, Files, Text]

**Output Format:** [Markdown source file, rendered PNG image, and one-line summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cards are intended to stay concise, with one concept per card and a maximum of 195 words.]

## Skill Version(s):

1.6.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
