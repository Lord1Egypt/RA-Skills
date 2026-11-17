## Description:

IRIS代码格式化专业版 helps enterprise IRIS development teams review, format, configure rules for, and export reports about ObjectScript code quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review and format InterSystems IRIS ObjectScript projects, apply team-specific quality rules, and generate Markdown or HTML review reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad review and formatting instructions may lead an agent to propose changes outside the intended project scope.

Mitigation: Keep the skill pointed at explicit project directories and review proposed shell commands before execution.

Risk: Formatting, reset, import, save, or delete-style actions can modify project files.

Mitigation: Require a dry run or explicit confirmation before any change-making action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/iris-formatter-tool-pro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, YAML, JSON, HTML, and ObjectScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated review reports, configuration snippets, command proposals, execution logs, and structured JSON-style status output.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
