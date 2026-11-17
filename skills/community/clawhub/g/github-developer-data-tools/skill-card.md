## Description:

GitHub & Developer Data gives AI agents live GitHub repository metadata, repository audits and risk scoring, user profiles, recent releases, and gist content through paid x402 HTTPS GET endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colinhughes2121](https://clawhub.ai/user/colinhughes2121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, dependency reviewers, and dev-tool agents use this skill to look up live GitHub repository, release, user, and gist data. It supports developer research, open source dependency due diligence, repository audits, and related automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger paid x402 API calls and the security evidence notes that automatic wallet payment is described without confirmation, budget, maximum price, or retry safeguards.

Mitigation: Use only with a wallet or runtime that requires explicit payment confirmation, enforces a maximum price per call, applies a session budget, and limits retries; treat repeated lookups as potentially billable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/colinhughes2121/skills/github-developer-data-tools)
- [Publisher Profile](https://clawhub.ai/user/colinhughes2121)
- [GoCreative API Base URL](https://api.gocreativeai.com)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, Guidance]

**Output Format:** [JSON API responses with concise agent-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid x402 HTTPS GET calls that may incur USDC charges per request.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
