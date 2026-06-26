## Description: <br>
Distance, routing, and geocoding using OSRM and Nominatim/OpenStreetMap public services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adhishthite](https://clawhub.ai/user/adhishthite) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and agents use this skill to convert place names to coordinates and estimate distance, travel time, and road routes for driving, walking, or cycling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Place names and route coordinates are sent to public Nominatim/OpenStreetMap and OSRM services. <br>
Mitigation: Avoid submitting sensitive home, workplace, medical, legal, or private travel locations unless third-party processing is acceptable. <br>
Risk: Public OSRM and Nominatim services may be rate-limited, unavailable, or unsuitable for high-volume production use. <br>
Mitigation: Use reasonable request volume, follow Nominatim's one-request-per-second policy, and use a dedicated or self-hosted routing/geocoding service for high-volume workloads. <br>
Risk: Travel durations are estimates without live traffic or public transit routing. <br>
Mitigation: Treat returned travel times as planning estimates and verify critical routes with an authoritative local source. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/adhishthite/maps-osrm) <br>
- [Nominatim](https://nominatim.openstreetmap.org/) <br>
- [OSRM Demo Server](https://router.project-osrm.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text route, distance, duration, and geocoding results with optional shell command usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and sends lookup requests to public OSRM and Nominatim services; no API key is required.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
