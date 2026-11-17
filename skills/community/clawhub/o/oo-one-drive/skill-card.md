## Description:

OneDrive (microsoft.com). Use this skill for ANY OneDrive request — reading, creating, updating, and deleting data. Whenever a task involves OneDrive, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected OneDrive account use this skill to search, inspect, download, upload, and manage OneDrive files and folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs downloaded CLI code, and the remote installers and installed CLI version have not been verified.

Mitigation: Review and approve the CLI installation separately before enabling the skill.

Risk: Startup synchronization can introduce persistent skills across other agents without explaining those effects.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 to prevent startup skill synchronization.

Risk: OneDrive writes and deletions can change or remove user data.

Mitigation: Review OneDrive permissions and retain confirmation for the exact write or deletion.

## Reference(s):

- [OneDrive](https://www.microsoft.com/microsoft-365/onedrive/online-cloud-storage)
- [OneDrive and Microsoft Graph](https://learn.microsoft.com/en-us/graph/onedrive-concept-overview)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [API Calls, Files, Text]

**Output Format:** [JSON action results and file content or metadata returned through the oo CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read, create, update, download, upload, or delete OneDrive items.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
