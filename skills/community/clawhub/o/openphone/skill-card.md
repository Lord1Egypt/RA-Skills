## Description:

Manage business phone calls, SMS, and contacts through the OpenPhone API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dwhite-oss](https://clawhub.ai/user/dwhite-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business operations users use this skill to draft OpenPhone API requests for listing phone numbers, contacts, messages, calls, recordings, voicemail, and for creating contacts or sending SMS/MMS with an authorized OpenPhone account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help send real SMS/MMS messages and create or change contacts in an OpenPhone account.

Mitigation: Require manual confirmation before sending messages, creating contacts, or running bulk operations.

Risk: The skill may expose or retrieve conversation history, call recordings, voicemail, and transcripts from an OpenPhone workspace.

Mitigation: Use only with accounts and conversations approved by the workspace, and avoid regulated or highly confidential communications unless OpenPhone and internal policies allow that use.

Risk: The artifact requires an OPENPHONE_API_KEY for API access.

Mitigation: Store the API key in the environment or a secrets manager, avoid pasting it into prompts, logs, or shared files, and rotate it if exposed.

## Reference(s):

- [OpenPhone API base](https://api.openphone.com/v1)
- [ClawHub skill page](https://clawhub.ai/dwhite-oss/skills/openphone)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an OPENPHONE_API_KEY environment variable and authorized OpenPhone workspace access.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
