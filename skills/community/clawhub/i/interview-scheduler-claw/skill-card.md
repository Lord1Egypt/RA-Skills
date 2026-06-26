## Description: <br>
面试邀约自动化协调：根据候选人和面试官信息协调飞书日历空闲时间、创建面试会议，并生成或发送面试邀请邮件。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiting and HR teams use this skill to coordinate batches of candidate interviews from Excel, CSV, or natural-language requests. It helps identify interviewer availability, propose candidate-specific time slots, create Feishu video meetings after confirmation, and prepare invitation email text or send mail when SMTP is configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles real calendar, contact, email, and token access. <br>
Mitigation: Scope Feishu and SMTP credentials tightly and review each calendar event, attendee list, candidate email, and meeting link before sending. <br>
Risk: The fallback script caches Feishu tenant access tokens in a weak shared temporary-file location. <br>
Mitigation: Prefer the OAuth-based Feishu plugin path; if the fallback script is used, change the cache to a private per-user location with restrictive permissions and remove cached tokens after use. <br>


## Reference(s): <br>
- [Feishu Calendar API Reference](references/feishu-calendar-api.md) <br>
- [Interview Email Templates](references/email-templates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/tujinsama/interview-scheduler-claw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured summaries, JSON API examples, shell command examples, and email draft text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require user confirmation before creating calendar events or sending email] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
