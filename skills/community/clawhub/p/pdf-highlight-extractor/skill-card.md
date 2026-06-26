## Description: <br>
Extracts highlight annotations from a user-provided PDF and helps create a Markdown reading-notes file with YAML front matter, excerpts by page, and a content summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhengbin1973](https://clawhub.ai/user/zhengbin1973) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and knowledge workers use this skill when they want an agent to extract highlighted text from a PDF, organize excerpts by page, and prepare Markdown reading notes with a concise summary and tags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads highlighted text from user-selected PDFs and writes a Markdown file in the same directory, which can expose document content if that folder is shared, synced, or version-controlled. <br>
Mitigation: Use the skill only with appropriate PDFs, review the output location before sharing or syncing, and avoid confidential documents unless the generated Markdown file is acceptable there. <br>
Risk: The skill may install PyMuPDF before extraction. <br>
Mitigation: Review and approve dependency installation in the target Python environment before running the install script. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhengbin1973/pdf-highlight-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [JSON highlight data and Markdown notes with YAML front matter] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes Markdown next to the source PDF by default and can filter highlights by color.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
