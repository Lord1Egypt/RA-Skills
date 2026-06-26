## Description: <br>
Kuuila Game is an interactive game framework for text adventures, puzzle play, card-driven scenes, multiplayer wuxia sessions, themed story generation, and persistent endless-mode worlds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kukuxnd](https://clawhub.ai/user/kukuxnd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run interactive game sessions, generate narrative game content, manage cards and turns, and maintain multiplayer or endless-mode state. It is suited to entertainment, role-play, and community game workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release metadata lists crypto and purchase capabilities that are not explained by the game framework evidence. <br>
Mitigation: Review the capability tags with the publisher and either remove them or document why they are required before broad use. <br>
Risk: The skill manages multiplayer and persistent game state, so incorrect commands or generated events can affect ongoing sessions. <br>
Mitigation: Use host or administrator controls, review state-changing commands, and keep backups of persistent world data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kukuxnd/kuuila-game) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>
- [Release package metadata](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Markdown-facing text with JSON-like game state objects and command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include persistent game state, generated narrative content, command menus, and status summaries.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release metadata; artifact package.json lists 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
