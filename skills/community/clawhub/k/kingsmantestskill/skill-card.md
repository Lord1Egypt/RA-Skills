## Description: <br>
每天定时汇总"昨天"的10条民航相关新闻，输出结构化快速总览，并通过邮件发送给指定收件人。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuyun1118](https://clawhub.ai/user/wuyun1118) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users who track civil aviation developments use this skill to compile yesterday's public aviation news into a concise Chinese morning brief and send it by email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated results may be sent to a preset outside email address without clear user control over the destination. <br>
Mitigation: Confirm the exact recipient before sending, change it to an address the user controls, and avoid sending private prompts, sensitive generated content, or operational details unless each send is explicitly approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuyun1118/kingsmantestskill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [Chinese Markdown-style news summary with numbered items, sources, timestamps, one-sentence summaries, impact notes, and observation points.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets yesterday's Beijing-time news window and may email the brief to a preset recipient.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
