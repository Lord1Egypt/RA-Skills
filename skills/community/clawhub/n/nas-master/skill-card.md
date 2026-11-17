## Description:

NAS Master provides hardware-aware ASUSTOR NAS metadata scraping and planning guidance using SMB file crawling, SSH system inspection, and read-only resource guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[afajohn](https://clawhub.ai/user/afajohn)

### License/Terms of Use:


## Use Case:

Developers and NAS administrators use this skill to inventory ASUSTOR storage metadata, inspect RAID and Btrfs status, and design PHP/MySQL dashboards for search and visualization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad NAS and SSH credentials while creating persistent metadata indexes.

Mitigation: Use a dedicated low-privilege NAS account, define explicit scan roots and exclusions, and review collected metadata before storing or sharing it.

Risk: SSH behavior and database defaults could weaken the deployment if used without hardening.

Mitigation: Pin SSH host keys and replace blank MySQL root access with a limited database user before running any scraper workflow.

Risk: A generated local dashboard could expose indexed NAS metadata through the web stack.

Mitigation: Only deploy the dashboard intentionally, restrict access to trusted users, and avoid publishing the indexed metadata beyond the intended local environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/afajohn/skills/nas-master)
- [Molt Bot Skill Documentation](https://docs.molt.bot/tools/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code, SQL, configuration, and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed before execution, especially where NAS credentials, database access, SSH behavior, or web dashboard exposure are involved.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
