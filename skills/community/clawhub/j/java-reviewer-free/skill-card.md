## Description:

Reviews Java code changes and produces structured review reports with issue severity, repair suggestions, and optional consistency checks against requirements or design documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review Java diffs or source files, identify code quality issues, and generate actionable Markdown or HTML review reports. It can also compare changes against supplied requirements or design documents for consistency checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for command execution and file-writing authority while its scope and safety controls are broad.

Mitigation: Use it in a limited workspace or read-only copy unless the publisher narrows the trigger scope, documents allowed commands, and makes report writing the only default mutation.

Risk: Generated review reports and repair suggestions may be incorrect or misleading.

Mitigation: Have a developer review findings and proposed fixes before applying code changes or relying on the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/java-reviewer-free)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report by default; optional HTML when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include issue severity, file and line references, repair suggestions, code snippets, and consistency checks when requirements or design documents are provided.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
