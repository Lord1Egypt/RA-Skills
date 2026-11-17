## Description:

Creates consultant-grade PowerPoint presentations from scratch with python-pptx, using a McKinsey-style design system with layout patterns, typography, and file-compatibility guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[likaku](https://clawhub.ai/user/likaku)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers, analysts, consultants, and business teams use this skill to generate professional PPTX decks and reusable python-pptx code patterns for strategy decks, board presentations, dashboards, timelines, and other business presentations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation may introduce supply-chain or reproducibility risk when python-pptx, lxml, or mutable @latest commands are used without review.

Mitigation: Install in a virtual environment or low-privilege workspace, pin dependency versions, and review packages before use.

Risk: The skill can create or modify local PPTX files during normal use.

Mitigation: Run it in a workspace where generated presentation files are expected, and review outputs before distributing them.

Risk: Generated presentations apply a Chinese/English typography style by default.

Mitigation: Customize fonts and style settings when the default KaiTi, Georgia, and Arial treatment is not appropriate for the audience or environment.

## Reference(s):

- [Color Palette Quick Reference](references/color-palette.md)
- [Layout Catalog - 36 Slide Types](references/layout-catalog.md)
- [Project Homepage](https://github.com/likaku/Mck-ppt-design-skill)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with python-pptx code snippets and shell commands; generated artifacts are PPTX files when the agent executes the code.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, pip, python-pptx, and lxml; examples save local PPTX files.]

## Skill Version(s):

1.6.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
