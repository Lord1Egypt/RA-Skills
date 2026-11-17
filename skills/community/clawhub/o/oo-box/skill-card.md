## Description:

Box (box.com). Use this skill for ANY Box request — reading, creating, updating, and deleting data. Whenever a task involves Box, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected Box account use this skill to search, read, upload, organize, update, and delete Box files and folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified remote code and may introduce broader agent changes; the installer contents were not available for inspection.

Mitigation: Review setup first and install a verified CLI release separately. Check automatic skill synchronization and use OO_SKILLS_SYNC_DISABLED to disable it if needed.

Risk: Write and deletion actions can change Box data or move files and folders to the trash.

Mitigation: Confirm the exact effect and payload before writes; confirm the target and get explicit approval before deletions.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [oo CLI installation guide](https://cli.oomol.com/install-guide.md)
- [Box](https://www.box.com/)
- [Box API reference](https://developer.box.com/reference)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON action results with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected Box action.]

## Skill Version(s):

1.0.4 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
