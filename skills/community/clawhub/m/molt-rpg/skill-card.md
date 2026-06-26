## Description: <br>
A local RPG game engine for AI agents that works offline for single-player use and includes optional online dashboard, multiplayer, and A2A communication features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NoizceEra](https://clawhub.ai/user/NoizceEra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to run a local AI-agent RPG game, simulate battles and raids, manage local in-game wallet state, and optionally connect to multiplayer, A2A, or Telegram bot features. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional online sync, A2A messaging, and Telegram bot features can transmit gameplay, player, or agent messages outside the local environment when enabled. <br>
Mitigation: Use offline mode for no network use, and enable OnlineSync or telegram_bot.py only deliberately after reviewing what game and message data will be shared. <br>
Risk: Telegram bot operation may require a bot token and can expose messages to the configured Telegram channel or bot context. <br>
Mitigation: Use a dedicated Telegram bot token for this game and avoid sending sensitive information through game, A2A, or Telegram messages. <br>


## Reference(s): <br>
- [MoltRPG ClawHub listing](https://clawhub.ai/NoizceEra/molt-rpg) <br>
- [MoltRPG Player Hub](https://molt-rpg-web.vercel.app) <br>
- [MoltRPG Player Hub API](https://molt-rpg-web.vercel.app/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline Python and shell examples, plus local game text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Offline mode is local by default; online, A2A, and Telegram behavior are optional and user-started.] <br>

## Skill Version(s): <br>
2.1.1 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
