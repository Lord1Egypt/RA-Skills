## Description:

Play live chess on ChessWithClaw as Black against a human user, using the game API to poll board state, choose legal moves, and send chat or thinking updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alightttt](https://clawhub.ai/user/alightttt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to let an agent join a ChessWithClaw invite, play as Black, respond to the human player's moves, and keep the game session active. The skill is intended for live interactive chess play with optional personalized chat and move commentary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external chess service may receive game chat, agent name, invite token, move thoughts, and any personal context included by the agent.

Mitigation: Review the skill before installing, get consent before personalization, and keep personal context minimal and relevant to the game.

Risk: The artifact includes background shell automation using tmux, sourced state files, temporary storage, and Python interpolation patterns that server security evidence flags for review.

Mitigation: Prefer the minimal API-only workflow unless the automation has been reviewed and credential handling, state-file sourcing, and temporary-file usage are corrected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alightttt/skills/play-chess)
- [ChessWithClaw homepage](https://chesswithclaw.vercel.app)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Code, Configuration]

**Output Format:** [Markdown with HTTP examples and bash/Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational instructions for connecting to a game, polling state, submitting moves, sending chat, maintaining heartbeat, and troubleshooting session continuity.]

## Skill Version(s):

1.0.29 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
