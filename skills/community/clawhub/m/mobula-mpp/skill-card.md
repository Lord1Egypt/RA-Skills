## Description:

Mpp Mobula lets agents fetch Mobula crypto prices, wallet positions, and market data through pay-per-call Tempo USDC.e wallet payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flotapponnier](https://clawhub.ai/user/flotapponnier)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to create or load low-balance Tempo wallets, make paid Mobula API calls, and return crypto price, wallet position, activity, or market data without an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a funded hot wallet for paid API calls, and the generic call path may be steered in ways that trigger unintended automatic wallet payments.

Mitigation: Use only a very low-balance wallet, avoid exposing generic paid calls to untrusted or model-generated paths, and require stronger validation of origin, endpoint path, challenge fields, recipient, and cumulative spend before automatic signing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flotapponnier/skills/mobula-mpp)
- [Publisher profile](https://clawhub.ai/user/flotapponnier)
- [Mobula MPP API](https://mpp.mobula.io)
- [Tempo bridge](https://relay.link/bridge/tempo)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [JSON API responses, terminal text, and Markdown documentation with TypeScript and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Networked calls may spend USDC.e from a funded hot wallet; the artifact describes encrypted wallet storage and a per-call payment cap.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
