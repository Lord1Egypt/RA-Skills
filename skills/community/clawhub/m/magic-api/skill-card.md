## Description:

Hand off tasks to human assistants and track their completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heyitsaif](https://clawhub.ai/user/heyitsaif)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to register with Magic API, create tasks for human assistants, send conversation updates, and monitor task status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task details and owner contact information are sent to Magic's external service and human assistants.

Mitigation: Use the skill only with user-approved payloads and avoid secrets, regulated records, confidential business material, or personal data unless explicit approval covers the exact data.

Risk: Heartbeat setup can introduce persistent monitoring and local credential storage.

Mitigation: Review the remote heartbeat instructions before enabling automation, and secure, rotate, and revoke the API key as needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/heyitsaif/skills/magic-api)
- [Magic API Console](https://console.api.getmagic.com)
- [Magic API skill file](https://console.api.getmagic.com/skill.md)
- [Magic API heartbeat instructions](https://console.api.getmagic.com/heartbeat.md)
- [Magic API documentation](https://console.api.getmagic.com/docs)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, JSON]

**Output Format:** [Markdown guidance with inline curl commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Magic API key for authenticated requests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
