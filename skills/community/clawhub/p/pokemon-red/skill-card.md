## Description: <br>
Play Pokemon Red autonomously through a local PyBoy emulator server that exposes screenshots, RAM-derived game state, navigation, battle, quest, and save controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drbarq](https://clawhub.ai/user/drbarq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill to play Pokemon Red by starting a local emulator server, inspecting game screenshots and state, then issuing navigation, battle, interaction, quest, and save actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to download and run unpinned external code that is not included in the reviewed bundle. <br>
Mitigation: Review or pin the external Pokemon-OpenClaw repository and Python dependencies before use, and run them in a virtual environment or container. <br>
Risk: The skill operates a local emulator server and requires a Pokemon Red ROM. <br>
Mitigation: Use only a legally obtained ROM, keep the server bound to localhost, and stop the background emulator server after gameplay. <br>


## Reference(s): <br>
- [Pokemon Red Skill Page](https://clawhub.ai/drbarq/pokemon-red) <br>
- [Game Instructions](references/game_instructions.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, API calls, configuration, guidance, text] <br>
**Output Format:** [Markdown instructions with shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.10+, PyBoy dependencies, a legally obtained Pokemon Red ROM, and a local emulator server.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
