## Description:

Propose on-chain payments from a shared wallet when a user asks to send crypto, make a payment, or create a shared wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xhyumiracle](https://clawhub.ai/user/xhyumiracle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to set up shared crypto wallets and prepare on-chain payment proposals for human approval. It is suited to workflows where an agent drafts transaction details but a human must review and approve before funds move.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles crypto payment proposals and persistent local signing authority, so incorrect transaction details can put funds at risk.

Mitigation: Verify every recipient, chain, amount, nonce, and approval URL independently before asking the user to approve a transaction.

Risk: The agent signing key is stored on disk under ~/.nodpay, making local file access controls important.

Mitigation: Restrict access to ~/.nodpay, keep ~/.nodpay/.env at chmod 600, and avoid sharing or exposing the directory in broader agent workspaces.

Risk: The documented workflow runs the NodPay CLI through unpinned npm execution.

Mitigation: Prefer a pinned or preinstalled reviewed CLI version and limit its access to only the NodPay configuration and wallet files needed for the task.

## Reference(s):

- [NodPay ClawHub Skill Page](https://clawhub.ai/xhyumiracle/skills/nodpay)
- [NodPay Homepage](https://nodpay.ai)
- [Safe](https://safe.global)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces wallet setup instructions, transaction proposal commands, approval links, nonce checks, and local wallet configuration guidance.]

## Skill Version(s):

0.2.33 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
