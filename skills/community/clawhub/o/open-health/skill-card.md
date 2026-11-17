## Description:

Open Health helps agents search for and book real virtual mental health appointments with licensed US providers through a public booking API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gljirain](https://clawhub.ai/user/gljirain)

### License/Terms of Use:

MIT-0

## Use Case:

External users seeking US mental health telehealth appointments use this skill to search provider availability by service, state, payment method, and timing, then book a selected slot after providing required patient details.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill can create real mental-health appointments.

Mitigation: Require clear user intent and explicit confirmation before making the final booking call.

Risk: The booking flow handles sensitive mental-health, identity, contact, and insurance data.

Mitigation: Avoid logging, persisting, or adding patient JSON to memory or summaries; use the data only for the immediate API call.

Risk: The skill is not appropriate for crisis situations, diagnosis, medical advice, or prescription refills.

Mitigation: Redirect crisis or immediate-danger requests to emergency resources and leave clinical assessment to licensed providers.

## Reference(s):

- [Klarity Booking API Reference](references/api-reference.md)
- [Klarity booking API base URL](https://rx.helloklarity.com)
- [Open Health ClawHub page](https://clawhub.ai/gljirain/skills/open-health)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, JSON]

**Output Format:** [Markdown responses with shell command invocations and JSON API payloads or results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces time-sensitive availability and booking responses; patient data should be used only for the immediate booking flow and then discarded.]

## Skill Version(s):

1.0.1 (source: server release metadata, created 2026-03-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
