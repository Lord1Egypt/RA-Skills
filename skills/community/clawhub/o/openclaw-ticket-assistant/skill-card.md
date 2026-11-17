## Description:

OpenClaw Ticket Assistant analyzes customer support screenshots, identifies the customer, reporter, platform, and issue, and guides an agent through creating a ticket.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mskmz](https://clawhub.ai/user/mskmz)

### License/Terms of Use:


## Use Case:

Support employees use this skill to convert customer conversation screenshots into confirmed ticket fields and submit tickets in the OpenClaw workflow. The skill is intended for environments where the agent has authorized browser access to the ticketing system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill bundles customer names, accounts, and UID identifiers used to populate ticket fields.

Mitigation: Review the bundled customer directory before installation, minimize retained customer data, and prefer an authenticated lookup when available.

Risk: The skill automates internal login and browser actions for ticket creation.

Mitigation: Run it only with least-privilege ticket-system access and require user review of extracted fields before submission.

Risk: Support screenshots may contain unnecessary sensitive data.

Mitigation: Ask users to provide only the screenshot content needed for customer, reporter, platform, and issue identification.

## Reference(s):

- [OpenClaw Ticket Assistant ClawHub Listing](https://clawhub.ai/mskmz/skills/openclaw-ticket-assistant)
- [Domain Account Login Guide](references/login-guide.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Configuration]

**Output Format:** [Concise text or Markdown confirmations, ticket summaries, and user prompts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before ticket submission and depends on browser access to the ticketing system.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
