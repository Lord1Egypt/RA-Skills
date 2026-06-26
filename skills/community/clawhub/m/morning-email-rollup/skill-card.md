## Description: <br>
Daily morning rollup of important emails and calendar events at 8am with AI-generated summaries <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[am-will](https://clawhub.ai/user/am-will) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and individual users use this skill to receive a daily Markdown-style digest of important or starred Gmail messages and same-day Google Calendar events, including AI-generated email summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow accesses Gmail message bodies and calendar titles from the configured Google account and sends email content to Gemini for summarization. <br>
Mitigation: Use only an intended Google account, review GOG_ACCOUNT before scheduling, and confirm that Gemini processing of selected email content is acceptable. <br>
Risk: The rollup is delivered through the configured messaging channel, which may expose sensitive email summaries or calendar titles to unintended recipients. <br>
Mitigation: Verify the delivery channel and cron session before enabling automation, and adjust the Gmail search query or MAX_EMAILS to limit included content. <br>
Risk: The default Gmail query includes important or starred messages from the last 24 hours, which can include personal or confidential information. <br>
Mitigation: Review and narrow the Gmail search query before daily use if only specific senders, labels, or unread messages should be summarized. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/am-will/morning-email-rollup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style text with inline shell command examples and a generated daily rollup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses GOG_ACCOUNT and MAX_EMAILS configuration, writes a local run log, and can be scheduled with cron.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
