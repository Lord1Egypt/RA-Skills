## Description:

M10 OneSource Blockchain Agent answers natural-language questions about blockchain data, covering historical on-chain activity, live chain state, and smart contract bytecode analysis through the OneSource service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnwollenberg](https://clawhub.ai/user/shawnwollenberg)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to ask natural-language questions about Ethereum mainnet, Sepolia, and Avalanche C-Chain data and receive structured summaries and Markdown analyses without writing queries or SDK code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each query may incur a $0.04 USDC charge through HTTP 402/x402 payment handling.

Mitigation: Confirm payment behavior and cost controls before use, and ensure the calling client handles x402 payment signatures intentionally.

Risk: Natural-language queries, blockchain addresses, and returned query traces are sent to an external OneSource service.

Mitigation: Do not submit private keys, seed phrases, sensitive non-public information, or addresses that should not be shared with the external service.

Risk: The response can include query_traces that may echo user input and internal lookup details.

Mitigation: Omit query_traces from user-facing output unless the audit trail is specifically needed.

Risk: Unbounded full-index scan requests are rejected by the agent.

Mitigation: Add bounded filters such as address, time range, event type, contract, or aggregation scope when asking broad blockchain questions.

## Reference(s):

- [OneSource homepage](https://onesource.io)
- [OneSource agent endpoint](https://agent.onesource.io)
- [x402 protocol](https://github.com/coinbase/x402)
- [ClawHub skill page](https://clawhub.ai/shawnwollenberg/skills/m10-blockchain-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [JSON response with a plain-text summary, Markdown analysis, step metadata, usage details, and optional query traces]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and paid HTTP 402/x402 payment handling by the calling client; query traces may be omitted from user-facing output when not needed.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
