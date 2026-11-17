## Description:

Maxxit 0G Trading helps agents use Maxxit Lazy Trading with 0G decentralized compute for portfolio-aware trade decisions, DEX trading workflows, market research, copy trading, and alpha marketplace listings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhi152003](https://clawhub.ai/user/abhi152003)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading agents use this skill to inspect Maxxit Lazy Trading account state, request market research, route confirmed trades across supported venues, run bundled strategy scripts, and interact with alpha listings backed by 0G storage proofs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled strategy scripts can place leveraged trades automatically.

Mitigation: Use separate exposure limits, dry-run behavior where available, and explicit approval before running scripts against funded accounts.

Risk: Trading API credentials are sent to a configurable API URL.

Mitigation: Verify MAXXIT_API_URL is the intended Maxxit HTTPS origin before use and revoke API keys promptly if misconfiguration or suspicious behavior is observed.

Risk: Delegated trading keys may permit real financial activity.

Mitigation: Use only API keys the user is willing to delegate, scope or rotate keys where possible, and monitor open positions after automated runs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/abhi152003/skills/maxxit-0g)
- [Maxxit App](https://maxxit.ai)
- [Maxxit Lazy Trading Setup](https://maxxit.ai/lazy-trading)
- [0G](https://0g.ai)
- [Binance Klines API](https://api.binance.com/api/v3/klines)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with curl examples, Python strategy commands, API call guidance, and concise trading workflow summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MAXXIT_API_KEY and MAXXIT_API_URL; bundled scripts can create or update trading positions through Maxxit programmatic endpoints.]

## Skill Version(s):

0.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
