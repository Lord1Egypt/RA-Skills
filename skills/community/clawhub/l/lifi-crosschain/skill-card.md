## Description: <br>
Cross-chain token swaps and bridges via the LI.FI protocol. Get quotes, execute transfers, track progress, and compose DeFi operations across 35+ blockchains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rhlsthrm](https://clawhub.ai/user/rhlsthrm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to help an OpenClaw agent quote, compare, prepare, and track LI.FI cross-chain swaps, bridges, and DeFi zap operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prepare wallet-signable swap, bridge, and zap transactions that may move real blockchain assets. <br>
Mitigation: Before signing, manually verify the chain, token, amount, destination, spender or approval amount, contract-call details, route, slippage, fees, and bridge timing. <br>
Risk: Token approvals can authorize more spending than intended. <br>
Mitigation: Prefer explicit per-transaction approvals and avoid unlimited token approvals unless the user deliberately requests them. <br>
Risk: Cross-chain bridge transfers are asynchronous and may be delayed, partially completed, failed, or refunded. <br>
Mitigation: Track the transfer status after the source-chain transaction and confirm destination-chain results before treating the operation as complete. <br>


## Reference(s): <br>
- [LI.FI Documentation](https://docs.li.fi) <br>
- [LI.FI API Reference](https://apidocs.li.fi) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [ClawHub Listing](https://clawhub.ai/rhlsthrm/lifi-crosschain) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown, configuration] <br>
**Output Format:** [Markdown with curl commands, route summaries, and transactionRequest JSON details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; LIFI_API_KEY is optional for higher LI.FI API rate limits.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
