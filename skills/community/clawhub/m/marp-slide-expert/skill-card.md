## Description:

Helps create and refine Marp slide decks from Markdown, including layouts, inline SVG diagrams, image preparation, and rendering checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mebusw](https://clawhub.ai/user/mebusw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other presentation creators use this skill to turn Markdown into Marp slide decks with layouts, diagrams, speaker notes, and practical export guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unreviewed or globally installed packages and commands may affect the local environment.

Mitigation: Pin package versions or use a reviewed Git commit; review commands before running them and avoid global installs when unnecessary.

Risk: Speaker notes hidden from slides remain visible in the source Markdown.

Mitigation: Review and remove confidential notes before sharing the source deck.

Risk: The optional Obsidian plugin fix changes a local plugin file.

Mitigation: Apply it only after reviewing the change and confirming that modifying the plugin is intended.

## Reference(s):

- [Publisher's source repository](https://github.com/mebusw/marp-slide-expert)
- [Marp Slide Expert on ClawHub](https://clawhub.ai/mebusw/skills/marp-slide-expert)
- [Marpit documentation](https://marpit.marp.app/)
- [Image syntax and asset preparation](artifact/references/image-syntax.md)
- [Slide layout patterns](artifact/references/layout-patterns.md)
- [SVG infographic guidance](artifact/references/infographics-svg/INDEX.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Guidance]

**Output Format:** [Marp Markdown with optional inline SVG and CSS, plus rendering guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PDF, HTML, and PPTX exports require a separate Marp rendering step.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
