## Description: <br>
Play Any Game is an AI game companion that analyzes game screenshots, answers stuck-player questions, and can perform simple clicks or key actions for supported games such as Genshin Impact and Honkai: Star Rail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cgandgameenginelearner](https://clawhub.ai/user/cgandgameenginelearner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this Windows-focused skill for in-game assistance when a player is stuck, needs a screenshot interpreted, or wants limited UI help. It is intended as an advisory game companion, not unattended farming or account automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access screenshots and saved local images, which may reveal sensitive desktop or game-account information. <br>
Mitigation: Use it only when comfortable sharing the visible game window, keep unrelated sensitive windows closed, and review saved screenshots. <br>
Risk: The skill has broad mouse and keyboard control with weak limits, so incorrect coordinates or model output could affect the wrong window. <br>
Mitigation: Prefer dry-run or advisory use, restrict actions to a visible game window, and avoid background or global clicks unless reviewed. <br>
Risk: The skill stores or reads a DashScope API key for GUI model calls. <br>
Mitigation: Protect the local configuration, prefer environment-based secret handling where practical, and do not publish the API key. <br>
Risk: Automated actions could affect purchases, accounts, files, or non-game windows if used without supervision. <br>
Mitigation: Do not use it for unattended farming or for purchase, account, file, or non-game workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cgandgameenginelearner/play-any-game) <br>
- [Skill documentation](SKILL.md) <br>
- [README](README.md) <br>
- [BetterGI click analysis](references/better-gi-click-analysis.md) <br>
- [Game automation patterns](references/game-patterns.md) <br>
- [Alibaba Cloud GUI automation documentation](https://help.aliyun.com/zh/model-studio/gui-automation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance and JSON command results, with local screenshot file paths when actions capture the screen] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local PNG screenshots and may perform mouse or keyboard actions on the Windows desktop.] <br>

## Skill Version(s): <br>
1.4.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
