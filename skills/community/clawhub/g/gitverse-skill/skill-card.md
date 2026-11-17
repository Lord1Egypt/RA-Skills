## Description:

Own GitVerse (gitverse.ru) skill: repos, issues, PRs via REST API with a dependency-free Python CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[viknsagit](https://clawhub.ai/user/viknsagit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage GitVerse repositories, issues, and pull requests from an agent-accessible Python CLI. It supports repository lookup plus issue and pull request list, view, create, comment, close, and merge workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends a bearer token to an API base URL that can be changed with GITVERSE_BASE_URL.

Mitigation: Leave GITVERSE_BASE_URL unset unless a trusted HTTPS GitVerse API endpoint is required, and use a narrowly scoped token.

Risk: Issue creation, comments, issue closure, pull request creation, and pull request merge commands can change repository state.

Mitigation: Require explicit confirmation before write or merge actions and review the target owner, repository, issue, branch, and pull request number before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/viknsagit/skills/gitverse-skill)
- [GitVerse token settings](https://gitverse.ru/settings/tokens)
- [Default GitVerse API endpoint](https://api.gitverse.ru)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with bash commands; CLI responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GitVerse bearer token from GITVERSE_TOKEN or ~/.gitverse_token.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
