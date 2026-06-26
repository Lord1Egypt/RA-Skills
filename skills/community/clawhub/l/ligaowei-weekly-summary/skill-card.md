## Description: <br>
为李高伟（收钱吧培训师）生成每周工作总结。支持按自定义周期（默认上周五至本周四）自动查询飞书日历日程和聊天记录，产出的总结以洞察分析为主而非事项罗列。触发场景：用户说"周报"、"周总结"、"本周内容"、"总结本周"、"周回顾"。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runkecheng](https://clawhub.ai/user/runkecheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and agents use this skill to generate concise weekly work summaries for 李高伟, a 收钱吧 training role, from Feishu calendar events and chat messages. It emphasizes work themes, impact, representative metrics, role observations, and next-week priorities instead of daily item lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to query Feishu calendar events and chat messages, which may include internal work details and personal identifiers. <br>
Mitigation: Use it only in an authorized workspace and include only information appropriate for the intended weekly summary audience. <br>
Risk: Weekly summaries can overstate impact or omit context when inferred from meetings and messages. <br>
Mitigation: Review the generated Markdown before sharing and correct unsupported conclusions, metrics, or follow-up priorities. <br>
Risk: The security verdict is clean but low confidence according to the supplied scan evidence. <br>
Mitigation: Confirm the packaged skill files and metadata before installation or publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runkecheng/ligaowei-weekly-summary) <br>
- [Weekly summary template](artifact/references/template.md) <br>
- [User profile](artifact/references/user_profile.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown weekly summary with concise narrative sections, selected metrics, role observations, and follow-up priorities.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default reporting period is previous Friday through current Thursday unless the user specifies another period.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
