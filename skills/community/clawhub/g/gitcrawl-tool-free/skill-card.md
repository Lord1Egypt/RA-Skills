## Description:

仓库归档搜索 helps agents query cached GitHub issue and pull request archives, check archive freshness, and run targeted gitcrawl or gh commands for repository history lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, contributors, and technical researchers use this skill to search a single repository's cached issue and pull request archive, inspect nearby discussions, and decide when a manual refresh or live GitHub check is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill permits command execution and local writes for gitcrawl and gh workflows.

Mitigation: Use it only in workspaces where gitcrawl and gh command execution is expected, and review proposed commands before execution.

Risk: Live GitHub queries may require GitHub authentication.

Mitigation: Use narrowly scoped GitHub tokens or GitHub CLI authentication and avoid embedding tokens in files or prompts.

Risk: The skill stores or updates local archive data under the user's home directory.

Mitigation: Confirm the cache location and data retention expectations before syncing repositories.

Risk: Security evidence says the instructions broaden into unrelated development and analytics tasks.

Mitigation: Limit use to repository issue and pull request archive search unless the publisher narrows the release instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/gitcrawl-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented command output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke gitcrawl and gh commands, may read repository archive data, and may maintain local cache data under the user's home directory.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
