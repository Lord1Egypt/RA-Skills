## Description: <br>
飞书消息智能摘要：从飞书会话中提取关键信息，生成结构化摘要。支持群聊消息分析、重要信息提取、多维度分类统计。当用户需要快速了解消息内容、整理会话要点、生成会议记录或跟进事项时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lqwzz](https://clawhub.ai/user/lqwzz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and teams using Feishu use this skill to summarize group or direct-message conversations, extract decisions and follow-up tasks, and organize discussion context for review or sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may handle sensitive Feishu conversation content. <br>
Mitigation: Use explicit chat names and time ranges, avoid private or regulated conversations without consent or organizational approval, and summarize only content the agent is authorized to access. <br>
Risk: Generated summaries, decisions, and action items may omit context or misstate responsibility. <br>
Mitigation: Review extracted decisions and follow-up tasks against the source conversation before sharing, archiving, or creating downstream tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lqwzz/messages-summary) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code] <br>
**Output Format:** [Markdown or structured text summary, with optional JSON-like parsed message data from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries may include overview, decisions, action items, key discussions, participant statistics, and time ranges.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
