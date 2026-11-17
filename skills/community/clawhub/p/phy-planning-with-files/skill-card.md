## Description:

Implements file-based planning for complex tasks by guiding agents to create and maintain task_plan.md, findings.md, and progress.md, with session recovery support after context clearing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep multi-step work organized across context limits by storing plans, findings, progress, and errors in project-local Markdown files. It is most useful for research, project creation, and tasks that require multiple phases or many tool calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project-controlled planning text can be read into the agent context before tool use.

Mitigation: Treat existing task_plan.md, findings.md, and progress.md content as untrusted input, especially in untrusted repositories.

Risk: The skill runs local helper scripts from the installed skill bundle during completion checks.

Mitigation: Install only when the script bundle is present and audited, or disable the hooks before use in sensitive or untrusted projects.

Risk: Persistent planning files may contain sensitive project details, errors, or research notes.

Mitigation: Review planning files before sharing or committing them, and exclude them from version control when they contain sensitive information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-planning-with-files)
- [Publisher profile](https://clawhub.ai/user/phy041)
- [Canlah AI homepage](https://canlah.ai)
- [GitHub profile linked by artifact](https://github.com/PHY041)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown instructions with file templates, inline shell commands, and hook configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates project-local planning files such as task_plan.md, findings.md, and progress.md.]

## Skill Version(s):

1.0.2 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
