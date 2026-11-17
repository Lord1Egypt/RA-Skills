## Description:

A text adventure game engine that lets an agent run a humorous Hitchhiker's Guide-inspired game, manage local state, and narrate player choices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hallwayskiing](https://clawhub.ai/user/hallwayskiing)

### License/Terms of Use:


## Use Case:

External users and game-playing agents use this skill to run a persistent text adventure session with narrated turns, inventory, stats, flags, randomness, and local save progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps local game progress, action history, and generated guide entries in its own assets directory.

Mitigation: Install only if local persistence of this game data is acceptable for the target environment.

Risk: The reset command clears the current local save.

Mitigation: Use reset only when intentionally starting over, and preserve the save file separately if the current session must be retained.

## Reference(s):

- [README](artifact/README.md)
- [Mechanics and Logic](artifact/references/mechanics.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown prose with inline shell commands and JSON state output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local save state and generated guide entries under the skill assets directory.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
