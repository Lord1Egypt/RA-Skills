## Description:

Turns a meeting transcript into structured meeting memory: a dated meeting note, append-only entity mentions, and a recap email drafted for review but never sent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skillsandagentsco](https://clawhub.ai/user/skillsandagentsco)

### License/Terms of Use:

MIT-0

## Use Case:

Teams use Meeting Scribe after calls to maintain local meeting memory. It reads a transcript and entity folder, writes a dated meeting note, appends quote-grounded mentions to matched entity files, proposes unmatched entities, flags ambiguous matches, and drafts a recap email for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads user-selected transcripts and entity folders and appends meeting history to local files.

Mitigation: Install only when the agent may access those files, and review generated notes and mention lines before relying on them.

Risk: Unmatched or ambiguous names can create incorrect meeting memory if accepted without review.

Mitigation: Review proposed new entities and ambiguity flags before creating entities or taking follow-up action.

Risk: The generated recap could be mistaken for an authorized outbound email.

Mitigation: Treat the recap as draft-only text; the skill has no email-sending step or external connector.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skillsandagentsco/skills/meeting-scribe)
- [Skills & Agents catalog page](https://skillsandagents.co/skills/meeting-scribe/)
- [USV Meeting Scribe inspiration](https://blog.usv.com/meet-the-agents)
- [Mention proposal shape](references/mention-proposal.md)
- [Sample transcript](references/sample-transcript.md)
- [Sample entity files](references/sample-entities/)

## Skill Output:

**Output Type(s):** [Markdown, Text, Files]

**Output Format:** [Markdown files plus draft recap email text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes scoped local meeting notes and append-only mention lines; does not send email or use external connectors.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
