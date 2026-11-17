## Description:

Envoie le resultat de l'INR (International Normalized Ratio) a un centre de telemedecine specialise ou pour un test.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gillescv](https://clawhub.ai/user/gillescv)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to send Gilles's INR self-measurement value by email to a telemedicine recipient or to a test address.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends sensitive health information and includes hardcoded personal identity details.

Mitigation: Use it only for the named patient and intended recipients; remove hardcoded personal details from the published package and configure identifying details privately before operational use.

Risk: The skill can send an email without validating the INR value or confirming the destination and message.

Mitigation: Validate the INR value and require a clear confirmation that shows the destination and message summary before sending.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gillescv/skills/inr-sender)
- [Publisher profile](https://clawhub.ai/user/gillescv)

## Skill Output:

**Output Type(s):** [shell commands, text, guidance]

**Output Format:** [Markdown with inline shell command usage and generated email message text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts an INR value and optional test flag; sends the formatted message through a configured Gmail command.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
