## Description:

Send real, physical greeting cards through the mail by helping the user design custom cards, preview them, and place mail orders through the Index Cards API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonwheatley](https://clawhub.ai/user/jonwheatley)

### License/Terms of Use:


## Use Case:

External users use this skill to create and mail personalized physical greeting cards for birthdays, holidays, thank-yous, and other occasions. It guides card design, recipient details, payment by credits, order confirmation, and delivery status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recipient names, mailing addresses, phone numbers, artwork, occasion text, and messages are sent to Index Cards when an order is approved.

Mitigation: Confirm the recipient, address, message, cost, and order details with the user before placing an irreversible order.

Risk: The optional contacts cache stores names, birthdays, addresses, phone numbers, notes, and card history locally in plaintext.

Mitigation: Create or read the contacts cache only after explicit user consent, and remind the user that the file is local, user-visible, and deletable.

Risk: Payment is required when the user has no credits.

Mitigation: Use only Stripe-hosted checkout links returned by the service, and do not collect payment card data through the agent or skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jonwheatley/skills/index-cards)
- [Index Cards homepage](https://indexcards.com)
- [Index Cards privacy policy](https://indexcards.com/privacy)
- [Index Cards API base](https://indexcards.com/v1/)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Conversational Markdown with API request guidance and order summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce hosted image URLs, preview video URLs, Stripe checkout links, and optional local contact-cache entries with user consent.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
