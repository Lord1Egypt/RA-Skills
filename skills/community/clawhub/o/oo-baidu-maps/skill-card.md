## Description:

Search Baidu Maps and retrieve map data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can search places, geocode addresses, plan routes, and retrieve administrative area, IP location, and weather data through an OOMOL-connected Baidu Maps account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup can execute downloaded code that has not been verified and may install or update additional agent skills.

Mitigation: Review and pin a verified oo CLI release before setup, and check which additional skills it installs or updates.

Risk: Map queries send location inputs through OOMOL to Baidu Maps.

Mitigation: Submit only location information you intend to share.

## Reference(s):

- [Baidu Maps homepage](https://lbsyun.baidu.com)
- [Baidu Maps Place API documentation](https://lbsyun.baidu.com/docs/webapi?title=placev3%2Fguide%2Fwebservice-placeapiV3%2FinterfaceDocumentV2)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub release page](https://clawhub.ai/oomol/skills/oo-baidu-maps)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [Baidu Maps connector results returned as JSON and used as conversational text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result fields vary by action, including place details, coordinates, routes, and weather data.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
