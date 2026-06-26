## Description: <br>
AI-powered Gmail automation, email triage, and smart inbox assistant for creating rules, checking messages, summarizing email, connecting downstream apps, forwarding email content, and sending replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tourmind](https://clawhub.ai/user/tourmind) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and teams use MailClaw to manage Gmail-driven workflows, including inbox triage, daily digests, rule-based automation, and user-confirmed actions in Slack, Notion, Google Calendar, Linear, HubSpot, and Gmail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MailClaw requires ongoing access to Gmail-derived data and uses scheduled polling for mailbox updates. <br>
Mitigation: Install only after confirming the mailbox access model, OAuth revocation path, and ability to disable heartbeat jobs. <br>
Risk: The skill stores a local API key used for authenticated requests. <br>
Mitigation: Keep the API key in the intended local config only, rotate it if exposed, and remove it when uninstalling the skill. <br>
Risk: Rules and suggested actions can create persistent downstream effects such as messages, pages, calendar events, issues, records, or sent email. <br>
Mitigation: Require explicit user confirmation before saving rules, sending email, or executing each suggested action. <br>
Risk: Host-invoked runbook behavior can broaden the effect of scheduled tasks if the host does not constrain execution. <br>
Mitigation: Use the bundled heartbeat only for the read-only digest flow and review host scheduling permissions before enabling it. <br>


## Reference(s): <br>
- [MailClaw ClawHub listing](https://clawhub.ai/tourmind/mailclaw) <br>
- [MailClaw publisher profile](https://clawhub.ai/user/tourmind) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with API call guidance, configuration steps, rule summaries, and email digest text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May present user-confirmed downstream actions and scheduled digest outputs; stores a local API key for authenticated requests.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
