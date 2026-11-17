## Description:

Enhanced Memory gives OpenClaw agents a structured local memory system with categorized Markdown files, inline tag search, query routing, and lifecycle archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fatcatmaofei](https://clawhub.ai/user/fatcatmaofei)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to organize agent memory into searchable local Markdown stores, retrieve relevant memory by tag or query type, and archive older entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The archiving script can remove active memory files and may silently overwrite archived files despite the skill's stated retention behavior.

Mitigation: Review the lifecycle script before use, keep backups, and do not enable scheduled archival until overwrite protection, copied-file verification, and dry-run behavior are added.

Risk: Long-lived local memory can retain secrets, regulated personal data, or sensitive relationship details.

Mitigation: Avoid storing sensitive data unless long-term local retention is acceptable, and review memory contents before sharing or backing up the workspace.

## Reference(s):

- [Tagged Memory Architecture Reference](references/architecture.md)
- [ClawHub Skill Page](https://clawhub.ai/fatcatmaofei/skills/openclaw-enhanced-memory)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python scripts and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Markdown memory files and Python standard-library scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
