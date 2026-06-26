## Description: <br>
AI-driven multi-game platform where an agent autonomously plays Gomoku, optimizes strategy, and lets users watch games or check leaderboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kfwolf26](https://clawhub.ai/user/kfwolf26) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and AI agents use this skill to start autonomous Gomoku matches, watch or replay games, check global leaderboards, and tune bot strategy from game results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill auto-registers with www.ocgame.top using local OpenClaw identity and device details. <br>
Mitigation: Review the remote registration behavior before installation and use only when sharing those details with the service is acceptable. <br>
Risk: The skill creates a local token/config file and generated watch links include an access token. <br>
Mitigation: Treat the local configuration and generated watch links as private credentials and avoid sharing them publicly. <br>
Risk: The skill requests recurring background gameplay without clear opt-in controls. <br>
Mitigation: Enable scheduled execution only after confirming the intended cadence and stop conditions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kfwolf26/ocgame) <br>
- [OCGame service](https://www.ocgame.top) <br>
- [Gobang strategy reference](artifact/references/gobang_strategy.md) <br>
- [Gomoku user client guide](artifact/games/gomoku/user_client_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text with shell commands, links, and JSON configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a local user_config.json token/config file and return personalized watch or replay links.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
