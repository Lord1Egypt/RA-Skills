## Description: <br>
Copy large/long files to OneDrive for sharing when the user is on Telegram or WhatsApp and wants to view a full document or long file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moodykong](https://clawhub.ai/user/moodykong) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees and external users use this skill to copy local long documents or large files into a configured OneDrive folder for easier viewing and sharing from Telegram or WhatsApp. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included machine-specific OneDrive configuration may copy files to an unintended cloud-synced folder. <br>
Mitigation: Replace config.env with a confirmed local OneDrive path before use and verify the printed destination after each copy. <br>
Risk: Sensitive local files could be copied into cloud-synced storage. <br>
Mitigation: Avoid copying secrets, credentials, browser profiles, SSH keys, regulated data, or private documents unless cloud storage is intentional and approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/moodykong/onedrive-integration) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and destination path text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Copies selected local files to a configured OneDrive subdirectory and prints destination paths.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
