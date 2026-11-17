## Description:

Make AI-powered phone calls via Bland AI to book restaurants, make appointments, inquire about services, and report back with transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dru-ca](https://clawhub.ai/user/dru-ca)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to initiate Bland AI outbound phone calls for practical tasks such as bookings, appointment inquiries, and service questions, then review returned call IDs, transcripts, summaries, or recordings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate real outbound calls without a built-in confirmation step.

Mitigation: Require explicit user confirmation of the phone number, task, and recording option before running call commands.

Risk: Phone numbers, task instructions, transcripts, summaries, and recordings may include personal, business, medical, financial, or legally sensitive details sent to or returned from Bland AI.

Mitigation: Avoid sensitive call content where possible, follow recording-consent requirements, and review Bland AI handling policies before use.

Risk: Broad account API keys can be exposed if stored where other local tools can read them.

Mitigation: Store BLAND_API_KEY in a restricted secret store or environment with least-privilege access and rotate it if exposure is suspected.

Risk: The artifact claims data stays secure because it is self-hosted, but server security evidence says data is sent to a third-party API.

Mitigation: Treat the skill as a third-party API integration and disclose that call data leaves the local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dru-ca/skills/phone-calls-bland)
- [Bland AI application](https://app.bland.ai)
- [Bland AI dashboard](https://app.bland.ai/dashboard)
- [Bland AI API base URL](https://api.bland.ai/v1)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Text, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON or text call-status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BLAND_API_KEY; call tasks, phone numbers, transcripts, summaries, and optional recordings are exchanged with Bland AI.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
