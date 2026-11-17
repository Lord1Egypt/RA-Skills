## Description:

Official KYC-rip Monero Agent Skill. Manage XMR wallets on Mainnet/Stagenet via Ripley Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xbtoshi](https://clawhub.ai/user/xbtoshi)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and wallet operators use this skill to let an agent check Monero wallet status, create subaddresses, send XMR, and handle XMR402 payment challenges through a local Ripley Gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can authorize irreversible Monero transfers.

Mitigation: Use a minimally funded wallet, enforce gateway spending limits, and require manual approval for every transfer.

Risk: XMR402 payment flows can be triggered by outside websites.

Mitigation: Restrict paywalled requests to trusted HTTPS origins and require manual approval before paying any challenge.

Risk: Duplicate or replayed payment challenges can cause repeated spending.

Mitigation: Check the transaction log for an existing matching nonce before paying and recover proof instead of paying again.

Risk: AGENT_API_KEY grants wallet gateway authority.

Mitigation: Provide the key through the environment, avoid command-line exposure, and keep gateway access bound to the local trusted service.

Risk: The setup depends on external Docker components and Python dependencies.

Mitigation: Review or pin the external Docker setup and Python dependencies before use.

## Reference(s):

- [Ripley XMR Gateway](https://github.com/KYC-rip/ripley-xmr-gateway)
- [Ripley setup](https://kyc.rip/ripley)
- [XMR402 protocol](https://xmr402.org)
- [Monero Wallet skill page](https://clawhub.ai/xbtoshi/skills/monero-wallet)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Ripley Gateway, python3, curl, requests, and AGENT_API_KEY.]

## Skill Version(s):

1.0.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
