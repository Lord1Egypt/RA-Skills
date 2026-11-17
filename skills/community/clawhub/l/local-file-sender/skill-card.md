## Description:

Local File Sender helps a locally deployed OpenClaw agent identify a user-specified local file path, upload the file to cloud storage, and return a download link across Windows, Linux, and macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2656255594](https://clawhub.ai/user/2656255594)

### License/Terms of Use:

MIT-0

## Use Case:

People running OpenClaw locally use this skill to share local files through chat platforms by uploading the selected file and sending a download link when direct local-file sending is unsupported.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Arbitrary local file paths can cause unintended sensitive files to leave the machine.

Mitigation: Require explicit confirmation of the exact file before upload, restrict uploads to approved sharing folders, and avoid secrets or credential files.

Risk: Public cloud download links may make uploaded files accessible beyond the intended recipient.

Mitigation: Confirm link visibility before sending and prefer scoped, expiring, or otherwise access-controlled links where available.

Risk: Shell-based file checks can be fragile for unusual paths and safer path handling is needed.

Mitigation: Replace shell path checks with a safe filesystem API and validate paths before upload.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2656255594/skills/local-file-sender)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown response with download links and inline shell or JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local filesystem access and produces cloud-hosted download links for selected files.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
