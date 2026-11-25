## Description:

Public 1688 data through okdata: products, shops. 4 endpoints, $0.022 a call. Use when a task needs 1688 data. 通过 okdata 取1688公开数据：products、shops。4 个接口，每次 $0.022。

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can retrieve public 1688 product listings, offer details, buyer reviews, and supplier products through okdata to support sourcing and marketplace research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects to api.okdata.online, and scan coverage is partial with medium confidence.

Mitigation: Use the API only if you trust the service, and avoid sending sensitive information until you have verified how it is handled.

## Reference(s):

- [okdata 1688 API reference](https://okdata.online/apis/alibaba_1688/?src=skill-okdata-alibaba-1688)
- [okdata agent setup guide](https://okdata.online/agents.md)

## Skill Output:

**Output Type(s):** [API Calls, Text]

**Output Format:** [Text data with source attribution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One page per API call; retrieving additional pages requires additional calls.]

## Skill Version(s):

0.2.3 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
