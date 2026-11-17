## Description:

Read live market intelligence from a running Oracle-X terminal, including prices, candles, technical levels, news analysis, macro regime, chain metrics, derivatives positioning, ownership, prediction-market odds, and historical market memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yigtwxx](https://clawhub.ai/user/yigtwxx)

### License/Terms of Use:

MIT

## Use Case:

Developers and market-analysis agents use this skill to choose Oracle-X API endpoints, issue calls against a reachable Oracle-X instance, and summarize returned market data without inventing missing values. It is especially suited for building code or workflows around the Oracle-X API rather than replacing the running terminal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configurable Oracle-X URL can send user prompts, market questions, and bearer tokens to an untrusted or non-HTTPS service.

Mitigation: Use only a trusted Oracle-X instance, prefer HTTPS for remote ORACLE_X_URL values, and avoid sending ORACLE_X_TOKEN over plain HTTP except to localhost.

Risk: Authenticated chat, watchlist, and analysis-job calls can access personal account data or spend the operator's LLM provider budget.

Mitigation: Use open endpoints when authentication is not needed, keep ORACLE_X_TOKEN short-lived and scoped, and check cached/status endpoints before starting generation jobs.

Risk: Financial answers can become misleading if the terminal is unavailable, an upstream is degraded, payloads are stale, or symbols are unresolved.

Mitigation: Report only API-returned data with timestamps or stale flags, distinguish 404 and outage responses from valid empty data, and do not fill missing prices or technical levels from memory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yigtwxx/skills/oracle-x-api)
- [Oracle-X GitHub Repository](https://github.com/Yigtwxx/OracleX)
- [Oracle-X Endpoint Reference](references/endpoints.md)
- [Oracle-X Authentication Reference](references/auth.md)
- [Oracle-X Multi-Step Recipes](references/recipes.md)
- [Oracle-X API Examples](examples/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with endpoint paths, JSON-derived summaries, shell commands, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a reachable Oracle-X instance; authenticated chat, watchlist, and analysis-job endpoints require ORACLE_X_TOKEN.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact frontmatter reports 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
