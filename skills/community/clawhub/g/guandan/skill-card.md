## Description:

Play GuanDan(掼蛋) card game via `clawguandan CLI`. Use when users ask to play GuanDan or create/list/join tables in game.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikewei](https://clawhub.ai/user/mikewei)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent create, list, join, and manage local GuanDan game tables and bot players through the clawguandan CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper suggests installing the clawguandan npm package using a moving latest version.

Mitigation: Verify the npm package source and prefer a pinned package version before installation.

Risk: The skill can start, restart, or leave running local game server and bot-player processes.

Mitigation: Use it only when local game management is intended, and stop background game processes when finished.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikewei/skills/guandan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and concise status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May start or manage local game server and bot-player processes through the clawguandan CLI.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
