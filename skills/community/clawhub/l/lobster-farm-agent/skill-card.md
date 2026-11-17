## Description:

Lobster MUD lets an agent register, manage, and play a browser-based Lobster Tamagotchi game, including farm care, chat, diary retrieval, MUD adventures, and daily behavior reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaredwei01](https://clawhub.ai/user/jaredwei01)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent operate a persistent virtual lobster pet in the browser, including registration, routine care, game actions, chat replies, diary display, and adventure play.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A remote server receives the persistent lobster KEY, game state, chat messages, and daily work or activity summaries.

Mitigation: Use the skill only after explicit user consent, keep reported summaries aggregate, and provide a clear way to disable telemetry or delete the associated key data.

Risk: The evidence security summary identifies plaintext HTTP for telemetry and game-server communication.

Mitigation: Avoid sending sensitive information and require HTTPS before normal approval or broad deployment.

Risk: Autonomous or proactive play can perform repeated game actions and reports without a fresh user request.

Mitigation: Narrow triggers, require opt-in for proactive checks, and let users stop autonomous sessions and telemetry reporting.

## Reference(s):

- [Lobster Farm JS Bridge API](artifact/references/api-endpoints.md)
- [Lobster Farm Game Guide](artifact/references/game-guide.md)
- [Lobster Farm Strategy Guide](artifact/references/strategy-tips.md)
- [Lobster Farm Game](http://82.156.182.240/lobster-farm/)
- [ClawHub Skill Page](https://clawhub.ai/jaredwei01/skills/lobster-farm-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown prose with shell, JavaScript, JSON, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct browser actions and HTTP calls to the Lobster Farm game server.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
