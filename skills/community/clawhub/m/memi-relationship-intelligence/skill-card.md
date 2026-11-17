## Description:

Personal CRM and relationship intelligence. Extracts contacts from conversations, tracks commitments, detects cooling relationships, delivers morning briefs, preps you before meetings, and gets smarter about your relationships the more you use it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mukund2](https://clawhub.ai/user/mukund2)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this OpenClaw skill as a local personal CRM for remembering contacts, tracking commitments, preparing for meetings, and receiving relationship follow-up prompts. It is intended for agents that can maintain a SQLite-backed memory store and optionally use Google data through gog.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can maintain a long-lived local database of personal and third-party relationship information.

Mitigation: Use explicit save commands, review the local SQLite database periodically, and avoid storing secrets, regulated data, or information about people who would not expect it.

Risk: Optional gog integration can expose Gmail, Calendar, and Contacts data.

Mitigation: Enable gog only when the user is comfortable granting Google access, and keep Google-derived context scoped to the intended relationship-management workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mukund2/skills/memi-relationship-intelligence)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Concise conversational text and Markdown, with occasional shell commands or SQLite guidance when setup or local data inspection is needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local relationship memory in SQLite and can optionally use gog for Gmail, Calendar, and Contacts context.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
