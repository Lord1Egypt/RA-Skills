## Description:

Checks deployed EVM contracts for common risk indicators using Magneta’s service, with free quick flags and an optional $0.01 USDC report that requires explicit user approval; it is not an audit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bosacks](https://clawhub.ai/user/bosacks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to review an unfamiliar deployed EVM contract before trading, approving, bridging to, or integrating it, and to decide whether further review is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The payment examples permit up to five times the stated $0.01 report price.

Mitigation: Before enabling payments, enforce exactly $0.01 USDC on Base per approved report; keep the dedicated low-balance wallet and require fresh user approval for paid calls.

## Reference(s):

- [Magneta Contract Risk service](https://x402.magneta.finance)
- [Coinbase x402 buyer quickstart](https://docs.cdp.coinbase.com/x402/buyer/quickstart)
- [Magneta Contract Risk on ClawHub](https://clawhub.ai/bosacks/skills/magneta-contract-risk)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, JSON, Guidance]

**Output Format:** [JSON risk reports with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One contract per request; scores are heuristic and do not replace an audit.]

## Skill Version(s):

0.1.1 (source: artifact frontmatter, server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
