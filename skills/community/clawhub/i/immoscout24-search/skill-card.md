## Description:

Search ImmoScout24 Germany real estate listings through the ImmoScout24 mobile API, with filters and expose details for heating, energy, parking, condition, and property report fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mihaimacarie98](https://clawhub.ai/user/mihaimacarie98)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search German ImmoScout24 property listings, retrieve expose details, and compile property reports with pricing, location, heating, energy, parking, and condition information.

### Deployment Geography for Use:

Global; focused on German real estate listings.

## Known Risks and Mitigations:

Risk: The skill deliberately bypasses ImmoScout24/DataDome anti-bot controls.

Mitigation: Review legal, policy, and terms-of-service implications before installation or use, and run it only when automated access is authorized.

Risk: The prerequisite guidance recommends installing a dependency with --break-system-packages.

Mitigation: Install dependencies in an isolated virtual environment and avoid --break-system-packages.

Risk: The script sends automated requests to ImmoScout24 mobile API endpoints.

Mitigation: Use conservative request rates, stop on access or error responses, and confirm the dependency and API behavior are acceptable for the intended environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mihaimacarie98/skills/immoscout24-search)
- [ImmoScout24 expose URL pattern](https://www.immobilienscout24.de/expose/{id})
- [ImmoScout24 mobile search API endpoint](https://api.mobile.immobilienscout24.de/search/list)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands; script output can be text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include listing IDs, URLs, prices, area, rooms, address, postcode, publication date, and expose detail fields when available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
