## Description:

Atomic node skill to upload a file to Google Drive using the gog CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a specified local file needs to be uploaded to Google Drive through the gog CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload a specified local file to Google Drive, which may expose secrets, credentials, personal data, or unintended files if the path is not reviewed.

Mitigation: Confirm the exact local file path before use and avoid uploading sensitive or unwanted files to the Drive account.

## Reference(s):

- [Google Drive Upload File on ClawHub](https://clawhub.ai/zvirb/skills/google-drive-upload-file)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline shell command and JSON example]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected command output is a JSON object confirming the uploaded file and its Drive ID.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
