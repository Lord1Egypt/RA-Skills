## Description: <br>
PDF toolkit: extract, merge, split, compress, convert, watermark, and protect PDFs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreataide86](https://clawhub.ai/user/andreataide86) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to perform common PDF document tasks such as extracting text, merging or splitting files, compressing PDFs, converting pages to images, extracting images, watermarking documents, and adding or removing password protection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PDF operations create local output files and can affect important documents if the wrong path is used. <br>
Mitigation: Use copies for important PDFs and follow the skill's no-overwrite convention unless the user explicitly asks to overwrite a file. <br>
Risk: Password-protected PDFs may require the user to provide a password during the task. <br>
Mitigation: Ask for the password only when needed and avoid storing it in files or reusable commands. <br>
Risk: Large PDFs or heavy compression can take more time and may reduce document quality. <br>
Mitigation: Warn before processing large PDFs and compress only when the user explicitly requests compression. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/andreataide86/pdf-power) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated local files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce text content, PDF files, PNG or JPEG images, or output folders beside the input file or at a specified output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
