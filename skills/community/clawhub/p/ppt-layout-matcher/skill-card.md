## Description:

PPT Layout Matcher analyzes presentation content and recommends PowerPoint slide layouts from a 45-page 16:9 design library across 10 layout categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zrxparley](https://clawhub.ai/user/zrxparley)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and presentation creators use this skill to analyze slide-ready content such as bullet points, metrics, comparisons, timelines, or process descriptions and select an appropriate PowerPoint layout before generating or editing a deck.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad PPT-related triggers may activate the skill when the user only wants discussion or planning.

Mitigation: Confirm the user's intent and the selected layout before creating or modifying any PowerPoint file.

Risk: Generated decks may be written to an unintended path or overwrite an existing presentation.

Mitigation: Ask the user to confirm the output path and file action before writing PPTX output.

Risk: The artifact defaults to Chinese-language examples and documentation, which may not match every audience.

Mitigation: Review generated slide text and localize terminology, examples, and labels for the target audience.

Risk: The skill depends on python-pptx for PowerPoint generation.

Mitigation: Install and review dependencies under the user's normal environment and package policy.

## Reference(s):

- [Layout Templates Reference](artifact/references/layout_templates.md)
- [ClawHub Skill Page](https://clawhub.ai/zrxparley/skills/ppt-layout-matcher)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python code examples and optional PPTX file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations usually include the top three layouts with scores, slide references, structure notes, and confirmation before PowerPoint generation.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
