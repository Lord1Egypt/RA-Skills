## Description:

Interact with GitHub using the `gh` CLI for issues, pull requests, CI runs, and advanced API queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengxinjipai](https://clawhub.ai/user/zhengxinjipai)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to ask an agent for GitHub CLI commands and usage guidance for issues, pull requests, workflow runs, and GitHub API queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated GitHub CLI commands can mutate repository data using the authenticated account's permissions.

Mitigation: Review commands before execution, especially commands that create, edit, delete, merge, close, rerun, or otherwise change repository data.

## Reference(s):

- [GitHub CLI Skill on ClawHub](https://clawhub.ai/zhengxinjipai/skills/github-cli-tool)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the GitHub CLI (`gh`) and uses the permissions of the authenticated local GitHub account.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
