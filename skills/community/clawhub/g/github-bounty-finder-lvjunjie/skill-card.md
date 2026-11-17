## Description:

Scan GitHub and Algora for high-value bounties, analyze competition and freshness, score opportunities, and provide actionable recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte)

### License/Terms of Use:

MIT

## Use Case:

Developers, bounty hunters, open source contributors, and dev agencies use this skill to scan bounty sources, rank opportunities by value and competition, and decide which issues to pursue.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses GitHub and Algora credentials for API access.

Mitigation: Use dedicated low-privilege credentials, keep .env files out of source control and shared workspaces, and rotate keys if exposure is suspected.

Risk: Terminal output and exported results can include public issue data and URLs from external services.

Mitigation: Treat printed and exported result content as untrusted before opening links, sharing files, or using results in downstream automation.

Risk: Dependency integrity depends on the package source and installed dependency versions.

Mitigation: Install from a reviewed package and prefer a lockfile or audited dependency versions before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lvjunjie-byte/skills/github-bounty-finder-lvjunjie)
- [Publisher profile](https://clawhub.ai/user/lvjunjie-byte)
- [GitHub personal access tokens](https://github.com/settings/tokens)
- [Algora API settings](https://algora.io/settings/api)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with CLI commands and optional JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print public issue titles, bounty URLs, competition signals, opportunity scores, and pricing recommendations.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
