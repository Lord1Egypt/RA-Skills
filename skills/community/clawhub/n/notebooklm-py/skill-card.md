## Description: <br>
Provides agent guidance for using the unofficial notebooklm-py CLI and Python API to automate Google NotebookLM notebook management, source uploads, generated artifacts, downloads, and Q&A. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonia-sz](https://clawhub.ai/user/antonia-sz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to direct an agent through NotebookLM workflows such as creating notebooks, adding web or local sources, generating audio, video, slides, quizzes, reports, and downloading outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable broad NotebookLM upload, login, and notebook-management actions on the user's behalf. <br>
Mitigation: Use a dedicated account where possible and require explicit confirmation before uploads, deletions, or other notebook-changing actions. <br>
Risk: Files or source material sent to NotebookLM may include confidential or regulated information. <br>
Mitigation: Avoid uploading confidential or regulated files unless the user has approved the data handling implications. <br>
Risk: NotebookLM CLI credentials may be stored locally after login. <br>
Mitigation: Confirm where tokens are stored and how to revoke or remove them before authorizing agent use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/antonia-sz/notebooklm-py) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce instructions that cause NotebookLM to create or download files such as mp3, mp4, pdf, pptx, json, markdown, csv, and png.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
