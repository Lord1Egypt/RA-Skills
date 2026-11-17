## Description:

Hourly electricity prices for Finland with optimal EV charging window calculation (3h, 4h, 5h).

This skill is ready for commercial/non-commercial use.

## Publisher:

[ovaris](https://clawhub.ai/user/ovaris)

### License/Terms of Use:

MIT

## Use Case:

People and agents monitoring Finnish electricity prices use this skill to fetch current pricing, daily price statistics, and low-cost charging windows for energy-intensive tasks such as EV charging.

### Deployment Geography for Use:

Finland

## Known Risks and Mitigations:

Risk: The skill makes outbound requests to api.porssisahko.net when used.

Mitigation: Install and run it only in environments where outbound access to that public electricity-price API is acceptable.

Risk: Charging-window recommendations are advisory and may be affected by timezone handling or API error handling limitations.

Mitigation: Review the returned prices and windows before relying on them for automated or high-cost scheduling.

## Reference(s):

- [Porssisahko.net latest prices API](https://api.porssisahko.net/v2/latest-prices.json)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes current price, current hourly average, optimal 3h, 4h, and 5h charging windows, and daily average, minimum, and maximum prices.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata; artifact/package.json reports 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
