## Description:

Query real-time New Zealand state highway traffic conditions, road events, closures, roadworks, traffic cameras, and travel conditions from the Waka Kotahi NZTA Traffic and Travel API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bobwattienz](https://clawhub.ai/user/bobwattienz)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to answer New Zealand highway traffic questions by checking NZTA road events, journeys, regions, and traffic cameras.

### Deployment Geography for Use:

New Zealand

## Known Risks and Mitigations:

Risk: The skill depends on a public trafficnz.info API and may return unavailable, incomplete, or stale traffic data if the service changes or is unreachable.

Mitigation: Treat results as current API reports, review important travel decisions against official NZTA sources, and handle empty or failed API responses explicitly.

Risk: The skill is scoped to NZTA and New Zealand state highway traffic questions, not generic traffic routing or non-New Zealand road conditions.

Mitigation: Use it for New Zealand highway events, closures, roadworks, journeys, and cameras; choose another source for unrelated traffic requests.

## Reference(s):

- [NZTA Traffic and Travel API Reference](artifact/references/api-endpoints.md)
- [NZTA Traffic and Travel API Base](https://trafficnz.info/service/traffic/rest/4/)
- [ClawHub Skill Page](https://clawhub.ai/bobwattienz/skills/nzta-traffic)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON API output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries the public trafficnz.info API and can return formatted summaries or raw JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
