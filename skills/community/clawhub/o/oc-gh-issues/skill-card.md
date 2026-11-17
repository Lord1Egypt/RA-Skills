## Description:

Fetch GitHub issues, select candidates, spawn background fix agents, open PRs, and optionally process PR review comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and repository maintainers use this skill to find actionable GitHub issues, delegate fixes, open pull requests, and handle review comments. It can also report candidates without making changes when run in dry-run mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The --yes and --cron modes skip per-run confirmation and can dispatch agents that create branches and open pull requests.

Mitigation: Use --dry-run to review candidates first and keep interactive confirmation enabled unless unattended execution is intended; review generated branches and pull requests before merging.

## Reference(s):

- [Gh Issues on ClawHub](https://clawhub.ai/hillstreet-ph/skills/oc-gh-issues)
- [Publisher profile: hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Text]

**Output Format:** [Issue and pull request summaries with links; code changes in worker branches and pull requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run, interactive selection, watch, reviews-only, and unattended cron modes.]

## Skill Version(s):

1.0.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
