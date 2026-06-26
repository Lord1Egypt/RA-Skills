## Description: <br>
Automates Linux forensic collection and archival by generating system reports covering users, network, logs, processes, packages, and disk usage, then helping upload reports to Google Drive or email results for incident response, audits, and security workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peachhfuzz](https://clawhub.ai/user/peachhfuzz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security operators, incident responders, auditors, and Linux administrators use this skill to collect system forensic snapshots and prepare archival or notification workflows through Google Drive and Gmail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Forensic reports can contain sensitive Linux host details, including users, network state, processes, logs, packages, cron jobs, and recently modified files. <br>
Mitigation: Review the target system and report contents before sharing, and collect only with explicit authorization for the host and incident scope. <br>
Risk: The documented Drive upload and Gmail workflows can share forensic material outside the local system. <br>
Mitigation: Confirm recipients, Drive folder permissions, and shareable-link settings before upload or email delivery. <br>
Risk: OAuth tokens used by the documented Google workflows enable continued access if exposed. <br>
Mitigation: Store tokens with restrictive file permissions, rotate or revoke them after incidents, and reinstall only when the displayed version matches the reviewed files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/peachhfuzz/linux-forensics-automation) <br>
- [Google Drive API Documentation](https://developers.google.com/drive/api) <br>
- [OAuth 2.0 for Desktop Apps](https://developers.google.com/identity/protocols/oauth2/native-app) <br>
- [Linux Manual Pages](https://www.man7.org/linux/man-pages/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe generated forensic report files and external sharing steps when the user authorizes collection and upload.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
