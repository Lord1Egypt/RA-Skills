## Description:

Interact with Gitea using the `tea` CLI. Use `tea issue`, `tea pr`, `tea actions`, and `tea api` for issues, PRs, Actions, and advanced queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[razzeee](https://clawhub.ai/user/razzeee)

### License/Terms of Use:


## Use Case:

Developers and repository maintainers use this skill to operate Gitea projects with the tea CLI, including issues, pull requests, Actions metadata, advanced API queries, and login configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using this skill with private repositories or CI/CD administration can expose sensitive repository data, Actions secrets, or token-scoped API access.

Mitigation: Use least-privilege, short-lived Gitea tokens; avoid pasting real tokens into chat or shell history; review `tea actions` and `tea api` commands before execution.

Risk: The Go install metadata resolves `code.gitea.io/tea@latest`, which may change the CLI version over time.

Mitigation: Pin and review the tea CLI version before using the skill in sensitive workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/razzeee/skills/gitea-2)
- [Tea CLI Go module](https://code.gitea.io/tea)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the tea CLI; some examples use jq for filtering.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
