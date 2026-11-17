## Description:

Location awareness via privacy-friendly GPS tracking (Home Assistant, OwnTracks, GPS Logger). Set location-based reminders and ask about movement history, travel time, and nearby POIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hegghammer](https://clawhub.ai/user/hegghammer)

### License/Terms of Use:


## Use Case:

External users and administrators use this skill to let an agent answer location questions, manage saved places and location reminders, estimate travel time, and surface nearby points of interest from configured location providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles precise location, destinations, saved places, reminders, and location-service credentials.

Mitigation: Install only for users who accept that data handling, protect ~/.openclaw/.env and local configuration files, and use dedicated least-privilege provider credentials.

Risk: ETA, nearby-place, address, and map-link features can disclose precise location or destination data to third-party mapping services.

Mitigation: Run those features only when third-party location disclosure is acceptable, and document the mapping services used in deployment review.

Risk: Cron-based checks can create ongoing background location processing and notifications.

Mitigation: Enable scheduled checks only when continuous monitoring is intended, and disable or avoid them for one-off interactive use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hegghammer/skills/location-awareness)
- [Publisher Profile](https://clawhub.ai/user/hegghammer)
- [OpenStreetMap Nominatim](https://nominatim.openstreetmap.org/)
- [OpenStreetMap Overpass API](https://overpass-api.de/api/interpreter)
- [OSRM Demo Server](http://router.project-osrm.org/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON returned by shell commands, with setup guidance in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can emit map links, coordinates, geofence and reminder state, travel estimates, history summaries, nearby place lists, and configuration instructions.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
