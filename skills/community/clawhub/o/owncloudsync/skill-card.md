## Description:

Check that new files on Google Drive are present on OwnCloud and send an email report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sydneyphoenix26](https://clawhub.ai/user/sydneyphoenix26)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to compare recently created or imported Google Drive files with an OwnCloud inventory service. It produces an emailed status report that identifies files as OK, MISSING, or NEED UPDATE.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs or depends on a persistent OwnCloud inventory web service that may expose file inventory metadata on port 8443.

Mitigation: Limit access to the service with firewall or network controls before enabling the sync workflow.

Risk: The sample configuration and service definition include hardcoded default credentials.

Mitigation: Replace all credentials before use and restrict permissions on configuration and service files.

Risk: The OwnCloud inventory file is stored under /tmp, which the security evidence flags as unsafe temporary-file handling.

Mitigation: Move the inventory file into a protected service directory with restricted ownership and permissions.

Risk: Daily email reports can disclose filenames and sync status to the configured recipient.

Mitigation: Confirm the report recipient and the exact metadata included in reports before scheduling automated email delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sydneyphoenix26/skills/owncloudsync)
- [Allfiles service README](allfiles-service/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown with shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires owncloud.json, Google Drive access through gog, and access to the OwnCloud inventory service.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
