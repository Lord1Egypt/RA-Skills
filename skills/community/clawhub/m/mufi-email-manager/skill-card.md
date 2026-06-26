## Description: <br>
Mufi Email Manager integrates Gmail, Naver, Daum, and Kakao mail over IMAP/SMTP for unread-mail summaries, keyword filtering, template replies, and daily digests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to manage Korean email accounts from an agent workflow, including checking unread mail, summarizing messages, filtering important mail, and drafting or sending template-based replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles real mailbox credentials and configured mailbox contents. <br>
Mitigation: Use app passwords where available, keep the .env file private, and install only when mailbox access is acceptable. <br>
Risk: Reply and send commands can transmit email from configured accounts. <br>
Mitigation: Review any reply before invoking a send command. <br>
Risk: Cron jobs can create recurring mailbox access. <br>
Mitigation: Avoid adding cron jobs unless recurring mailbox checks or digests are intended. <br>
Risk: Dependencies may need updates before regular use. <br>
Mitigation: Update dependencies before deploying or using the skill regularly. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mupengi-bot/mufi-email-manager) <br>
- [Publisher profile](https://clawhub.ai/user/mupengi-bot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell command examples and text, HTML email, or JSON reports from the provided scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May access configured mailboxes and can send replies when the user invokes sending commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
