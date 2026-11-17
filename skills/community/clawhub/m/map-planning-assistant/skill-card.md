## Description:

Helps agents generate AMap-based POI recommendations, routes, local activity suggestions, cultural notes, user profile/history views, and shareable personal map links or QR codes for Chinese cities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tix007](https://clawhub.ai/user/tix007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn natural-language city, scenario, or travel requests into POI recommendations, itinerary and route summaries, local activity suggestions, cultural explanations, and AMap personal map outputs.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Location queries and generated map point data may be sent to AMap.

Mitigation: Use only with clear user consent, avoid sensitive-location requests when possible, and disclose that AMap receives the map and POI data needed for live results.

Risk: Travel history, recent interactions, preferences, and profile data may be stored locally in plaintext.

Mitigation: Run in an isolated single-user environment or add authenticated user identity, restrictive file permissions, retention and deletion controls, and explicit consent notices before multi-user use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tix007/skills/map-planning-assistant)
- [Publisher profile](https://clawhub.ai/user/tix007)
- [AMap Open Platform](https://lbs.amap.com/)
- [API Guide](artifact/API_GUIDE.md)
- [Personal Map Feature](artifact/MAP_FEATURE.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown text with POI lists, route summaries, activity suggestions, cultural notes, AMap map links, QR-code links, and occasional code or configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AMAP_API_KEY for live AMap requests; outputs may include shareable AMap URLs and QR-code URLs.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
