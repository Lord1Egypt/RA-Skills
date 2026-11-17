## Description:

Helps shoppers find live KnifeRevive products and arrange SF Bay Area knife sharpening through buyer-approved checkout and booking handoffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[svetlyoh](https://clawhub.ai/user/svetlyoh)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers use this skill to browse and compare KnifeRevive goods, review selected quantities at native checkout, or request eligible knife sharpening with transparent service and trip fees. Payment and contact sharing require buyer approval.

### Deployment Geography for Use:

Goods depend on merchant-supported shipping zones; sharpening serves the SF Bay Area, with prepaid pickup and delivery limited to eligible Contra Costa and Santa Clara ZIP codes.

## Known Risks and Mitigations:

Risk: Product prices, shipping, fees, taxes, or sharpening availability may change before checkout.

Mitigation: Confirm live item details and native fulfillment rates; have the buyer review the final quote, dates, and total on the merchant site.

Risk: Private checkout links and customer contact or payment details are sensitive.

Mitigation: Keep review links private, collect sensitive details only through the merchant's protected flow, and require buyer approval before sharing contact details or paying.

Risk: A shopping or booking request could be mistaken for a paid order or confirmed appointment.

Mitigation: Only report payment or booking as complete after merchant verification; authorize any wallet payment through a separately scoped host approval flow.

## Reference(s):

- [KnifeRevive Concierge on ClawHub](https://clawhub.ai/svetlyoh/skills/kniferevive-concierge)
- [API workflow](artifact/references/api.md)
- [Product discovery](artifact/references/product-discovery.md)
- [Listing checkout](artifact/references/listing-checkout.md)
- [Sharpening booking](artifact/references/booking.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with product images and links, itemized quotes, booking choices, and private checkout handoffs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live merchant availability and final totals require verification; the buyer approves payment.]

## Skill Version(s):

0.6.0 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
