## Description: <br>
PhishGuard monitors Gmail and Outlook inboxes for phishing, scores incoming email with static rules and Claude API analysis, and can label, quarantine, alert, and notify Slack or Teams for higher-risk messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lichq1337](https://clawhub.ai/user/lichq1337) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security and IT teams use this skill to monitor business mailboxes, analyze suspected phishing emails, and trigger mailbox labels plus Slack or Teams alerts for messages above the configured risk thresholds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill continuously reads mailbox content and sends email-derived data to third-party AI and notification services. <br>
Mitigation: Require administrator approval for mailbox processing and alert destinations, restrict webhook channels, and use redaction or approval controls before production use. <br>
Risk: The skill can automatically add warning or quarantine labels to business email with limited controls documented. <br>
Mitigation: Test first on a dedicated mailbox, run with dry-run or human approval where possible, and document rollback procedures for label changes. <br>
Risk: The installation guide includes a curl-to-bash path and depends on the external Gmail connector being installed and authenticated. <br>
Mitigation: Use a reviewed installation method, verify the Gmail connector before enabling monitoring, and grant only the Gmail permissions needed for reading and labeling messages. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lichq1337/phishguard) <br>
- [Installation guide](artifact/INSTALACION.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, API calls] <br>
**Output Format:** [Plain text risk reports, session summaries, mailbox labels, and optional Slack or Teams notification payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Risk levels are LOW, MEDIUM, HIGH, and CRITICAL; analysis uses static rule matches plus Claude API scoring.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
