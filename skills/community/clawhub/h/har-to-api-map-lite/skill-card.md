## Description:

Turn a DevTools .har capture into an endpoint inventory — API requests grouped by host/method/normalized path with counts and status codes. Local parse only, nothing executed. Use when the user shares a .har or asks what API calls a page made.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nenadzivotic](https://clawhub.ai/user/nenadzivotic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect a user-captured HAR file they are authorized to analyze and summarize the observed API endpoints by host, method, normalized path, count, and response status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HAR captures can contain live cookies and authorization credentials.

Mitigation: Analyze only captures the user is authorized to inspect; treat the capture as a secret, and never copy, extract, or replay credential values.

Risk: The security review was partial, and the inventory only represents requests that fired during recording.

Mitigation: Consider the review limitation when installing, and present the endpoint list as an observed sample rather than a complete API specification.

## Reference(s):

- [ClawHub release](https://clawhub.ai/nenadzivotic/skills/har-to-api-map-lite)
- [Publisher profile](https://clawhub.ai/user/nenadzivotic)

## Skill Output:

**Output Type(s):** [JSON, Markdown]

**Output Format:** [JSON endpoint inventory and a Markdown endpoint table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Groups observed requests by host, method, and normalized path with counts and statuses; covers only requests present in the recording and does not report credentials or request/response shapes.]

## Skill Version(s):

1.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
