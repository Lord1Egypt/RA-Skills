## Description:

This skill helps agents geocode place names and estimate route distance and travel time using OSRM and Nominatim/OpenStreetMap without API keys, requiring python3 3.6+.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adhishthite](https://clawhub.ai/user/adhishthite)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to geocode place names, calculate route distance, and estimate travel duration for driving, walking, or cycling routes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Place names and precise coordinates are sent to public Nominatim/OpenStreetMap and OSRM services.

Mitigation: Avoid sensitive home, work, medical, legal, or confidential travel locations unless that disclosure is acceptable.

Risk: Public routing services may be best-effort and may not be suitable for high-volume production use.

Mitigation: Use the skill for normal interactive route lookups and review service terms, limits, and availability before operational deployment.

Risk: Travel durations are estimates and do not include live traffic or public transit routing.

Mitigation: Present results as estimates and use a traffic-aware or transit-aware source when those factors affect the decision.

## Reference(s):

- [ClawHub OSRM Maps Skill](https://clawhub.ai/adhishthite/skills/maps-osrm)
- [Nominatim OpenStreetMap Search API](https://nominatim.openstreetmap.org/)
- [OSRM Public Routing Service](https://router.project-osrm.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and route summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Route summaries include distance, duration, mode, and raw OSRM distance/time values when the scripts are used.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
