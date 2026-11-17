## Description:

Trade on Hyperliquid. Supports 228+ perps, HIP-3 equity/commodity perps (TSLA, GOLD), market scanning, sentiment analysis, Grok web/X search, and prediction market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoan37](https://clawhub.ai/user/zoan37)

### License/Terms of Use:

MIT

## Use Case:

External users and agent developers use HyperClaw to retrieve Hyperliquid market and account data, scan trading opportunities, place or manage perpetual futures orders, and request optional Grok-powered market intelligence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make live financial trades on Hyperliquid.

Mitigation: Use a separate low-privilege Hyperliquid API wallet with limited funds, test on testnet first, and review commands before execution.

Risk: The skill runs an unauthenticated caching proxy with broader network exposure than users may expect.

Mitigation: Bind or firewall the proxy to localhost and do not expose the proxy port to other machines or containers.

Risk: The skill stores Hyperliquid credentials in a local .env file.

Mitigation: Treat the .env file as a private key store and keep HL_ACCOUNT_ADDRESS and HL_SECRET_KEY out of shared logs, prompts, and repositories.

Risk: Optional Grok intelligence commands may send user queries to xAI.

Mitigation: Avoid enabling Grok features unless users are comfortable sending those queries to xAI.

## Reference(s):

- [HyperClaw on ClawHub](https://clawhub.ai/zoan37/skills/hyperclaw)
- [Hyperliquid](https://hyperliquid.xyz)
- [Hyperliquid API keys](https://app.hyperliquid.xyz/API)
- [AgentSkills](https://agentskills.io)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, CLI output summaries, and JSON-like API data when commands request raw data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute account, market data, trading, proxy, and optional Grok-backed intelligence workflows through local scripts.]

## Skill Version(s):

0.1.15 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
