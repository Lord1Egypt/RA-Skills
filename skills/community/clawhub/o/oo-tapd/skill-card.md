## Description:

TAPD (tapd.cn). Use this skill for ANY TAPD request — searching and reading data. Whenever a task involves TAPD, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use the skill to search and read TAPD project data, including bugs, iterations, stories, tasks, wikis, and project details, through their connected TAPD account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup executes downloaded code, and the installer contents have not been verified.

Mitigation: Review and approve a fixed CLI release before installation.

Risk: The CLI dependency can install other agent skills, and automatic synchronization may add skills beyond TAPD access.

Mitigation: If only TAPD access is needed, consider disabling automatic skill synchronization with OO_SKILLS_SYNC_DISABLED.

Risk: Deployed connector behavior remains unverified, and account access depends on the connected TAPD account and project scopes.

Mitigation: Connect only the intended TAPD account and limit requested projects.

## Reference(s):

- [oo CLI project documentation](https://github.com/oomol-lab/oo-cli)
- [TAPD homepage](https://www.tapd.cn/)
- [TAPD API documentation](https://open.tapd.cn/document/api-doc/API文档/api_reference/)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON connector responses with user-facing text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only TAPD queries; results may be paginated for list actions.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
