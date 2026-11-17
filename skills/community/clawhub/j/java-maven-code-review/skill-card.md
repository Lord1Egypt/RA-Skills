## Description:

Review a Java Maven project delivered as a ZIP archive or a GitLab repository URL for code规范, naming, module boundaries, maintainability problems, duplicated logic, structure issues, and整改建议.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrliugangqiang](https://clawhub.ai/user/mrliugangqiang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Java Maven projects for naming, structure, module-boundary, maintainability, duplication, and configuration-risk issues. It produces a formal code review report with evidence, impact, and remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads Java/Maven project files, including configuration files that may contain secrets.

Mitigation: Use it only with projects that may be exposed to the agent environment, and review generated reports for sensitive content before sharing.

Risk: The skill creates review output files and may overwrite an existing report if the same path is reused.

Mitigation: Choose a fresh report filename or review the target business/ path before running the report workflow.

Risk: Rule-based findings can miss design problems or flag items that require project-specific interpretation.

Mitigation: Treat the report as a first-pass review and confirm important findings with human code review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrliugangqiang/skills/java-maven-code-review)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown report written under business/, with structured scan findings available as JSON when the bundled scanner is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include project scope, findings, evidence, impact, and suggested remediation.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
