## Description:

A Chinese-language novel-writing workflow skill that guides an agent from story direction through outline planning, chapter drafting, quality checks, and final delivery using FBS workflow scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z625662197](https://clawhub.ai/user/z625662197)

### License/Terms of Use:

MIT-0

## Use Case:

External writers, developers, and agent operators use this skill to plan and produce long-form Chinese web-novel manuscripts with structured stages, persistent book memory, chapter tracking, quality gates, and delivery checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read project files and possibly WorkBuddy profile or memory data.

Mitigation: Use it only in workspaces where that access is acceptable; disable or review host-profile import before using confidential manuscripts.

Risk: External search can expose manuscript context or research queries outside the local workspace.

Mitigation: Disable or explicitly review network search for confidential projects and keep search use auditable.

Risk: Bundled maintenance, publishing, and self-evolution scripts can change project state or release artifacts.

Mitigation: Require explicit manual review and command approval before running those scripts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/z625662197/skills/novel-architect)
- [FBS-BookWriter Homepage](https://fbs-bookwriter.u3w.com/)
- [Artifact Skill Definition](artifact/SKILL.md)
- [Artifact Script Index](artifact/scripts/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write manuscript state, memory files, chapter drafts, deliverables, and audit reports under a configured book root.]

## Skill Version(s):

1.2.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0 and package.json reports 2.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
