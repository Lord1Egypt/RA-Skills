## Description:

Emit analytics events to Millimetric (track, identify, batch, forget). Use when the user wants to send a custom event, log a signup/purchase/pageview, link an anonymous visitor to a user_id, bulk-import events, or process a GDPR delete request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soybelli](https://clawhub.ai/user/soybelli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send server-side Millimetric analytics events, identify users, upload event batches, and handle GDPR erasure requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analytics events may include personal data.

Mitigation: Avoid sending unnecessary personal data and review event properties before ingestion.

Risk: Millimetric API keys can be exposed or misused.

Mitigation: Keep MILLIMETRIC_KEY scoped and secret, and use server-side secret keys only where required.

Risk: Requests may be sent to an unintended endpoint.

Mitigation: Verify MILLIMETRIC_HOST before use.

Risk: Delete or forget requests can remove user data.

Mitigation: Require explicit confirmation before running forget/delete requests.

Risk: The optional npm package may change behavior across versions.

Mitigation: Pin the optional npm package in production.

## Reference(s):

- [Millimetric API](https://api.millimetric.ai)
- [Millimetric Track on ClawHub](https://clawhub.ai/soybelli/skills/millimetric-track)
- [soybelli ClawHub Profile](https://clawhub.ai/user/soybelli)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, JSON, and TypeScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request examples for track, identify, batch, and forget operations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
