## Description: <br>
Paimon.skill is a Genshin Impact-focused OpenClaw game companion that captures the game window, analyzes UI state, gives play guidance, and can perform simple clicks or key presses when asked. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cgandgameenginelearner](https://clawhub.ai/user/cgandgameenginelearner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and game-assistant developers use this skill to let OpenClaw inspect Genshin Impact screens, answer gameplay questions, locate UI elements, and perform simple user-requested interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can capture visible game windows and save screenshots locally. <br>
Mitigation: Keep unrelated or sensitive windows closed before use and review saved screenshots before sharing logs or artifacts. <br>
Risk: The click_text workflow can send screenshots to Aliyun/DashScope for multimodal UI analysis. <br>
Mitigation: Use click_text only when cloud analysis is acceptable, and prefer the DASHSCOPE_API_KEY environment variable instead of storing the key in a config file. <br>
Risk: The skill can inject mouse and keyboard actions into the game, including background clicks. <br>
Mitigation: Use foreground interaction or dry-run analysis when possible, and avoid background clicking unless the operator understands the behavior and risk. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cgandgameenginelearner/paimon-skill) <br>
- [BetterGI click analysis](artifact/references/better-gi-click-analysis.md) <br>
- [Game patterns reference](artifact/references/game-patterns.md) <br>
- [Aliyun GUI-Plus API documentation](https://bailian.console.aliyun.com/cn-beijing?tab=api#/api/?type=model&url=2997660) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results from the local CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI can return screenshot paths, detected UI coordinates, action metadata, and post-action screenshot paths.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
