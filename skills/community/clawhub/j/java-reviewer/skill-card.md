## Description:

Java代码 helps developers review Java diffs or source files and produce structured review reports with issue severity, code-level findings, and suggested fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review Java code changes, inspect git diffs or source files, and generate Markdown or HTML reports with prioritized issues and repair guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad command and file authority and may route beyond Java review into development, deployment, Git, or file-modifying workflows.

Mitigation: Use it only for explicit Java code review or report generation, and confirm any commands, file writes, Git operations, or deployment-related outputs before allowing execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/java-reviewer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown by default; HTML when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include issue counts, severity ordering, file and line references, code snippets, and suggested fixes.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
