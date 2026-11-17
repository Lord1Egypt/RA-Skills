## Description:

Extracts structured data from plain text emails into concise JSON, including company, email address, contact person, discount code, and email type.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fdrummer](https://clawhub.ai/user/fdrummer)

### License/Terms of Use:


## Use Case:

Developers and operations teams can use this skill to convert plain text email content into structured JSON for lightweight routing, analysis, or data capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email content can contain personal or business-sensitive information.

Mitigation: Use the skill only with email text that is appropriate to provide to the agent, and review extracted JSON before downstream use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fdrummer/skills/mailparser)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [JSON object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns only the extracted fields: company, email, contact_person, discount_code, and type.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
