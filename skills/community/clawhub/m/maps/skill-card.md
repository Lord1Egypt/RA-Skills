## Description: <br>
Plan place search, geocoding, routing, and map-link workflows across Google Maps, Apple Maps, OpenStreetMap, and other providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and travel-planning agents use this skill to choose map providers, normalize place and route data, prepare safe map links, and avoid mixing provider schemas or wasting paid quota. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live map calls or generated links may send addresses, coordinates, route origins, destinations, and place-search text to the selected provider. <br>
Mitigation: Use planning-only mode unless live calls are approved, preview high-impact routes or shared links, and confirm before sending sensitive location details. <br>
Risk: Paid providers may consume API quota or create billing impact when repeated geocoding, routing, matrix, or static-map calls are made. <br>
Mitigation: Prefer the cheapest provider that satisfies the task, cache confirmed recurring places after user approval, and stop repeated calls when quota or retry red flags appear. <br>
Risk: Local map memory can expose private travel patterns if sensitive routes, itineraries, or secrets are stored there. <br>
Mitigation: Keep ~/maps/ limited to reusable preferences and non-sensitive context, and do not store API keys, private itineraries, or sensitive location history by default. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/maps) <br>
- [Skill homepage](https://clawic.com/skills/maps) <br>
- [Google Maps APIs endpoint](https://maps.googleapis.com) <br>
- [Apple Maps links](https://maps.apple.com) <br>
- [OpenStreetMap Nominatim endpoint](https://nominatim.openstreetmap.org) <br>
- [OSRM routing endpoint](https://router.project-osrm.org) <br>
- [Mapbox API endpoint](https://api.mapbox.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance with normalized request plans, structured summaries, and map links when approved] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local ~/maps/ configuration and requires confirmation before live provider calls involving sensitive location data.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
