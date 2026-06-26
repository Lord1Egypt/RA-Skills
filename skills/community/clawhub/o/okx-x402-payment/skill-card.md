## Description: <br>
HTTP 402 Payment Required dispatcher for x402 and MPP that detects the payment protocol, routes to the matching playbook, and returns a ready-to-paste authorization header. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ok-james-01](https://clawhub.ai/user/ok-james-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to handle HTTP 402 payment-gated resources by decoding x402 or MPP challenges, presenting payment details for confirmation, signing through a wallet or local key path, and assembling the authorization header for request replay. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help authorize crypto-based HTTP 402 payments and sign transactions. <br>
Mitigation: Before approving any action, verify the network, token, amount, recipient, channel_id, deposit or top-up amount, and signing method. <br>
Risk: Wallet use and private-key fallback remain sensitive even though the release is disclosed and requires confirmation. <br>
Mitigation: Use a limited-purpose wallet instead of a primary wallet and avoid exposing production private keys to local signing flows. <br>
Risk: MPP session operations such as voucher, top-up, close, and settle can affect active channel balances. <br>
Mitigation: Confirm the active channel_id and requested session operation with the user before signing or replaying payment headers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ok-james-01/okx-x402-payment) <br>
- [Publisher profile](https://clawhub.ai/user/ok-james-01) <br>
- [OKX Web3](https://web3.okx.com) <br>
- [x402 protocol](https://x402.org) <br>
- [MPP protocol playbook](artifact/protocols/mpp.md) <br>
- [x402 protocol playbook](artifact/protocols/x402.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples, decoded payment details, and copyable authorization headers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before wallet checks or signing; supports MPP charge/session flows and x402 v1/v2 payment headers.] <br>

## Skill Version(s): <br>
3.1.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
