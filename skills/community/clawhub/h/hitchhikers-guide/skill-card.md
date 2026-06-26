## Description: <br>
A text adventure game engine inspired by The Hitchhiker's Guide to the Galaxy and the 1984 Infocom classic, for playing a humorous interactive story with an AI game master. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hallwayskiing](https://clawhub.ai/user/hallwayskiing) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Players and interactive-fiction users use this skill to play a persistent Hitchhiker's Guide-inspired text adventure. Agents use the skill's helper commands to track location, inventory, stats, flags, improbability, and history between turns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gameplay progress and history are stored locally by a Python helper, so sensitive information entered during play may be persisted in the skill's assets folder. <br>
Mitigation: Avoid entering sensitive information during gameplay and review local save or guide files before sharing the skill workspace. <br>
Risk: The reset command replaces the local save state. <br>
Mitigation: Use reset only when intentionally starting over, and preserve a copy of the save file first when existing progress matters. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Mechanics and Logic](references/mechanics.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/hallwayskiing/hitchhikers-guide) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown narrative text with inline shell commands and local JSON save-state updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update local game save and guide files under the skill's assets folder.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
