## Description: <br>
通用互动游戏框架，支持文字冒险、猜谜和问答等互动游戏类型，包含剧情分支、角色状态和存档功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yangyunxiao-ai](https://clawhub.ai/user/yangyunxiao-ai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agent users use this skill to start and play lightweight text adventure, riddle, and quiz games inside an agent conversation. Developers can extend the included JavaScript modules with new game types, themes, and input handlers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate during unrelated conversations if broad game-related phrasing is treated as a trigger. <br>
Mitigation: Use explicit game-start phrases such as starting a text adventure or riddle game before invoking the skill. <br>
Risk: The artifact includes publication guide commands for ClawHub login and publishing that are not needed for gameplay. <br>
Mitigation: Do not run login or publish commands unless intentionally maintaining or publishing the skill under an authorized account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yangyunxiao-ai/interactive-games) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Conversational game text, Markdown usage guidance, JavaScript examples, and JSON-compatible save state objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Game state is maintained locally by the included engine and can be represented as JSON save data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
