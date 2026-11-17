## Description:

Interact with GitLab using the `glab` CLI for merge requests, CI/CD pipelines, issues, releases, and API requests across gitlab.com and self-hosted instances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[portavion](https://clawhub.ai/user/portavion)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to let an agent work with GitLab projects through the `glab` CLI, including merge requests, CI/CD pipelines, issues, releases, variables, and REST or GraphQL API queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples can change repository state through merge request approval, merge, release creation, CI retry, issue updates, variable changes, and raw API commands.

Mitigation: Confirm the target GitLab project, merge request, issue, release tag, variable name, and command intent before execution.

Risk: CI/CD variable and API commands can expose or modify sensitive project data.

Mitigation: Do not reveal secret CI/CD variable values in chat or logs, and treat raw REST or GraphQL API calls as sensitive operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/portavion/skills/glab-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-oriented `glab api` and `jq` command patterns for automation.]

## Skill Version(s):

1.0.0 (source: evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
