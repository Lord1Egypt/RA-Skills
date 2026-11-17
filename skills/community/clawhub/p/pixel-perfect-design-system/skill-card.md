## Description:

Pixel Perfect Design System generates AI-readable Markdown design systems for vibe-coding apps, covering Chinese and English site patterns, bundled product-style templates, and nine-part UI guidance without requiring Figma.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijinhongucl-pixel](https://clawhub.ai/user/lijinhongucl-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to generate DESIGN.md files that give coding agents concrete UI guidance for page and component creation. It is intended for local design-system generation and design-standardization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local Python generator can create or overwrite the output path supplied by the user.

Mitigation: Run it in the intended project directory, choose an explicit output filename, and review or back up existing files before generation.

Risk: The documentation is largely Chinese, and the CLI may not expose every bundled template despite the 58-template claim.

Mitigation: Use the list command to confirm available templates and review generated DESIGN.md content before relying on it for production UI work.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lijinhongucl-pixel/skills/pixel-perfect-design-system)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Introduction](artifact/INTRODUCTION.md)
- [Code Audit Report](artifact/CODE_AUDIT_REPORT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Python 3 and can create or overwrite the output path supplied by the user.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
