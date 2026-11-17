## Description:

Search Google Flights for prices, availability, deals, flexible travel dates, filtered itineraries, connection quality, and price tracking alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kris-hansen](https://clawhub.ai/user/kris-hansen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search, compare, filter, and monitor flight prices for one-way, round-trip, flexible-date, and regular-route travel planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup installs the unpinned third-party fast-flights dependency.

Mitigation: Review the dependency source before installing and pin a known acceptable version for controlled environments.

Risk: Price tracking stores routes, travel dates, alert thresholds, and price history locally.

Mitigation: Use tracking only when local travel-history storage is acceptable, and delete the tracking files when they are no longer needed.

## Reference(s):

- [ClawHub Google Flights skill page](https://clawhub.ai/kris-hansen/skills/google-flights)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown-style command output, optional JSON search output, and local JSON or JSONL tracking files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write tracked flights, watched routes, and price history under ~/clawd/memory when tracking features are used.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
