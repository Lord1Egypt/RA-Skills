## Description:

Amap location-service skill for POI search, nearby search, route planning, travel planning, and heatmap or map-link generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyanfe](https://clawhub.ai/user/zhangyanfe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to answer map-search requests, find nearby places, plan routes by travel mode, assemble city travel plans, and produce Amap visualization links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags an unsafe shell command pattern for raw user-provided locations.

Mitigation: Prefer the JavaScript axios helpers or another structured HTTP client that URL-encodes parameters, and review any generated curl command before execution.

Risk: The security summary flags weak API-key storage through local configuration.

Mitigation: Use AMAP_WEBSERVICE_KEY or AMAP_KEY from the environment or a managed secret store, and avoid saving or committing config.json.

Risk: Heatmap workflows can expose or load user-provided data URLs.

Mitigation: Use only public, non-sensitive, trusted heatmap data URLs.

Risk: The scanner guidance recommends dependency review before sensitive use.

Mitigation: Pin and audit axios before installing the skill in a sensitive workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhangyanfe/skills/ll)
- [Amap Web Service API Overview](https://lbs.amap.com/api/webservice/summary)
- [Create an Amap Application and Key](https://lbs.amap.com/api/webservice/create-project-and-key)
- [Amap POI Search API Documentation](https://lbs.amap.com/api/webservice/guide/api-advanced/newpoisearch)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with URLs, command examples, JavaScript snippets, and JSON API data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Amap Web Service API key and Node.js with axios for API-backed workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata; artifact SKILL.md frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
