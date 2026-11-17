## Description:

Place manual Polymarket trades through an agent, including FAK orders, GTC limit orders, market URL import, price discovery, and order cancellation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djdyll](https://clawhub.ai/user/djdyll)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to place or cancel manual Polymarket orders by giving an agent a market identifier or URL, side, amount, order type, and optional limit price.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place live Polymarket orders using private-key credentials.

Mitigation: Run only with a dedicated low-balance wallet, a scoped Simmer API key, conservative trade amounts, and explicit user approval before execution.

Risk: Cancellation mode can cancel real open orders and does not honor dry-run before cancellation.

Mitigation: Do not use dry-run as a cancellation safeguard; review the target market and side before running cancel commands.

Risk: Credentials are loaded from /root/.openclaw/.env, which may contain unrelated secrets.

Mitigation: Store only the required SIMMER_API_KEY and WALLET_PRIVATE_KEY for this trading workflow in the runtime environment.

Risk: Automatic price discovery and fallback pricing can lead to unintended execution prices.

Mitigation: Provide explicit prices for limit orders and review quoted book data before placing a trade.

Risk: The skill depends on simmer-sdk behavior for signing and order submission.

Mitigation: Pin and review the simmer-sdk version before installation or upgrade.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/djdyll/skills/polymarket-manual-trade)
- [Simmer Markets](https://www.simmer.markets/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command invocations and plain-text trade status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses environment variables for Simmer API and wallet credentials; can execute live trades when run without dry-run mode.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
