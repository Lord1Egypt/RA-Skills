## Description:

Helps agents use a Python CLI to open and list GitHub pull requests, check commit status, and push a single file to a remote branch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect pull requests and commit status or make targeted GitHub repository changes without installing the git or gh command-line tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A GitHub personal access token may grant the agent permission to alter repositories.

Mitigation: Use a least-privilege token and grant access only to the repositories needed.

Risk: Pull request creation and file pushes change remote repository state without a technical confirmation step.

Mitigation: Preview write commands with --dry-run and verify the repository, branch, file path, and commit or pull request details before executing them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/github-workflow-integration)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain-text CLI results and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports pull request details, commit status, or a commit SHA; CLI exit codes distinguish success, API errors, and usage errors.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
