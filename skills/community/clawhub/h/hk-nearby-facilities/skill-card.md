## Description:

Find nearby Hong Kong public toilets from official FEHD data by place keyword or shared coordinates, with support for Cantonese, Chinese, and English queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimpang8](https://clawhub.ai/user/jimpang8)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer nearby public-toilet requests in Hong Kong by searching official FEHD facility data and returning practical navigation details.

### Deployment Geography for Use:

Hong Kong

## Known Risks and Mitigations:

Risk: The skill contacts FEHD government endpoints when used, so endpoint availability or data changes can affect results.

Mitigation: Tell users results come from FEHD data and qualify answers when the endpoint fails or no likely match is returned.

Risk: User requests may include place names or precise coordinates for nearby-facility ranking.

Mitigation: Use only the minimum location detail needed for the lookup and avoid exposing precise coordinates except in user-facing navigation links.

Risk: The quick-start examples include a hardcoded local install path that may not match another environment.

Mitigation: Adjust script paths to the actual installed skill location before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimpang8/skills/hk-nearby-facilities)
- [FEHD public toilet map data](https://www.fehd.gov.hk/english/map/getMapData.php?type=toilet)
- [FEHD accessible toilets data](https://www.fehd.gov.hk/english/map/getAccessibleToilets.php?type=toilet)
- [FEHD universal toilets data](https://www.fehd.gov.hk/english/map/getUniversalToilets.php?type=toilet)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, JSON]

**Output Format:** [Markdown or plain text with optional JSON from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include facility name, address, district, distance, accessibility flags, and Google Maps links.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
