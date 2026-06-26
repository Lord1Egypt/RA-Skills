## Description: <br>
Local File Sender helps a local OpenClaw agent upload a user-specified local file to cloud storage and send a download link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2656255594](https://clawhub.ai/user/2656255594) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, or operators running a local OpenClaw deployment use this skill to share files from their local filesystem through platforms that cannot send local file paths directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload local files to cloud storage and return public download links without a required confirmation step. <br>
Mitigation: Confirm the exact file path and intended recipient before upload, and avoid uploading secrets, credentials, private documents, browser profiles, SSH keys, or system configuration files unless disclosure is intended. <br>
Risk: Cloud-hosted agents cannot access the user's local filesystem, so file checks and uploads may fail outside a local OpenClaw deployment. <br>
Mitigation: Use only in a local deployment, or use platform-native file upload features when running in a cloud deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2656255594/local-file-sender) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown messages with file checks, upload results, and download links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local deployment with access to the requested file path and the lightclaw_upload_file tool.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter states 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
