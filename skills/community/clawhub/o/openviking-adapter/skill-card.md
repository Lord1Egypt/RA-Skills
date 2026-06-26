## Description: <br>
字节OpenViking记忆系统适配器 - 分层加载优化，Token降低83% <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yyu812707-wq](https://clawhub.ai/user/yyu812707-wq) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to analyze local memory token usage, generate layered memory summaries, and search relevant memories on demand. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw memory, USER, and SOUL files, which may contain private or sensitive personal context. <br>
Mitigation: Install only for sessions where local memory access is intended, avoid storing secrets in source memory files, and review generated memory_viking summaries. <br>
Risk: Generated summaries may persist sensitive details under ~/.openclaw/workspace/memory_viking. <br>
Mitigation: Restrict access to that workspace and delete or edit generated summaries before sharing the environment with other agents. <br>


## Reference(s): <br>
- [OpenViking](https://github.com/bytedance/OpenViking) <br>
- [Skill Page](https://clawhub.ai/yyu812707-wq/openviking-adapter) <br>
- [Publisher Profile](https://clawhub.ai/user/yyu812707-wq) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Text and Markdown reports with generated local Markdown memory summary files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create L0_soul.md and L1_overview.md under ~/.openclaw/workspace/memory_viking.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, skill.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
