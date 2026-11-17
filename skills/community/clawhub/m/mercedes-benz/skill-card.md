## Description:

Locate Mercedes-Benz dealerships and search for new, used, and certified pre-owned vehicle inventory across the United States using zip code based filters and detailed vehicle specifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaudata](https://clawhub.ai/user/kaudata)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to find Mercedes-Benz USA dealers and compare nearby new, used, or certified pre-owned inventory by location, model, class, price, mileage, color, fuel type, year, and related filters.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: If npm start exposes the REST server beyond localhost, it can become an unauthenticated proxy to MBUSA services with weak input limits.

Mitigation: Keep the server bound to localhost or place it behind authentication, then add rate limits and strict input validation before any network exposure.

Risk: The skill contacts MBUSA services to retrieve dealer and inventory data.

Mitigation: Install only when that external service access is acceptable for the deployment environment and user workflow.

Risk: The security guidance calls for dependency updates.

Mitigation: Update the flagged npm dependencies before deployment and repeat the release security scan.

## Reference(s):

- [Mercedes-Benz USA Utilities on ClawHub](https://clawhub.ai/kaudata/skills/mercedes-benz)
- [kaudata publisher profile](https://clawhub.ai/user/kaudata)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [JSON tool results summarized as Markdown with clickable links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns dealer contact details, service links, inventory records, vehicle specifications, prices, image URLs, and dealer website URLs when available.]

## Skill Version(s):

0.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
