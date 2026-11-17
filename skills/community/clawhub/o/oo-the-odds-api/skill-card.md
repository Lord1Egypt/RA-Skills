## Description:

Use your OOMOL-connected account to search and read data from The Odds API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve odds, scores, events, markets, participants, and supported sports through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded software without a clear approval step, and the installer contents and exact system changes are unverified.

Mitigation: Review and approve CLI installation separately, preferably using a pinned, verified release.

Risk: API requests may consume account credits.

Mitigation: Check expected request costs and available credits before running actions.

## Reference(s):

- [The Odds API](https://the-odds-api.com)
- [The Odds API v4 documentation](https://the-odds-api.com/liveapi/guides/v4/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON API responses and shell commands with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only odds and sports data; action inputs are checked against the live connector schema.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
