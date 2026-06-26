## Description: <br>
Place Polymarket trades through Aionmarket when the user wants to search markets, register wallet credentials, verify a wallet, or submit an order with an Aionmarket API key, Polymarket CLOB credentials, wallet private key, or pre-signed EIP712 order. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fivegive249-ship-it](https://clawhub.ai/user/fivegive249-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare, inspect, and submit Polymarket trades through Aionmarket, including wallet credential registration, market review, signed order submission, and post-trade checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can handle live trading credentials and an optional wallet private key. <br>
Mitigation: Prefer pre-signed orders or scoped, revocable credentials; treat secrets as transient; never persist them in files, examples, commits, logs, or markdown artifacts. <br>
Risk: Live orders can execute unintended trades if market, side, size, price, order type, or endpoint details are wrong. <br>
Mitigation: Independently verify the Aionmarket endpoint and require explicit approval for each live order with the exact market, side, size, price, and order type before execution. <br>


## Reference(s): <br>
- [Aionmarket Polymarket Reference](references/aionmarket-polymarket.md) <br>
- [Aionmarket SDK Reference](references/aionmarket-sdk.md) <br>
- [Trade Request Template](assets/trade-request-template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/fivegive249-ship-it/polymarket-aion-trader) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, API calls, Configuration guidance] <br>
**Output Format:** [Markdown guidance with Python SDK snippets, REST endpoint details, and structured trade intake fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Aionmarket API key for authenticated actions and may require Polymarket CLOB credentials plus either a pre-signed EIP712 order or wallet private key for local signing.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
