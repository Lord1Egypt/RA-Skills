## Description:

Uses command-line scripts to call Google Maps Platform APIs for geocoding, reverse geocoding, route planning, place search, place details, elevation lookup, and timezone lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deusyu](https://clawhub.ai/user/deusyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when they need an agent to select and run Google Maps command-line queries for addresses, coordinates, routes, places, elevation, or timezone data. It is suited to workflows that can provide a restricted Google Maps API key and consume raw Google Maps JSON responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Google Maps API keys may appear in error output for some failed requests.

Mitigation: Use a restricted Google Maps API key with tight API, quota, billing, and application restrictions; avoid sharing terminal or agent logs from failed runs until URL redaction is fixed.

Risk: Location and place queries are sent to Google Maps Platform APIs.

Mitigation: Avoid sensitive personal location queries unless sending them to Google is intended and permitted for the workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deusyu/skills/google-maps-skill)
- [Command Map](references/command-map.md)
- [Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and raw Google Maps JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GOOGLE_MAPS_API_KEY; command results are emitted as unwrapped Google Maps API JSON.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
