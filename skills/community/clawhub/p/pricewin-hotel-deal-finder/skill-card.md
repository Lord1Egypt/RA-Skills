## Description:

Find the cheapest hotel deal by comparing live prices across Booking.com, Agoda, Google Hotels, and OpenTravel for any city worldwide and any travel dates; one command returns ranked best-value, cheapest, and quality picks with direct booking links, all normalized to USD.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cotghw](https://clawhub.ai/user/cotghw)

### License/Terms of Use:

MIT-0

## Use Case:

Travelers, travel planners, and agents use this skill to compare public hotel prices for a destination, date range, and guest count across multiple providers and return ranked booking options. It is intended for normal hotel deal finding and OTA price comparison workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local browser daemon that can navigate and read pages during hotel searches.

Mitigation: Run it as an unprivileged user, especially in shared environments or when the agent has broad filesystem access.

Risk: Search results include booking links from external providers.

Mitigation: Verify booking-link destinations before clicking or sharing them.

Risk: A custom OpenTravel API base URL can redirect search data to an unexpected service.

Mitigation: Use `OPENTRAVEL_API_BASE_URL` only with trusted endpoints.

Risk: A failed search may leave the PriceWin browser daemon running locally.

Mitigation: Be prepared to manually stop the PriceWin daemon after failures.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cotghw/skills/pricewin-hotel-deal-finder)
- [Project homepage](https://github.com/Price-Win/pricewin-skills-hub)
- [Security and data handling](SECURITY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-formatted hotel price comparison with ranked picks, per-night prices, and direct booking links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prices are normalized to USD; provider coverage may be partial when a source has no inventory or is blocked.]

## Skill Version(s):

1.1.3 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
