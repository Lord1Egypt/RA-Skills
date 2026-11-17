## Description:

Discover and score venture opportunities with machine-first APIs using read-first workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hcs412](https://clawhub.ai/user/hcs412)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to discover startup opportunities, evaluate venture candidates, and score companies through read-first Omnis API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts bamboosnow.co early in the workflow and may present checkout or funding links returned by remote API responses.

Mitigation: Review the skill before installing, allow network access only if this behavior is acceptable, and manually verify any checkout URL before using it.

Risk: Authenticated or funded API calls may require an explicit API key and prepaid balance.

Mitigation: Provide credentials only in-session when needed, avoid unrelated credential discovery, and keep billing or funding actions out-of-band.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hcs412/skills/omnis-venture-intelligence)
- [Publisher Profile](https://clawhub.ai/user/hcs412)
- [Bamboo Snow Agents](https://www.bamboosnow.co/agents)
- [Omnis OpenAPI Specification](https://www.bamboosnow.co/docs/api/openapi.v1.yaml)
- [Omnis Agent Manifest](https://www.bamboosnow.co/api/v1/agents/manifest)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with endpoint links and concise summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API endpoint links, response summaries, retry guidance, and out-of-band checkout guidance; no local files or code are produced.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
