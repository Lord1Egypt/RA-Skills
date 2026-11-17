## Description:

Scans GitHub Issues and Algora bounties, scores opportunities by value, competition, and freshness, and returns recommendations for developers seeking bounty work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, open source contributors, bounty hunters, and developer teams use this skill to discover paid GitHub and Algora work, filter out noisy opportunities, and prioritize bounties with lower visible competition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub and Algora API tokens are required for normal live scanning and could expose account access if stored or shared carelessly.

Mitigation: Use least-privilege, revocable tokens; keep .env files out of source control; rotate tokens if exposure is suspected.

Risk: Dependency versions are declared with ranges and no lockfile is present in the artifact evidence.

Mitigation: For stricter environments, request pinned dependency versions and a lockfile before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lvjunjie-byte/skills/github-bounty-finder)
- [Publisher profile](https://clawhub.ai/user/lvjunjie-byte)
- [GitHub personal access tokens](https://github.com/settings/tokens)
- [Algora API settings](https://algora.io/settings/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [CLI text output and optional JSON export, with Markdown documentation and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GitHub and Algora API tokens for live scans; demo mode can produce sample text output without API keys.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
