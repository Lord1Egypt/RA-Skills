## Description: <br>
Synology NAS integration for OpenClaw that centralizes file storage for multi-agent teams via SSH. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neal-collab](https://clawhub.ai/user/neal-collab) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and multi-agent team operators use this skill to route shared file storage, retrieval, and backups through a designated File Master agent connected to a NAS or SSH-accessible server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: One File Master agent can mediate broad SSH-based access to NAS storage. <br>
Mitigation: Use a restricted NAS account limited to intended directories and define which agents may read or write each area. <br>
Risk: Scheduled memory backups may copy secrets or sensitive files into shared storage. <br>
Mitigation: Exclude secrets from memory backups, apply encryption and retention limits, and enable cron backups only after those controls are in place. <br>
Risk: Unvalidated paths in file requests can cause unintended reads or writes. <br>
Mitigation: Validate and quote paths before use and keep agent storage areas separated by role. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/neal-collab/nas-agent-sync) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with shell, JSON, and agent configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operator guidance for configuring NAS-backed file workflows; it does not directly execute file transfers.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
