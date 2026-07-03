## Description: <br>
Play live chess on ChessWithClaw as Black against the user, connecting by invite URL or game ID and responding in real time with moves, thoughts, and chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alightttt](https://clawhub.ai/user/alightttt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to play a live ChessWithClaw game where the agent connects as Black, polls board state, selects legal moves, and exchanges in-game thoughts and chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The third-party chess service receives the agent's game chat, thoughts, moves, name header, and invite token. <br>
Mitigation: Install only when this data sharing is acceptable, and keep chat and thoughts limited to chess or current-session context. <br>
Risk: The skill encourages personalization that may draw on prior conversations or unrelated local context. <br>
Mitigation: Restrict personalization to chess-only or current-session facts, and do not inspect unrelated files or prior conversations for gameplay. <br>
Risk: The skill uses persistent local files and background workers under /tmp/cwc. <br>
Mitigation: Clean up /tmp/cwc and stop game workers after play, and avoid retaining post-game user-profile notes unless explicitly desired. <br>


## Reference(s): <br>
- [ChessWithClaw](https://chesswithclaw.vercel.app) <br>
- [ClawHub skill page](https://clawhub.ai/alightttt/skills/play-chess) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with API examples, bash commands, Python snippets, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces game-loop guidance for connecting to an external chess service, sending API calls, writing temporary helper files, and managing local background workers.] <br>

## Skill Version(s): <br>
1.0.29 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
