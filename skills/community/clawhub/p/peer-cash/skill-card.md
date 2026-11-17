## Description:

Cash out Base USDC to fiat through Peer with custody-separated MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adwilkinson](https://clawhub.ai/user/adwilkinson)

### License/Terms of Use:

MIT-0

## Use Case:

External users and wallet operators use Peer Cash to cash out Base USDC to fiat, compare payout rails, prepare unsigned transactions, track deposits, and recover or adjust orders while keeping wallet signing outside the skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses an unpinned npm MCP package in a financial workflow, which creates supply-chain risk before installation.

Mitigation: Install only if the peer-cash-mcp package and publisher are trusted, and prefer a pinned reviewed version or verified local install.

Risk: Prepared wallet transactions could move funds if destination, value, calldata, or order details are misunderstood.

Mitigation: Independently inspect destination, value, calldata, and order details before approving any signature or submission.

## Reference(s):

- [Peer Cash MCP repository](https://github.com/zkp2p/peer-cash-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and transaction-review details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user approval before wallet signing or transaction submission; may include deposit IDs and recovery guidance for order tracking.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
