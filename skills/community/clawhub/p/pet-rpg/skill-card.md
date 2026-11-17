## Description:

A Tamagotchi-style digital pet for AI agents. Raise your pet, battle others, evolve through stages. Includes A2A multiplayer for agent challenges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noizceera](https://clawhub.ai/user/noizceera)

### License/Terms of Use:


## Use Case:

External users and developers use PetRPG to run a local digital pet game for agents, including pet care actions, stats, evolution, turn-based battles, and achievement tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact describes A2A multiplayer behavior, but the inspected files do not implement online synchronization.

Mitigation: Treat multiplayer documentation as unimplemented and require separate review before adding networked data sharing, peer authentication, or user-consent flows.

Risk: Achievement tracking can write local progress data.

Mitigation: Run the skill only in a workspace where creating or updating data/achievements.json is acceptable.

## Reference(s):

- [PetRPG ClawHub skill page](https://clawhub.ai/noizceera/skills/pet-rpg)
- [NoizceEra ClawHub publisher profile](https://clawhub.ai/user/noizceera)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with Python code snippets, shell commands, and text or ASCII-art game output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local data/achievements.json file when achievement tracking is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
