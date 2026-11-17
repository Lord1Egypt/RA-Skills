## Description:

Personal CRM and relationship intelligence. Extracts contacts from conversations, tracks commitments, detects cooling relationships, delivers morning briefs, preps you before meetings, and gets smarter about your relationships the more you use it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mukund2](https://clawhub.ai/user/mukund2)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to maintain a local personal relationship memory: saving contacts, tracking commitments, preparing for meetings, surfacing follow-ups, and finding useful context across their network.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently builds a detailed relationship database containing contacts, notes, commitments, preferences, meeting context, email-derived signals, and communication patterns.

Mitigation: Install only when the user can control or audit the local SQLite database and delete stored relationship data when needed.

Risk: When gog is available, the skill can use existing Google credentials to read Gmail, Calendar, and Contacts data for relationship intelligence.

Mitigation: Enable Google ingestion only when the user is comfortable with that access, and disable gog-based features when Gmail, Calendar, or Contacts mining is not wanted.

## Reference(s):

- [Memi on ClawHub](https://clawhub.ai/mukund2/skills/memi)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Conversational Markdown with occasional inline shell commands and structured relationship guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local SQLite relationship database and, when gog is available, use Google Calendar, Gmail, and Contacts data through the user's credentials.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
