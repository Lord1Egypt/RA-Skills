## Description:

Composes and sends emails using a LangChain email agent with human approval before outgoing messages are sent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jawadsadiq01](https://clawhub.ai/user/jawadsadiq01)

### License/Terms of Use:


## Use Case:

Developers and teams can use this skill to add AI-assisted email composition and sending to an application while requiring a human approve, edit, or reject decision before delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can send email based on generated content and user-provided recipient details.

Mitigation: Keep the human approve, edit, or reject step before delivery and review EmailTool validation for recipients, sender identity, message body, attachments, and approval decisions before installation.

Risk: User-provided email instructions are placed into a privileged prompt while the agent has access to the email-sending tool.

Mitigation: Use a fixed system prompt and place user instructions in a lower-privilege, clearly delimited message; treat generated email fields as untrusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jawadsadiq01/skills/langchain-email-agent)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [String]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the final agent message after composing or attempting the email workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
