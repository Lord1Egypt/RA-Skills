## Description:

PlaceCall lets your agent call US businesses for reservations, inquiries and quotes, and gets through IVRs, holds and transfers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voygr](https://clawhub.ai/user/voygr)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams use an AI agent to find US businesses and handle reservations, inquiries, follow-ups, or quote requests by phone, then review the reported outcome and transcript.

### Deployment Geography for Use:

United States (excluding Indiana, Louisiana, Minnesota, Montana, and Nebraska)

## Known Risks and Mitigations:

Risk: The security assessment reports a credential-handling weakness and unsafe storage of an API-returned value as executable shell text.

Mitigation: Keep PLACECALL_API_KEY in the configured secret slot or an environment variable, never in prompts or chat, and treat API-returned content as data rather than shell commands.

Risk: Calls reach real people on the user's behalf, and call recordings and transcripts are retained for 90 days.

Mitigation: Call only numbers the user is authorized to contact, review the number and brief before dialing, and include only details needed for the task. Calls open with a recording notice by default.

## Reference(s):

- [PlaceCall ClawHub release](https://clawhub.ai/voygr/skills/placecall)
- [Project homepage listed in skill metadata](https://github.com/voygr-tech/placecall)
- [PlaceCall API deprecations documentation](https://api.voygr.tech/docs/placecall/deprecations/)

## Skill Output:

**Output Type(s):** [Text, JSON data, Audio recordings]

**Output Format:** [Structured call outcomes, summaries, and transcripts; optional call recordings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes place suggestions when no phone number is supplied; calls are limited to supported US destinations.]

## Skill Version(s):

6.6.3 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
