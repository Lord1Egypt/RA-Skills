## Description:

Accesses Granola meeting notes, summaries, transcripts, and attendees through the official Granola public REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gtkumar777](https://clawhub.ai/user/gtkumar777)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers with authorized Granola Business or Enterprise API access use this skill to list recent meetings, retrieve summaries, attendees, and metadata, and fetch transcripts when verbatim detail is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorized use can expose sensitive Granola meeting summaries, attendee details, metadata, and transcripts.

Mitigation: Install only for trusted users, prefer a personal API key over a broad workspace key when possible, and avoid broad or vague Granola prompts that may retrieve more meeting content than intended.

## Reference(s):

- [Official Granola API docs](https://docs.granola.ai/introduction)
- [Granola](https://granola.ai)
- [ClawHub skill page](https://clawhub.ai/gtkumar777/skills/granola-direct-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash and JSON examples; API responses may include JSON, plain-text summaries, Markdown summaries, and transcript text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GRANOLA_API_KEY plus curl and jq; transcript retrieval should be used only when verbatim meeting content is needed.]

## Skill Version(s):

1.0.3 (source: frontmatter and server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
