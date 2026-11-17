## Description:

Provides read-only GitHub CLI workflows for agents that minimize token use with JSON field selection, result limits, compact jq output, caching, timeouts, retries, and write-operation blacklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moniq888](https://clawhub.ai/user/moniq888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to inspect GitHub repositories, pull requests, issues, CI runs, code, and metadata through read-only GitHub CLI commands while keeping responses compact and token efficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make read-only GitHub queries using the user's configured GitHub credentials.

Mitigation: Use a least-privilege token and confirm the target repositories are appropriate for agent-assisted read access.

Risk: Broad activation triggers may cause the skill to be used for more GitHub-related requests than intended.

Mitigation: Review planned commands before execution and keep use limited to explicit repository inspection tasks.

Risk: Temporary caching may expose private repository data on shared machines.

Mitigation: Disable or harden the cache for sensitive repositories and clear temporary cache files after use.

Risk: Automatic login guidance may encourage expanding GitHub credential access.

Mitigation: Avoid unnecessary scope refreshes and prefer read-only or narrowly scoped credentials.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/moniq888/skills/git-hub-cli-token)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are designed for compact read-only GitHub output using --json, --limit, jq -c, caching, timeouts, and truncation.]

## Skill Version(s):

1.0.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
