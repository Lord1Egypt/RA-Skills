## Description:

An autonomous Notion coworker agent that monitors Gmail for Notion comment mentions, understands the request, researches an answer using memory, conversation history, the Notion workspace, and optionally the web, then replies directly in the Notion discussion thread and documents the research in a subpage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laurobrcwb](https://clawhub.ai/user/laurobrcwb)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and workspace collaborators use this skill to delegate Notion comment mentions to an agent that can read notification emails, gather context from memory and Notion, reply in the relevant discussion, and create a research trail subpage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use private chat history, memory, Notion workspace content, and Notion notification emails to create persistent Notion replies and research pages.

Mitigation: Install only when that access and publication behavior are intended; use explicit approval steps, source limits, and redaction rules before publishing content derived from private context.

Risk: Automatic replies or research pages may expose sensitive context or overstate uncertain findings in a shared workspace.

Mitigation: Review generated replies and research pages before posting, especially for medium- or low-confidence answers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/laurobrcwb/skills/notion-coworker)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Concise Notion comment text, Markdown research subpage content, and a user-facing processing summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confidence notes, source summaries, processed email summaries, and inbox housekeeping guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
