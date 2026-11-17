## Description:

Fetches monday.com Notetaker meeting notes and prepares context for the owner's next meeting using calendar and notetaker data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or workspace owners use this skill to retrieve recent monday.com Notetaker summaries, search meetings by person, topic, or date, and prepare for upcoming meetings from calendar participants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may access the owner's Google Calendar, attendee lists, and notetaker history.

Mitigation: Install only where those data scopes are intended, use platform-managed scoped credentials, and avoid raw credential sourcing.

Risk: The skill can create monday.com items from meeting action items with limited board-selection controls.

Mitigation: Require explicit board selection and confirmation before creating monday.com items.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/netanel-abergel/skills/meeting-notetaker)
- [Publisher profile](https://clawhub.ai/user/netanel-abergel)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown responses with meeting summaries, participant lists, topics, action items, and next-meeting prep.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses concise same-language responses, asks for clarification on ambiguous meeting matches, and omits empty sections.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
