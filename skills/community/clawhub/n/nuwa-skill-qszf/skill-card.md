## Description:

女娲造人 — 输入人名/主题，自动深度调研蒸馏成可运行的Skill

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxy0905](https://clawhub.ai/user/dxy0905)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and internal skill authors use this skill to research a person or topic, distill source material into a thinking framework, and produce a runnable agent skill. It is aimed at skill creation workflows that may generate SKILL.md files, references, scripts, templates, and lifecycle guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may search broad local drives for books, documents, or papers.

Mitigation: Require explicit source paths, show a preview of candidate files before reading, and redact sensitive material before publishing generated skill artifacts.

Risk: The skill may automate web collection without enough scoping or consent controls.

Mitigation: Limit collection to approved domains and articles, review site terms before automation, and require operator approval before downloading or reusing collected content.

Risk: The installation guidance references an unpinned raw URL.

Mitigation: Use a pinned commit URL, checksum, or reviewed release artifact before installing the skill in a production agent environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dxy0905/skills/nuwa-skill-qszf)
- [ClawHub publisher profile](https://clawhub.ai/user/dxy0905)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated skill file specifications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe generated SKILL.md, references, scripts, and templates for downstream skill packaging.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata; artifact SKILL.md frontmatter states 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
