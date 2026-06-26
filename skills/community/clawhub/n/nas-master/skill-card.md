## Description: <br>
A hardware-aware, hybrid SMB and SSH suite for ASUSTOR NAS metadata scraping, NAS infrastructure assistance, database-backed indexing, and lightweight dashboard generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afajohn](https://clawhub.ai/user/afajohn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, NAS administrators, and technical operators use this skill to inspect ASUSTOR NAS metadata, collect RAID and Btrfs status through SSH, index file metadata into MySQL, and plan related PHP/AJAX dashboard or data-analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests NAS, SMB, SSH, and database access that could expose broad private file metadata or privileged system information. <br>
Mitigation: Use a dedicated least-privilege read-only NAS account, restrict scans to approved volumes, and avoid storing real admin passwords in the skill directory. <br>
Risk: SSH collection can connect to NAS infrastructure and retrieve RAID and Btrfs status. <br>
Mitigation: Verify or pin the SSH host key before connecting and limit SSH permissions to the specific read-only inspection commands required. <br>
Risk: The artifact is designed to crawl hidden NAS paths and persist indexed file metadata. <br>
Mitigation: Exclude sensitive hidden paths unless explicitly needed, document the indexing scope, and review database contents for sensitive metadata exposure. <br>
Risk: The MySQL and PHP dashboard workflow can expose collected metadata if left unsecured. <br>
Mitigation: Secure or disable the dashboard, protect database credentials, and limit local network access to authorized users. <br>


## Reference(s): <br>
- [ClawHub nas-master release page](https://clawhub.ai/afajohn/nas-master) <br>
- [Molt Bot skills documentation](https://docs.molt.bot/tools/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, SQL] <br>
**Output Format:** [Markdown with code blocks and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include NAS scraping workflow guidance, MySQL schema updates, PHP/AJAX dashboard suggestions, and operational checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
