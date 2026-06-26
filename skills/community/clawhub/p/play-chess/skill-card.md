## Description: <br>
Play live chess on ChessWithClaw as Black against the user, connecting by invite URL or game ID and responding in real time with moves, thoughts, and chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alightttt](https://clawhub.ai/user/alightttt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to join a live ChessWithClaw game, play as Black against the human user, choose legal chess moves from the game state, and maintain game chat and presence during play. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends free-form chat, thoughts, game identifiers, agent name, and game activity to the external ChessWithClaw service. <br>
Mitigation: Use only with game tokens intended for ChessWithClaw, avoid sensitive content in chat or thoughts, and review external-service exposure before play. <br>
Risk: The skill encourages personalized messages based on prior conversations or files, which could disclose sensitive personal context to the remote service. <br>
Mitigation: Limit personalization to non-sensitive details the user is comfortable sharing and avoid references to private files, secrets, credentials, health, financial, or other sensitive information. <br>
Risk: The terminal workflow can leave temporary token, context, log, and tmux session state under /tmp/cwc after the game. <br>
Mitigation: Clean up /tmp/cwc files and stop related tmux sessions after play, especially on shared or persistent systems. <br>


## Reference(s): <br>
- [ChessWithClaw](https://chesswithclaw.vercel.app) <br>
- [ClawHub skill listing](https://clawhub.ai/alightttt/skills/play-chess) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with HTTP examples, shell commands, and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may produce live game moves, companion thoughts, chat messages, heartbeat calls, and temporary local files for game state.] <br>

## Skill Version(s): <br>
1.0.27 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
