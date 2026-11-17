## Description:

Gitea (about.gitea.com). Use this skill for ANY Gitea request — reading, creating, updating, and deleting data. Whenever a task involves Gitea, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and repository maintainers use this agent skill to inspect and manage Gitea repositories, issues, pull requests, releases, and related resources through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup may run downloaded CLI code and install additional agent skills that have not been verified.

Mitigation: Review and explicitly approve a fixed, verified CLI release and any additional skills before installation.

Risk: Gitea write and destructive actions can change or delete account data.

Mitigation: Limit the connected account's permissions and retain confirmations for changes and deletions.

## Reference(s):

- [Gitea](https://about.gitea.com/products/gitea/)
- [Gitea API usage documentation](https://docs.gitea.com/development/api-usage)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Text]

**Output Format:** [Shell command examples with JSON action payloads and structured Gitea results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs the agent to inspect each action's schema and confirm state-changing or destructive actions with the user.]

## Skill Version(s):

1.0.7 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
