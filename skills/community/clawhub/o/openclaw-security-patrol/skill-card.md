## Description: <br>
OpenClaw security-patrol is a multimode security audit skill that runs local host checks by default and can optionally upload summary audit data to Changeway threat-intelligence endpoints after explicit user consent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zsyjx0115](https://clawhub.ai/user/zsyjx0115) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users run this skill to inspect local system security posture, review installed skill inventory, save local audit reports, and optionally request a remote threat-intelligence score. It is intended for manual or scheduled security patrol workflows where users understand the local inspection and optional upload behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs host-level security inspection that can read sensitive local information such as logs, process metadata, system configuration, workspace files, and installed skill inventory. <br>
Mitigation: Review the skill before installing and run it only in environments where that level of local inspection is acceptable. <br>
Risk: --push mode sends identifiable audit summaries and device-related data to Changeway/auth.ctct.cn. <br>
Mitigation: Use the default local mode unless the user explicitly trusts the endpoint and confirms the upload for that manual run. <br>
Risk: Scheduled scans create ongoing local inspection and should not silently enable remote upload. <br>
Mitigation: Keep scheduled runs in local mode and avoid adding --push to cron configuration. <br>
Risk: The security evidence warns not to rely on the embedded integrity hash until the publisher fixes it. <br>
Mitigation: Treat the release as requiring review before installation and use server-provided file hashes for release verification where available. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zsyjx0115/openclaw-security-patrol) <br>
- [Cron setup guide](references/cron-setup.md) <br>
- [Changeway audit upload endpoint](https://auth.ctct.cn:10020/changeway-open/api/pushAuditData) <br>
- [Changeway skill assessment endpoint](https://auth.ctct.cn:10020/changeway-open/api/skills/assessment) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, json] <br>
**Output Format:** [Markdown and concise text summaries with inline shell commands; the audit script writes local TXT and JSON report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default local mode avoids network upload; --push mode uploads summary audit data only after explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.8 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
