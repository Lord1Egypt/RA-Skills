## Description:

Convert Markdown research reports, fact-checks, and proposal documents into styled PDFs with native CJK font support while keeping Markdown as the editable source.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcjl](https://clawhub.ai/user/0xcjl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agent users use this skill to turn long-form Markdown research reports, fact-checks, and proposals into shareable PDF deliverables while preserving the Markdown source. It is especially focused on reports with Chinese or mixed CJK/English text, tables, links, and callout blocks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically send generated reports to chat platforms, which may disclose files to the wrong destination if the target is not checked.

Mitigation: Confirm the exact chat or platform before sending attachments and avoid target="all" unless broad delivery is explicitly intended.

Risk: Markdown-to-PDF conversion executes local Python dependencies and processes report content supplied by the user or agent.

Mitigation: Use trusted Markdown inputs, consider running conversion in an isolated environment, and pin dependencies for repeatable behavior.

Risk: The artifact includes unrelated personal template requirements that may not match another user's workflow.

Mitigation: Remove or ignore Jialin/Helen-specific template requirements unless they are intentionally part of the deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0xcjl/skills/md-pdf-report)
- [macOS CJK Font Reference](references/macos-cjk-fonts.md)
- [PDF Engine Comparison](references/pdf-engine-comparison.md)
- [weasyprint C Library Bootstrap Recipe](references/weasyprint-bootstrap.md)

## Skill Output:

**Output Type(s):** [markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; generated artifacts are Markdown source files and PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include optional HTML debug output when conversion is run with keep-html behavior.]

## Skill Version(s):

0.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
