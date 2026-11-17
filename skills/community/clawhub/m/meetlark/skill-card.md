## Description:

Meetlark helps humans and agents create scheduling polls, share participation links, collect votes, and find the best meeting time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkelk](https://clawhub.ai/user/mkelk)

### License/Terms of Use:


## Use Case:

External users and their agents use this skill to coordinate meetings through Meetlark by creating scheduling polls, sharing participant links, checking votes, and closing polls when a time is chosen.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to retain a private poll admin token, which could expose poll administration if stored or repeated in chats, logs, or summaries.

Mitigation: Keep admin tokens out of shared messages, logs, and summaries; use them only for authorized poll management and remove them when they are no longer needed.

Risk: Participate URLs are shareable links that allow anyone with the link to vote in the poll.

Mitigation: Share participate links only with intended participants and avoid posting them in public or unrelated channels.

## Reference(s):

- [Meetlark website](https://meetlark.ai)
- [Meetlark OpenAPI spec](https://meetlark.ai/api/v1/openapi.json)
- [Meetlark interactive docs](https://meetlark.ai/docs)
- [Meetlark AI plugin manifest](https://meetlark.ai/.well-known/ai-plugin.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, API calls]

**Output Format:** [Markdown guidance with API endpoints and short share-message templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include participant-facing message text, poll status summaries, and token-authenticated poll actions.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
