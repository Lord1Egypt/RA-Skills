## Description: <br>
Automates uploading multiple sources (files, URLs, YouTube, Drive, text) to a NotebookLM notebook, generating a deep dive audio overview in a preferred language, and downloading the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shiyanch](https://clawhub.ai/user/shiyanch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn selected documents, web links, YouTube URLs, Google Drive documents, or pasted text into a NotebookLM deep-dive audio overview and save the generated audio locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected sources are uploaded to Google's NotebookLM for processing. <br>
Mitigation: Use only sources you are authorized to upload, avoid confidential or regulated documents unless approved, and delete the NotebookLM notebook afterward if the uploaded sources should not be retained there. <br>
Risk: Generated audio is saved to a local destination selected during the workflow. <br>
Mitigation: Choose the download folder deliberately and verify the downloaded file before sharing or relying on it. <br>


## Reference(s): <br>
- [NotebookLM Audio Generator on ClawHub](https://clawhub.ai/shiyanch/notebooklm-audio-generator) <br>
- [epub2txt](https://github.com/SPACESODA/epub2txt.git) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and a downloaded audio file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a NotebookLM audio artifact saved locally as an MP3 after user-selected sources are processed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
