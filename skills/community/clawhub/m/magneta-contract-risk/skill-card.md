## Description:

Check a smart contract's risk before trading, approving, bridging or integrating it, using the Magneta Contract Risk x402 service (0-100 score, proxy/owner/mint/blacklist/fee flags, verified-source and static-analysis findings, 20 EVM chains). Free bytecode-only quick flags need only curl; the full report costs $0.01 USDC on Base per call and is paid only with explicit user approval. Use when about to sign a transaction involving an unfamiliar token or contract, or when asked whether a token looks like a rug or honeypot. Not an audit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bosacks](https://clawhub.ai/user/bosacks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to review an unfamiliar EVM contract before swapping, approving, bridging, sending funds, or integrating it. It provides free quick flags and an optional paid report to inform a transaction decision; it is not a substitute for an audit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a possible gap in user approval for paid requests and says a mixed payment offer may pass the payment check.

Mitigation: Before any paid report, disclose the $0.01 USDC Base charge and obtain explicit user approval. Confirm that the payment is only for the approved amount, asset, and network; reject mixed or unexpected offers, and do not retry or batch paid calls without fresh approval.

Risk: A private key or payment credential used for the paid path could expose funds if mishandled.

Mitigation: Use a dedicated low-balance wallet; keep secrets in environment variables and never paste, print, or log them. Use the free quick-flags path when a paid report is unnecessary.

Risk: Risk scores and selector-based flags can be incomplete or misleading and do not establish that a contract is safe or exploitable.

Mitigation: Treat the report as one input to a decision, review the underlying flags and proxy administrator, and do not use the result as a substitute for an audit.

## Reference(s):

- [Magneta Contract Risk service](https://x402.magneta.finance)
- [Magneta Contract Risk on ClawHub](https://clawhub.ai/bosacks/skills/magneta-contract-risk)
- [Coinbase x402 buyer quickstart](https://docs.cdp.coinbase.com/x402/buyer/quickstart)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Code, Shell commands, Guidance]

**Output Format:** [JSON risk reports and quick-flag results, with Markdown guidance and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Contract risk score, level, and reported flags; results are informational and are not an audit.]

## Skill Version(s):

0.1.2 (source: frontmatter; corroborated by server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
