## Description:

Scans Kalshi sports markets against sportsbook odds to identify potential edge plays and optionally execute Kelly-sized Kalshi orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[themsquared](https://clawhub.ai/user/themsquared)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and traders use this skill to configure and run a Python scanner that compares Kalshi market prices with sportsbook-implied probabilities for NBA, NCAAB, NHL, and MLB markets. It is intended to surface candidate trades for review and can place live orders when explicitly run with buying enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can place live Kalshi orders with minimal safeguards.

Mitigation: Review all candidate plays manually, avoid --buy until the strategy and order payloads are understood, and use a dedicated low-balance Kalshi account or strict account limits.

Risk: The artifact ships hardcoded Odds API and Kalshi identifiers.

Mitigation: Replace hardcoded identifiers before use and manage credentials through environment-specific secret handling.

Risk: The script depends on local Python packages and external APIs.

Mitigation: Install dependencies in an isolated environment with pinned versions and confirm API behavior before allowing order execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/themsquared/skills/kalshi-odds-scanner-pro)
- [The Odds API](https://the-odds-api.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown setup and usage guidance, Python code, shell commands, and terminal text tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can make network API calls and place live Kalshi orders when the script is run with --buy.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-03-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
