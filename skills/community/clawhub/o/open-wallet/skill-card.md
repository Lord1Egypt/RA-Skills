## Description:

Use https://tx.steer.fun to have a user execute a wallet action (send a transaction or sign a message) with their own wallet via a shareable URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stephancill](https://clawhub.ai/user/stephancill)

### License/Terms of Use:


## Use Case:

Developers and external agents use this skill to create shareable wallet action links for user-approved JSON-RPC requests such as signing messages, sending transactions, signing typed data, or submitting batch wallet calls. The skill helps route the resulting transaction hash, signature, object response, or error back to the agent manually or through an optional redirect URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated links can ask a user's wallet to sign messages or submit transactions.

Mitigation: Before opening a link, verify the chain, target address or contract, function, value or token amount, and expected wallet action.

Risk: Redirect URLs can automatically send wallet results or errors to another destination.

Mitigation: Use redirect_url only when the destination is trusted, and avoid redirects for signatures unless the destination has been reviewed.

Risk: Broad JSON-RPC support can create requests with more authority than the user intends.

Mitigation: Prefer least-privilege requests and explain the wallet action in plain language before asking the user to open the link.

## Reference(s):

- [Open Wallet ClawHub page](https://clawhub.ai/stephancill/skills/open-wallet)
- [tx.steer.fun wallet action link service](https://tx.steer.fun/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown with URL examples and JSON-RPC parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces shareable wallet action URLs and instructions for handling returned transaction hashes, signatures, JSON responses, or errors.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
