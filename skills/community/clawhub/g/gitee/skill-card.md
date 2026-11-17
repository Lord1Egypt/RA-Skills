## Description:

Gitee operations via OpenAPI and git for repositories, pull requests, issues, comments, file contents, and gitee.com remotes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvy](https://clawhub.ai/user/jvy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect and automate Gitee repositories, pull requests, issues, file reads, and git remote workflows from a terminal when no dedicated CLI is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Gitee access token can expose repository data or authorize repository changes if granted broad permissions.

Mitigation: Use a least-privilege token and prefer read-only permissions for inspection tasks.

Risk: Commands for creating issues, creating pull requests, updating files, or pushing branches can modify repository state.

Mitigation: Require explicit approval before running write operations or pushing branches.

## Reference(s):

- [Gitee OpenAPI v5 documentation](https://gitee.com/api/v5/swagger)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Configuration, Guidance]

**Output Format:** [Markdown with bash and jq command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, git, jq, and a Gitee access token for authenticated workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
