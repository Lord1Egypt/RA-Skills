## Description: <br>
多飞书机器人去重回复规则。当同一用户通过多个机器人渠道同时发送相同消息时，AI 只回复一次，避免重复打扰。适用于配置了多路飞书机器人接入的 OpenClaw 场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scottrao635-svg](https://clawhub.ai/user/scottrao635-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to prevent duplicate AI replies when the same Feishu user message reaches multiple bot channels. It defines when to suppress a repeated reply and when to update local deduplication state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local dedup_state.json file retains sender IDs, timestamps, and message hashes. <br>
Mitigation: Inspect or clear dedup_state.json when that metadata should not be retained. <br>
Risk: A legitimate repeated Feishu message can be skipped within the 30-second duplicate window. <br>
Mitigation: Use the documented exceptions for changed topics, messages older than 30 seconds, or explicit repeat requests such as asking the agent to say it again. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scottrao635-svg/multi-bot-dedup) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/scottrao635-svg) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration] <br>
**Output Format:** [Markdown behavioral rule with JSON state-file guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains deduplication state keyed by sender, timestamp, and a hash of the first 50 message characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
