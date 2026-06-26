## Description: <br>
Text-based Texas Hold'em poker game with auto AI players for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dream-Pig](https://clawhub.ai/user/Dream-Pig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a local, text-based Texas Hold'em game in OpenClaw chat interactions, with the human player controlling the small blind and automated AI players handling the other positions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Node scripts to start gameplay. <br>
Mitigation: Install it only when a local text poker game is desired and keep normal command and file approval prompts enabled. <br>
Risk: The artifact includes multiple game entrypoints with different behavior. <br>
Mitigation: Prefer the documented scripts/final-game.js entrypoint when hidden AI cards and fair turn-based play matter. <br>
Risk: The skill documentation describes chip-accounting edge cases that affect game correctness. <br>
Mitigation: Use the documented chip total checks when modifying or extending betting, folding, or showdown logic. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Dream-Pig/holdem-poker) <br>
- [Dream-Pig publisher profile](https://clawhub.ai/user/Dream-Pig) <br>
- [Game configuration](references/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code] <br>
**Output Format:** [Plain text game output with Markdown command examples and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with Node; game settings are configured in references/config.json.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
