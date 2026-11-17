## Description:

Compare live hotel room rates across Booking.com, Agoda, Traveloka, and OpenTravel for specific dates, including the cheapest source for the same property, per-room prices, and free-cancellation terms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cotghw](https://clawhub.ai/user/cotghw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-focused agents use this skill to compare hotel prices for named properties or city searches across supported booking sources and to summarize the cheapest option, room prices, and cancellation terms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send the user's original hotel request text to PriceWin's hosted service, which can expose unrelated personal details if the request includes them.

Mitigation: Use only structured hotel, city, date, guest, and room details in requests, and avoid including phone numbers, medical or accessibility details, employer context, confidential travel plans, or other unrelated personal information.

Risk: The skill depends on a hosted third-party service for live hotel search and comparison inputs.

Mitigation: Review the security guidance before installation and avoid the skill unless sending travel search details to the hosted service is acceptable.

## Reference(s):

- [Tool reference](reference.md)
- [Security and data handling](SECURITY.md)
- [PriceWin skills hub](https://github.com/Price-Win/pricewin-skills-hub)
- [ClawHub skill page](https://clawhub.ai/cotghw/skills/pricewin-price-comparison)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown comparison summaries with structured hotel, price, source, and cancellation details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include links and pricing details returned by the approved PriceWin MCP tools.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
