## Description:

Text-based Texas Hold'em poker game with auto AI players for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dream-pig](https://clawhub.ai/user/dream-pig)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to run a local, text-based Texas Hold'em game for OpenClaw chat interactions with automated AI opponents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged bin points to game.mjs, which evidence.security flags as having a card-visibility game-fairness bug.

Mitigation: Invoke the documented node {baseDir}/scripts/final-game.js path until the package bin is fixed.

Risk: The skill executes a local interactive Node.js game.

Mitigation: Install and run it only in an environment where a local Node poker game is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dream-pig/skills/holdem-poker)
- [references/config.json](references/config.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JavaScript examples, and text game output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Node.js runtime; default game settings are configured in references/config.json.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
