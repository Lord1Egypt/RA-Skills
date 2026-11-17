## Description:

Play Any Game is an AI game companion that analyzes game screenshots, answers gameplay questions, and can perform simple UI actions for games such as Genshin Impact and Honkai: Star Rail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cgandgameenginelearner](https://clawhub.ai/user/cgandgameenginelearner)

### License/Terms of Use:

MIT-0

## Use Case:

Players and agent operators use this skill when a player is stuck, uncertain how to operate a game UI, or wants contextual help from the current game screen. The skill supports screenshot analysis, gameplay guidance, and supervised simple controls such as clicks and key presses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control the local desktop through clicks and key presses.

Mitigation: Run it only for the intended game window, supervise actions, and review proposed operations before execution.

Risk: Screenshots may contain private information and can be sent to an Aliyun-compatible AI service when visual analysis is configured.

Mitigation: Keep unrelated windows closed or outside capture scope, avoid full-screen desktop capture, and use a restricted API key.

Risk: API keys can be stored in config.json.

Mitigation: Prefer environment-variable storage and avoid committing or sharing local configuration files.

Risk: Game-specific SOUL files may try to replace higher-priority host or safety instructions.

Mitigation: Treat SOUL files as persona context only and keep platform, host, and safety instructions authoritative.

## Reference(s):

- [SKILL.md](SKILL.md)
- [README.md](README.md)
- [BetterGI Click Implementation Analysis](references/better-gi-click-analysis.md)
- [Game Automation Patterns](references/game-patterns.md)
- [Aliyun GUI Automation Documentation](https://help.aliyun.com/zh/model-studio/gui-automation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, JSON command results, and screenshot file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save screenshots locally and may send screenshots to an Aliyun-compatible model when configured.]

## Skill Version(s):

1.4.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
