## Description:

Detect mispriced correlations between Polymarket prediction markets and surface cross-market arbitrage signals for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sbaker5](https://clawhub.ai/user/sbaker5)

### License/Terms of Use:

MIT

## Use Case:

External developers and AI agents use this skill to compare two Polymarket markets, estimate correlation-based mispricing, and receive a signal with confidence and reasoning. The release also documents a paid live API path for querying the analyzer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled service includes a live paid API that handles Base USDC payments and has payment-replay and availability weaknesses.

Mitigation: Test paid flows only with a dedicated low-balance wallet, avoid production credentials, and validate payment consumption, caching, and availability controls before operational use.

Risk: The dashboard and payment-related data may be exposed if the service is published without protective controls.

Mitigation: Do not expose the dashboard publicly without authentication, rate limits, and review of disclosed payment or activity data.

Risk: Correlation signals may be incomplete because category-level estimates are rough, specific patterns require manual curation, and liquidity or slippage are not accounted for.

Mitigation: Treat outputs as decision-support analysis rather than financial advice, review assumptions manually, and verify market liquidity and execution costs independently.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sbaker5/skills/polyedge)
- [PolyEdge live correlation API](https://api.nshrt.com/api/v1/correlation?a=<slug>&b=<slug>)
- [PolyEdge dashboard](https://api.nshrt.com/dashboard)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)
- [BaseScan API](https://api.basescan.org/api)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON analysis with market summaries, mispricing estimates, confidence labels, and signal actions; Markdown guidance may include shell commands and configuration notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses market identifiers or slugs as inputs and may rely on live Polymarket, Base RPC, BaseScan, and paid API availability.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
