## Description:

A Chinese-language multi-agent workflow for planning, drafting, reviewing, and refining long-form fiction projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[micromsf](https://clawhub.ai/user/micromsf)

### License/Terms of Use:

MIT-0

## Use Case:

Writers and agent builders use this skill to coordinate a serial novel workflow: project setup, worldbuilding, character design, chapter outlining, draft generation, quality review, and revision planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chapter range arguments in local shell scripts can lead to unintended command execution.

Mitigation: Review the scripts before use, run them only in a fresh version-controlled project directory, and pass simple numeric ranges such as 1-10 until safer input validation is added.

Risk: The workflow writes generated project files into a user-supplied directory.

Mitigation: Use a dedicated project directory and review generated Markdown files before publishing or reusing their content.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/micromsf/skills/novel-multi-agent-skill)
- [Artifact README](artifact/README.md)
- [Quickstart](artifact/QUICKSTART.md)
- [Skill overview](artifact/SKILL.md)
- [Collaboration workflow rules](artifact/rules/协作流程规范.md)
- [Quality scoring rules](artifact/rules/质量评分标准.md)
- [Content review rules](artifact/rules/内容审查红线.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files, shell command snippets, and structured workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates project scaffolding and staged writing artifacts such as outlines, drafts, review reports, and final manuscript files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
