## Description:

Read-only Polymarket interface for browsing trending markets, viewing detailed odds, searching active markets, and tracking watchlists without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingmadellc](https://clawhub.ai/user/kingmadellc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect public Polymarket market data, compare probabilities, search active markets, and monitor configured watchlists. It is informational and read-only; it does not place trades or require account credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes public HTTP requests to Polymarket Gamma and CLOB APIs.

Mitigation: Install only in environments where outbound requests to gamma-api.polymarket.com and clob.polymarket.com are acceptable, and review domain permissions before deployment.

Risk: The skill creates and reads a local watchlist state directory under ~/.openclaw/state.

Mitigation: Use non-sensitive market slugs in watchlists and review local file permissions on shared systems.

Risk: Market outputs can be delayed, unavailable, or temporarily stale because they depend on public APIs and short-lived caching.

Mitigation: Treat results as informational market data and verify time-sensitive values against the source before making decisions.

## Reference(s):

- [Polymarket API Reference](references/api-reference.md)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)
- [Polymarket CLOB API](https://clob.polymarket.com)
- [ClawHub Skill Page](https://clawhub.ai/kingmadellc/skills/polymarket-command-center)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style text with market summaries, probability bars, market slugs, links, and status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public market data; responses may use short-lived in-memory caching; watchlist output depends on local watchlist configuration.]

## Skill Version(s):

1.1.0 (source: server release metadata; changelog: v1.1.0 unified stack release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
