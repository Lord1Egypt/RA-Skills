## Description:

Retrieve Solana token data, community content, market sentiment, watchlists, and token-related API guidance through OpenDEX endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solpenguin](https://clawhub.ai/user/solpenguin)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to look up Solana token market data, community-submitted content, sentiment, and watchlist state through the OpenDEX API. It can also guide API-key registration and wallet-signed submission or voting workflows when the user explicitly authorizes those actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses can expose user activity or identity context when used in lookups, key registration, sentiment, or watchlist actions.

Mitigation: Use wallet addresses only when necessary, prefer read-only token lookups, and avoid submitting another person's wallet address.

Risk: Unauthenticated watchlist and sentiment endpoints can change wallet-linked state.

Mitigation: Require explicit user approval before any watchlist or sentiment-changing request and show the wallet and mint address before sending it.

Risk: API keys are returned once and can authorize community content requests.

Mitigation: Store API keys securely, avoid logging or displaying full keys, and revoke keys that are no longer needed.

## Reference(s):

- [OpenDEX Skill Page](https://clawhub.ai/solpenguin/skills/opendex)
- [OpenDEX API Base URL](https://opendex-api-dy30.onrender.com)
- [OpenDEX Web API Page](https://opendex.online/api.html)
- [OpenDEX Frontend](https://opendex.online)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with endpoint examples, JSON payloads, and curl-style commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only lookups are public and rate-limited; API-key and wallet-linked workflows require explicit key, wallet, or signature handling.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
