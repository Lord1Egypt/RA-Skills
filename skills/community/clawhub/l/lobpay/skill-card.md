## Description:

LobPay Agent Skill - Purchase items via X402 protocol on Base network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[web3senior](https://clawhub.ai/user/web3senior)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use LobPay to retrieve checkout information, initiate X402 payment flows on the Base network, record purchases, view transaction history, and leave merchant feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs blockchain-backed purchase flows and can spend funds through wallet-based X402 payments.

Mitigation: Use a dedicated low-value wallet, prefer testnet, and require explicit confirmation of item, amount, merchant, network, and endpoint before running purchase commands.

Risk: The skill stores wallet private keys and API keys in local LobPay configuration.

Mitigation: Avoid entering private keys in shared shells or CI logs, restrict file access to the local configuration, and rotate credentials if exposure is suspected.

Risk: The API endpoint is configurable, so a wrong or untrusted endpoint could receive API credentials or payment requests.

Mitigation: Verify the LobPay API URL before use and send API keys only to trusted LobPay endpoints.

## Reference(s):

- [LobPay Skill Page](https://clawhub.ai/web3senior/skills/lobpay)
- [LobPay API Reference](references/api.md)
- [Database Schemas](references/schemas.md)
- [X402 Protocol Integration](references/x402.md)
- [X402 Spec](https://github.com/coinbase/x402)
- [Base Docs](https://docs.base.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JavaScript CLI behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing purchase, checkout, feedback, history, and configuration workflows that may call LobPay API endpoints and create local configuration or history files.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
