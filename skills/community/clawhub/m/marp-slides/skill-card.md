## Description:

Turn docs, notes, data, logs, screenshots, and code summaries into polished Marp slide decks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuller-stack-dev](https://clawhub.ai/user/fuller-stack-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and other external users use this skill to convert notes, reports, data, logs, screenshots, code summaries, and mixed source material into concise Marp presentations with a clear takeaway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may write source and rendered slide files containing user-provided material.

Mitigation: Review output paths and avoid including sensitive material unless the workspace and generated files are approved for that content.

Risk: The Marp CLI dependency can be installed without a pinned version.

Mitigation: Use a pinned or preinstalled Marp CLI version when stronger supply-chain control is required.

## Reference(s):

- [Marp](https://marp.app)
- [Marp Slide Patterns](references/slide-patterns.md)
- [Marp Output Formats](references/output-formats.md)
- [ClawHub skill page](https://clawhub.ai/fuller-stack-dev/skills/marp-slides)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Marp Markdown source plus rendered HTML, PDF, PPTX, notes text, PNG, or JPEG slide outputs when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keeps an editable *.slides.md source deck when rendering another output format.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
