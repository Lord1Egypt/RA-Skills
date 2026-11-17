## Description:

PPT-Matcher analyzes existing PPTX presentations to extract color, font, layout, and decorative patterns so agents can redesign or add slides with consistent styling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuobadaidai](https://clawhub.ai/user/tuobadaidai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, presentation editors, and file-agent workflows use this skill to analyze a reference PowerPoint deck, extract visual style guidelines, and produce slide content or layout specifications that keep new or revised pages visually consistent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Slide edits can delete, recreate, or materially alter important presentation pages.

Mitigation: Work on a copy of the deck and confirm exact slide numbers before any page is deleted or recreated.

Risk: Installing runtime dependencies from an untrusted source can introduce supply-chain risk.

Mitigation: Install python-pptx in a virtual environment from a trusted package index, ideally with pinned versions.

## Reference(s):

- [Common PPT page design patterns](artifact/references/design-patterns.md)
- [PPT-Matcher ClawHub release](https://clawhub.ai/tuobadaidai/skills/ppt-matcher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and console analysis output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference a local PPTX path and optional comma-separated slide numbers; depends on python-pptx.]

## Skill Version(s):

1.1.0 (source: frontmatter, server release metadata, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
