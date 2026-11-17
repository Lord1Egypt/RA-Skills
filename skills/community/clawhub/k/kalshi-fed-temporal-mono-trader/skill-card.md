## Description:

Exploits temporal monotonicity violations in Fed rate markets on Kalshi by scanning for cases where an earlier Fed-rate outcome is priced higher than a later inclusive outcome, and requires SIMMER_API_KEY and simmer-sdk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading-oriented developers use this skill to scan Kalshi Fed rate markets for temporal monotonicity violations, review detected signals, and optionally execute or manage trades through Simmer SDK in paper or live mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can execute real-money trades using high-value trading credentials and a Solana private key.

Mitigation: Use paper mode unless live automated trading is intentional; if live mode is used, use dedicated low-balance wallets and tightly limited trading credentials.

Risk: The strategy is broader than its arbitrage framing and may be speculative if both sides of the claimed arbitrage are not validated and executed.

Mitigation: Treat the strategy as speculative unless the implementation is changed or externally reviewed to validate and execute both legs before live use.

Risk: Credential exposure could affect funds or trading authority.

Mitigation: Do not provide a main Solana wallet private key, and rotate or revoke credentials after testing or suspected exposure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/kalshi-fed-temporal-mono-trader)
- [Publisher profile](https://clawhub.ai/user/diagnostikon)
- [Simmer Markets skills](https://simmer.markets/skills)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Console text, JSON automaton summaries, and Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce dry-run trade recommendations, live trade attempts when --live is used, position summaries, and configuration updates.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
