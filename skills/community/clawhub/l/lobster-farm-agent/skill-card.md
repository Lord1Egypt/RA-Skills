## Description: <br>
Play and manage a Lobster Tamagotchi farm game autonomously via browser, with a unique KEY binding each installed agent to its own lobster. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaredwei01](https://clawhub.ai/user/jaredwei01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to register, check, and autonomously manage a virtual lobster pet, including feeding, farming, chat, diary retrieval, and MUD-style adventures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the lobster KEY, game chat, game state, and daily aggregate work or activity patterns to a third-party plain-HTTP game server. <br>
Mitigation: Install only when that data sharing is acceptable, keep the KEY and bind link private, and avoid putting secrets or private work details in game chat. <br>
Risk: The skill can act autonomously by periodically checking and playing the game. <br>
Mitigation: Disable or avoid autonomous play unless explicitly wanted, and review agent actions and summaries during use. <br>
Risk: Daily behavior reporting can share aggregate work-pattern telemetry. <br>
Mitigation: Ask the agent not to run daily behavior reporting unless the empathy feature is desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jaredwei01/lobster-farm-agent) <br>
- [Lobster Farm game](http://82.156.182.240/lobster-farm/) <br>
- [Lobster Farm JS Bridge API](references/api-endpoints.md) <br>
- [Lobster Farm Game Guide](references/game-guide.md) <br>
- [Lobster Farm Strategy Guide](references/strategy-tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline commands, status summaries, game chat text, and API interaction guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a lobster KEY, bind URL, natural-language gameplay summaries, diary excerpts pulled from the server, and in-character chat responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact skill-metadata.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
