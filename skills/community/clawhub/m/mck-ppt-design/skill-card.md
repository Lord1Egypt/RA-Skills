## Description:

Create professional, consultant-grade PowerPoint presentations from scratch using python-pptx with McKinsey-style design.

This skill is ready for commercial/non-commercial use.

## Publisher:

[likaku](https://clawhub.ai/user/likaku)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and business teams use this skill to create polished strategy decks, board presentations, quarterly reviews, pitch decks, and other consultant-style PPTX deliverables from structured prompts or generated Python code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated PPTX files may be sent to chat channels without a per-send confirmation step.

Mitigation: Use the skill in a controlled environment, pin dependencies, and remove or gate deliver_to_channel() when local-save-only behavior is required.

Risk: Confidential business, board, or strategy deck content could be exposed if automatic channel delivery is enabled in the wrong environment.

Mitigation: Review generated scripts before execution and disable channel delivery for sensitive presentations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/likaku/skills/mck-ppt-design)
- [Color Palette Quick Reference](references/color-palette.md)
- [Layout Catalog](references/layout-catalog.md)
- [python-pptx documentation](https://python-pptx.readthedocs.io)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with Python code and shell commands; generated artifacts are PPTX files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated scripts may save PPTX files locally and send them through available OpenClaw messaging channels.]

## Skill Version(s):

2.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
