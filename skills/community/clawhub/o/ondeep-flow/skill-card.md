## Description:

ONDEEP Flow helps agents discover, publish, buy, and sell marketplace offerings such as services, compute, data, goods, and human tasks through the ondeep.net API with BSC or ETH escrow settlement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cethum](https://clawhub.ai/user/cethum)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to connect agents to ONDEEP's external marketplace for listing services, searching providers, managing orders, and coordinating crypto escrow payment flows. It is suited for agent commerce workflows that require explicit operator approval for spending and settlement actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports external crypto marketplace flows where order creation, fund transfer, receipt confirmation, escrow release, or delisting can affect real assets or listings.

Mitigation: Require human confirmation for those actions, set transaction and daily spending limits, use address allowlists, and operate with a dedicated low-balance wallet.

Risk: Marketplace product text, descriptions, and order notes are untrusted counterparty input and may contain prompt-injection content.

Mitigation: Treat marketplace text as display-only unless explicitly validated; sanitize or frame it as untrusted data before terminal display or LLM use.

Risk: Authenticated heartbeat and account-management examples use ONDEEP credentials and may maintain persistent outbound network activity.

Mitigation: Protect ONDEEP_ACCID and ONDEEP_TOKEN, keep heartbeat behavior opt-in and stoppable, and process heartbeat order data as read-only.

## Reference(s):

- [ONDEEP homepage](https://ondeep.net)
- [ONDEEP API docs](https://ondeep.net/docs)
- [ClawHub skill page](https://clawhub.ai/cethum/skills/ondeep-flow)
- [API reference](artifact/api-reference.md)
- [Usage examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl commands, Python examples, JSON API payloads, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ONDEEP_ACCID and ONDEEP_TOKEN for authenticated endpoints; examples interact with ondeep.net over HTTPS.]

## Skill Version(s):

1.0.7 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
