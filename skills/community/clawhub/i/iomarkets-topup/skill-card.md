## Description:

Buy real-world things for your principal with USDC on Algorand via x402: travel eSIMs for 200+ destinations, and mobile airtime and data top-ups in 150+ countries delivered to any phone number.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergovashakmadze](https://clawhub.ai/user/sergovashakmadze)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to discover, quote, and purchase travel eSIMs or mobile airtime/data top-ups with explicit human confirmation. It is also used to create payment links, check FX rates, verify receipts, and report settlement or refund details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help an agent spend USDC on real-world purchases when payment capability is configured.

Mitigation: Use hosted mode or payment-link flow when the agent should not hold a wallet key; otherwise set a low budget and require human confirmation before every purchase.

Risk: Local wallet mnemonics could be exposed if placed directly in MCP configuration.

Mitigation: Store the mnemonic in a protected local file and never inline it in configuration.

Risk: Top-ups can be irreversible after delivery, and a wrong operator or phone number can produce a successful but unusable purchase.

Mitigation: Confirm the operator, recipient number, delivered item, and USDC price with the human before buying.

Risk: Catalog availability, supplier float, and server-side purchase limits can change independently of the skill text.

Mitigation: Check the live catalog and limits before quoting or buying, and re-quote smaller when supplier float is insufficient.

## Reference(s):

- [IoMarkets homepage](https://iomarkets.app)
- [IoMarkets agent documentation](https://iomarkets.app/agent.md)
- [ClawHub skill page](https://clawhub.ai/sergovashakmadze/skills/iomarkets-topup)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration, Shell commands]

**Output Format:** [Markdown guidance with HTTP examples and JSON MCP configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce payment links, order status summaries, receipts, eSIM activation details, settlement URLs, and refund URLs when used by an agent.]

## Skill Version(s):

0.2.7 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
