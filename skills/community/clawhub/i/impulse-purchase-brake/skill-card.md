## Description:

Helps users slow down supermarket or online impulse purchases by analyzing promotion traps, extra filler spending, and likely unused items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangyang7-star-jpg](https://clawhub.ai/user/yangyang7-star-jpg)

### License/Terms of Use:

MIT-0

## Use Case:

External users invoke this skill when deciding whether to buy during shopping promotions such as threshold discounts, second-item half-price offers, or multi-item sales. The skill gathers cart, promotion, and monthly spending context, then produces a concise analysis that distinguishes needed items from filler or impulse purchases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask for remaining monthly spending money and use strong loss-framing language.

Mitigation: Users should share only the budget detail needed for the analysis and avoid sensitive financial information unless they want that calculation.

Risk: Assertive anti-purchase guidance could feel overly forceful for some users.

Mitigation: Keep advice grounded in user-provided prices and promotion rules, and stop persuading if the user chooses to proceed.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/Yangyang7-star-jpg/skills/tree/main/impulse-purchase-brake)
- [ClawHub skill page](https://clawhub.ai/yangyang7-star-jpg/skills/impulse-purchase-brake)
- [Publisher profile](https://clawhub.ai/user/yangyang7-star-jpg)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, Guidance]

**Output Format:** [Markdown with tables, bullet lists, and short decision prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided cart prices, promotion rules, and monthly spending balance; does not require code execution or external data access.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
