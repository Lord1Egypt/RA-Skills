## Description:

Get a real Google Hotels price quote for a listing and dates, then compare that property against the offers StayingAPI can resolve for it to find the cheapest rate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stayingapi](https://clawhub.ai/user/stayingapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve a Google Hotels price quote for a known listing and dates, then compare available offers for the same property when StayingAPI can resolve them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hotel lookup details are sent to StayingAPI during live use.

Mitigation: Use the skill only when sending those details to StayingAPI is acceptable, and use a sandbox key for testing.

Risk: The required STAYINGAPI_KEY may be exposed if pasted into prompts, logs, or insecure shell history.

Mitigation: Store STAYINGAPI_KEY in a protected secret store or runtime environment variable, and rotate it if exposure is suspected.

Risk: Cross-OTA comparison coverage can vary by property and may return only one offer.

Mitigation: Check the returned offers length before presenting the result as a multi-platform comparison.

## Reference(s):

- [StayingAPI homepage](https://stayingapi.com)
- [StayingAPI docs](https://stayingapi.com/docs)
- [StayingAPI OpenAPI contract](https://api.stayingapi.com/openapi.json)
- [Auth setup](references/auth-setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration]

**Output Format:** [Markdown guidance with API request details and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include guidance for polling asynchronous jobs, interpreting offer coverage, and handling API-key setup.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
