## Description:

Go安全质量检查专业版 helps Go development teams run dependency vulnerability checks, code security analysis, call-path review, batch project scans, CI/CD security gates, SARIF reporting, and vulnerability monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to guide Go repository security scanning with govulncheck and gosec, produce JSON or SARIF reports, and plan remediation for approved projects. It is intended for authorized security checks, compliance review, quality checks, and CI/CD security gate workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes remediation commands that can change repository dependencies and module files.

Mitigation: Require explicit user confirmation before dependency updates, run changes on a branch or disposable workspace, and review diffs and tests before merging.

Risk: Security scan outputs and SARIF reports may expose sensitive project, dependency, file path, or vulnerability details.

Mitigation: Run scans only on approved repositories and handle generated reports as sensitive artifacts with appropriate access controls.

Risk: Batch scans, tool installation, and uploads to GitHub Code Scanning can affect systems or services outside the immediate task.

Mitigation: Confirm the target scope, installation steps, and upload destination before execution, especially outside the current repository.

## Reference(s):

- [Detailed reference](artifact/references/detail.md)
- [SARIF 2.1.0 JSON Schema](https://json.schemastore.org/sarif-2.1.0.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, YAML, Python, JSON, and SARIF-oriented examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce scan summaries, execution logs, JSON reports, SARIF report files, CI snippets, and dependency update commands.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
