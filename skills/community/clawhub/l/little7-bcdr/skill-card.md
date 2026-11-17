## Description:

Create, maintain, and verify Little7 business continuity and disaster recovery backups for identity, memory, learnings, scripts, and local skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[little7unifai](https://clawhub.ai/user/little7unifai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to automate daily and weekly Little7 continuity backups, retain restore notes, and verify that current state and optional secrets archives are present before claiming restore readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The backup workflow may archive identity, memory, local skills, and selected secret paths.

Mitigation: Review the included paths and the secret allowlist before use, and enable cron automation only after confirming that sensitive material is intentionally included.

Risk: Selected secrets may be stored in plaintext and synced to Google Drive.

Mitigation: Add encryption, apply restrictive file permissions and umask settings, and restore secrets only on trusted machines.

Risk: Backup staging and archive destinations can expose continuity data if local paths or cloud sync permissions are too broad.

Mitigation: Use secure temporary-directory handling, restrict destination access, and periodically run the health check to confirm expected archives and manifests.

## Reference(s):

- [Little7 Bcdr ClawHub Skill Page](https://clawhub.ai/little7unifai/skills/little7-bcdr)
- [Backup implementation](artifact/scripts/little7_backup.sh)
- [Weekly verification](artifact/scripts/little7_backup_healthcheck.sh)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with inline shell commands and file path references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation and verification of local tar archives, manifests, restore notes, and optional secrets backups.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
