## Description: <br>
Emit analytics events to Millimetric (track, identify, batch, forget). Use when the user wants to send a custom event, log a signup/purchase/pageview, link an anonymous visitor to a user_id, bulk-import events, or process a GDPR delete request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[soybelli](https://clawhub.ai/user/soybelli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send server-side analytics events to Millimetric, identify users, submit batches, and process GDPR erasure requests from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a sensitive server API key to submit analytics data. <br>
Mitigation: Keep MILLIMETRIC_KEY secret, use server-side sk_* keys only, and avoid placing browser pk_* keys in shell or server code. <br>
Risk: Analytics traits and properties can include personal data. <br>
Mitigation: Review payloads before submission and avoid unnecessary personal data in traits or event properties. <br>
Risk: Batch imports and GDPR forget requests can change or delete analytics records at scale. <br>
Mitigation: Require explicit confirmation before running batch imports or forget/delete requests, and verify the target user or event set first. <br>
Risk: A misconfigured host could send credentials or analytics events to the wrong endpoint. <br>
Mitigation: Verify MILLIMETRIC_HOST before use, especially when switching between production and local development. <br>


## Reference(s): <br>
- [Millimetric API](https://api.millimetric.ai) <br>
- [ClawHub skill page](https://clawhub.ai/soybelli/millimetric-track) <br>
- [Publisher profile](https://clawhub.ai/user/soybelli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline bash, TypeScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose authenticated API requests for track, identify, batch, and forget operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
