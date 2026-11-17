## Description:

Maps Cli is an OpenStreetMap CLI for geocoding, reverse geocoding, routing, point-of-interest search, timezone lookup, and CSV export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itspremkumar](https://clawhub.ai/user/itspremkumar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, field operations teams, and agents use this skill to retrieve OpenStreetMap-backed location data, routes, nearby places, timezone information, and CSV exports from a local Python CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions reference mutable remote code from a raw main-branch URL.

Mitigation: Install from the reviewed bundled artifact or a pinned release, and manually review the artifact before use.

Risk: Geocoding, routing, POI, and timezone commands send coordinates or place queries to public OSM-related endpoints.

Mitigation: Avoid submitting sensitive home, workplace, customer, or route coordinates unless sharing them with those public services is acceptable.

Risk: The included CI verifier executes product self-tests.

Mitigation: Run CI verification only for trusted code and preferably in an isolated environment.

## Reference(s):

- [ClawHub Maps Cli skill page](https://clawhub.ai/itspremkumar/skills/maps-cli)
- [Nominatim API endpoint](https://nominatim.openstreetmap.org)
- [OSRM routing endpoint](https://router.project-osrm.org)
- [Overpass API endpoint](https://overpass-api.de/api/interpreter)

## Skill Output:

**Output Type(s):** [text, json, csv, shell commands, guidance]

**Output Format:** [Plain text, JSON, or CSV returned from Python CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.8+ and live network access to public OSM-related endpoints.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter and script report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
