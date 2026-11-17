## Description:

Provides Chinese-language wealth-management product explanations, product matching suggestions, and personal-finance Q&A for bank wealth products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krillingone](https://clawhub.ai/user/krillingone)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to ask Chinese-language questions about bank wealth products, yield rules, holding periods, holiday earnings, and related policy or product concepts. The skill provides informational product matching suggestions but does not open accounts, transact, promise returns, or handle sensitive identity or account data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the financial product data is expired and product files show information valid through 2026-03-30.

Mitigation: Verify product terms, availability, risk level, fees, redemption rules, and disclosures in an official bank channel before acting on any recommendation.

Risk: The security summary says the skill always pushes users toward a remotely hosted purchase QR image.

Mitigation: Review and allow-list the external image URL before deployment, and treat the purchase prompt as optional navigation rather than financial advice or an endorsement.

Risk: The skill gives personal-finance and product-matching guidance in a regulated domain.

Mitigation: Present responses as informational assistance only, avoid return promises or purchase decisions, and do not collect account, identity, phone, or password data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krillingone/skills/personal-finance-skill)
- [Skill definition](artifact/SKILL.md)
- [Routing and response patterns](artifact/patterns.md)
- [Product catalog](artifact/products/理财产品全量列表.md)
- [Referenced official mini-program QR image](https://static.hepei.club/contact.png)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese-language Markdown responses with explanations, product lists, risk notes, and an optional image link.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product recommendation responses are expected to include concise risk reminders and product-data freshness context.]

## Skill Version(s):

1.0.16 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
