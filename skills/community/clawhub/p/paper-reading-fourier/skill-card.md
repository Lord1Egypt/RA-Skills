## Description: <br>
Read academic papers from local PDF files, arXiv URLs, or paper titles and generate structured reading notes in Chinese. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fourierer](https://clawhub.ai/user/fourierer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and technical readers use this skill to fetch or read academic PDFs, extract text, analyze the paper, and create standardized Chinese reading notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can contact arXiv and download PDFs based on a URL or title. <br>
Mitigation: Confirm the requested paper source before network access and use non-sensitive inputs when possible. <br>
Risk: The skill can write downloaded PDFs, extracted text, and generated notes to user-specified paths. <br>
Mitigation: Choose output paths deliberately and avoid paths that could overwrite important existing files. <br>
Risk: PDF text extraction can miss content from complex layouts, figures, equations, or tables. <br>
Mitigation: Review extracted text against the source PDF and ask for clarification when important sections are incomplete. <br>


## Reference(s): <br>
- [Paper note template](references/note-template.md) <br>
- [mHC example note](references/mHC.md) <br>
- [ClawHub skill page](https://clawhub.ai/fourierer/paper-reading-fourier) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown notes with optional shell commands and extracted PDF text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese prose with English technical terms preserved; formulas use LaTeX; optional PDF and text files are written to user-specified paths.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
