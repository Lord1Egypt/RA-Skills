## Description:

Automated code review assistant that analyzes code changes, pull requests, and files for quality issues, best-practice gaps, security concerns, and style violations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michealxie001](https://clawhub.ai/user/michealxie001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review selected files, staged Git changes, commits, or diff files before commit, pull request review, or CI submission. It produces issue summaries, per-file findings, line references, metrics, and suggested fixes for supported Python, JavaScript, and TypeScript files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the files or Git changes selected by the user, which may include proprietary source paths, snippets, or findings.

Mitigation: Run it only on repositories and file sets appropriate for local review, and review generated reports before sharing or uploading them.

Risk: The --output option can overwrite the target report file.

Mitigation: Choose an explicit report path and check whether the file already exists before writing output.

Risk: CI report artifacts may expose proprietary filenames, snippets, metrics, or security findings.

Mitigation: Review CI artifact retention, access controls, and upload settings before publishing generated reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/michealxie001/skills/openclaw-code-review)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance, shell commands, configuration]

**Output Format:** [Markdown or JSON reports with issue summaries, file details, line references, metrics, and suggested fixes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write reports to a user-specified output path and can return a nonzero exit code when --fail-on-error is enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
