## Description:

Use this skill when the user mentions creating a payment link, paying a paymentId or a2a payment link, or checking a2a payment status for the `onchainos payment a2a-pay` protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ok-james-01](https://clawhub.ai/user/ok-james-01)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create internal agent-to-agent payment links, pay seller-issued payment IDs, and check payment settlement status through the Onchain OS CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can invoke wallet-backed payment commands and sign server-provided payment challenges without an in-skill preview or fresh confirmation.

Mitigation: Before buyer payment, independently verify the paymentId, amount, token, recipient, and network with the seller or upstream workflow.

Risk: A user may attempt to create or pay without an authenticated wallet session.

Mitigation: Check wallet status first and ask the user to log in before create or pay operations.

Risk: Keyword-only upstream routing can create duplicate payment links after a buyer reports successful payment.

Mitigation: Route messages containing an existing paymentId to status checks and reuse non-terminal payment IDs for the same order context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ok-james-01/skills/okx-a2a-payment)
- [Publisher profile](https://clawhub.ai/user/ok-james-01)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include payment IDs, delivery URLs, transaction hashes, block numbers, fee displays, and terminal payment status guidance.]

## Skill Version(s):

3.1.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
