## Description: <br>
AI-powered email triage via IMAP (himalaya) or Google API that fetches inbox messages, classifies urgency and category, recommends actions, pulls upcoming calendar events, and generates daily markdown digests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gruted](https://clawhub.ai/user/gruted) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Email users and operators use this skill to triage recent inbox and calendar activity, prioritize urgent messages, choose follow-up actions, and produce a daily markdown digest. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes sensitive inbox and calendar contents on a recurring schedule. <br>
Mitigation: Use only with accounts approved for this processing, limit mailbox and calendar access where possible, and review generated digests before sharing. <br>
Risk: OAuth credentials, Gmail app passwords, and API keys may expose email, calendar, or AI-service access if stored insecurely. <br>
Mitigation: Verify requested Google OAuth scopes, store credentials outside shared workspaces, restrict file permissions, and rotate tokens if exposure is suspected. <br>
Risk: Optional AI classification or summarization may send message content to an external service. <br>
Mitigation: Disable or restrict AI summarization when external processing is not acceptable, and confirm the configured provider and retention policy before use. <br>
Risk: Daily markdown digests can persist sensitive email and calendar summaries. <br>
Mitigation: Write digests only to protected paths, apply limited retention, and avoid appending reports to broadly readable files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gruted/gruted-inbox-triage) <br>
- [Project repository](https://github.com/gruted/inbox-triage-bot) <br>
- [Project landing page](https://gruted.github.io/inbox-triage-bot/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown daily digest reports, JSON command output, and bash setup examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports himalaya or Google API email backends, optional AI classification through OPENAI_API_KEY, and scheduled digest generation through cron.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
