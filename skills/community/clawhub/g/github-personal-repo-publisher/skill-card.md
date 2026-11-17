## Description:

Creates a repository under a personal GitHub account, connects a local Git project to it, and pushes committed history safely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grey0758](https://clawhub.ai/user/grey0758)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to publish a local Git repository to their personal GitHub account, create the remote repository if needed, wire origin, push committed history, and report any local-only changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow hardcodes a specific GitHub account, SSH alias, and 1Password PAT reference.

Mitigation: Install or run it only when `grey0758`, `github-grey0758`, and the named 1Password PAT are intentionally the configured account details.

Risk: The workflow can rewire a repository remote and push committed code.

Mitigation: Before execution, confirm the GitHub login, repository owner/name, visibility, current `origin`, final push URL, and branch to be pushed.

Risk: The workflow may be inappropriate for proprietary or sensitive repositories if the account or visibility is wrong.

Mitigation: Avoid using it on proprietary or sensitive repositories unless account, repository, visibility, remote, and branch checks pass.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/grey0758/skills/github-personal-repo-publisher)
- [README](README.md)
- [Workflow](WORKFLOW.md)
- [FAQ](FAQ.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and concise status reporting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports local repository status, GitHub repository creation or existence, remote wiring, push status, and remaining local-only work.]

## Skill Version(s):

1.0.0 (source: server release metadata and CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
