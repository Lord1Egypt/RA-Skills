## Description: <br>
会议纪要助手可整理会议内容、提取关键讨论点、生成结构化会议纪要、识别待办事项，并记录面向企业微信、飞书和钉钉的推送用法。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuyongliang-eccom](https://clawhub.ai/user/xuyongliang-eccom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and teams can use this skill to turn raw meeting notes into structured minutes with discussion points, decisions, and action items. Operators should review the generated minutes before sharing them because the artifact only includes a local formatter script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documented todo extraction and channel push commands are not implemented in the provided artifact. <br>
Mitigation: Use only scripts/extract_minutes.py for local formatting unless additional scripts are supplied and reviewed. <br>
Risk: Meeting minutes may contain confidential or sensitive business information. <br>
Mitigation: Confirm the destination channel and sharing permissions before posting or forwarding generated minutes. <br>
Risk: The local formatter uses keyword-based section extraction and may miss or misclassify discussion points, decisions, or action items. <br>
Mitigation: Review the generated Markdown before relying on it for official records or task tracking. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuyongliang-eccom/meeting-minutes-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown meeting minutes and command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated minutes include dated discussion, decision, and todo sections; users should verify extracted content before distribution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
