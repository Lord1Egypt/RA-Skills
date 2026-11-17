## Description:

Get real-time NJ PATH train service alerts, delays, status updates, and live arrival times from Port Authority alerts and GTFS-Realtime data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liamsx45](https://clawhub.ai/user/liamsx45)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check NJ PATH service alerts, line status, and live station arrivals without API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes live outbound requests to public PATH transit feeds.

Mitigation: Review and approve network access to the Port Authority alerts endpoint and PATH GTFS-Realtime feed before deployment.

Risk: Dependency and data-handling hygiene issues may affect reliability or output safety.

Mitigation: Pin or update Node dependencies and sanitize remote alert text before rendering it to users.

Risk: Upstream transit feed failures can produce misleading normal-service messages.

Mitigation: Report upstream feed failures as unavailable rather than treating missing data as normal service.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liamsx45/skills/path-alerts-main)
- [Project Homepage](https://github.com/LiamSx45/openclaw-path-alerts)
- [Port Authority Alerts API](https://www.panynj.gov/bin/portauthority/everbridge/incidents)
- [PATH GTFS-Realtime Feed](https://path.transitdata.nyc/gtfsrt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, API Calls, Guidance]

**Output Format:** [Markdown text and JavaScript API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, internet access, and the gtfs-realtime-bindings package; no API keys are required.]

## Skill Version(s):

1.0.0 (source: release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
