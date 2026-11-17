## Description:

Fetch public X (Twitter) posts, account details, search results, trends, threads, lists, and community data through okdata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conn-ho](https://clawhub.ai/user/conn-ho)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers can retrieve public X data for monitoring, research, and analysis of posts, accounts, trends, lists, and communities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requests to an external okdata API, and request data may be shared with that service.

Mitigation: Review the API destination and the data you plan to send before installing or making requests.

Risk: API calls can incur per-call charges, including separate charges for additional pages.

Mitigation: Before paid calls, state the endpoint, number of calls, and maximum expected cost; use the documented per-call caps.

## Reference(s):

- [X API reference](https://okdata.online/apis/x/?src=skill-okdata-x)
- [okdata agent setup guide](https://okdata.online/agents.md)

## Skill Output:

**Output Type(s):** [Text, Analysis]

**Output Format:** [Text summaries and structured API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One page per call; additional pages require separate calls.]

## Skill Version(s):

0.2.2 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
