## Description:

PAPI helps agents send and automate WhatsApp messages through the PAPI WhatsApp Cloud API, including text, PTT voice notes, media, interactive buttons, polls, lists, and webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafacpti23](https://clawhub.ai/user/rafacpti23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure agents that send WhatsApp messages and interactive workflows through a PAPI account. It supports onboarding, connectivity checks, and examples for text, voice notes, media, buttons, lists, polls, and webhook-aware messaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send WhatsApp messages through the user's PAPI account to recipient JIDs.

Mitigation: Keep the PAPI API key private, verify recipient JIDs before sending, and obtain appropriate recipient consent.

Risk: Message content, media URLs, recipient identifiers, and webhook data pass through PAPI and WhatsApp infrastructure.

Mitigation: Avoid sending sensitive content unless that data flow is acceptable for the user's privacy and compliance requirements.

## Reference(s):

- [PAPI homepage](https://papi.api.br)
- [ClawHub skill page](https://clawhub.ai/rafacpti23/skills/papi)
- [Mensagens Interativas reference](references/interactive.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with bash, YAML, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PAPI_API_KEY, PAPI_INSTANCE_ID, and PAPI_BASE_URL for live API use.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
