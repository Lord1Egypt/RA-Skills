## Description: <br>
Adaptive AI that evaluates health, enemy strength, and zone state to select attack, retreat, scouting, rotation, avoidance, or deceptive gameplay actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hakuramasam](https://clawhub.ai/user/hakuramasam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Game and simulation agents use this skill to choose tactical actions from current health, enemy, and zone signals. It is intended for gameplay-style decision guidance, not as a general-purpose instruction set outside that context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The prompt uses harsh combat-oriented wording and deception tactics that are appropriate only for gameplay or simulation contexts. <br>
Mitigation: Use it only for game or simulation tactic prompting, and do not treat it as a general-purpose instruction set. <br>
Risk: Applying the action rules outside their intended game-state inputs could produce misleading or unsuitable guidance. <br>
Mitigation: Constrain use to agents that provide explicit health, enemy, and zone-state signals and review outputs before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hakuramasam/godmode-battle-ai) <br>
- [Publisher profile](https://clawhub.ai/user/hakuramasam) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown gameplay prompt with action-selection rules] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution, credentials, network access, or system changes requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
