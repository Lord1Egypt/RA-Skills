## Description:

Query your Telegram chat history using a LifeQuery instance. Use when the user wants to search past conversations, find shared links, or ask about specific people/events from their Telegram messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ngtwolf](https://clawhub.ai/user/ngtwolf)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search Telegram chat history, retrieve old conversation context, and find links, files, people, events, or topics from messages through a configured LifeQuery instance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can query an entire private Telegram history.

Mitigation: Ask the user to narrow the chat, topic, or time range before use, and treat each query as disclosure of private Telegram context.

Risk: Sensitive queries and bearer tokens can be sent to unvalidated or plaintext remote endpoints.

Mitigation: Use only a LifeQuery instance the user controls, prefer localhost or HTTPS, avoid remote HTTP endpoints, and do not set LIFEQUERY_API_KEY where it could be sent over plaintext.

## Reference(s):

- [LifeQuery](https://github.com/nikira-studio/lifequery)
- [ClawHub skill page](https://clawhub.ai/ngtwolf/skills/lifequery)
- [Publisher profile](https://clawhub.ai/user/ngtwolf)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Plain text or Markdown answers with citations returned by LifeQuery]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LIFEQUERY_BASE_URL and optionally LIFEQUERY_API_KEY; queries may disclose private Telegram context to the configured LifeQuery endpoint.]

## Skill Version(s):

1.0.1 (source: skill.yaml and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
