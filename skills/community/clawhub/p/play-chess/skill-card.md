## Description: <br>
Play live chess on ChessWithClaw as Black against a human user, connecting by invite URL or game ID and responding in real time with moves, thoughts, and chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alightttt](https://clawhub.ai/user/alightttt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to let an agent play a live ChessWithClaw game as Black, poll the game state, choose legal chess moves, and send in-game chat and thoughts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses remembered personal details in messages sent to ChessWithClaw. <br>
Mitigation: Avoid putting sensitive facts in /tmp/cwc/user_context.txt and limit personalization to details the user is comfortable sharing during the game. <br>
Risk: The skill stores game tokens in /tmp/cwc/creds.env and runs background tmux sessions. <br>
Mitigation: Clear /tmp/cwc/creds.env and stop cwc tmux sessions after each game. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alightttt/skills/play-chess) <br>
- [ChessWithClaw](https://chesswithclaw.vercel.app) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with bash, Python, JSON, and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local /tmp/cwc files and tmux sessions while using token-authenticated ChessWithClaw API calls.] <br>

## Skill Version(s): <br>
1.0.28 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
