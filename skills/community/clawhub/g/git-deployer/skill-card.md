## Description:

Push static site content to GitHub Pages repositories. Clone, copy files, commit with timestamp, force-push. Use when updating GitHub Pages sites, deploying static sites, or syncing local content to a git-based host.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kryzl19](https://clawhub.ai/user/kryzl19)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site maintainers use this skill to deploy local static site output to GitHub Pages or another git-backed hosting repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Forced pushes can overwrite the target branch, including shared branches.

Mitigation: Use a dedicated deployment repository or branch, least-privileged credentials, and confirm the target remote and branch before execution.

Risk: Checkout and copy behavior in a reused temporary clone can expose credentials or run unexpected local Git hooks.

Mitigation: Use a fresh private checkout, avoid credential-bearing HTTPS URLs, do not point the skill at untrusted site directories, and review logs before sharing them.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and deployment status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports success or failure, commit hash, target remote, branch, and push status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
