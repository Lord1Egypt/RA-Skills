## Description: <br>
A Tamagotchi-style digital pet for AI agents. Raise your pet, battle others, evolve through stages. Includes A2A multiplayer for agent challenges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NoizceEra](https://clawhub.ai/user/NoizceEra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent developers use PetRPG to run a local digital pet game with pet care, evolution, turn-based battles, achievements, and optional agent-to-agent challenge concepts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Achievement tracking may create or update local progress data. <br>
Mitigation: Install and run the skill only where local game state under data/achievements.json is acceptable. <br>
Risk: The skill advertises online or A2A multiplayer concepts, but the shipped artifact does not include an online.py implementation. <br>
Mitigation: Review any separately added multiplayer implementation for connection targets, transmitted pet or user data, and challenge authentication before enabling it. <br>


## Reference(s): <br>
- [PetRPG ClawHub release](https://clawhub.ai/NoizceEra/pet-rpg) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown instructions with Python command examples and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local game progress such as data/achievements.json when achievement tracking is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
