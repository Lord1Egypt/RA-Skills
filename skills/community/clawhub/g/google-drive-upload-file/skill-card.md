## Description: <br>
Atomic node skill to upload a file to Google Drive using the gog CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a local file needs to be uploaded to Google Drive through a configured gog CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may upload a local file to Google Drive that the user did not intend to share, including sensitive files. <br>
Mitigation: Confirm the exact file path and Google account before upload, and avoid uploading secrets, private keys, .env files, credentials, or other sensitive local data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zvirb/google-drive-upload-file) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with an inline shell command and JSON result expectation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gog binary; upload results are expected as JSON with the uploaded file and Drive ID.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
