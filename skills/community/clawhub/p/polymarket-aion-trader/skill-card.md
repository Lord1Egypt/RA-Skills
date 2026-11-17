## Description:

Place Polymarket trades through Aionmarket, including market search, wallet credential registration, wallet verification, and Polymarket order submission with Aionmarket and Polymarket credentials or a pre-signed EIP712 order.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fivegive249-ship-it](https://clawhub.ai/user/fivegive249-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare, inspect, and submit Polymarket trades through Aionmarket. It guides credential checks, wallet setup, market review, signed-order requirements, and post-trade follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can support live financial trading and may cause unintended order submission or financial loss if trade details are wrong.

Mitigation: Require final review of market, side, size, price, wallet, signed order, and live environment before submitting any order.

Risk: Wallet private keys, Polymarket CLOB credentials, and Aionmarket API keys could expose funds or accounts if shared or stored insecurely.

Mitigation: Prefer pre-signed orders or an external wallet/signer, request secrets only for the next required step, and do not write secrets to repository files, logs, commits, or markdown artifacts.

Risk: Using an unexpected Aionmarket endpoint could send credentials or signed orders to the wrong service.

Mitigation: Confirm the exact Aionmarket endpoint before sharing credentials or submitting trade payloads.

## Reference(s):

- [Aionmarket Polymarket Reference](references/aionmarket-polymarket.md)
- [Aionmarket SDK Reference](references/aionmarket-sdk.md)
- [Trade Request Template](assets/trade-request-template.md)
- [ClawHub Skill Page](https://clawhub.ai/fivegive249-ship-it/skills/polymarket-aion-trader)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration, API calls]

**Output Format:** [Markdown with inline code, JSON payload examples, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live-trading checklists, credential requirements, SDK setup guidance, REST endpoint guidance, signed-order payload guidance, and post-trade review steps.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
