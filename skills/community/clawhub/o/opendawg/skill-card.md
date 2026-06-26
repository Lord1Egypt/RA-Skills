## Description: <br>
Universal entertainment and gaming engine for AI agents that can run text-based arcade games, group tournaments, leaderboards, streaks, virtual currency, and player profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcools1977](https://clawhub.ai/user/jcools1977) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
External bot operators and agent developers use this skill to add text-only entertainment features such as slots, trivia, word games, riddles, tournaments, prediction games, leaderboards, achievements, and persistent player profiles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation triggers can start game behavior from boredom cues or group banter without an explicit command. <br>
Mitigation: Require explicit opt-in commands for arcade sessions and disable auto-activation in channels where games are not expected. <br>
Risk: Persistent player profiles, leaderboards, streaks, achievements, and stats can store user activity over time. <br>
Mitigation: Provide visible privacy controls, document what is stored, restrict access to the data directory, and support profile viewing and deletion. <br>
Risk: Paid tournaments, tips, sponsored content, affiliate links, virtual currency, and chance-based games can create monetization and compliance concerns. <br>
Mitigation: Keep chance-based mechanics virtual-only unless reviewed, label sponsored or affiliate content, and require operator approval before enabling paid features. <br>
Risk: Streaks, variable rewards, leaderboards, and social pressure can encourage high-engagement or pressure-oriented usage patterns. <br>
Mitigation: Set reasonable play limits, avoid manipulative prompts, and make reminders, streaks, and leaderboards configurable or opt-in. <br>


## Reference(s): <br>
- [Bot Arcade ClawHub Release](https://clawhub.ai/jcools1977/opendawg) <br>
- [Bot Arcade README](README.md) <br>
- [Game Catalog & Detailed Mechanics](references/game-catalog.md) <br>
- [Economy & Progression System](references/economy-system.md) <br>
- [Monetization Playbook](references/monetization-playbook.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text with optional JSON from the local arcade state script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Python stdlib file storage for player profiles, leaderboards, streaks, achievements, and global stats when the bundled script is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
