## Description:

Play Pokemon Red autonomously through a local PyBoy emulator session, using screenshots, game state, and HTTP actions for navigation, battles, quests, and saves.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drbarq](https://clawhub.ai/user/drbarq)

### License/Terms of Use:


## Use Case:

External agents and developers use this skill to play Pokemon Red in an emulator, inspect state and screenshots, and choose navigation, battle, healing, quest, and save actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run mutable third-party code and unpinned Python packages.

Mitigation: Review the Pokemon-OpenClaw repository before use, pin it to a trusted commit, and install dependencies in a virtual environment with locked versions and hashes.

Risk: The emulator server controls a local game session through localhost endpoints.

Mitigation: Run the emulator server with limited local permissions and keep it bound to localhost for the intended game-control workflow.

Risk: The workflow requires a Pokemon Red ROM.

Mitigation: Use only a legally obtained ROM and avoid packaging or redistributing ROM files with the skill.

## Reference(s):

- [OpenClaw Pokemon Red AI Player Instructions](references/game_instructions.md)
- [Pokemon-OpenClaw setup repository](https://github.com/drbarq/Pokemon-OpenClaw.git)
- [ClawHub skill page](https://clawhub.ai/drbarq/skills/pokemon-red)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local emulator server, Python dependencies, and a legally obtained Pokemon Red ROM.]

## Skill Version(s):

1.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
