## Description: <br>
Identity Guess Game hosts a multiplayer deduction game where players receive secret identities, share clues across three rounds, guess each other's identities, and receive scores and rankings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loongfay](https://clawhub.ai/user/loongfay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and community agents use this skill to run a group chat identity-guessing party game with private identity assignment, clue collection, guessing, scoring, and rankings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to group member lists and private messaging to distribute secret identities without exposing them in the group chat. <br>
Mitigation: Install it only where the agent is permitted to read group members and send private messages, and start games with an explicit command or confirmation. <br>
Risk: Game identities, clues, scores, and rankings remain in local JSON files until removed. <br>
Mitigation: Review retention expectations for the deployment and delete game or ranking files when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/loongfay/identity-guess-game) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Natural-language chat messages, private identity notifications, and concise game status or scoring summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local JSON files for game state and rankings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
