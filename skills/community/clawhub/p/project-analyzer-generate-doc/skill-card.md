## Description:

Java Maven multi-module project documentation generator. Supports MyBatis SQL mapping, Maven dependency analysis, generates L3(file-level) to L2(module-level) to L1(project-level) hierarchical docs. Features task monitoring, auto-retry, checkpoint resume, and health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[endcy](https://clawhub.ai/user/endcy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate hierarchical Markdown documentation for Java, Maven, Spring Boot, and MyBatis projects. It supports full-project documentation, module-level summaries, file-level business logic descriptions, incremental updates, checkpoint resume, and task monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill scans source and configuration files, which may contain sensitive values.

Mitigation: Install only for repositories you are allowed to scan, and review and redact generated documentation before sharing or committing it.

Risk: Generated .ai-doc documentation and state files are persistent and may expose project structure or sensitive implementation details.

Mitigation: Add or keep .ai-doc in .gitignore unless the generated content has been reviewed and approved for publication.

Risk: Migration, merge, delete, or restore actions can change documentation files.

Mitigation: Do not confirm these actions until you have reviewed the proposed plan.

Risk: Subagents may process many project files during large documentation runs.

Mitigation: Avoid untrusted repositories unless the agent environment can confine subagents to the intended project files and output directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/endcy/skills/project-analyzer-generate-doc)
- [SKILL.md](SKILL.md)
- [README.md](README.md)
- [Checkpoint resume guide](references/checkpoint-resume.md)
- [Context compression guide](references/context-compression.md)
- [Incremental update flow](references/incremental-update.md)
- [Retry mechanism guide](references/retry-mechanism.md)
- [Task monitoring guide](references/task-monitoring.md)

## Skill Output:

**Output Type(s):** [markdown, files, guidance, shell commands, configuration]

**Output Format:** [Markdown documentation files, progress/status JSON, task logs, and concise execution summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated documentation under .ai-doc by default and may use configured subagent chunking, retry, and checkpoint behavior.]

## Skill Version(s):

2.1.4 (source: server release metadata and CHANGELOG-v2.1.4.md, released 2026-03-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
