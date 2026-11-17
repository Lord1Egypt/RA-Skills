## Description:

Helps agents search Granola meeting notes, retrieve summaries and transcripts, and find action items through a user-authorized Maton connection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People with authorized Granola access use this skill to search meetings, review notes and transcripts, and identify decisions and action items. With separate approval, they can set up scheduled or event-driven workflows using Maton.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting notes and transcripts may contain sensitive information.

Mitigation: Install only if you trust Maton; use the authorized OAuth connection and avoid exposing API keys or sharing meeting content with third parties without explicit intent.

Risk: Connections, hosted functions, triggers, and writes can create or change access and ongoing automation.

Mitigation: Approve each new connection, function, trigger, destination, and write separately before use.

Risk: Persistent destinations may forward event data outside the intended workflow.

Mitigation: Confirm the destination and data flow before enabling forwarding; keep meeting content out of third-party destinations unless explicitly intended.

## Reference(s):

- [Granola skill release](https://clawhub.ai/byungkyu/skills/granola-api)
- [Maton](https://maton.ai)
- [Meeting query schema](schemas/query_granola_meetings.json)
- [Meeting transcript schema](schemas/get_meeting_transcript.json)
- [Schedule trigger reference](references/time/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with meeting findings and optional command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Meeting content is limited by the user's authorized connection.]

## Skill Version(s):

1.2.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
