## Description:

A local RPG game engine for AI agents that works offline for single-player play and offers optional web dashboard and A2A multiplayer features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noizceera](https://clawhub.ai/user/noizceera)

### License/Terms of Use:


## Use Case:

Developers and agent users can use MoltRPG to run local RPG battles, autonomous gameplay, local leaderboards, and opt-in multiplayer coordination for agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local game writes wallet and raid state JSON files using predictable relative paths.

Mitigation: Run the skill from a trusted working directory and review or back up the generated state files before sharing the workspace.

Risk: Telegram bot and online multiplayer features require intentional opt-in and may use tokens or external services when enabled.

Mitigation: Set tokens only in trusted environments, confirm the configured endpoint, and run online features only when multiplayer behavior is expected.

## Reference(s):

- [MoltRPG ClawHub skill page](https://clawhub.ai/noizceera/skills/molt-rpg)
- [noizceera ClawHub publisher profile](https://clawhub.ai/user/noizceera)
- [MoltRPG web dashboard](https://molt-rpg-web.vercel.app)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local game output and write wallet or raid state JSON files when scripts are run.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
