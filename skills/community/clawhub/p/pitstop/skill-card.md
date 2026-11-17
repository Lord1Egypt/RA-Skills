## Description:

pitstop helps agents answer Italian fuel-price and EV-charger lookup questions by municipality, province, brand, coordinate, and related filters using public data sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galjos](https://clawhub.ai/user/galjos)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find Italian fuel stations, compare daily fuel prices, inspect station result quality, and locate EV chargers near places or coordinates. Agents should surface freshness, outlier, coordinate, and tariff-handoff caveats when answering.

### Deployment Geography for Use:

Italy

## Known Risks and Mitigations:

Risk: Fuel prices come from daily open data and may be stale or include outliers.

Mitigation: Check freshness, quality, stale-cache, and outlier indicators before presenting a result as a good option.

Risk: EV charger results do not provide verified per-station kWh tariffs.

Mitigation: Use the operator tariff link for charging-cost questions and avoid guessing prices.

Risk: The skill installs and runs the pitstop package from the Python package ecosystem and fetches public data over the network.

Mitigation: Install with the documented uvx or pipx flow in an appropriate environment and account for local caching and network access.

## Reference(s):

- [ClawHub pitstop skill page](https://clawhub.ai/galjos/skills/pitstop)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and JSON or GeoJSON result guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include navigation URLs, freshness and quality notes, outlier warnings, and links to official charger tariff pages.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
