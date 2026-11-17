## Description:

Syncs daily health and fitness data from Oura Ring into markdown files, including sleep, readiness, activity, heart rate, stress, SpO2, and workout data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freakyflow](https://clawhub.ai/user/freakyflow)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to sync their Oura Ring health and fitness data into local markdown files that an agent can read for health, recovery, activity, and workout context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes sensitive Oura health records to local markdown files.

Mitigation: Use a private output directory and keep generated health files out of shared workspaces, backups, cloud sync, and version control unless that exposure is intended.

Risk: Scheduled sync can expose the Oura token if it is embedded directly in a crontab or shared configuration.

Mitigation: Store the Oura token through OpenClaw secret handling and avoid placing the token directly in scheduled command text.

Risk: The inline oura-ring dependency may change behavior when scheduled sync is enabled.

Mitigation: Pin or lock the oura-ring dependency before relying on unattended scheduled sync.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/freakyflow/skills/oura-ring)
- [Publisher Profile](https://clawhub.ai/user/freakyflow)
- [OpenClaw](https://openclaw.ai)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Oura Personal Access Tokens](https://cloud.ouraring.com/personal-access-tokens)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown files and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes one local health/YYYY-MM-DD.md file per synced day when data is available.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
