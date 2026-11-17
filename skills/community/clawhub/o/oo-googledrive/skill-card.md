## Description:

Use this skill to read, create, update, and delete Google Drive data through a connected OOMOL account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People with an OOMOL-connected Drive account can use the skill to find and manage files, shared drives, comments, permissions, and revisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run an unverified online installer without first requesting approval.

Mitigation: Review and approve the CLI installation separately; prefer a pinned release with verified integrity.

Risk: Automatic skill synchronization may make persistent changes to other agents.

Mitigation: Check the CLI's automatic synchronization settings before allowing persistent changes.

Risk: Connected Drive access can expose or change files, including edits, sharing, or deletion.

Mitigation: Connect only the Drive access needed and retain the stated approval steps for edits, sharing, and deletion.

## Reference(s):

- [Google Drive](https://workspace.google.com/products/drive/)
- [Google Drive API guide](https://developers.google.com/workspace/drive/api/guides/about-sdk)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Google Drive skill on ClawHub](https://clawhub.ai/oomol/skills/oo-googledrive)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Files, Text]

**Output Format:** [JSON action results or requested Drive file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected Drive action.]

## Skill Version(s):

1.0.10 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
