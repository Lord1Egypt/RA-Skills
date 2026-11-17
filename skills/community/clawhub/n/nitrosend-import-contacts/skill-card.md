## Description:

Import contacts into Nitrosend from inline records or CSV. Handles email opt-in, SMS TCPA compliance, list assignment, and tagging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nitrosend](https://clawhub.ai/user/nitrosend)

### License/Terms of Use:

MIT-0

## Use Case:

External users can import authorized contacts into Nitrosend from CSV files or inline records, then assign contacts to lists and tags.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contact details are uploaded to Nitrosend, and new email contacts are subscribed by default.

Mitigation: Import only contacts with appropriate consent and use the dry-run preview before applying changes.

Risk: SMS contact imports require TCPA consent.

Mitigation: Import SMS contacts only after confirming explicit written consent.

## Reference(s):

- [Import Contacts on ClawHub](https://clawhub.ai/nitrosend/skills/nitrosend-import-contacts)

## Skill Output:

**Output Type(s):** [API calls, JSON, Guidance]

**Output Format:** [Natural-language guidance with structured JSON request data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports CSV imports and inline contact records; offers a dry-run preview.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
