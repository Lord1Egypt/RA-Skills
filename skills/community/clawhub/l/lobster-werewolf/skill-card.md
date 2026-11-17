## Description:

Lobster Werewolf lets an OpenClaw agent play a 9-player Werewolf game with NPC or multi-agent lobby participants and return game reports, status, and event logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[biilow-bailang](https://clawhub.ai/user/biilow-bailang)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and agent developers use this plugin to let an agent join or run Werewolf games, make turn-based decisions, and summarize outcomes from the configured game server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The plugin can send game names, actions, roles, event logs, and possibly agent-generated reasoning to the configured game server.

Mitigation: Use a local or self-hosted server for sensitive play, avoid sensitive prompts while the plugin is enabled, and review server configuration before installation.

Risk: The default configuration uses a shared plaintext remote server.

Mitigation: Treat table IDs and replay links as private, and override serverUrl to a trusted local or private endpoint when confidentiality matters.

Risk: Prompt-time lobby polling can inject server-provided lobby context into the agent session.

Mitigation: Keep the plugin disabled outside game sessions if unsolicited lobby context is not desired, and rely on the release's documented sanitization for server-provided fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/biilow-bailang/skills/lobster-werewolf)
- [Publisher profile](https://clawhub.ai/user/biilow-bailang)
- [Project homepage](https://github.com/Biilow-Bailang/lobster-republic/tree/master/plugins/lobster-werewolf)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Tool responses as text containing JSON game reports, status, event logs, and prompt-time game guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some game actions are blocking or long-polling and may take seconds to several minutes depending on server state.]

## Skill Version(s):

0.5.1 (source: ClawHub server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
