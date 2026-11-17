## Description:

Scan GitHub and Algora bounties to find high-value, low-competition opportunities with automated scoring and actionable recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, OSS contributors, bounty hunters, and agencies use this skill to scan GitHub Issues and Algora bounties, rank opportunities by value, competition, and freshness, and export results for review or automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub token permissions may exceed the read-only search behavior the skill needs.

Mitigation: Use unauthenticated public search when acceptable, or use a least-privileged, short-lived token without write, admin, workflow, or private-repository access.

Risk: Secrets are configured through environment variables and .env files, with weak secret-handling guidance in the artifact.

Mitigation: Keep .env files out of source control, restrict local file access, and rotate GitHub or Algora keys if exposure is suspected.

Risk: JSON export can overwrite the user-provided output path.

Mitigation: Write exports to a dedicated path and review the destination before running automated scans.

Risk: Dependencies are not pinned in the artifact.

Mitigation: Install in an isolated environment and review or lock dependencies before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lvjunjie-byte/skills/github-bounty-finder-cn)
- [GitHub Personal Access Tokens](https://github.com/settings/tokens)
- [Algora API Settings](https://algora.io/settings/api)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown-style agent guidance with CLI commands and optional JSON result exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18 or higher and may call GitHub and Algora APIs when configured with credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence, target metadata, package.json, and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
