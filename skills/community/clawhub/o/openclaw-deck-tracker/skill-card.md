## Description:

Track OpenClaw tasks on a NextCloud Deck board, adding tasks to Queue and moving them through workflow states.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skanderhelali](https://clawhub.ai/user/skanderhelali)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to track OpenClaw task lifecycle activity in NextCloud Deck, including task creation, progress logging, completion, and daily cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may encourage agents to record every user request in an external NextCloud Deck board, which can expose sensitive prompt or task details.

Mitigation: Use a board dedicated to agent task tracking and avoid storing secrets, credentials, private user prompts, or sensitive business data in card titles or descriptions.

Risk: Heartbeat monitoring can send recurring notifications to a default recipient.

Mitigation: Disable or override the default heartbeat recipient before use and confirm the intended recipient for long-running tasks.

Risk: Archiving, deleting, or using remote card contents for memory can cause data loss or preserve unintended information.

Mitigation: Require explicit confirmation before archive, delete, or memory-synthesis actions, and review card contents before long-term retention.

## Reference(s):

- [NextCloud Deck App](https://apps.nextcloud.com/apps/deck)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [ClawHub Skill Page](https://clawhub.ai/skanderhelali/skills/openclaw-deck-tracker)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, JSON, Markdown]

**Output Format:** [Markdown guidance with shell command examples and JSON-producing commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands interact with a configured NextCloud Deck board and may update, archive, delete, or dump card data.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
