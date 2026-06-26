## Description: <br>
Play a four-digit number guessing game where each guess receives feedback on how many digits are correct in both value and position. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lydia9781](https://clawhub.ai/user/Lydia9781) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People using a ClawHub agent can play a four-digit deduction game. The agent starts a local game, checks each guess, and returns position-match feedback until the number is solved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates temporary local files for game state. <br>
Mitigation: Run it in a non-sensitive workspace and remove any remaining game state files after interruption. <br>
Risk: The active game's secret number is stored locally while play is in progress. <br>
Mitigation: Avoid running it from shared directories where other users or processes can inspect temporary state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lydia9781/guess-number) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain text game feedback] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates temporary local game state files during play.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
