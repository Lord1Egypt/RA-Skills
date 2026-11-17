## Description:

Helps agents create, edit, and inspect PowerPoint presentations, with optional image generation and quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mebusw](https://clawhub.ai/user/mebusw)

### License/Terms of Use:

MIT-0

## Use Case:

People preparing presentations use this skill to generate editable slide decks, revise existing PPTX files, and review slide content and layout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional image generation or QA may share sensitive deck content with other skills or services.

Mitigation: Review data handling before enabling these options; avoid using them for sensitive decks unless approved.

Risk: The LibreOffice helper may load unsafe native code from a shared temporary location.

Mitigation: Use an isolated workspace, avoid shared multi-user hosts, and review or control the helper before routine use.

Risk: Installing dependencies without review may introduce untrusted code.

Mitigation: Review the skill and pin or inspect its dependencies before installation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/mebusw/skills/jackyshen-gen-pptx)
- [Server-resolved source repository](https://github.com/mebusw/jackyshen-gen-pptx)
- [Presentation creation guide](artifact/creating.md)
- [Presentation editing guide](artifact/editing.md)
- [Slide layouts](artifact/references/slide-layouts.md)
- [PptxGenJS documentation](https://gitbrent.github.io/PptxGenJS/)

## Skill Output:

**Output Type(s):** [Files, Code, Guidance]

**Output Format:** [PPTX presentations, JavaScript source, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional images and quality checks when requested.]

## Skill Version(s):

0.1.2 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
