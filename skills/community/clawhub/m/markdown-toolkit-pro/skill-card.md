## Description:

Markdown 工具箱专业版 helps teams manage multi-file Markdown documentation sites, including TOC generation, lint rules, link checks, and export workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and documentation teams use this skill to plan and automate multi-file Markdown site generation, documentation linting, link checking, and HTML/PDF/DocBook export workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for command execution and file-writing authority without tight scoping.

Mitigation: Run it only for explicit documentation tasks, preferably within a limited docs directory, and review commands before execution.

Risk: Export, delete, global install, network check, or bulk rewrite actions could change files or environment state beyond the intended documentation task.

Mitigation: Confirm those actions before allowing them and review generated changes before keeping them.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples, configuration snippets, and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose file writes and command execution for documentation tasks; validate commands before running in sensitive repositories.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
