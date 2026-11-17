## Description:

Gift Genius helps agents find location-aware Valentine's Day gifts by routing requests to supported merchants and returning two or three curated options with decision rationale and buy links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evoleinik](https://clawhub.ai/user/evoleinik)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to narrow gift searches by recipient, budget, location, and category. It then presents a small set of Valentine's gift recommendations with delivery and purchase guidance.

### Deployment Geography for Use:

Global, with merchant routing documented for the United States, Singapore, Australia, Europe, and other regions.

## Known Risks and Mitigations:

Risk: Gift preferences, recipient context, budget, and location may be sent to AirShelf or merchant services.

Mitigation: Disclose external service use and avoid sharing sensitive recipient details unless needed for the gift search.

Risk: Checkout-link generation may move the user toward a purchase without clear consent boundaries.

Mitigation: Require explicit user confirmation before creating checkout links or sending cart requests.

Risk: Calendar-related behavior could access personal calendar context without sufficient consent.

Mitigation: Ask for explicit permission before any calendar access and use only authorized calendar tooling.

Risk: Expanded merchant and category coverage may produce recommendations outside the user's expected gift scope.

Mitigation: Confirm recipient, location, budget, and category constraints when they are unclear, and state which merchant category is being searched.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evoleinik/skills/gift-genius)
- [Publisher profile](https://clawhub.ai/user/evoleinik)
- [AirShelf search API](https://dashboard.airshelf.ai/api/search?q=QUERY&merchant_ids=MERCHANT_ID&min_price=MIN&max_price=MAX&limit=5)
- [AirShelf checkout API](https://dashboard.airshelf.ai/api/merchants/MERCHANT_ID/checkout)
- [UrbanStems product examples](https://urbanstems.com/products/the-peony)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Guidance]

**Output Format:** [Markdown recommendations with inline links and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns two recommendations by default, three maximum, with concise decision rationale, delivery context, and purchase guidance.]

## Skill Version(s):

4.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
