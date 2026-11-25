## Description:

Queries Chinese surname origins, notable people, and migration or distribution information using Jike Data's open API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jikeapi-cn](https://clawhub.ai/user/jikeapi-cn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Chinese culture or general knowledge questions about a surname's origin, notable people, and migration or distribution details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can redirect API requests to an arbitrary host if JIKE_API_BASE_URL is set, which may expose the AppKey.

Mitigation: Review before installing, avoid setting JIKE_API_BASE_URL, and prefer a version that fixes or validates the API host before attaching the AppKey.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jikeapi-cn/skills/jike-surname-query)
- [Jike Data homepage](https://www.jikeapi.cn/)
- [Surname query API endpoint](https://api.jikeapi.cn/v1/surname/query)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Chinese text or JSON returned from a command-line API lookup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a Jike Data AppKey provided through JIKE_SURNAME_QUERY_KEY or JIKE_APPKEY.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
