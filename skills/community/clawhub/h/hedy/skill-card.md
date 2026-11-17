## Description:

Access and manage Hedy meeting data: sessions, transcripts, highlights, todos, topics, contexts, vocabulary, and webhooks via the Hedy REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[julianpscheid](https://clawhub.ai/user/julianpscheid)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve and manage Hedy meeting records, transcripts, highlights, todos, topics, contexts, vocabulary, and webhook settings from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive meeting transcripts, notes, highlights, todos, and profile data through the configured Hedy API key.

Mitigation: Install only when the user trusts Hedy with the data available to that key, keep the key out of chat and logs, and present retrieved meeting data only as needed for the user's request.

Risk: Webhook creation can send future meeting-derived data to an external destination until the webhook is deleted.

Mitigation: Confirm the exact destination host and event list before creating a webhook, and warn the user that matching Hedy data will leave Hedy.

Risk: Write, update, and delete operations can change Hedy topics, contexts, todos, vocabulary, and webhook configuration.

Mitigation: Require explicit user confirmation before POST, PUT, PATCH, or DELETE requests, and require extra confirmation for deletions.

## Reference(s):

- [Hedy API base URL](https://api.hedy.bot)
- [Hedy EU API base URL](https://eu-api.hedy.bot)
- [ClawHub skill page](https://clawhub.ai/julianpscheid/skills/hedy)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include Hedy API responses and summaries of meeting-derived data when authorized by the user's configured API key.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
