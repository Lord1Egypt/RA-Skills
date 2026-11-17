## Description:

Human-agent-agent-human dispatch. Sends requests to trusted circle of people and receives answers from their agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilyabelikin](https://clawhub.ai/user/ilyabelikin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Haah to let an agent ask trusted circles for help, collect attributed answers, and draft responses to incoming circle questions or direct messages with human approval before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incoming messages can prompt the agent to look up local private data and draft responses for external recipients.

Mitigation: Review inbound questions and every outbound draft for private data before allowing a reply, dispatch, or direct message.

Risk: The skill uses a Haah API key and stores local caches of circles and direct-message contacts.

Mitigation: Protect the API key and local cache files, and install only where those contacts and circles may be handled by the agent.

Risk: Heartbeat or cron polling can repeatedly fetch messages and refresh social-contact state.

Mitigation: Enable heartbeat or cron only when recurring polling is desired, and keep the cadence bounded.

Risk: Moving main-branch and unpinned install commands can change the installed skill content over time.

Mitigation: Prefer a pinned or reviewed install source for production or sensitive use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ilyabelikin/skills/haah)
- [Publisher Profile](https://clawhub.ai/user/ilyabelikin)
- [Haah Service](https://haah.ing)
- [Haah API Base](https://api.haah.ing/v6)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API Calls, Guidance]

**Output Format:** [Markdown guidance with YAML configuration examples, shell commands, and HTTP API call descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Haah API key; outbound dispatches, replies, and direct messages are intended to wait for explicit human approval.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
