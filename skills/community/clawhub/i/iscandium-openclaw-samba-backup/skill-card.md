## Description: <br>
Backs up OpenClaw data to a remote Samba server and supports immediate or scheduled backup runs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iscandium](https://clawhub.ai/user/iscandium) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to copy local OpenClaw data to a Samba share, either on demand or through a scheduled OpenClaw cron job. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The backup configuration can contain local admin credentials and Samba credentials. <br>
Mitigation: Use a least-privilege Samba account, restrict permissions on configuration files, and prefer a preconfigured mount or narrow sudoers rule instead of storing an admin password. <br>
Risk: The default backup can copy sensitive OpenClaw files to a remote share. <br>
Mitigation: Trust and control the Samba destination, define explicit exclusions for secrets before use, and run a manual test before enabling scheduled backups. <br>
Risk: Automated cron runs and privileged cleanup can repeatedly copy data and remove old backup directories. <br>
Mitigation: Validate the target path, retention count, mount point, and cron settings before enabling unattended execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/iscandium/iscandium-openclaw-samba-backup) <br>
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and manages timestamped backup directories on a configured Samba share.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
