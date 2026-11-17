## Description:

Generates Chinese novel outlines from a genre, theme, and target word count using a 15-beat structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuzhihui886](https://clawhub.ai/user/yuzhihui886)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and writing agents use this skill during story planning to turn a short Chinese-language premise into a structured long-form novel outline with beats, character arcs, worldbuilding, foreshadowing, and writing tips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency ranges may resolve to different package versions over time.

Mitigation: Install in a virtual environment and consider pinning dependency versions or using a lockfile.

Risk: The tool writes Markdown output to a user-selected path and may create directories there.

Mitigation: Choose the output path intentionally and review the generated file before relying on it.

Risk: The skill expects Chinese-language inputs and produces Chinese-language output.

Mitigation: Use Chinese-capable review or translation when evaluating generated outlines for publication or production workflows.

## Reference(s):

- [15 Beat Structure Details](references/beat_sheet.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown novel outline]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output written to a selected Markdown file path.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
