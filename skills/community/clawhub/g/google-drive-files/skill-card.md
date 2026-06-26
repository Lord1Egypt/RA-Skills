## Description: <br>
Google Drive API integration with managed OAuth. Search Drive files, manage permissions, organize folders, upload and download files, and handle sharing changes. Use this skill when users want to find, organize, share, or move files in Google Drive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent search, organize, upload, download, share, and manage files in a connected Google Drive account through managed OAuth. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill brokers OAuth access to the user's connected Google account through ClawLink. <br>
Mitigation: Install only when ClawLink is trusted for the connected account, review Google permission prompts, and prefer a least-privilege account when possible. <br>
Risk: The skill can perform sharing, deletion, upload, move, and metadata-change operations in Google Drive. <br>
Mitigation: Confirm the target resource and intended effect before allowing any write operation, especially destructive actions such as deletion, trash emptying, or permission removal. <br>


## Reference(s): <br>
- [Google Drive API Overview](https://developers.google.com/drive/api/v3/about) <br>
- [Google Drive Files Resource](https://developers.google.com/drive/api/v3/reference/files) <br>
- [Google Drive Permissions Resource](https://developers.google.com/drive/api/v3/reference/permissions) <br>
- [ClawLink OpenClaw Documentation](https://docs.claw-link.dev/openclaw) <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/google-drive-files) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, text, markdown] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool-call parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Google Drive file metadata, permission details, download or export guidance, and confirmation prompts before write operations.] <br>

## Skill Version(s): <br>
1.0.5 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
