## Description:

Automates Linux forensic data collection, generates detailed reports, and uploads them to Google Drive or emails results for fast incident response and audits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peachhfuzz](https://clawhub.ai/user/peachhfuzz)

### License/Terms of Use:

MIT-0

## Use Case:

Security operations, incident response, audit, and engineering teams use this skill to collect Linux system forensic data and prepare commands or workflow guidance for archiving reports to Google Drive or sending status by email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Forensic reports may contain sensitive system, user, network, process, log, package, cron, file, and disk usage data.

Mitigation: Use only for authorized incident response or audit work, redact or encrypt reports before sharing, and review collected fields against local policy.

Risk: Reports can be uploaded to Google Drive or referenced in email workflows, which can expose sensitive data if permissions are too broad.

Mitigation: Confirm Drive folder permissions, avoid public or broadly shared links, restrict OAuth scopes, and review token storage before use.

Risk: Long-lived OAuth refresh tokens can enable continued access beyond a single forensic task.

Mitigation: Store tokens with restrictive permissions, rotate or revoke them when no longer needed, and require local review of any referenced scripts before installation or execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/peachhfuzz/skills/linux-forensics-automation)
- [Google Drive API Documentation](https://developers.google.com/drive/api)
- [OAuth 2.0 for Desktop Apps](https://developers.google.com/identity/protocols/oauth2/native-app)
- [Linux man-pages project](https://www.man7.org/linux/man-pages/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe collection, upload, and email workflows that handle sensitive forensic reports.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
