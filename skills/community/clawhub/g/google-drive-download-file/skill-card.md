## Description:

Atomic node skill to download a file from Google Drive using the gog CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to download a known Google Drive file to a local path through the gog CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-controlled Drive file IDs or destination paths could lead to unsafe command execution or unexpected file writes if passed through a shell or left unvalidated.

Mitigation: Pass gog arguments without a shell, validate the Drive file ID, and restrict output paths to an approved download directory.

Risk: The skill depends on the external gog binary and the workflow that supplies the file ID and path.

Mitigation: Install only in trusted workflows where gog is available and the invoking agent controls or verifies the download inputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zvirb/skills/google-drive-download-file)
- [Publisher Profile](https://clawhub.ai/user/zvirb)

## Skill Output:

**Output Type(s):** [shell commands, text, guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the gog binary and a Google Drive file ID plus local output path.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
